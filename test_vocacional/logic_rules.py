"""
=============================================================================
MÓDULO LÓGICO - logic_rules.py
=============================================================================
Paradigma: LÓGICO
Librería:  pyDatalog

Este módulo define la base de conocimiento de carreras universitarias mediante
hechos (facts) y reglas (rules) en pyDatalog. A partir del perfil de intereses
y habilidades del usuario, infiere lógicamente qué carreras son candidatas.

Regla central:
    es_candidato(Usuario, Carrera) si:
        el usuario tiene interés en [Tema] con score >= UMBRAL_MINIMO
        Y el usuario tiene habilidad en [Habilidad] con score >= UMBRAL_MINIMO
        Y la carrera requiere ese Tema e Habilidad
=============================================================================
"""

from pyDatalog import pyDatalog

# ---------------------------------------------------------------------------
# 1. Umbral mínimo de score (escala 1-5) para considerarse apto
# ---------------------------------------------------------------------------
UMBRAL_MINIMO = 3

# ---------------------------------------------------------------------------
# 2. Base de conocimiento: Carreras y sus requisitos de interés + habilidad
# ---------------------------------------------------------------------------
KNOWLEDGE_BASE = [
    # Carrera                                      Interés                       Habilidad
    ('Desarrollo de Software y Cloud',             'Tecnología y Programación',  'Lógica y Matemática'),
    ('Inteligencia Artificial y Ciencia de Datos',  'Tecnología y Programación',  'Pensamiento Crítico e Investigación'),
    ('Ciberseguridad y Redes de Información',      'Tecnología y Programación',  'Razonamiento Verbal y Análisis'),
    ('Medicina y Cirugía',                         'Ciencias de la Salud',       'Destreza Manual e Instrumental'),
    ('Psicología Clínica y Psicoterapia',          'Ciencias de la Salud',       'Empatía y Relación Social'),
    ('Enfermería y Salud Comunitaria',             'Ciencias de la Salud',       'Empatía y Relación Social'),
    ('Administración y Estrategia Corporativa',    'Negocios y Liderazgo',       'Razonamiento Verbal y Análisis'),
    ('Marketing Digital y E-Commerce',             'Persuasión y Ventas',        'Empatía y Relación Social'),
    ('Economía y Finanzas de Mercado',             'Finanzas y Economía',        'Lógica y Matemática'),
    ('Derecho Corporativo y Fiscal',               'Leyes y Política',           'Razonamiento Verbal y Análisis'),
    ('Relaciones Internacionales y Diplomacia',    'Leyes y Política',           'Empatía y Relación Social'),
    ('Ingeniería Civil y Estructuras',             'Construcción e Ingeniería',  'Habilidad Espacial y Visual'),
    ('Arquitectura y Diseño Urbano',               'Construcción e Ingeniería',  'Habilidad Espacial y Visual'),
    ('Ingeniería Mecánica y Robótica',             'Construcción e Ingeniería',  'Destreza Manual e Instrumental'),
    ('Biotecnología y Bioingeniería',              'Investigación Científica',   'Lógica y Matemática'),
    ('Química y Farmacia',                         'Investigación Científica',   'Destreza Manual e Instrumental'),
    ('Ciencias Ambientales y Energías Renovables', 'Ciencias de la Tierra',      'Pensamiento Crítico e Investigación'),
    ('Geología y Recursos Naturales',              'Ciencias de la Tierra',      'Pensamiento Crítico e Investigación'),
    ('Diseño Gráfico y UX/UI',                     'Arte y Creatividad',         'Habilidad Espacial y Visual'),
    ('Artes Visuales y Animación Digital',         'Arte y Creatividad',         'Habilidad Espacial y Visual'),
    ('Periodismo Digital y Producción de Medios',  'Comunicación y Medios',      'Razonamiento Verbal y Análisis'),
    ('Música y Producción Musical',                'Expresión Musical',          'Destreza Manual e Instrumental'),
    ('Artes Escénicas y Teatro',                   'Arte y Creatividad',         'Empatía y Relación Social'),
    ('Gastronomía y Gestión Culinaria',            'Arte y Creatividad',         'Destreza Manual e Instrumental'),
]

