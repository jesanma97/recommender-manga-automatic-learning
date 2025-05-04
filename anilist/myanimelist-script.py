import requests

# 🔹 Configuración de la API
CLIENT_ID = "936e9c1e951f2cb6157f2c9631bdb122"  # Reemplázalo con tu Client ID de MAL
GENRE_ID = 27  # ID del género Shounen en MAL
BASE_URL = "https://api.myanimelist.net/v2/manga"

# 🔹 Función para obtener mangas del género Shounen
def get_shounen_manga_count():
    headers = {
        "X-MAL-CLIENT-ID": CLIENT_ID
    }
    params = {
        "genres": GENRE_ID,
        "limit": 50  # Máximo permitido por petición
    }

    total_mangas = 0
    next_page = f"{BASE_URL}/ranking"

    while next_page:
        response = requests.get(next_page, headers=headers, params=params)

        if response.status_code != 200:
            print(f"❌ Error {response.status_code}: {response.text}")
            return None

        data = response.json()
        total_mangas += len(data.get("data", []))

        # Revisar si hay más páginas de resultados
        next_page = data.get("paging", {}).get("next", None)

    return total_mangas

# 🔹 Ejecutar y mostrar resultado
if __name__ == "__main__":
    count = get_shounen_manga_count()
    if count is not None:
        print(f"📖 Total de mangas con el género Shounen: {count}")