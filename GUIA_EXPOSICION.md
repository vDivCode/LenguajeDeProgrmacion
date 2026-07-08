# 🧭 Brújula Vocacional — Guía Completa del Proyecto para Exposición

> Documento de estudio para explicar el proyecto como un ingeniero de sistemas:
> qué es, cómo funciona, qué tecnologías usa, dónde está cada cosa y por qué se diseñó así.

---

## 1. ¿De qué trata el proyecto?

**Brújula Vocacional** es un **sistema web de recomendación de carreras universitarias**.
El usuario responde un test de **18 preguntas** en escala Likert (del 1 al 5):

- **12 preguntas de intereses** (tecnología, salud, negocios, arte, leyes, construcción, naturaleza, comunicación, economía, música, ciencias, persuasión)
- **6 preguntas de habilidades** (lógica-matemática, empatía, habilidad espacial, destreza manual, razonamiento verbal, pensamiento crítico)

Con esas respuestas, el sistema **infiere y rankea** las carreras más afines de un catálogo de **24 carreras** agrupadas en 7 áreas (Tecnología, Salud, Negocios, Derecho, Ingeniería, Ciencias y Artes), y muestra un **Top 5 de recomendaciones** con un perfil visual (gráfico de radar).

### El punto académico clave: es un proyecto MULTIPARADIGMA

Este proyecto es del curso **Lenguajes de Programación**, y su valor no es solo la app web, sino que demuestra **tres paradigmas de programación conviviendo en un mismo sistema**, cada uno en el módulo donde es más natural:

| Paradigma | Módulo | ¿Qué hace? |
|---|---|---|
| **Imperativo / Orientado a Objetos** | `paradigmas/controlador_imperativo.py` | Controla el flujo paso a paso: validar → parsear → inferir → rankear |
| **Lógico (declarativo)** | `paradigmas/reglas_logicas.py` | Infiere carreras candidatas con hechos y reglas usando **pyDatalog** |
| **Funcional** | `paradigmas/procesador_funcional.py` | Calcula el scoring con funciones puras, `map`, `filter`, `reduce` y `lambda` |

---

## 2. Stack tecnológico (frameworks y herramientas)

| Capa | Tecnología | ¿Para qué se usa? |
|---|---|---|
| Lenguaje | **Python 3.11+** | Todo el backend |
| Framework web | **Django 5.0.14** | Ruteo, vistas, templates, sesiones, seguridad (CSRF) |
| Motor lógico | **pyDatalog 0.17.4** | Programación lógica: hechos y reglas al estilo Prolog/Datalog |
| Base de datos en la nube | **Supabase** (PostgreSQL) | Almacena preguntas, carreras, reglas, configuración y resultados |
| Base de datos local | **SQLite** (`db.sqlite3`) | Solo para sesiones de Django y el panel admin |
| Frontend | **HTML + CSS puro + JavaScript vanilla** (templates de Django) | Sin frameworks JS; el radar se dibuja con la **Canvas API** nativa |
| Servidor de producción | **Gunicorn + WhiteNoise** | Gunicorn sirve la app; WhiteNoise sirve los estáticos comprimidos |
| Despliegue | **Render** (script `build.sh`) | Hosting en la nube |
| Variables de entorno | **python-dotenv** (`.env`) | Credenciales de Supabase y config de Django |
| Testing | **pytest + pytest-django** (9 tests) | Una suite por paradigma + tests de vistas |

**Dato importante para explicar:** el proyecto usa **dos bases de datos con roles distintos**:
- **Supabase (PostgreSQL en la nube)** = los *datos del dominio* (preguntas, carreras, reglas del conocimiento, resultados de usuarios).
- **SQLite local** = solo infraestructura de Django (sesiones, admin). Por eso **no hay `models.py` con modelos propios**: el acceso a datos se hace vía el cliente de Supabase, no vía el ORM de Django.

---

## 3. Arquitectura general

El proyecto sigue el patrón **MVT de Django (Model–View–Template)** extendido con una **capa de paradigmas** (la lógica de negocio) y una **capa de servicios/datos**:

