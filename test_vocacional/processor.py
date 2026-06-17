"""
=============================================================================
MÓDULO FUNCIONAL - processor.py
=============================================================================
Paradigma: FUNCIONAL
Técnicas:  Funciones puras, map(), filter(), reduce(), lambda, sorted()

Este módulo recibe la lista de carreras candidatas (del módulo lógico) y los
scores del usuario, y realiza el procesamiento puramente funcional para:
  1. Calcular un puntaje de afinidad PONDERADO para cada carrera candidata.
  2. Filtrar carreras con muy bajo puntaje.
  3. Rankear las carreras de mayor a menor afinidad.
  4. Enriquecer los resultados con metadatos descriptivos.

Algoritmo de scoring v2 (ponderado multi-factor):
  - Factor primario (70%): promedio del score de interés requerido y habilidad
    requerida, normalizado a 100.
  - Factor secundario (30%): bonus por alineación del perfil completo del
    usuario con todas las áreas de interés relacionadas a la carrera.
    Se calcula como la media de los scores sobre el umbral mínimo dividido
    entre el número de intereses relacionados.

No hay estado mutable ni efectos secundarios en este módulo.
=============================================================================
"""

from functools import reduce

# ---------------------------------------------------------------------------
# Pesos del algoritmo de scoring ponderado
# ---------------------------------------------------------------------------
PESO_PRIMARIO    = 0.70   # Interés + Habilidad requeridos
PESO_SECUNDARIO  = 0.30   # Alineación del perfil completo

# Mapas de afinidad entre áreas de interés (carreras que comparten dominio)
INTERESES_RELACIONADOS = {
    'Tecnología y Programación':  ['Investigación Científica', 'Finanzas y Economía'],
    'Ciencias de la Salud':       ['Investigación Científica', 'Ciencias de la Tierra'],
    'Negocios y Liderazgo':       ['Finanzas y Economía', 'Persuasión y Ventas', 'Leyes y Política'],
    'Arte y Creatividad':         ['Comunicación y Medios', 'Expresión Musical'],
    'Leyes y Política':           ['Negocios y Liderazgo', 'Comunicación y Medios'],
    'Construcción e Ingeniería':  ['Investigación Científica', 'Ciencias de la Tierra'],
    'Investigación Científica':   ['Tecnología y Programación', 'Ciencias de la Salud', 'Ciencias de la Tierra'],
    'Comunicación y Medios':      ['Arte y Creatividad', 'Persuasión y Ventas', 'Leyes y Política'],
    'Finanzas y Economía':        ['Negocios y Liderazgo', 'Leyes y Política'],
    'Expresión Musical':          ['Arte y Creatividad', 'Comunicación y Medios'],
    'Ciencias de la Tierra':      ['Investigación Científica', 'Construcción e Ingeniería'],
    'Persuasión y Ventas':        ['Negocios y Liderazgo', 'Comunicación y Medios'],
}

