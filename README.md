# Brújula Vocacional — Sistema de Recomendación de Carrera Profesional

Sistema web **multiparadigma** en Python / Django que recomienda carreras universitarias basándose en el perfil de intereses y habilidades del usuario.

---

## Paradigmas aplicados

| Módulo | Paradigma | Descripción |
|--------|-----------|-------------|
| `controller.py` | **Imperativo / OO** | `TestVocacionalController` coordina el flujo completo: valida, parsea, llama a reglas lógicas, llama al ranking funcional y retorna la vista. |
| `logic_rules.py` | **Lógico** | Usa `pyDatalog` para inferir carreras candidatas mediante hechos (`pd_carrera_req`) y reglas declarativas (`pd_candidato`). Incluye fallback robusto. |
| `processor.py` | **Funcional** | Pipeline de funciones puras con `map()`, `filter()`, `reduce()` y `lambda`. Implementa un algoritmo de scoring ponderado multi-factor (v2). |

---

## Algoritmo de recomendación (v2)

El scoring ya no es simplemente `(interés + habilidad) / 10`. Ahora usa una fórmula ponderada:

```
score_primario   = (score_interés_req + score_habilidad_req) / 10 × 100   → peso 70%
score_secundario = bonus por alineación del perfil con áreas relacionadas  → peso 30%
afinidad_final   = primario × 0.70 + secundario × 0.30
```

Esto produce resultados diferenciados: dos usuarios que marcan `5` en el interés principal pueden obtener puntajes distintos si el resto de su perfil difiere.

---

## Requisitos

- Python 3.11 o superior
- Las dependencias están en `requirements.txt`

---

## Instalación

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux / Mac:
source venv/bin/activate

pip install -r requirements.txt
```

---

## Ejecución

```bash
python manage.py runserver
```

Abrir: `http://127.0.0.1:8000`

---

## Pruebas

```bash
python manage.py test test_vocacional
```

---

## Estructura del proyecto

```
Proyecto_TestVocacional/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── run_server.bat
│
├── Proyecto_TestVocacional/       # Configuración Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
└── test_vocacional/               # App principal
    ├── controller.py              # Paradigma Imperativo / OO
    ├── logic_rules.py             # Paradigma Lógico (pyDatalog)
    ├── processor.py               # Paradigma Funcional
    ├── views.py                   # Vistas Django
    ├── urls.py                    # Rutas de la app
    ├── models.py
    ├── tests.py                   # Suite de pruebas (4 clases)
    └── templates/
        └── test_vocacional/
            ├── base.html          # Layout base (navbar, footer, estilos globales)
            ├── home.html          # Portada con estadísticas animadas
            ├── test.html          # Cuestionario con progreso por sección
            └── results.html       # Resultados con radar, mini-barras y pasos siguientes
```

---

## Carreras incluidas (24)

| Área | Carreras |
|------|---------|
| Tecnología | Desarrollo de Software y Cloud · IA y Ciencia de Datos · Ciberseguridad |
| Salud | Medicina y Cirugía · Psicología Clínica · Enfermería |
| Negocios | Administración Corporativa · Marketing Digital · Economía y Finanzas |
| Derecho | Derecho Corporativo · Relaciones Internacionales |
| Ingeniería | Ingeniería Civil · Arquitectura · Ingeniería Mecánica |
| Ciencias | Biotecnología · Química y Farmacia · Ciencias Ambientales · Geología |
| Artes | Diseño Gráfico/UX · Artes Visuales · Periodismo · Música · Teatro · Gastronomía |

---

## Funcionalidades del sistema (v2)

- **Test con 18 preguntas** en escala Likert (12 de interés + 6 de habilidad)
- **Barra de progreso sticky** con mini-contadores por sección (Intereses / Habilidades)
- **Badge de categoría** en cada pregunta
- **Validación frontend** con scroll automático a la primera pregunta sin responder y botón bloqueado hasta completar
- **Mensajes de error amigables** que usan el texto de la pregunta, no IDs técnicos
- **Gráfico de radar** del perfil completo (Canvas API puro, sin librerías externas)
- **Mini-barras de componente** por carrera (interés requerido, habilidad requerida, perfil secundario)
- **Top 3** de intereses y habilidades visibles en el perfil
- **Sección "¿Qué hacer ahora?"** con pasos de acción post-test
- **Estadísticas animadas** en la portada con count-up al entrar en el viewport
