import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://www.listadomanga.es/"
EDITORIAL_URL = "https://www.listadomanga.es/editorial.php?id=65"

def obtener_enlaces_colecciones():
    response = requests.get(EDITORIAL_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table")[1:-4]  # Ignorar las últimas 3 tablas
    # Imprimir el número de tablas encontradas
    print(f"Se encontraron {len(tables)} tablas.")
    enlaces = []
    
    for table in tables:
        inner_table = table.find("table")
        if inner_table:
            tds = inner_table.find_all("td")
            if len(tds) > 1:  # Verificar que hay al menos dos tds
                enlaces_found = tds[1].find_all("a")
                for enlace in enlaces_found:
                    if enlace:
                        enlaces.append(BASE_URL + enlace["href"])
    print(enlaces)
    
    return enlaces

def obtener_detalles_coleccion(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    body = soup.find("body")
    # Obtener todos los hijos directos de <body>
    children = soup.body.findChildren(recursive=False)
    # Filtrar solo los elementos <center>
    centers = [child for child in children if child.name == "center"]
    center = centers[0].find("center")
    first_table = center.find("table")  # Seleccionar el segundo hijo center dentro de body
    inner_table = first_table.find("table")
    td_izq = inner_table.find("td", class_="izq")
    
    if not td_izq:
        return None
    
    def extraer_info(label):
        elemento = td_izq.find("b", string=label)
        if elemento:
            contenido = elemento.next_sibling
            texto = []
            while contenido and (contenido.name == "br" or contenido.name is None or contenido.name == "a"):
                if contenido.name == "a":  # Capturar enlaces como texto
                    texto.append(contenido.text.strip())
                elif contenido.string:
                    texto.append(contenido.string.strip())
                contenido = contenido.next_sibling
            return " ".join(texto).strip()
        return ""
    
    if extraer_info("Números en inglés:"):
        return None  # Si encuentra "Números en inglés:", no agregar esta colección
    
    title = td_izq.find("h2").text.strip() if td_izq.find("h2") else None
    original_title = extraer_info("Título original:")
    
    if original_title and "(" in original_title:
        original_title = original_title.split("(")[1].split(")")[0]  # Extraer solo el primer paréntesis
    
    script = extraer_info("Guion:")
    artist = extraer_info("Dibujo:")
    ed_japanese = extraer_info("Editorial japonesa:")
    demography = extraer_info("Colección:")
    
    num_japanese = extraer_info("Números en japonés:")
    num_japanese = num_japanese.split()[0] if num_japanese else ""
    
    num_korean = extraer_info("Números en coreano:")
    num_korean = num_korean.split()[0] if num_korean else ""

    print(f"Title: {title}")
    
    return {
        "title": title,
        "original_title": original_title,
        "script": script,
        "artist": artist,
        "ed_japanese": ed_japanese,
        "demography": demography,
        "num_japanese": num_japanese,
        "num_korean": num_korean,
        "synopsis": extraer_sinopsis(center)
    }


def extraer_sinopsis(center):
    try:
        tables = center.findChildren("table", recursive=False)  # Obtiene solo tablas de primer nivel dentro de <center>
        if len(tables) > 3:  # Verificamos que haya al menos 4 tablas
            sinopsis_table = None
            for table in tables:
                h2 = table.find("h2")
                if h2 and "Sinopsis de" in h2.text:
                    sinopsis_table = table
                    break  # Detenemos la búsqueda cuando encontramos la tabla correcta
            td_izq = sinopsis_table.find("table").find("td")
            h2 = td_izq.find("h2")
            if h2:
                h2.extract()  # Eliminar el h2 para no incluirlo en la sinopsis
            for hr in td_izq.find_all("hr"):
                hr.extract()  # Eliminar <hr>
            for br in td_izq.find_all("br"):
                br.replace_with(" ")  # Reemplazar <br> por espacio
            return td_izq.text.strip()
    except:
        return ""


def obtener_mangas():
    enlaces = obtener_enlaces_colecciones()
    lista_mangas = []
    
    for enlace in enlaces:
        detalles = obtener_detalles_coleccion(enlace)
        if detalles:
            lista_mangas.append(detalles)
    
    return lista_mangas

obtener_mangas()