# ---------------------------------------------------------------------------
# 1. Metadatos de carreras (descripción, área)
#    Se usa como base de datos funcional (estructura inmutable)
# ---------------------------------------------------------------------------
METADATA_CARRERAS = {
    'Desarrollo de Software y Cloud': {
        'descripcion': 'Diseño, construcción e implementación de aplicaciones, arquitecturas en la nube y sistemas de software escalables.',
        'area': 'Ingeniería y Tecnología',
        'color': '#2563EB',
    },
    'Inteligencia Artificial y Ciencia de Datos': {
        'descripcion': 'Desarrollo de modelos de aprendizaje automático, procesamiento de grandes volúmenes de datos y algoritmos de inteligencia artificial.',
        'area': 'Ingeniería y Ciencias Exactas',
        'color': '#3B82F6',
    },
    'Ciberseguridad y Redes de Información': {
        'descripcion': 'Protección de infraestructuras críticas digitales, auditoría de vulnerabilidades y diseño de políticas de seguridad informática.',
        'area': 'Ingeniería y Seguridad',
        'color': '#1D4ED8',
    },
    'Medicina y Cirugía': {
        'descripcion': 'Diagnóstico, tratamiento y prevención de patologías humanas, combinando fundamentos científicos y prácticas clínicas quirúrgicas.',
        'area': 'Ciencias de la Salud',
        'color': '#DC2626',
    },
    'Psicología Clínica y Psicoterapia': {
        'descripcion': 'Evaluación, diagnóstico y terapia de la salud mental y el comportamiento, promoviendo el bienestar emocional.',
        'area': 'Ciencias de la Salud y Sociales',
        'color': '#DB2777',
    },
    'Enfermería y Salud Comunitaria': {
        'descripcion': 'Atención y cuidado integral del paciente, gestión hospitalaria y desarrollo de programas preventivos de salud pública.',
        'area': 'Ciencias de la Salud',
        'color': '#EC4899',
    },
    'Administración y Estrategia Corporativa': {
        'descripcion': 'Planificación, organización y toma de decisiones estratégicas para optimizar recursos financieros y liderar organizaciones.',
        'area': 'Negocios y Administración',
        'color': '#059669',
    },
    'Marketing Digital y E-Commerce': {
        'descripcion': 'Diseño de campañas de posicionamiento, análisis de comportamiento del consumidor en entornos digitales y comercio electrónico.',
        'area': 'Negocios y Comunicación',
        'color': '#10B981',
    },
    'Economía y Finanzas de Mercado': {
        'descripcion': 'Análisis de tendencias económicas globales, mercados de valores, modelado financiero y asignación estratégica de recursos.',
        'area': 'Economía y Finanzas',
        'color': '#047857',
    },
    'Derecho Corporativo y Fiscal': {
        'descripcion': 'Asesoría jurídica empresarial, cumplimiento de normativas fiscales, redacción de contratos y resolución de disputas legales.',
        'area': 'Derecho y Ciencias Jurídicas',
        'color': '#6D28D9',
    },
    'Relaciones Internacionales y Diplomacia': {
        'descripcion': 'Análisis de la política global, diplomacia, resolución de conflictos internacionales y gestión en organismos no gubernamentales.',
        'area': 'Ciencias Sociales y Políticas',
        'color': '#7C3AED',
    },
    'Ingeniería Civil y Estructuras': {
        'descripcion': 'Diseño estructural, supervisión y construcción de infraestructuras complejas como puentes, autopistas y edificaciones.',
        'area': 'Ingeniería y Construcción',
        'color': '#78350F',
    },
    'Arquitectura y Diseño Urbano': {
        'descripcion': 'Planificación de espacios habitables, diseño arquitectónico sostenible y ordenamiento urbano que armoniza estética y funcionalidad.',
        'area': 'Artes y Construcción',
        'color': '#92400E',
    },
    'Ingeniería Mecánica y Robótica': {
        'descripcion': 'Diseño, manufactura y automatización de sistemas mecánicos complejos, robótica industrial y maquinaria.',
        'area': 'Ingeniería y Manufactura',
        'color': '#374151',
    },
    'Biotecnología y Bioingeniería': {
        'descripcion': 'Manipulación genética y celular de organismos vivos para desarrollar soluciones aplicadas a la farmacia, medicina y agricultura.',
        'area': 'Investigación y Ciencias Exactas',
        'color': '#0369A1',
    },
    'Química y Farmacia': {
        'descripcion': 'Investigación y síntesis de compuestos químicos, diseño farmacológico y control de calidad de medicamentos.',
        'area': 'Investigación y Salud',
        'color': '#0891B2',
    },
    'Ciencias Ambientales y Energías Renovables': {
        'descripcion': 'Evaluación de impacto ambiental, conservación biológica y desarrollo de tecnologías de generación energética sostenible.',
        'area': 'Ciencias de la Tierra y Ambientales',
        'color': '#15803D',
    },
    'Geología y Recursos Naturales': {
        'descripcion': 'Estudio de la estructura terrestre, prospección de recursos minerales e hídricos, y mitigación de riesgos sísmicos.',
        'area': 'Ciencias de la Tierra',
        'color': '#166534',
    },
    'Diseño Gráfico y UX/UI': {
        'descripcion': 'Conceptualización visual, identidad de marca, tipografía y diseño de experiencias e interfaces digitales amigables.',
        'area': 'Artes y Medios Digitales',
        'color': '#EA580C',
    },
    'Artes Visuales y Animación Digital': {
        'descripcion': 'Producción artística, modelado tridimensional, ilustración digital y animación para cine, videojuegos y medios interactivos.',
        'area': 'Artes y Entretenimiento',
        'color': '#F97316',
    },
    'Periodismo Digital y Producción de Medios': {
        'descripcion': 'Investigación periodística, redacción de reportajes interactivos y dirección editorial en plataformas digitales multiplataforma.',
        'area': 'Comunicación y Medios',
        'color': '#0F172A',
    },
    'Música y Producción Musical': {
        'descripcion': 'Teoría e historia musical, composición, interpretación instrumental avanzada y mezcla o producción de audio digital.',
        'area': 'Artes y Música',
        'color': '#581C87',
    },
    'Artes Escénicas y Teatro': {
        'descripcion': 'Estudio del lenguaje corporal, actuación escénica y cinematográfica, dramaturgia y dirección teatral.',
        'area': 'Artes y Espectáculo',
        'color': '#9D174D',
    },
    'Gastronomía y Gestión Culinaria': {
        'descripcion': 'Técnicas culinarias globales, química de los alimentos y administración estratégica de negocios gastronómicos.',
        'area': 'Artes Culinarias y Negocios',
        'color': '#C2410C',
    },
}