```
   NAVEGADOR (usuario)
        │  HTTP GET/POST
        ▼
┌─────────────────────────────┐
│  urls.py (ruteo)            │   /  →  /test/  →  /resultados/
└─────────────────────────────┘
        ▼
┌─────────────────────────────┐
│  views.py (vistas Django)   │   HomeView · TestView · ResultadosView
│  Paradigma: imperativo      │   (manejan HTTP y sesión, delegan la lógica)
└─────────────────────────────┘
        ▼
┌─────────────────────────────────────────────────────┐
│  CAPA DE PARADIGMAS (lógica de negocio)             │
│                                                     │
│  controlador_imperativo.py  ← ORQUESTADOR (OO)      │
│        │ 1. valida    │ 2. parsea                   │
│        ▼                                            │
│  reglas_logicas.py  ← INFERENCIA (pyDatalog)        │
│        │ 3. devuelve carreras candidatas            │
│        ▼                                            │
│  procesador_funcional.py ← SCORING (map/filter/     │
│        4. rankea Top 5        reduce/lambda)        │
└─────────────────────────────────────────────────────┘
        ▼
┌─────────────────────────────┐      ┌──────────────────────┐
│  datos/loader.py            │─────▶│  SUPABASE (Postgres)  │
│  (caché con @lru_cache)     │      │  services/            │
│                             │      │  supabase_client.py   │
└─────────────────────────────┘      └──────────────────────┘
        ▼
┌─────────────────────────────┐
│  templates/ (HTML)          │   home.html · test.html · results.html
│  + static/ (CSS)            │
└─────────────────────────────┘
```

### Flujo de una petición completa (esto es lo que más te van a preguntar)

1. El usuario entra a `/` → `HomeView` limpia la sesión y muestra la portada.
2. Va a `/test/` → `TestView.get()` pide al controlador la estructura del test (las 18 preguntas cargadas desde Supabase) y renderiza `test.html`.
3. El usuario responde y envía el formulario (POST a `/test/`).
4. `TestView.post()` llama a `controlador.ejecutar_pipeline(request.POST)`, que ejecuta los 3 paradigmas en cadena:
   - **Imperativo**: `validar_respuestas()` (¿están las 18? ¿son enteros del 1 al 5?) y `parsear_respuestas()` (convierte los IDs de pregunta a categorías con valores acotados).
   - **Lógico**: `obtener_candidatos_pyDatalog()` inserta las respuestas como *hechos* y consulta la regla `pd_candidato` → devuelve las carreras cuyo interés Y habilidad requeridos tienen puntaje ≥ 3 (umbral).
   - **Funcional**: `procesar_recomendaciones()` calcula la afinidad ponderada de cada candidata, filtra por umbral de 40%, ordena descendente y toma el Top 5.
5. El resultado se guarda en **Supabase** (creando un usuario anónimo si no existe) y en la **sesión** de Django.
6. Redirige a `/resultados/` → `ResultadosView` lee la sesión y renderiza `results.html` con las recomendaciones, el perfil y el gráfico de radar.

---

## 4. Los tres paradigmas en detalle (corazón de la exposición)

### 4.1 Paradigma Imperativo/OO — `test_vocacional/paradigmas/controlador_imperativo.py`

- Clase `TestVocacionalController` (orientación a objetos: estado interno `self.errores`, `self.advertencias`).
- Es **imperativo** porque describe *cómo* hacer las cosas paso a paso, con secuencia, condicionales y bucles `for`.
- Métodos clave:
  - `obtener_estructura_test()` — arma el diccionario con las preguntas para el template.
  - `validar_respuestas(datos_post)` — recorre todas las preguntas, acumula errores legibles ("Falta responder: «…»").
  - `parsear_respuestas(datos_post)` — mapea `id de pregunta → categoría` y acota valores con `max(1, min(5, valor))`.
  - `ejecutar_pipeline(datos_post)` — **el orquestador**: llama en orden a validación → parseo → lógica → funcional, y maneja los fallbacks (si pyDatalog falla usa la versión imperativa `obtener_candidatos()`; si no hay candidatas usa todo el catálogo con una advertencia).

### 4.2 Paradigma Lógico — `test_vocacional/paradigmas/reglas_logicas.py`

- Usa **pyDatalog** (Datalog embebido en Python, familia de Prolog).
- Es **declarativo**: no se dice *cómo* buscar carreras, se declara *qué* es una carrera candidata y el motor infiere.
- **Hechos** (se cargan al arrancar desde la base de conocimiento):
  ```
  pd_carrera_req('Desarrollo de Software', 'Tecnología y Programación', 'Lógica y Matemática')
  ```
