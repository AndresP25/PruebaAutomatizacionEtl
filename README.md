# PruebaAutomatizacionEtl

Scraping de Libros - README

Este script realiza web scraping para extraer información de libros desde el sitio web Books to Scrape
•	El script extrae datos como el precio, disponibilidad, calificación, cantidad en stock y título de los libros. 
•	Posteriormente, los datos son transformados y guardados en formatos CSV, JSON, y en una base de datos SQLite.
Este script realiza scraping de varias páginas (50) del sitio Books to Scrape. El script utiliza concurrent.futures para ejecutar el scraping de manera concurrente, acelerando el proceso al dividir las páginas en "ranges" y procesarlas en paralelo.


Requisitos

Este script requiere las siguientes dependencias:
•	Python 3.x
•	requests: para hacer solicitudes HTTP a las páginas web.
•	BeautifulSoup4: para analizar y extraer los datos del HTML.
•	pandas: para manipulación y transformación de datos.
•	sqlite3: para interactuar con bases de datos SQLite.
•	concurrent.futures: para realizar scraping de manera concurrente.



Instala las dependencias necesarias:
•	pip install requests beautifulsoup4 pandas

Instalación de SQLite:
La librería sqlite3 ya viene incluida con Python, por lo que no es necesario instalarla de forma adicional.




Archivos Generados

El script genera los siguientes archivos:
•	productos.csv: Un archivo CSV con los datos de los libros extraídos.
•	productos.json: Un archivo JSON con los datos en formato de registros.
•	productos.db: Una base de datos SQLite que almacena la información de los libros.


Ejecución del Script

Ejecuta el script:

  python etl.py


Descripción de lo que hace el script:

•	extraer_datos(url, page_range): Extrae los datos de los libros de una página específica.
•	transformar_datos(libros): Realiza transformaciones sobre los datos extraídos (homologación de calificación, conversión de precios y cantidad de stock).
•	guardar_archivos(df_libros): Guarda los datos transformados en archivos CSV y JSON.
•	cargar_sqlite(df_libros): Inserta o actualiza los datos en la base de datos SQLite.


•	Una breve explicación de por qué elegiste requests+BeautifulSoup o Selenium para esta tarea.
Utilice  requests+BeautifulSoup debido a que no requiero interaccion directa con la web 

•	Una descripción de cualquier suposición o decisión que tomaste durante el desarrollo.
Diseñé una tabla en sqlLite de acuerdo con estándares de modelado de datos, es decir, el campo en_stock, lo nombre como un CampoBandera, al igual que el campo cantidad_stock, como un CampoValor, adicionalmente, implementé una lógica de carga en la que determina si el registro ya existe en la base de datos, es decir, debido a que no tengo un identifiacador único del producto, decidí dejar el nombre del producto como la llave primaria, por ende, cuando exista esta llave en la tabla, se actualizará el registro, si no, se insertará un nuevo registro. 

•	Pregunta de reflexión: ¿Cómo adaptarías este script para que se ejecute automáticamente todos los días en un entorno de producción? (ej: cron, Airflow, GitHub Actions, etc.). No es necesario implementarlo, solo descríbelo.
No tengo conocimiento claro sobre los pasos necesarios para realizar esta tarea.

•	Pregunta de reflexión: Si tuvieras que escalar este proceso para 100 sitios web diferentes, ¿cuáles serían los principales componentes de tu arquitectura?
Básicamente, si los datos que se deben extraer coinciden con los extraidos en este ejercicio, solo se debería implementar la lógica de busqueda y extracción para estos 100 sitios diferentes, y que se unan todos los datos extraidos en el mismo dataframe.
