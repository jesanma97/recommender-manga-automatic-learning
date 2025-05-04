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

def get_manga_titles_and_demography():
    try:
        # Conexión a la base de datos
        conn = psycopg2.connect(
            dbname="manga_db",
            user="user_master",
            password="PassMaster97",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        # Ejecutar la consulta
        cur.execute("SELECT id, title, original_title FROM mangas_base;")
        mangas = [{"id": row[0],"title": row[1], "original_title": row[2]} for row in cur.fetchall()]  # Lista de diccionarios

        # Cerrar conexión
        cur.close()
        conn.close()

        return mangas

    except Exception as e:
        print(f"❌ Error al recuperar los títulos: {e}")
        return []

def insert_manga_data_into_db(id_manga, manga_data):
    try:
        # Verificar si el ID ya existe en la base de datos
        cur.execute("SELECT 1 FROM mangas_extra WHERE id_manga = %s", (id_manga,))
        exists = cur.fetchone()

        if exists:
            print(f"⚠️ ID {id_manga} ya existe en la base de datos. Saltando inserción.")
            return  # No insertamos si ya existe

        # Insertar solo si no existe
        cur.execute("""
            INSERT INTO mangas_extra (id_manga, tags, start_date, end_date, status, average_score, popularity, mean_score)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            id_manga,
            manga_data["tags"],
            manga_data["start_date"],
            manga_data["end_date"],
            manga_data["status"],
            manga_data["average_score"],
            manga_data["popularity"],
            manga_data["mean_score"]
        ))

        conn.commit()
        print(f"✅ Insertado ID {id_manga} en la base de datos.")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error insertando ID {id_manga}: {e}")



url = "https://graphql.anilist.co"
query = """
query ($page: Int, $search: String) {
  Page(page: $page, perPage: 50) {
    pageInfo {
      hasNextPage
    }
    media(type: MANGA, isLicensed: true, search: $search) {
        title {
            english
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
# 🔹 Función para formatear fechas en "dd/mm/yyyy"
def format_date(date_dict):
    """ Convierte un diccionario de fecha {day, month, year} a 'YYYY-MM-DD' o None si hay valores nulos. """
    if not date_dict or None in (date_dict["day"], date_dict["month"], date_dict["year"]):
        return None  # Retorna NULL si hay valores nulos

    return datetime(date_dict["year"], date_dict["month"], date_dict["day"]).strftime("%Y-%m-%d")

# 🔹 Función para obtener datos de AniList
def fetch_manga_data_from_anilist(title):
    page = 1
    all_manga_data = []

    while True:
        response = requests.post(url, json={"query": query, "variables": {"page": page, "search": title}})
        
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
            print(f"⚠️ Respuesta vacía para {title}")
            break

        page_data = data["data"].get("Page", {})
        media_list = page_data.get("media", [])

        if not media_list:
            print(f"❌ No se encontró información para {title}")
            break

        for media in media_list:
            manga_data = {
                "tags": json.dumps([tag["name"] for tag in media.get("tags", [])]),  
                "start_date": format_date(media.get("startDate", {})),
                "end_date": format_date(media.get("endDate", {})),
                "status": media.get("status"),
                "average_score": media.get("averageScore"),
                "mean_score": media.get("meanScore"),
                "popularity": media.get("popularity"),
            }
            all_manga_data.append(manga_data)

        if not page_data.get("pageInfo", {}).get("hasNextPage", False):
            break

        page += 1
        time.sleep(1)  

    return all_manga_data

# 🔹 Función principal que maneja el proceso completo
def process_mangas():
    manga_list = get_manga_titles_and_demography()

    if not manga_list:
        print("❌ No se encontraron mangas en la base de datos.")
        return

    for manga in manga_list:
        id_manga = manga["id"]
        title = manga["title"]
        original_title = manga["original_title"]

        print(f"🔍 Buscando datos para: {original_title}")

        manga_data_list = fetch_manga_data_from_anilist(original_title)

        
        # Si la consulta no devolvió datos, intentar con title
        if not manga_data_list and title and title != original_title:
            print(f"⚠️ No se encontraron datos para {original_title}, intentando con {title}...")
            manga_data_list = fetch_manga_data_from_anilist(title)

        # Si después de ambos intentos sigue sin datos, continuar con el siguiente manga
        if not manga_data_list:
            print(f"❌ No se encontraron datos ni con {original_title} ni con {title}.")
            continue

        # Insertar los datos en la base de datos
        for manga_data in manga_data_list:
            insert_manga_data_into_db(id_manga, manga_data)

    cur.close()
    conn.close()
    print("✅ Proceso completado.")


# 🔹 Ejecutar el proceso
if __name__ == "__main__":
    process_mangas()