# Mapa: carrera -> (interés requerido, habilidad requerida)
# Copia del knowledge base para cálculo funcional sin importar logic_rules
REQUISITOS_CARRERAS = {
    'Desarrollo de Software y Cloud':             ('Tecnología y Programación',  'Lógica y Matemática'),
    'Inteligencia Artificial y Ciencia de Datos':  ('Tecnología y Programación',  'Pensamiento Crítico e Investigación'),
    'Ciberseguridad y Redes de Información':      ('Tecnología y Programación',  'Razonamiento Verbal y Análisis'),
    'Medicina y Cirugía':                         ('Ciencias de la Salud',       'Destreza Manual e Instrumental'),
    'Psicología Clínica y Psicoterapia':          ('Ciencias de la Salud',       'Empatía y Relación Social'),
    'Enfermería y Salud Comunitaria':             ('Ciencias de la Salud',       'Empatía y Relación Social'),
    'Administración y Estrategia Corporativa':    ('Negocios y Liderazgo',       'Razonamiento Verbal y Análisis'),
    'Marketing Digital y E-Commerce':             ('Persuasión y Ventas',        'Empatía y Relación Social'),
    'Economía y Finanzas de Mercado':             ('Finanzas y Economía',        'Lógica y Matemática'),
    'Derecho Corporativo y Fiscal':               ('Leyes y Política',           'Razonamiento Verbal y Análisis'),
    'Relaciones Internacionales y Diplomacia':    ('Leyes y Política',           'Empatía y Relación Social'),
    'Ingeniería Civil y Estructuras':             ('Construcción e Ingeniería',  'Habilidad Espacial y Visual'),
    'Arquitectura y Diseño Urbano':               ('Construcción e Ingeniería',  'Habilidad Espacial y Visual'),
    'Ingeniería Mecánica y Robótica':             ('Construcción e Ingeniería',  'Destreza Manual e Instrumental'),
    'Biotecnología y Bioingeniería':              ('Investigación Científica',   'Lógica y Matemática'),
    'Química y Farmacia':                         ('Investigación Científica',   'Destreza Manual e Instrumental'),
    'Ciencias Ambientales y Energías Renovables': ('Ciencias de la Tierra',      'Pensamiento Crítico e Investigación'),
    'Geología y Recursos Naturales':              ('Ciencias de la Tierra',      'Pensamiento Crítico e Investigación'),
    'Diseño Gráfico y UX/UI':                     ('Arte y Creatividad',         'Habilidad Espacial y Visual'),
    'Artes Visuales y Animación Digital':         ('Arte y Creatividad',         'Habilidad Espacial y Visual'),
    'Periodismo Digital y Producción de Medios':  ('Comunicación y Medios',      'Razonamiento Verbal y Análisis'),
    'Música y Producción Musical':                ('Expresión Musical',          'Destreza Manual e Instrumental'),
    'Artes Escénicas y Teatro':                   ('Arte y Creatividad',         'Empatía y Relación Social'),
    'Gastronomía y Gestión Culinaria':            ('Arte y Creatividad',         'Destreza Manual e Instrumental'),
}