- **Regla declarativa** (léela así en la expo: "Una carrera es candidata SI existe un requisito para esa carrera, Y el usuario tiene el interés requerido con puntaje ≥ 3, Y tiene la habilidad requerida con puntaje ≥ 3"):
  ```python
  pd_candidato(PD_Carrera) <= (
      pd_carrera_req(PD_Carrera, PD_Interes, PD_Habilidad) &
      pd_tiene_int('usuario_activo', PD_Interes, PD_Score1) & (PD_Score1 >= 3) &
      pd_tiene_hab('usuario_activo', PD_Habilidad, PD_Score2) & (PD_Score2 >= 3)
  )
  ```
- En cada consulta: se *asertan* las respuestas del usuario como hechos, se consulta `pd_candidato(PD_Carrera)`, y luego se *retractan* los hechos para limpiar el motor.
- Incluye `obtener_candidatos()` como **fallback imperativo** que hace lo mismo con un `for` (robustez).

### 4.3 Paradigma Funcional — `test_vocacional/paradigmas/procesador_funcional.py`

- **Funciones puras** (sin estado, sin efectos secundarios): misma entrada → misma salida.
- Usa las herramientas clásicas del paradigma:
  - `reduce()` — suma acumulada de puntajes (`_calcular_bonus_perfil`, `calcular_resumen_perfil`).
  - `map()` — enriquece cada carrera candidata con su detalle de afinidad.
  - `filter()` — descarta carreras bajo el umbral del 40%.
  - `lambda` — en todos los pasos anteriores y en los `sorted(key=...)`.
- **Pipeline funcional** en `procesar_recomendaciones()`: `map → filter → sorted → slice → map` (enriquecer → filtrar → rankear → top 5 → numerar).

### 4.4 El algoritmo de scoring (fórmula v2)

```
score_primario   = (puntaje_interés_req + puntaje_habilidad_req) / 10 × 100    (peso 70%)
score_secundario = promedio de intereses RELACIONADOS al principal × 100       (peso 30%)
afinidad_final   = primario × 0.70 + secundario × 0.30
```

**Por qué es mejor que un promedio simple:** dos usuarios que marcan 5 en el mismo interés principal obtienen puntajes *distintos* si el resto de su perfil difiere — el 30% secundario captura la coherencia global del perfil. Los pesos (0.70/0.30) y el umbral (3) **no están hardcodeados**: vienen de la tabla `config_algoritmo` en Supabase.

---

## 5. Modelo de datos (tablas en Supabase / PostgreSQL)

No hay modelos ORM de Django; los "modelos" son **5 tablas de configuración** + **2 tablas transaccionales** en Supabase:

| Tabla | Contenido | Campos principales |
|---|---|---|
| `preguntas` | Las 18 preguntas del test | `id`, `texto`, `tipo` (interes/habilidad), `categoria`, `ordem` |
| `carreras` | Catálogo de 24 carreras | `nombre`, `descripcion`, `area`, `color`, `activa` |
| `reglas_conocimiento` | Base de conocimiento del motor lógico | `carrera`, `interes`, `habilidad` (triple: qué requiere cada carrera) |
| `config_algoritmo` | Parámetros del algoritmo | `clave`, `valor_numerico` (UMBRAL_MINIMO=3, PESO_PRIMARIO=0.70, PESO_SECUNDARIO=0.30) |
| `intereses_relacionados` | Grafo de afinidad entre áreas | `interes`, `relacionado` (para el score secundario) |
| `usuarios_test` | Usuarios que hacen el test (anónimos) | `id` (UUID), `nombre`, `email`, `edad`, `pais` |
| `resultados_test` | Historial de resultados | `usuario_id`, `carrera_top`, `puntaje_top`, `recomendaciones` (JSON), `perfil_intereses`, `perfil_habilidades` |

**Ventaja arquitectónica para mencionar:** las preguntas, carreras y reglas viven en la BD, no en el código → se puede agregar una carrera o cambiar el algoritmo **sin tocar ni redesplegar el código**.

---

## 6. Mapa de archivos: dónde está cada cosa

