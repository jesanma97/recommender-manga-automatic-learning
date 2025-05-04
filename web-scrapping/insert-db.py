import psycopg2
from scraper import obtener_mangas  # Importa la función del otro archivo

# 🔹 Conexión a PostgreSQL
conn = psycopg2.connect(
    dbname="manga_db",
    user="user_master",
    password="PassMaster97",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# 🔹 Insertar datos obtenidos del scraping
def insertar_manga(manga):
    cur.execute("""
        INSERT INTO mangas_base (title, original_title, script, artist, ed_japanese, demography,
                 num_japanese, num_korean, synopsis_es)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        manga["title"], 
        manga["original_title"], 
        manga["script"], 
        manga["artist"], 
        manga["ed_japanese"], 
        manga["demography"], 
        int(manga["num_japanese"]) if manga["num_japanese"].isdigit() else None,
        int(manga["num_korean"]) if manga["num_korean"].isdigit() else None,
        manga["synopsis"]
    ))
    conn.commit()

# 🔹 Obtener los datos desde el scraper
lista_mangas = obtener_mangas()  # Llama a la función que hace el scraping

# 🔹 Insertar en la base de datos
for manga in lista_mangas:
    insertar_manga(manga)

# 🔹 Cerrar conexión
cur.close()
conn.close()

print("✅ Datos insertados correctamente en la base de datos.")