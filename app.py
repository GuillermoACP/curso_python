from flask import Flask, render_template
import os
import json

app = Flask(__name__)

def load_chapters():
    chapters = []
    data_path = 'data'
    archivos_json = [f for f in os.listdir(data_path) if f.endswith('.json')]
    for archivo in archivos_json:
        ruta_archivo = os.path.join(data_path, archivo)
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                # Normalizar a lista
                if isinstance(data, list):
                    capitulos = data
                else:
                    capitulos = [data]

                for capitulo in capitulos:
                    cap_slug = capitulo.get('slug', archivo.replace('.json', ''))

                    lessons = []
                    for idx, leccion in enumerate(capitulo.get('lessons', [])):
                        leccion_slug = f"{cap_slug}-{idx}"
                        lessons.append({
                            'slug': leccion_slug,
                            'titulo': leccion['titulo']
                        })
                        leccion['slug'] = leccion_slug

                    capitulo['slug'] = cap_slug
                    capitulo['lessons'] = capitulo.get('lessons', [])

                    chapters.append({
                        'titulo': capitulo['titulo'],
                        'slug': cap_slug,
                        'descripcion': capitulo.get('descripcion', ''),
                        'nivel': capitulo.get('nivel', ''),
                        'link_doc': capitulo.get('link_doc', ''),
                        'tags': capitulo.get('tags', []),
                        'lessons': lessons,
                        'raw_lessons': capitulo['lessons']
                    })
            except json.JSONDecodeError:
                print(f"Error al decodificar el archivo {archivo}")
    return chapters

def load_lessons():
    lecciones_completas = []
    chapters = load_chapters()
    for chapter in chapters:
        for idx, leccion in enumerate(chapter['raw_lessons']):
            leccion_copy = leccion.copy()
            leccion_copy['slug'] = chapter['lessons'][idx]['slug']
            leccion_copy['capitulo'] = chapter['titulo']
            leccion_copy['capitulo_slug'] = chapter['slug']
            leccion_copy['capitulo_nivel'] = chapter.get('nivel', '')
            leccion_copy['capitulo_tags'] = chapter.get('tags', [])
            leccion_copy['capitulo_descripcion'] = chapter.get('descripcion', '')
            leccion_copy['link_doc'] = chapter.get('link_doc', '')
            lecciones_completas.append(leccion_copy)
    return lecciones_completas

@app.route('/')
def index():
    chapters = load_chapters()
    lecciones = load_lessons()
    first_lesson_slug = None
    for chapter in chapters:
        if chapter['lessons']:
            first_lesson_slug = chapter['lessons'][0]['slug']
            break
    return render_template('index.html', chapters=chapters, lecciones=lecciones, first_lesson_slug=first_lesson_slug)

@app.route('/leccion/<string:slug>')
def leccion(slug):
    chapters = load_chapters()
    lecciones = load_lessons()
    leccion = next((l for l in lecciones if l['slug'] == slug), None)
    if leccion:
        return render_template('leccion.html', leccion=leccion, chapters=chapters, lecciones=lecciones, active_slug=slug)
    else:
        return "Lección no encontrada", 404

if __name__ == '__main__':
    app.run(debug=True)