```
LenguajeDeProgramacion/
│
├── manage.py                     ← Punto de entrada de Django (runserver, test, migrate)
├── requirements.txt              ← Dependencias exactas (Django, pyDatalog, supabase, etc.)
├── build.sh                      ← Script de build para el deploy en Render
├── db.sqlite3                    ← SQLite local (solo sesiones y admin)
├── .env / .env.example           ← Credenciales de Supabase (SUPABASE_URL, SUPABASE_ANON_KEY)
├── README.md                     ← Documentación general del repo
│
├── Proyecto_TestVocacional/      ← ⚙️ CONFIGURACIÓN DEL PROYECTO DJANGO
│   ├── settings.py               ← Config global: apps, middleware, BD, Supabase, WhiteNoise, idioma es-pe, zona America/Lima
│   ├── urls.py                   ← Ruteo raíz: /admin/ + incluye las URLs de la app
│   ├── wsgi.py                   ← Entrada para Gunicorn (producción)
│   └── asgi.py                   ← Entrada asíncrona (no se usa activamente)
│
└── test_vocacional/              ← 📦 LA APLICACIÓN PRINCIPAL
    ├── views.py                  ← Las 3 vistas (HomeView, TestView, ResultadosView) — manejo HTTP y sesión
    ├── urls.py                   ← Rutas de la app:  ''  →  'test/'  →  'resultados/'
    ├── apps.py                   ← Registro de la app en Django
    │
    ├── paradigmas/               ← ⭐ EL CORAZÓN ACADÉMICO (los 3 paradigmas)
    │   ├── controlador_imperativo.py  ← Imperativo/OO: TestVocacionalController (pipeline)
    │   ├── reglas_logicas.py          ← Lógico: hechos + reglas pyDatalog + fallback
    │   └── procesador_funcional.py    ← Funcional: scoring con map/filter/reduce/lambda
    │
    ├── datos/
    │   └── loader.py             ← Carga TODO desde Supabase 1 sola vez (@lru_cache) + fallback si falla
    │
    ├── services/
    │   └── supabase_client.py    ← Cliente Supabase: get_client(), guardar_usuario(), guardar_resultado()
    │
    ├── templates/
    │   ├── componentes/          ← navbar.html, footer.html (componentes reutilizables)
    │   └── test_vocacional/
    │       ├── base.html         ← Layout base (hereda con {% extends %})
    │       ├── home.html         ← Portada con estadísticas animadas (count-up)
    │       ├── test.html         ← Cuestionario: barra de progreso sticky, validación JS, badges
    │       └── results.html      ← Resultados: radar en Canvas, mini-barras, top 3, "¿qué hacer ahora?"
    │
    ├── static/test_vocacional/css/
    │   └── estilos.css           ← Todos los estilos (~1750 líneas, CSS puro sin frameworks)
    │
    └── tests/                    ← 🧪 SUITE DE PRUEBAS (9 tests, una por paradigma)
        ├── fixtures.py           ← Datos mock que reemplazan a Supabase en los tests (patch del loader)
        ├── test_imperativo.py    ← Prueba validación y pipeline completo del controlador
        ├── test_logico.py        ← Prueba la inferencia (versión pyDatalog y versión robusta)
        ├── test_funcional.py     ← Prueba ranking de recomendaciones y resumen de perfil
        └── test_views.py         ← Prueba las vistas HTTP (GET home, GET test, POST válido)
```

---

## 7. Controles y funcionamiento de la interfaz (frontend)

- **`home.html`** — Portada con estadísticas animadas (count-up cuando entran al viewport). Botón que lleva al test.
- **`test.html`** — El cuestionario:
  - 18 preguntas en **escala Likert 1–5** (radio buttons), divididas en 2 secciones: Intereses y Habilidades.
  - **Barra de progreso sticky** con contadores por sección.
  - **Badge de categoría** en cada pregunta.
  - **Validación en frontend (JavaScript)**: el botón de enviar se bloquea hasta responder todo, y hace scroll automático a la primera pregunta sin responder.
  - **Validación en backend** (doble capa): aunque el JS falle o alguien manipule el formulario, `validar_respuestas()` del controlador rechaza datos faltantes o fuera de rango con mensajes amigables.
  - Protección **CSRF** de Django en el formulario.
- **`results.html`** — Resultados:
  - **Gráfico de radar** del perfil dibujado con **Canvas API pura** (sin Chart.js ni librerías — punto a favor para mencionar).
  - Top 5 de carreras con **mini-barras** que descomponen el puntaje (interés requerido, habilidad requerida, perfil secundario).
  - Top 3 de intereses y habilidades dominantes.
  - Sección "¿Qué hacer ahora?" con pasos post-test.
- **Manejo de sesión**: los resultados viajan por la **sesión de Django** (no por URL), así `/resultados/` sin haber hecho el test redirige a home.

---

## 8. Robustez y decisiones de diseño (para sonar como ingeniero)

