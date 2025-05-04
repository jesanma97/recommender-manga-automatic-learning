import psycopg2
import sys
import os
import time
import json
import requests
from datetime import datetime

# 🔹 Conexión a PostgreSQL
conn = psycopg2.connect(
    dbname="manga_db",
    user="user_master",
    password="PassMaster97",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# 🔹 Obtener todas las demografías distintas en manga_base
def get_unique_demographies():
    try:
        cur.execute("SELECT DISTINCT demography FROM mangas_base WHERE demography IS NOT NULL AND demography = 'Manwha';")
        return [row[0] for row in cur.fetchall()]
    except Exception as e:
        print(f"❌ Error al recuperar demografías: {e}")
        return []

def format_date(date_dict):
    """ Convierte un diccionario de fecha {day, month, year} a 'YYYY-MM-DD' o None si la fecha es inválida. """
    year = date_dict.get("year")
    month = date_dict.get("month")
    day = date_dict.get("day")

    if not year or not month or not day:
        return None  # Retorna NULL si hay valores nulos

    try:
        return datetime(year, month, day).strftime("%Y-%m-%d")
    except ValueError:
        return None  # Si la fecha es inválida, retorna None
    
# 🔹 Obtener datos de AniList filtrando por demografía (tag)
def fetch_manga_data_by_demography(demography):
    url = "https://graphql.anilist.co"
    query = """
    query ($page: Int) {
      Page(page: $page, perPage: 50) {
        pageInfo {
          hasNextPage
        }
        media(type: MANGA, isLicensed: true, countryOfOrigin: "KR") {
            title {
                romaji
                native
            }
            description
            tags {
                name
            }
            startDate {
                day
                month
                year
            }
            endDate {
                day
                month
                year
            }
            status
            volumes
            averageScore
            meanScore
            popularity
            countryOfOrigin
            staff {
                edges {
                    node {
                        name {
                            full
                        }
                    }
                    role
                }
            }
        }
      }
    }
    """

    page = 1
    all_manga_data = []

    while True:
        response = requests.post(url, json={"query": query, "variables": {"page": page}})
        
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 10))  
            print(f"⚠️ Demasiadas peticiones. Esperando {retry_after} segundos...")
            time.sleep(retry_after)
            continue

        if response.status_code != 200:
            print(f"❌ Error en la petición: {response.status_code} - {response.text}")
            break

        data = response.json()

        if "data" not in data or data["data"] is None:
            print(f"⚠️ Respuesta vacía para {demography}")
            break

        page_data = data["data"].get("Page", {})
        media_list = page_data.get("media", [])

        if not media_list:
            print(f"❌ No se encontraron datos para {demography}")
            break

        for media in media_list:
            manga_data = {
                "title": media["title"].get("romaji"),
                "original_title": media["title"].get("native"),
                "synopsis": media.get("description"),
                "num_japanese": media.get("volumes"),
                "country_origin": media.get("countryOfOrigin"),
                "tags": json.dumps([tag["name"] for tag in media.get("tags", [])]),  
                "start_date": format_date(media.get("startDate", {})),
                "end_date": format_date(media.get("endDate", {})),
                "status": media.get("status"),
                "average_score": media.get("averageScore"),
                "mean_score": media.get("meanScore"),
                "popularity": media.get("popularity"),
                "script": [],
                "artist": [],
            }

            # Procesar staff según el rol
            for staff_member in media.get("staff", {}).get("edges", []):
                name = staff_member["node"]["name"]["full"]
                role = staff_member["role"]

                if role == "Story & Art":
                    manga_data["script"].append(name)
                    manga_data["artist"].append(name)
                elif role == "Story":
                    manga_data["script"].append(name)
                elif role == "Art":
                    manga_data["artist"].append(name)

            manga_data["script"] = ", ".join(manga_data["script"]) if manga_data["script"] else None
            manga_data["artist"] = ", ".join(manga_data["artist"]) if manga_data["artist"] else None

            all_manga_data.append(manga_data)

        if not page_data.get("pageInfo", {}).get("hasNextPage", False):
            break

        page += 1
        time.sleep(1)  

    return all_manga_data

# 🔹 Insertar datos en manga_base
def insert_manga_into_base(manga_data):
    try:
        cur.execute("""
            INSERT INTO mangas_base (title, original_title, synopsis, num_japanese, country_origin, is_editorial, script, artist)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (
            manga_data["title"],
            manga_data["original_title"],
            manga_data["synopsis"],
            manga_data["num_japanese"],
            manga_data["country_origin"],
            False,
            manga_data["script"],
            manga_data["artist"]
        ))

        manga_id = cur.fetchone()[0]
        conn.commit()
        return manga_id

    except Exception as e:
        conn.rollback()
        print(f"❌ Error insertando en mangas_base: {e}")
        return None

# 🔹 Insertar datos en manga_extra
def insert_manga_into_extra(manga_id, manga_data):
    try:
        cur.execute("""
            INSERT INTO mangas_extra (id_manga, tags, start_date, end_date, status, average_score, popularity, mean_score)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            manga_id,
            manga_data["tags"],
            manga_data["start_date"],
            manga_data["end_date"],
            manga_data["status"],
            manga_data["average_score"],
            manga_data["popularity"],
            manga_data["mean_score"]
        ))

        conn.commit()
        print(f"✅ Insertado manga ID {manga_id} en mangas_extra.")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error insertando en mangas_extra: {e}")

# 🔹 Proceso principal
def process_mangas():
    demographies = get_unique_demographies()

    if not demographies:
        print("❌ No se encontraron demografías en la base de datos.")
        return

    for demography in demographies:
        print(f"🔍 Buscando datos para la demografía: {demography}")
        mangas = fetch_manga_data_by_demography(demography)

        if not mangas:
            print(f"❌ No se encontraron mangas para la demografía {demography}.")
            continue

        for manga in mangas:
            manga_id = insert_manga_into_base(manga)
            if manga_id:
                insert_manga_into_extra(manga_id, manga)

    cur.close()
    conn.close()
    print("✅ Proceso completado.")

# 🔹 Ejecutar el proceso
if __name__ == "__main__":
    process_mangas()