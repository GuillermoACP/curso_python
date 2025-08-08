from flask import Flask, render_template
import os
import json

#creamos instancia de Flask
app = Flask(__name__)

# Funcion para cargar configuraciones desde un archivo JSON
def load_lessons():
    lecciones_completas = []
    """Carga todas las lecciones desde un archivo JSON."""
    data_path = 'data'
    # Iteramos sobre los archivos en el directorio de datos
    archivos_json = [f for f in os.listdir(data_path) if f.endswith('.json')]
    for archivo in archivos_json:
        ruta_archivo = os.path.join(data_path, archivo)
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            try:
                lecciones = json.load(f)
                # Añadimos el slug del archivo como parte de cada lección
                for leccion in lecciones:
                    leccion['slug'] = archivo.replace('.json', '')
                lecciones_completas.extend(lecciones)
            except json.JSONDecodeError:
                print(f"Error al decodificar el archivo {archivo}")
    return lecciones_completas

# Definimos la ruta principal
@app.route('/')
def index():
    """Renderiza la página principal con la lista de lecciones."""
    lecciones = load_lessons()
    return render_template('index.html', lecciones=lecciones)

#Nueva para mostrar una lección específica
@app.route('/leccion/<string:slug>')
def leccion(slug):
    """Renderiza una lección específica."""
    lecciones = load_lessons()
    #Buscamos la lección por su slug  
    leccion = next((l for l in lecciones if l['slug'] == slug), None)
    if leccion:
        return render_template('leccion.html', leccion=leccion)
    else:
        # Retornamos un error 404 si no se encuentra la lección
        return "Lección no encontrada", 404

#Bloque para ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
    # Cambia debug=True a False en producción