# ---------------------------------------------------------------------------
# 2. Función pura v2: scoring ponderado multi-factor
# ---------------------------------------------------------------------------
def _calcular_bonus_perfil(interes_req: str, intereses: dict) -> float:
    """
    Función pura auxiliar: calcula el bonus de alineación del perfil completo.

    Suma los scores de los intereses 'relacionados' con el área principal de la
    carrera y los normaliza a un porcentaje 0-100.

    La idea: si un usuario tiene alto interés en áreas afines a la carrera
    (aunque no sean el interés principal), recibe un bonus.

    Retorna: float en [0, 100]
    """
    relacionados = INTERESES_RELACIONADOS.get(interes_req, [])
    if not relacionados:
        return 0.0

    # Suma de scores de áreas relacionadas (max teórico: 5 * len(relacionados))
    suma = reduce(
        lambda acc, area: acc + intereses.get(area, 1),
        relacionados,
        0
    )
    max_posible = 5.0 * len(relacionados)
    return (suma / max_posible) * 100.0


def calcular_afinidad_v2(carrera: str, intereses: dict, habilidades: dict) -> float:
    """
    Función pura — scoring ponderado multi-factor (v2).

    Fórmula:
        score_primario   = (score_interes + score_habilidad) / 10 * 100   [0–100]
        score_secundario = bonus por intereses relacionados                [0–100]
        afinidad_final   = primario * PESO_PRIMARIO + secundario * PESO_SECUNDARIO

    El resultado diferencia mejor entre perfiles mixtos vs. muy especializados.
    Retorna: float en [0, 100]
    """
    interes_req, habilidad_req = REQUISITOS_CARRERAS.get(carrera, ('', ''))
    score_interes   = intereses.get(interes_req, 1)
    score_habilidad = habilidades.get(habilidad_req, 1)

    score_primario   = (score_interes + score_habilidad) / 10.0 * 100.0
    score_secundario = _calcular_bonus_perfil(interes_req, intereses)

    return score_primario * PESO_PRIMARIO + score_secundario * PESO_SECUNDARIO


def calcular_afinidad_detallada(carrera: str, intereses: dict, habilidades: dict) -> dict:
    """
    Función pura que devuelve un diccionario con afinidad y metadatos de la carrera.
    """
    puntaje          = calcular_afinidad_v2(carrera, intereses, habilidades)
    interes_req, habilidad_req = REQUISITOS_CARRERAS.get(carrera, ('', ''))
    meta = METADATA_CARRERAS.get(carrera, {
        'descripcion': 'Carrera profesional universitaria.',
        'area': 'General',
        'color': '#6B7280',
    })

    score_interes   = intereses.get(interes_req, 1)
    score_habilidad = habilidades.get(habilidad_req, 1)

    # Desglose del score para la UI (componentes individuales)
    score_primario_pct   = round((score_interes + score_habilidad) / 10.0 * 100.0, 1)
    score_secundario_pct = round(_calcular_bonus_perfil(interes_req, intereses), 1)

    return {
        'nombre':               carrera,
        'puntaje':              round(puntaje, 1),
        'interes_clave':        interes_req,
        'habilidad_clave':      habilidad_req,
        'score_interes':        score_interes,
        'score_habilidad':      score_habilidad,
        'pct_primario':         score_primario_pct,
        'pct_secundario':       score_secundario_pct,
        **meta
    }


