import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime


def descargar_archivo(url):
    nombre_archivo = url.split("/")[-1]  # Obtener el nombre del archivo de la URL
    ruta_destino = r"E:\Emulator\4-Downloads\PS1" + "\\" + nombre_archivo
    sys.stdout.write(f"Descargando: {nombre_archivo} ")
    sys.stdout.flush()
    response = requests.get(url, stream=True)
    tamano_total = int(response.headers.get("Content-Length"))
    tamano_descargado = 0
    with open(ruta_destino, "wb") as archivo:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                archivo.write(chunk)
                tamano_descargado += len(chunk)
                porcentaje = (tamano_descargado / tamano_total) * 100
                sys.stdout.write(f"\rProgreso de la descarga: {porcentaje:.2f}% ")
                sys.stdout.flush()
    sys.stdout.write("\n")
    sys.stdout.flush()
    sys.stdout.write(f"{nombre_archivo} descargado correctamente.\n")
    sys.stdout.flush()


def guardar_enlaces(enlaces):
    nombre_archivo = datetime.now().strftime("%Y%m%d%H%M%S") + ".txt"
    ruta_archivo = r"E:\Emulator\4-Downloads\PS1" + "\\" + nombre_archivo
    with open(ruta_archivo, "w") as archivo:
        for enlace in enlaces:
            archivo.write(enlace + "\n")
    sys.stdout.write(f"Archivo de enlaces guardado correctamente: {nombre_archivo}\n")
    sys.stdout.flush()


def leer_registro():
    try:
        nombre_archivo = "registro_descargas.txt"
        ruta_archivo = r"E:\Emulator\4-Downloads\PS1" + "\\" + nombre_archivo
        with open(ruta_archivo, "r") as archivo:
            enlaces_descargados = archivo.read().splitlines()
        return enlaces_descargados
    except FileNotFoundError:
        return []


def guardar_registro(enlaces_descargados):
    nombre_archivo = "registro_descargas.txt"
    ruta_archivo = r"E:\Emulator\4-Downloads\PS1" + "\\" + nombre_archivo
    with open(ruta_archivo, "w") as archivo:
        for enlace in enlaces_descargados:
            archivo.write(enlace + "\n")
    sys.stdout.write("Registro de descargas actualizado.\n")
    sys.stdout.flush()


def analizar_pagina(url, palabras_filtro, limite_descargas, descargar_links):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    enlaces = soup.find_all("a")

    contador_descargas_posibles = 0
    descargas_realizadas = 0
    enlaces_atrapados = []
    enlaces_descargados = leer_registro()

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
                if urljoin(url, href) in enlaces_descargados:  # Verificar si el enlace ya ha sido descargado
                    sys.stdout.write(f"El archivo {href} ya ha sido descargado previamente.\n")
                    sys.stdout.flush()
                    continue
                url_descarga = urljoin(url, href)
                sys.stdout.write(f"Procesando enlace: {url_descarga}\n")
                sys.stdout.flush()
                descargar_archivo(url_descarga)
                descargas_realizadas += 1
                enlaces_descargados.append(urljoin(url, href))

    guardar_registro(enlaces_descargados)

    sys.stdout.write(f"Total de descargas posibles: {contador_descargas_posibles}\n")
    sys.stdout.write(f"Descargas realizadas: {descargas_realizadas}\n")
    sys.stdout.flush()

    if not descargar_links and enlaces_atrapados:
        guardar_enlaces(enlaces_atrapados)


# Ejemplo de uso
url_pagina = "https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation/"  # Reemplaza con la URL de la página que deseas analizar
palabras_filtro = ["japan", "europa", "eur", "jap", "(japan)", "(Japan)", "(JAPAN)", "(Europa)", "germany", "Germany",
                   "Germany", "France", "FRANCE", "france", "Italy", "ITALY", "(Netherlands)", "netherlands", "Korea",
                   "Scandinavia", "Australia", "(Australia)", "(Sweden)", "(Norway)", "(Denmark)", "(Russia)", "Russia",
                   "(China)", "china", "China", "Taiwan", "taiwan", "(Taiwan)", "portugal", "portuguese", "brazil",
                   "brasil", "fifa", "wwf", "football", "futbol", "volleyball", "Tenis", "(asia)", "(Asia)", "asia",
                   "NFL"]
limite_descargas = 5  # Límite de descargas simultáneas
descargar_links = False  # Indicador para descargar los enlaces (False para solo analizar)
analizar_pagina(url_pagina, palabras_filtro, limite_descargas, descargar_links)
