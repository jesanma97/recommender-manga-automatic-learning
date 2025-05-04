import time
import json
import requests

url = "https://graphql.anilist.co"
query = """
query ($page: Int) {
  Page(page: $page, perPage: 50) {
    pageInfo {
      hasNextPage
    }
    media(type: MANGA, tag: $demography, isLicensed: true, status: RELEASING, search: $search) {
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
    day = date_dict.get("day")
    month = date_dict.get("month")
    year = date_dict.get("year")

    if day is None or month is None or year is None:
        return None  

    return f"{day:02d}/{month:02d}/{year}"  

# 🔹 Función para obtener datos de AniList
def fetch_manga_data_from_anilist(title, demography):
    page = 1
    all_manga_data = []

    while True:
        response = requests.post(url, json={"query": query, "variables": {"page": page, "search": title, "demography": demography}})
        
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
