import psycopg2

# 🔹 Función para obtener los títulos originales de mangas_base
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
        cur.execute("SELECT id, original_title, demography FROM mangas_base;")
        mangas = [{"id": row[0],"title": row[1], "demography": row[2]} for row in cur.fetchall()]  # Lista de diccionarios

        # Cerrar conexión
        cur.close()
        conn.close()

        return mangas

    except Exception as e:
        print(f"❌ Error al recuperar los títulos: {e}")
        return []
