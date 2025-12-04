# Web Scraping a Excel

## Descripción
Este programa realiza un proceso de web scraping para extraer citas y sus autores desde la página web [Quotes to Scrape](https://quotes.toscrape.com/). Los datos extraídos se organizan y se exportan a un archivo Excel.

## Funcionalidades
- **Extracción de datos**: Obtiene citas y autores desde una página web.
- **Procesamiento**: Organiza los datos en un formato estructurado.
- **Exportación**: Guarda los datos en un archivo Excel para su posterior uso.

## Requisitos
- Python 3.10 o superior
- Bibliotecas necesarias:
  - `requests`
  - `beautifulsoup4`
  - `pandas`

## Instalación
1. Clona este repositorio o descarga el archivo `WebScraping2aExcel.py`.
2. Asegúrate de tener instaladas las bibliotecas necesarias. Puedes instalarlas ejecutando:
   ```bash
   pip install requests beautifulsoup4 pandas
   ```

## Uso
1. Ejecuta el script:
   ```bash
   python WebScraping2aExcel.py
   ```
2. El programa extraerá las citas y autores de la página web y las guardará en un archivo Excel en la ruta especificada:
   ```
   C:\Users\Juan\Desktop\python\Web Scraping\scraping1.xlsx
   ```

## Notas
- Asegúrate de tener conexión a internet al ejecutar el programa.
- Puedes cambiar la URL o la ruta de guardado modificando las variables `url` y `ruta_excel` en el script.

## Autor
Juan