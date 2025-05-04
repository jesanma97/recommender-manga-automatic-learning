import time
import requests

url = "https://graphql.anilist.co"
query = """
query ($page: Int) {
  Page(page: $page, perPage: 50) {
    pageInfo {
      hasNextPage
    }
    media(type: MANGA, tag: "Shounen", isLicensed: true) {
      id
      title {
        romaji
        english
      }
    }
  }
}
"""

mangas = []
page = 1
cont = 0

while True:
    response = requests.post(url, json={"query": query, "variables": {"page": page}})
    
    # Manejo del límite de peticiones
    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", 10))  # Espera recomendada por el servidor
       
        print(f"Demasiadas peticiones. Esperando {retry_after} segundos...")
        time.sleep(retry_after)
        continue

    if response.status_code != 200:
        print(f"Error en la petición: {response.status_code} - {response.text}")
        break

    data = response.json()

    if "data" not in data or data["data"] is None:
        print("Error: Respuesta vacía o inválida:", data)
        break

    page_data = data["data"].get("Page", {})
    media_list = page_data.get("media", [])

    if not media_list:
        print("No hay más mangas disponibles.")
        break

    mangas.extend(media_list)

    # Verificar si hemos alcanzado el límite de peticiones y esperar si es necesario
    remaining = int(response.headers.get("X-RateLimit-Remaining", 1))
    reset_time = int(response.headers.get("X-RateLimit-Reset", time.time()))

    if remaining == 0:
        wait_time = max(reset_time - int(time.time()), 1)
        print(f"Límite alcanzado. Esperando {wait_time} segundos...")
        time.sleep(wait_time)

    if not page_data.get("pageInfo", {}).get("hasNextPage", False):
        break

    page += 1
    time.sleep(1)  # Pequeño delay para evitar el 429

print(f"Se encontraron {len(mangas)} mangas.")
