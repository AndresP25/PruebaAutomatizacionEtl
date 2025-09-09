# PruebaAutomatizacionEtl

Scraping de Libros - README

Este script realiza web scraping para extraer información de libros desde el sitio web Books to Scrape
. El script extrae datos como el precio, disponibilidad, calificación, cantidad en stock y título de los libros. 
. Posteriormente, los datos son transformados y guardados en formatos CSV, JSON, y en una base de datos SQLite.
Este script realiza scraping de varias páginas (50) del sitio Books to Scrape. El script utiliza concurrent.futures para ejecutar el scraping de manera concurrente, acelerando el proceso al dividir las páginas en "ranges" y procesarlas en paralelo.

Requisitos

Este script requiere las siguientes dependencias:

Python 3.x

requests: para hacer solicitudes HTTP a las páginas web.

BeautifulSoup4: para analizar y extraer los datos del HTML.

pandas: para manipulación y transformación de datos.

sqlite3: para interactuar con bases de datos SQLite.

concurrent.futures: para realizar scraping de manera concurrente.

Instalación de Dependencias

Descarga el sctipt 'etl.py' en tu máquina.



Instala las dependencias necesarias:
. pip install requests beautifulsoup4 pandas


Instalación de SQLite:
La librería sqlite3 ya viene incluida con Python, por lo que no es necesario instalarla de forma adicional.



Archivos Generados

El script genera los siguientes archivos:
. productos.csv: Un archivo CSV con los datos de los libros extraídos.
. productos.json: Un archivo JSON con los datos en formato de registros.
. productos.db: Una base de datos SQLite que almacena la información de los libros.


Ejecución del Script

Ejecuta el script:

python etl.py


Descripción de lo que hace el script:

. extraer_datos(url, page_range): Extrae los datos de los libros de una página específica.
. transformar_datos(libros): Realiza transformaciones sobre los datos extraídos (homologación de calificación, conversión de precios y cantidad de stock).
. guardar_archivos(df_libros): Guarda los datos transformados en archivos CSV y JSON.
. cargar_sqlite(df_libros): Inserta o actualiza los datos en la base de datos SQLite.

