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

1. **Preparación:**
   ```bash
   git clone https://github.com/vDivCode/LenguajeDeProgrmacion.git
   cd LenguajeDeProgrmacion
   python -m venv venv
   source venv/bin/activate  # venv\Scripts\activate en Windows
   pip install -r requirements.txt
   ```

2. **Configuración de Entorno:**
   Cree un archivo `.env` con las siguientes variables:
   - `DJANGO_SECRET_KEY`
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`

3. **Inicio del Sistema:**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

---

## Pruebas

Se utiliza `pytest` para garantizar la integridad de los algoritmos de recomendación y el flujo de navegación:
- **Pruebas de Paradigmas:** Validación individual de los módulos lógico, funcional e imperativo.
- **Pruebas de Vistas:** Verificación del ciclo completo de petición-respuesta y manejo de sesiones.

---

## Estructura del Proyecto

```text
test_vocacional/
├── paradigmas/     # Lógica multimodelo (Corazón del sistema)
├── datos/          # Consumo de API y caché de configuración
├── services/       # Integración con base de datos externa
├── templates/      # Interfaces de usuario (Django Templates)
└── tests/          # Suite de validación técnica
```

---