# ---------------------------------------------------------------------------
# 3. Pipeline funcional principal
# ---------------------------------------------------------------------------
def procesar_recomendaciones(
    candidatas: list,
    intereses: dict,
    habilidades: dict,
    top_n: int = 5,
    umbral_min_pct: float = 40.0
) -> list:
    """
    Pipeline funcional puro que transforma la lista de carreras candidatas
    (del módulo lógico) en una lista ordenada y enriquecida de recomendaciones.

    Etapas:
      1. map()    → Enriquecer cada carrera con su puntaje v2 y metadata.
      2. filter() → Descartar carreras con afinidad menor al umbral mínimo.
      3. sorted() → Ordenar de mayor a menor puntaje (con lambda).
      4. slice    → Tomar solo el top N de resultados.

    Parámetros:
        candidatas      (list): Carreras inferidas por el módulo lógico.
        intereses       (dict): Scores de interés del usuario.
        habilidades     (dict): Scores de habilidad del usuario.
        top_n           (int):  Máximo de recomendaciones a devolver.
        umbral_min_pct  (float): Puntaje mínimo (%) para incluir en resultados.

    Retorna:
        list[dict]: Lista ordenada de diccionarios con info de cada carrera.
    """
    # Etapa 1: map() — Calcular afinidad detallada v2 para cada carrera candidata
    enriquecidas = list(map(
        lambda carrera: calcular_afinidad_detallada(carrera, intereses, habilidades),
        candidatas
    ))

    # Etapa 2: filter() — Descartar candidatas con puntaje muy bajo
    filtradas = list(filter(
        lambda c: c['puntaje'] >= umbral_min_pct,
        enriquecidas
    ))

    # Si el filtro dejó vacío, relajamos el umbral y tomamos todo
    if not filtradas:
        filtradas = enriquecidas

    # Etapa 3: sorted() con lambda — Rankear de mayor a menor puntaje
    rankeadas = sorted(filtradas, key=lambda c: c['puntaje'], reverse=True)

    # Etapa 4: Tomar solo las top_n recomendaciones
    top_resultados = rankeadas[:top_n]

    # Añadir posición de ranking con map() + enumerate
    top_con_rango = list(map(
        lambda par: {**par[1], 'rango': par[0] + 1},
        enumerate(top_resultados)
    ))

    return top_con_rango


def calcular_resumen_perfil(intereses: dict, habilidades: dict) -> dict:
    """
    Función pura que genera un resumen extendido del perfil del usuario usando reduce().

    Calcula:
      - Score total de intereses (suma).
      - Score total de habilidades (suma).
      - Interés dominante (el de mayor score).
      - Habilidad dominante (la de mayor score).
      - Top 3 intereses y top 3 habilidades (para el gráfico de radar).
      - Scores individuales de intereses y habilidades (para el radar).
    """
    # reduce() para sumar todos los scores de intereses
    total_intereses   = reduce(lambda acc, v: acc + v, intereses.values(), 0)
    total_habilidades = reduce(lambda acc, v: acc + v, habilidades.values(), 0)

    # Interés y habilidad dominantes usando max() con lambda
    interes_dominante   = max(intereses.items(), key=lambda x: x[1], default=('Ninguno', 0))
    habilidad_dominante = max(habilidades.items(), key=lambda x: x[1], default=('Ninguna', 0))

    # Top 3 intereses y habilidades (sorted con lambda, slice)
    top3_intereses   = sorted(intereses.items(),   key=lambda x: x[1], reverse=True)[:3]
    top3_habilidades = sorted(habilidades.items(), key=lambda x: x[1], reverse=True)[:3]

    # Listas ordenadas completas para el gráfico de radar (funcional: map sobre sorted)
    intereses_ordenados   = sorted(intereses.items(),   key=lambda x: x[1], reverse=True)
    habilidades_ordenadas = sorted(habilidades.items(), key=lambda x: x[1], reverse=True)

    # Listas serializables para JSON (map convierte tuplas a dict)
    radar_intereses   = list(map(lambda p: {'label': p[0], 'value': p[1]}, intereses_ordenados))
    radar_habilidades = list(map(lambda p: {'label': p[0], 'value': p[1]}, habilidades_ordenadas))

    return {
        'total_intereses':       total_intereses,
        'total_habilidades':     total_habilidades,
        'interes_dominante':     interes_dominante[0],
        'habilidad_dominante':   habilidad_dominante[0],
        'promedio_intereses':    round(total_intereses   / max(len(intereses),   1), 2),
        'promedio_habilidades':  round(total_habilidades / max(len(habilidades), 1), 2),
        'top3_intereses':        [{'nombre': k, 'score': v} for k, v in top3_intereses],
        'top3_habilidades':      [{'nombre': k, 'score': v} for k, v in top3_habilidades],
        'radar_intereses':       radar_intereses,
        'radar_habilidades':     radar_habilidades,
    }
