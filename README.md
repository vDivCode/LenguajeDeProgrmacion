# Brújula Vocacional
## Sistema de Recomendación de Carrera Profesional Multiparadigma

Sistema web construido en Python / Django que recomienda carreras universitarias a partir de un test de intereses y habilidades. Es el proyecto final del curso *Lenguaje de Programación*: implementa, sobre un mismo caso de uso, los paradigmas **imperativo/orientado a objetos**, **funcional** y **lógico**.

> Flujo de usuario: Inicio -> Test (18 preguntas) -> Resultados con recomendaciones y gráfico de radar.

---

## Tabla de contenidos

- [Descripción del Proyecto](#descripción-del-proyecto)
- [Funcionalidades del Sistema](#funcionalidades-del-sistema)
- [Paradigmas Aplicados](#paradigmas-aplicados)
- [Algoritmo de Recomendación](#algoritmo-de-recomendación)
- [Arquitectura y Flujo de Datos](#arquitectura-y-flujo-de-datos)
- [Instalación y Ejecución](#instalación-y-ejecución)
- [Pruebas](#pruebas)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Despliegue](#despliegue)

---

## Descripción del Proyecto

Brújula Vocacional es una herramienta diseñada para orientar a estudiantes en la elección de su carrera universitaria. A diferencia de los tests tradicionales, este sistema evalúa de forma independiente los intereses y las habilidades del usuario, cruzando estos datos con una base de conocimiento lógica para ofrecer recomendaciones precisas y personalizadas.

El valor académico del proyecto reside en su naturaleza multiparadigma, demostrando cómo diferentes enfoques de programación pueden resolver partes específicas de un problema de ingeniería dentro de una misma aplicación.

---

## Funcionalidades del Sistema

### Evaluación y Test
- **Cuestionario de 18 preguntas:** Basado en la escala Likert (1 a 5), dividido en 12 preguntas de intereses vocacionales y 6 de habilidades cognitivas.
- **Barra de progreso dinámica:** Visualización en tiempo real del avance del usuario, con indicadores específicos para las secciones de intereses y habilidades.
- **Validación robusta:** Sistema de validación en frontend y backend que identifica respuestas faltantes y realiza un scroll automático hacia la pregunta pendiente para mejorar la usabilidad.

### Análisis y Resultados
- **Gráfico de Radar Personalizado:** Generación de un perfil visual completo utilizando Canvas API nativa, mostrando el equilibrio entre las diferentes áreas evaluadas.
- **Ranking de Carreras:** Presentación de un Top 5 de carreras recomendadas, cada una acompañada de su puntaje de afinidad y una breve descripción.
- **Desglose de Afinidad:** Cada recomendación incluye mini-barras que detallan cuánto aporta el interés, la habilidad y el perfil secundario al puntaje final.
- **Resumen de Perfil:** Identificación de los 3 principales intereses y habilidades del usuario para una mejor autopercepción.

### Gestión y Persistencia
- **Almacenamiento Automático:** Registro de cada test realizado en Supabase, vinculando resultados a usuarios (registrados o anónimos) para análisis posteriores.
- **Sección de Orientación:** Incluye un apartado de "¿Qué hacer ahora?" con pasos de acción sugeridos tras obtener los resultados.
- **Administración de Datos:** Las preguntas, carreras y reglas lógicas son gestionadas externamente, permitiendo actualizaciones del catálogo sin modificar el código fuente.

---

## Estructura del Proyecto

```text
LenguajeDeProgrmacion/
├── manage.py
├── requirements.txt
├── build.sh                        # Script de build para despliegue (Render)
├── clean.ps1                       # Limpieza de archivos temporales (Windows)
├── .env.example                    # Plantilla de variables de entorno
├── GUIA_EXPOSICION.md              # Guía de exposición del proyecto
│
├── Proyecto_TestVocacional/        # Configuración del proyecto Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
└── test_vocacional/                # App principal
    ├── apps.py
    ├── views.py                    # Vistas Django (Home, Test, Resultados)
    ├── urls.py                     # Rutas de la app
    │
    ├── paradigmas/                 # Implementación de los tres paradigmas
    │   ├── controlador_imperativo.py
    │   ├── procesador_funcional.py
    │   └── reglas_logicas.py
    │
    ├── datos/
    │   └── loader.py               # Carga de datos desde Supabase + fallback + caché
    │
    ├── services/
    │   └── supabase_client.py      # Cliente Supabase (usuarios y resultados)
    │
    ├── tests/                      # Suite de pruebas por paradigma
    │   ├── fixtures.py
    │   ├── test_imperativo.py
    │   ├── test_funcional.py
    │   ├── test_logico.py
    │   └── test_views.py
    │
    ├── templates/
    │   ├── componentes/             # Partials reutilizables
    │   └── test_vocacional/
    │       ├── base.html            # Layout base
    │       ├── home.html            # Portada
    │       ├── test.html            # Cuestionario
    │       └── results.html         # Resultados
    │
    └── static/test_vocacional/      # CSS / JS propios (Canvas API)
```


---


## Paradigmas Aplicados

El núcleo del proyecto reside en la convivencia de tres paradigmas de programación, ubicados en `test_vocacional/paradigmas/`:

| Paradigma | Archivo | Función Específica |
| :--- | :--- | :--- |
| **Imperativo / OO** | `controlador_imperativo.py` | Gestiona el estado del proceso, valida la integridad de los datos y orquesta la comunicación entre los demás módulos. |
| **Lógico** | `reglas_logicas.py` | Utiliza el motor `pyDatalog` para realizar inferencias sobre qué carreras cumplen con los requisitos mínimos de interés y habilidad. |
| **Funcional** | `procesador_funcional.py` | Aplica transformaciones de datos mediante funciones puras y operaciones de orden superior para calcular el ranking final. |

---

## Algoritmo de Recomendación

El scoring se basa en una fórmula de afinidad ponderada (v2) que prioriza la alineación directa pero considera la versatilidad del perfil:

1. **Score Primario (70%):** Promedio de la coincidencia exacta entre el interés y la habilidad requerida por la carrera.
2. **Score Secundario (30%):** Bonus calculado a partir de la alineación del usuario con áreas de conocimiento relacionadas.
3. **Umbral de Corte:** Solo se muestran carreras con una afinidad superior al 40%, garantizando recomendaciones relevantes.

---

## Arquitectura y Flujo de Datos

- **Capa de Datos:** Implementa un cargador centralizado (`loader.py`) que consume la API de Supabase y utiliza `@lru_cache` para optimizar el rendimiento y reducir la latencia de red.
- **Capa de Servicios:** El cliente de Supabase gestiona la persistencia de resultados de forma desacoplada, asegurando que fallos en la red no interrumpan la experiencia del usuario.
- **Backend:** Desarrollado sobre Django 5.0, aprovechando su sistema de sesiones para el manejo temporal de resultados y su motor de plantillas para el renderizado dinámico.

---

## Instalación y Ejecución

### Pasos Iniciales
1. **Clonación del repositorio:**
   ```bash
   git clone https://github.com/vDivCode/LenguajeDeProgrmacion.git
   cd LenguajeDeProgrmacion
   ```
2. **Configuración del entorno:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # venv\Scripts\activate en Windows
   pip install -r requirements.txt
   ```

### Configuración de Variables de Entorno
Cree un archivo `.env` en la raíz del proyecto basado en `.env.example`. Estas variables son fundamentales para la seguridad y conectividad del sistema:

| Variable | Uso y Propósito |
| :--- | :--- |
| `DJANGO_SECRET_KEY` | Clave única utilizada para garantizar la integridad de las sesiones, cookies y firmas criptográficas de Django. |
| `DJANGO_DEBUG` | Controla el modo de depuración. Debe ser `True` en desarrollo y `False` en producción para evitar fugas de información técnica. |
| `SUPABASE_URL` | Dirección URL del proyecto en Supabase. Necesaria para que el sistema sepa a qué instancia de base de datos conectarse. |
| `SUPABASE_ANON_KEY` | Clave pública de API. Permite que el sistema realice consultas y guarde resultados en Supabase bajo las políticas de seguridad configuradas. |

### Inicio del Sistema
Una vez configuradas las variables, ejecute los siguientes comandos:
```bash
python manage.py migrate
python manage.py runserver
```

---

## Pruebas y Calidad de Código

El proyecto incluye una suite de pruebas exhaustiva organizada por paradigmas y capas de aplicación, utilizando `pytest` y `pytest-django`. Para ejecutar las pruebas, utilice:

```bash
pytest
```

### Organización de la Suite de Pruebas

#### 1. Pruebas del Paradigma Imperativo (`test_imperativo.py`)
- **Validación de Datos:** Verifica que el controlador identifique correctamente formularios incompletos o valores fuera de rango.
- **Parseo de Respuestas:** Asegura que los IDs de las preguntas se mapeen correctamente a sus categorías correspondientes.
- **Orquestación del Pipeline:** Valida que el flujo secuencial entre los paradigmas lógico y funcional se ejecute sin errores.

#### 2. Pruebas del Paradigma Lógico (`test_logico.py`)
- **Motor de Inferencia:** Evalúa que `pyDatalog` identifique correctamente las carreras candidatas basándose en los hechos inyectados.
- **Manejo de Fallbacks:** Verifica que, en caso de fallo del motor lógico, el sistema active la versión imperativa equivalente para no interrumpir el servicio.
- **Limpieza de Hechos:** Asegura que el motor lógico se limpie después de cada consulta para evitar contaminación de datos entre usuarios.

#### 3. Pruebas del Paradigma Funcional (`test_funcional.py`)
- **Cálculo de Scoring:** Valida la precisión de la fórmula ponderada (70/30) mediante casos de prueba con valores conocidos.
- **Funciones de Orden Superior:** Prueba la integridad de las operaciones `map`, `filter` y `reduce` utilizadas para transformar el catálogo de carreras.
- **Ranking y Filtrado:** Verifica que solo las carreras que superan el umbral del 40% aparezcan en el ranking final y que estén correctamente ordenadas.

#### 4. Pruebas de Integración y Vistas (`test_views.py`)
- **Ciclo de Vida HTTP:** Simula peticiones GET y POST para asegurar que las rutas (`/`, `/test/`, `/resultados/`) respondan correctamente.
- **Gestión de Sesiones:** Valida que los resultados se guarden y recuperen correctamente de la sesión de Django.
- **Simulación de Datos (Mocking):** Utiliza `fixtures.py` para simular la respuesta de Supabase, permitiendo ejecutar la suite completa sin necesidad de conexión a internet.



---


