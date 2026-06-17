# Sistema de Recomendación de Carrera Profesional - Django

Sistema web multiparadigma en Python 3.11+ usando Django. Recomienda carreras profesionales según intereses, habilidades y estilo de trabajo.

## Paradigmas aplicados

- **Imperativo / OO:** `CareerController` coordina el flujo: recibe datos del formulario, construye el perfil, llama a reglas lógicas, llama al ranking funcional y retorna la vista.
- **Funcional:** `processor/recommender.py` usa funciones puras, `map()`, `filter()`, `reduce()` y `lambda` para calcular puntajes y ordenar carreras.
- **Lógico:** `logic_rules/rules.py` usa `pyDatalog` para inferir carreras candidatas desde hechos y reglas.

## Requisitos

- Python 3.11 o superior

## Instalación

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

En Linux/Mac:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

```bash
python manage.py runserver
```

Abrir:

```text
http://127.0.0.1:8000
```

## Pruebas

```bash
pytest
```

## Estructura del proyecto

```text
career_recommender/
  settings.py
  urls.py
recommender/
  controllers/       # Paradigma imperativo / OO
  data/              # Base de conocimiento con más de 10 carreras
  logic_rules/       # Paradigma lógico con pyDatalog
  processor/         # Paradigma funcional
  templates/         # Interfaz web Django
  static/            # CSS
tests/
```

## Carreras incluidas

1. Ingeniería de Sistemas
2. Medicina
3. Derecho
4. Psicología
5. Administración
6. Contabilidad
7. Arquitectura
8. Ingeniería Civil
9. Diseño Gráfico
10. Educación
11. Marketing
12. Enfermería
13. Ingeniería Industrial
14. Comunicación
15. Negocios Internacionales
