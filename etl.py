import sqlite3
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import concurrent.futures


def extraer_datos(url, page_range):
    libros = []

    for page in page_range:
        response = requests.get(f"{url}/catalogue/page-{page}.html")
        soup = BeautifulSoup(response.text, 'html.parser')

        # Obtener los productos de la página
        productos = soup.select('.product_pod')

        for producto in productos:
            libro = {}
            try:
                # Extraer información visible de cada producto
                libro['precio'] = producto.select_one('.price_color').text
                libro['en_stock'] = producto.select_one('.availability').text.strip()

                # Calificación en cantidad de estrellas
                estrellas = producto.select('.star-rating')

                # Buscar el color en el archivo CSS
                for estrella in estrellas:
                    estrella_texto = estrella['class'][1]  # La clase que contiene la calificación ('Four', 'Five', etc.)
                libro['calificacion'] = estrella_texto

                # Obtener el enlace al libro para obtener más detalles
                book_url = url + "/catalogue/" + producto.select_one('.product_pod h3 a')['href']

                response = requests.get(book_url)
                soup_detail = BeautifulSoup(response.text, 'html.parser')

                # Obtener la cantidad de piezas en stock
                libro['cantidad_stock'] = soup_detail.select_one('.availability').text.strip()
                libro['titulo'] = soup_detail.select_one('h1').text

                libros.append(libro)
            except Exception as e:
                print(f"Ocurrió un error al procesar el producto: {e}")
                continue

    print("Datos extraidos exitosamente")
    return libros


def transformar_datos(libros):
    df_libros = pd.DataFrame(libros)

    # Homologación de calificación
    calificaciones_homologadas = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }

    # Limpieza de datos
    df_libros['en_stock'] = df_libros['en_stock'] == 'In stock'
    df_libros['precio'] = df_libros['precio'].replace({'Â£': '', ',': ''}, regex=True).astype(float)
    df_libros['cantidad_stock'] = df_libros['cantidad_stock'].apply(
        lambda x: int(re.search(r'\((\d+)\s+available\)', x).group(1)) if 'available' in x else 0)
    df_libros['calificacion'] = df_libros['calificacion'].map(calificaciones_homologadas)
    df_libros = df_libros.reindex(['titulo', 'en_stock', 'cantidad_stock', 'calificacion', 'precio'], axis=1)
    df_libros = df_libros.sort_values(by='titulo')

    print("Datos transformados exitosamente.")
    return df_libros


def guardar_archivos(df_libros):
    # Guardar en formato CSV
    df_libros.to_csv('productos.csv', index=False)

    # Guardar en formato JSON
    df_libros.to_json('productos.json', orient='records', lines=True)

    print("Formatos de archivos guardados exitosamente.")


def cargar_sqlite(df_libros):
    conn = sqlite3.connect('productos.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        Titulo TEXT PRIMARY KEY,
        CB_EnStock TEXT,
        CV_CantidadStock INTEGER,
        Calificacion INTEGER,
        Precio REAL
    )
    """)

    # Busca la llave, si la encuentra, actualiza el registro, si no, lo inserta
    for index, row in df_libros.iterrows():
        Titulo = row['titulo']
        CB_EnStock = 'S' if row['en_stock'] else 'N'
        CV_CantidadStock = row['cantidad_stock']
        Calificacion = row['calificacion']
        Precio = row['precio']

        cursor.execute("""
        INSERT OR REPLACE INTO productos (Titulo, CB_EnStock, CV_CantidadStock, Calificacion, Precio)
        VALUES (?, ?, ?, ?, ?)
        """, (Titulo, CB_EnStock, CV_CantidadStock, Calificacion, Precio))

    conn.commit()

    df_from_sql = pd.read_sql('SELECT * FROM productos', conn)
    print(df_from_sql)

    conn.close()

    print("Datos cargados exitosamente.")


def main():
    url = 'http://books.toscrape.com/'

    # Dividir las páginas a scrapear en chunks para utilizar múltiples procesos
    page_ranges = [range(1, 11), range(11, 21), range(21, 31), range(31, 41), range(41, 51)]

    # Extraer los datos utilizando concurrent.futures
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(extraer_datos, url, pages): pages for pages in page_ranges}
        libros = []
        for future in concurrent.futures.as_completed(future_to_url):
            result = future.result()
            if result:
                libros.extend(result)

    # Transformar
    df_libros = transformar_datos(libros)

    # Cargar
    cargar_sqlite(df_libros)

    # Guardar
    guardar_archivos(df_libros)


# Ejecutar el script
if __name__ == '__main__':
    main()