# ---------------------------------------------------------------------------
# 3. Declaración global de términos pyDatalog (nivel de módulo)
#    Deben estar en el módulo global para que pyDatalog los reconozca.
# ---------------------------------------------------------------------------
pyDatalog.create_terms(
    'PD_Carrera, PD_Interes, PD_Habilidad, PD_Score1, PD_Score2',
    'pd_carrera_req, pd_tiene_int, pd_tiene_hab, pd_candidato'
)

# Cargar la base de conocimiento de carreras como hechos globales
for _carrera, _interes, _habilidad in KNOWLEDGE_BASE:
    pyDatalog.assert_fact('pd_carrera_req', _carrera, _interes, _habilidad)

# Definir la regla lógica de inferencia a nivel global
pd_candidato(PD_Carrera) <= (
    pd_carrera_req(PD_Carrera, PD_Interes, PD_Habilidad) &
    pd_tiene_int('usuario_activo', PD_Interes, PD_Score1) &
    (PD_Score1 >= UMBRAL_MINIMO) &
    pd_tiene_hab('usuario_activo', PD_Habilidad, PD_Score2) &
    (PD_Score2 >= UMBRAL_MINIMO)
)


def _limpiar_hechos_usuario():
    """Elimina los hechos del usuario anterior sin tocar la base de carreras."""
    todos_intereses   = list({row[1] for row in KNOWLEDGE_BASE})
    todas_habilidades = list({row[2] for row in KNOWLEDGE_BASE})
    for interes in todos_intereses:
        try:
            pyDatalog.retract_fact('pd_tiene_int', 'usuario_activo', interes, None)
        except Exception:
            pass
    for habilidad in todas_habilidades:
        try:
            pyDatalog.retract_fact('pd_tiene_hab', 'usuario_activo', habilidad, None)
        except Exception:
            pass


def obtener_candidatos_pyDatalog(intereses_usuario: dict, habilidades_usuario: dict) -> list:
    """
    PARADIGMA LÓGICO (pyDatalog puro):
    Usa pyDatalog para hacer la inferencia con hechos y reglas declarativas.

    Los términos lógicos están declarados a nivel global del módulo.
    Se insertan hechos del usuario actual, se consulta la regla de inferencia,
    y se remueven los hechos del usuario al finalizar.
    """
    todos_intereses   = list({row[1] for row in KNOWLEDGE_BASE})
    todas_habilidades = list({row[2] for row in KNOWLEDGE_BASE})

    # Insertar hechos del usuario actual
    for interes in todos_intereses:
        score = intereses_usuario.get(interes, 1)
        pyDatalog.assert_fact('pd_tiene_int', 'usuario_activo', interes, score)

    for habilidad in todas_habilidades:
        score = habilidades_usuario.get(habilidad, 1)
        pyDatalog.assert_fact('pd_tiene_hab', 'usuario_activo', habilidad, score)

    # ---- CONSULTA LÓGICA ----
    resultado = pd_candidato(PD_Carrera)
    candidatas = [fila[0] for fila in resultado]

    # Limpiar hechos del usuario para próxima consulta
    for interes in todos_intereses:
        for score in range(1, 6):
            try:
                pyDatalog.retract_fact('pd_tiene_int', 'usuario_activo', interes, score)
            except Exception:
                pass
    for habilidad in todas_habilidades:
        for score in range(1, 6):
            try:
                pyDatalog.retract_fact('pd_tiene_hab', 'usuario_activo', habilidad, score)
            except Exception:
                pass

    return candidatas


def obtener_candidatos(intereses_usuario: dict, habilidades_usuario: dict) -> list:
    """
    PARADIGMA LÓGICO (versión robusta / fallback):
    Evalúa las reglas lógicas directamente contra la base de conocimiento.

    Regla implícita:
        es_candidato(carrera) <=
            carrera_requiere(carrera, interes, habilidad) AND
            tiene_interes(usuario, interes) >= UMBRAL AND
            tiene_habilidad(usuario, habilidad) >= UMBRAL
    """
    candidatas = []
    for carrera, interes_req, habilidad_req in KNOWLEDGE_BASE:
        score_interes   = intereses_usuario.get(interes_req, 1)
        score_habilidad = habilidades_usuario.get(habilidad_req, 1)
        if score_interes >= UMBRAL_MINIMO and score_habilidad >= UMBRAL_MINIMO:
            candidatas.append(carrera)
    return candidatas
