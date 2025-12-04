import requests

url = "https://jsonplaceholder.typicode.com/users"  # API de ejemplo
respuesta = requests.get(url)

# Revisar status
if respuesta.status_code == 200:
    datos = respuesta.json()  # convierte la respuesta a diccionario/lista
    for usuario in datos:
        print(usuario['name'], usuario['email'])
else:
    print("Error al consultar API")