1. **Caché de datos (`@lru_cache`)**: el loader consulta Supabase **una sola vez** al arrancar el servidor y todo queda en memoria → cero latencia de BD en cada request del test.
2. **Degradación elegante (graceful degradation)** en 3 niveles:
   - Si pyDatalog falla → fallback imperativo `obtener_candidatos()`.
   - Si no hay ninguna candidata → se muestran las mejores del catálogo completo con una advertencia.
   - Si Supabase está caído al guardar → el `try/except` evita el error 500 y el usuario igual ve sus resultados.
3. **Doble validación** (frontend JS + backend Python): nunca se confía en el cliente.
4. **Configuración externalizada**: pesos del algoritmo, umbral, preguntas y carreras están en la BD, no en el código.
5. **Separación de responsabilidades**: vistas (HTTP) ≠ lógica de negocio (paradigmas) ≠ acceso a datos (loader/services) ≠ presentación (templates).
6. **Usuarios anónimos automáticos**: no se obliga a registrarse; al enviar el test se crea un usuario anónimo en Supabase para enlazar el resultado (decisión de UX).
7. **Testing con mocks**: `fixtures.py` "parchea" el loader para que los tests no dependan de Supabase (aislamiento de pruebas).
8. **Preparado para producción**: Gunicorn + WhiteNoise (estáticos comprimidos con hash), variables de entorno, `build.sh` para Render, `ALLOWED_HOSTS` dinámico.

---

## 9. Cómo ejecutar y demostrar

```bash
# 1. Crear entorno virtual y activar (Windows)
python -m venv venv
venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Levantar servidor
python manage.py runserver
# → http://127.0.0.1:8000

# 4. Correr los tests (demostración en vivo recomendada)
python manage.py test test_vocacional
```

---

## 10. Preguntas probables del profesor (y cómo responderlas)

**P: ¿Por qué dicen que es multiparadigma? Python es un solo lenguaje.**
R: Python es un lenguaje multiparadigma; el proyecto lo aprovecha usando *deliberadamente* un paradigma distinto por módulo: OO/imperativo en el controlador (estado y secuencia), lógico con pyDatalog (hechos y reglas declarativas al estilo Prolog), y funcional en el scoring (funciones puras, map/filter/reduce, sin efectos secundarios).

**P: ¿Dónde está la programación lógica exactamente?**
R: En `reglas_logicas.py`. La base de conocimiento son hechos `pd_carrera_req(carrera, interés, habilidad)` y la regla `pd_candidato` declara qué es una candidata; el motor de pyDatalog hace la inferencia por unificación, nosotros no escribimos el algoritmo de búsqueda.

**P: ¿Por qué no usan el ORM de Django / models.py?**
R: Decisión de arquitectura: los datos del dominio viven en Supabase (PostgreSQL en la nube) y se acceden con su cliente oficial; SQLite solo soporta la infraestructura de Django (sesiones). Esto permite editar preguntas/carreras/pesos sin redesplegar.

**P: ¿Qué pasa si Supabase se cae?**
R: El loader tiene fallback y los guardados están en try/except: la app no lanza error 500; el flujo del test se completa igual con los datos en caché.

**P: ¿Cómo garantizan que las respuestas sean válidas?**
R: Doble validación: JS en el navegador (UX) y `validar_respuestas()` en el servidor (seguridad), más `max(1, min(5, v))` al parsear como tercera red de seguridad, y el token CSRF de Django contra formularios forjados.

**P: ¿Cómo probaron el sistema?**
R: 9 pruebas automatizadas organizadas por paradigma (test_imperativo, test_logico, test_funcional, test_views), con fixtures que reemplazan a Supabase por datos mock para que los tests sean deterministas y no dependan de la red.

---

## 11. Guion sugerido de exposición (5–7 min)

1. **Qué es** (30 s): sistema web que recomienda carreras a partir de un test de 18 preguntas. Demo rápida: home → test → resultados.
2. **El requisito académico** (1 min): tres paradigmas conviviendo — mostrar el árbol de `paradigmas/`.
3. **Flujo técnico** (2 min): seguir un POST del formulario por el pipeline: validación imperativa → inferencia lógica (mostrar la regla `pd_candidato` en pantalla) → ranking funcional (mostrar el `map/filter/sorted`).
4. **Arquitectura y datos** (1.5 min): Django MVT + capa de paradigmas + Supabase; enseñar el diagrama de la sección 3 y las tablas de la sección 5.
5. **Robustez** (1 min): fallbacks, caché, doble validación, tests por paradigma (correr `python manage.py test` en vivo).
6. **Cierre** (30 s): qué se aprendió — elegir el paradigma correcto para cada problema en lugar de forzar uno solo.
