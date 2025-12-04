import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# URL de prueba
url = "https://quotes.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Extraer frases y autores
quotes = soup.find_all("span", class_="text")
authors = soup.find_all("small", class_="author")

# Crear listas con los datos
titulos = [q.text.strip() for q in quotes]
autores = [a.text.strip() for a in authors]

# Mostrar en terminal
for titulo, autor in zip(titulos, autores):
    print(f"{titulo} — {autor}")

# Crear DataFrame
df = pd.DataFrame({
    "Título": titulos,
    "Autor": autores
})

# Ruta donde se guardará el archivo
ruta_excel = r"C:\Users\Juan\Desktop\python\Web Scraping\scraping1.xlsx"

# Guardar en Excel
df.to_excel(ruta_excel, index=False)
print(f"\n✅ Archivo guardado en: {ruta_excel}")