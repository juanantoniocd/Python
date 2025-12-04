# Aplicación Flask - Esqueleto Base

Una aplicación Flask simple y lista para usar, con estructura básica para comenzar tu proyecto.

## Estructura del Proyecto

```
gestor_tareas/
├── app.py                 # Archivo principal de la aplicación
├── requirements.txt       # Dependencias del proyecto
├── templates/            # Plantillas HTML
│   ├── base.html        # Plantilla base
│   ├── index.html       # Página de inicio
│   ├── about.html       # Página acerca de
│   └── 404.html         # Página de error 404
└── static/              # Archivos estáticos
    └── style.css        # Estilos CSS
```

## Instalación

1. Instala las dependencias:
```bash
py -m pip install -r requirements.txt
```

## Uso

1. Ejecuta la aplicación:
```bash
py app.py
```

2. Abre tu navegador y visita:
```
http://localhost:5000
```

## Características

- ✅ Estructura básica de Flask
- ✅ Plantillas HTML con Jinja2
- ✅ Estilos CSS modernos
- ✅ Manejo de errores 404
- ✅ Diseño responsive
- ✅ Navegación entre páginas

## Rutas Disponibles

- `/` - Página de inicio
- `/about` - Página acerca de
- Cualquier otra ruta mostrará el error 404 personalizado

## Desarrollo

La aplicación está configurada para ejecutarse en modo desarrollo con:
- `debug=True` - Recarga automática cuando hay cambios
- Puerto: `5000`
- Host: `0.0.0.0` (accesible desde cualquier interfaz de red)

## Próximos Pasos

Puedes expandir esta aplicación agregando:
- Base de datos (SQLite, PostgreSQL, etc.)
- Autenticación de usuarios
- API REST
- Formularios y validación
- Más rutas y funcionalidades
