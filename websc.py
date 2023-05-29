import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime


def descargar_archivo(url):
    nombre_archivo = url.split("/")[-1]  # Obtener el nombre del archivo de la URL
    ruta_destino = r"E:\Emulator\4-Downloads\PS1" + "\\" + nombre_archivo
    print(f"Descargando: {nombre_archivo}")
    response = requests.get(url)
    with open(ruta_destino, "wb") as archivo:
        archivo.write(response.content)
    print(f"{nombre_archivo} descargado correctamente.")


def guardar_enlaces(enlaces):
    nombre_archivo = datetime.now().strftime("%Y%m%d%H%M%S") + ".txt"
    ruta_archivo = r"E:\Emulator\4-Downloads\PS1" + "\\" + nombre_archivo
    with open(ruta_archivo, "w") as archivo:
        for enlace in enlaces:
            archivo.write(enlace + "\n")
    print(f"Archivo de enlaces guardado correctamente: {nombre_archivo}")


def analizar_pagina(url, palabras_filtro, limite_descargas, descargar_links):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    enlaces = soup.find_all("a")

    contador_descargas_posibles = 0
    descargas_realizadas = 0
    enlaces_atrapados = []

    for enlace in enlaces:
        href = enlace.get("href")
        if href and (href.endswith(".zip") or href.endswith(".rar") or href.endswith(".7z")):
            contador_descargas_posibles += 1
            if any(palabra.lower() in href.lower() for palabra in
                   palabras_filtro):  # Verificar si el enlace contiene alguna palabra filtro
                continue
            enlaces_atrapados.append(urljoin(url, href))
            if descargar_links:  # Verificar si se deben descargar los enlaces
                if not descargas_realizadas < limite_descargas:  # Verificar si se ha alcanzado el límite de descargas
                    break
                url_descarga = urljoin(url, href)
                print(f"Procesando enlace: {url_descarga}")
                descargar_archivo(url_descarga)
                descargas_realizadas += 1

    print(f"Total de descargas posibles: {contador_descargas_posibles}")
    print(f"Descargas realizadas: {descargas_realizadas}")

    if not descargar_links and enlaces_atrapados:
        guardar_enlaces(enlaces_atrapados)


# Ejemplo de uso
url_pagina = "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation/"  # Reemplaza con la URL de la página que deseas analizar
palabras_filtro = ["japan", "europa", "eur", "jap", "(japan)", "(Japan)", "(JAPAN)", "(Europa)", "germany", "Germany",
                   "Germany", "France", "FRANCE", "france", "Italy", "ITALY", "(Netherlands)", "netherlands", "Korea",
                   "Scandinavia", "Australia", "(Australia)", "(Sweden)", "(Norway)", "(Denmark)", "(Russia)", "Russia",
                   "(China)", "china", "China", "Taiwan", "taiwan", "(Taiwan)"]  # Palabras filtro
limite_descargas = 5  # Límite de descargas simultáneas
descargar_links = False  # Indicador para descargar los enlaces (False para solo analizar)
analizar_pagina(url_pagina, palabras_filtro, limite_descargas, descargar_links)
