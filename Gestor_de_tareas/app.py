from flask import Flask, render_template, request, redirect, url_for
import json
import os

# Crear la instancia de la aplicación Flask
app = Flask(__name__)

# Configuración
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

# Archivo para guardar las tareas
ARCHIVO_TAREAS = 'tareas.json'

# Lista global de tareas
tareas = []
contador_id = 1


def cargar_tareas():
    """Carga las tareas desde el archivo JSON"""
    global tareas, contador_id
    
    if os.path.exists(ARCHIVO_TAREAS):
        try:
            with open(ARCHIVO_TAREAS, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                tareas = datos.get('tareas', [])
                contador_id = datos.get('contador_id', 1)
        except (json.JSONDecodeError, FileNotFoundError):
            tareas = []
            contador_id = 1
    else:
        tareas = []
        contador_id = 1


def guardar_tareas():
    """Guarda las tareas en el archivo JSON"""
    datos = {
        'tareas': tareas,
        'contador_id': contador_id
    }
    with open(ARCHIVO_TAREAS, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


def agregar_tarea(texto):
    """Agrega una nueva tarea a la lista global"""
    global contador_id
    
    nueva_tarea = {
        'id': contador_id,
        'texto': texto,
        'hecho': False
    }
    tareas.append(nueva_tarea)
    contador_id += 1
    guardar_tareas()  # Guardar después de agregar


def completar_tarea(id_tarea):
    """Marca una tarea como completada o descompletada"""
    for tarea in tareas:
        if tarea['id'] == id_tarea:
            tarea['hecho'] = not tarea['hecho']
            guardar_tareas()  # Guardar después de completar
            break


def eliminar_tarea(id_tarea):
    """Elimina una tarea de la lista global"""
    global tareas
    tareas = [t for t in tareas if t['id'] != id_tarea]
    guardar_tareas()  # Guardar después de eliminar


def editar_tarea(id_tarea, nuevo_texto):
    """Edita el texto de una tarea"""
    for tarea in tareas:
        if tarea['id'] == id_tarea:
            tarea['texto'] = nuevo_texto
            guardar_tareas()  # Guardar después de editar
            break


def obtener_tarea_por_id(id_tarea):
    """Obtiene una tarea por su ID"""
    for tarea in tareas:
        if tarea['id'] == id_tarea:
            return tarea
    return None


# Cargar tareas al iniciar la aplicación
cargar_tareas()


# Ruta principal - mostrar lista de tareas
@app.route('/')
def index():
    """Página principal: muestra la lista de tareas"""
    return render_template('index.html', tareas=tareas)


# Ruta para agregar una nueva tarea
@app.route('/agregar', methods=['POST'])
def agregar():
    """Procesa el formulario para agregar una nueva tarea"""
    texto_tarea = request.form.get('texto_tarea', '').strip()
    
    if texto_tarea:  # Solo agregar si hay texto
        agregar_tarea(texto_tarea)
    
    return redirect(url_for('index'))


# Ruta para completar una tarea
@app.route('/completar/<int:id>')
def completar(id):
    """Marca una tarea como completada"""
    completar_tarea(id)
    return redirect(url_for('index'))


# Ruta para eliminar una tarea
@app.route('/eliminar/<int:id>')
def eliminar(id):
    """Elimina una tarea"""
    eliminar_tarea(id)
    return redirect(url_for('index'))


# Ruta para mostrar formulario de edición (GET)
@app.route('/editar/<int:id>')
def mostrar_editar(id):
    """Muestra el formulario para editar una tarea"""
    tarea = obtener_tarea_por_id(id)
    if not tarea:
        return redirect(url_for('index'))
    return render_template('editar.html', tarea=tarea)


# Ruta para procesar la edición (POST)
@app.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    """Procesa el formulario para editar una tarea"""
    nuevo_texto = request.form.get('texto_tarea', '').strip()
    
    if nuevo_texto:
        editar_tarea(id, nuevo_texto)
    
    return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    # Ejecutar la aplicación en modo desarrollo
    app.run(debug=True, host='0.0.0.0', port=5000)
