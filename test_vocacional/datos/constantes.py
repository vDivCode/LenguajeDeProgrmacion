"""
=============================================================================
MÓDULO DE DATOS - constantes.py
=============================================================================
Este módulo concentra toda la base de conocimiento estática del sistema.
=============================================================================
"""

UMBRAL_MINIMO = 3
PESO_PRIMARIO    = 0.70
PESO_SECUNDARIO  = 0.30

PREGUNTAS_INTERESES = [
    {'id': 'int_tecnologia', 'categoria': 'Tecnología y Programación', 'texto': '¿Qué tanto te interesa el desarrollo de software, la programación y el diseño de sistemas informáticos o en la nube?'},
    {'id': 'int_salud', 'categoria': 'Ciencias de la Salud', 'texto': '¿Te atrae el estudio de la medicina, la anatomía, el diagnóstico clínico y el cuidado físico o mental de los pacientes?'},
    {'id': 'int_liderazgo', 'categoria': 'Negocios y Liderazgo', 'texto': '¿Cuánto te interesa dirigir equipos de trabajo, planificar estrategias corporativas y coordinar el crecimiento de organizaciones?'},
    {'id': 'int_arte_diseno', 'categoria': 'Arte y Creatividad', 'texto': '¿Qué tanto disfrutas expresarte mediante las artes visuales, la animación digital, el diseño de interfaces o la actuación?'},
    {'id': 'int_leyes', 'categoria': 'Leyes y Política', 'texto': '¿Te interesa analizar el marco legal, las políticas públicas, la defensa de los derechos ciudadanos y la justicia social?'},
    {'id': 'int_construccion', 'categoria': 'Construcción e Ingeniería', 'texto': '¿Te atrae el diseño estructural de edificios, la robótica industrial, el funcionamiento de máquinas o la planificación de obras?'},
    {'id': 'int_naturaleza', 'categoria': 'Ciencias de la Tierra', 'texto': '¿Cuánto te apasiona la ecología, el impacto de las energías renovables y la conservación del medio ambiente y los recursos naturales?'},
    {'id': 'int_comunicacion', 'categoria': 'Comunicación y Medios', 'texto': '¿Qué tanto te interesa la redacción periodística, la producción audiovisual y la comunicación de información en plataformas digitales?'},
    {'id': 'int_economia', 'categoria': 'Finanzas y Economía', 'texto': '¿Te atrae analizar los mercados financieros, la asignación de recursos económicos y las estrategias de inversión o comercio?'},
    {'id': 'int_musica', 'categoria': 'Expresión Musical', 'texto': '¿Cuánto te interesa la teoría musical, la composición, la interpretación de instrumentos o la producción de audio?'},
    {'id': 'int_ciencias', 'categoria': 'Investigación Científica', 'texto': '¿Te apasiona la experimentación en laboratorios, el estudio de la bioquímica, la genética o el desarrollo de nuevos fármacos?'},
    {'id': 'int_persuasion', 'categoria': 'Persuasión y Ventas', 'texto': '¿Qué tanto disfrutas diseñar campañas publicitarias, negociar acuerdos comerciales o convencer a un público de adoptar una idea?'},
]

PREGUNTAS_HABILIDADES = [
    {'id': 'hab_logica_matematica', 'categoria': 'Lógica y Matemática', 'texto': '¿Qué nivel de facilidad tienes para resolver problemas matemáticos, aplicar el pensamiento abstracto y analizar datos estructurados?'},
    {'id': 'hab_empatia', 'categoria': 'Empatía y Relación Social', 'texto': '¿Qué tan bien logras comprender las emociones de los demás, comunicarte con sensibilidad y resolver conflictos interpersonales?'},
    {'id': 'hab_espacial', 'categoria': 'Habilidad Espacial y Visual', 'texto': '¿Qué tan desarrollado tienes el sentido de orientación, la visualización de volúmenes en tres dimensiones y el dibujo técnico?'},
    {'id': 'hab_destreza_manual', 'categoria': 'Destreza Manual e Instrumental', 'texto': '¿Qué facilidad posees para manipular herramientas con precisión, tocar instrumentos musicales o realizar trabajos que exigen coordinación motora fina?'},
    {'id': 'hab_verbal', 'categoria': 'Razonamiento Verbal y Análisis', 'texto': '¿Qué tan bueno/a eres para redactar informes detallados, argumentar ideas complejas por escrito y debatir con claridad?'},
    {'id': 'hab_critico', 'categoria': 'Pensamiento Crítico e Investigación', 'texto': '¿Qué tan desarrollado tienes el hábito de cuestionar hechos, investigar hipótesis científicas y evaluar objetivamente la validez de la información?'},
]

ID_A_CATEGORIA_INTERES   = {p['id']: p['categoria'] for p in PREGUNTAS_INTERESES}
ID_A_CATEGORIA_HABILIDAD = {p['id']: p['categoria'] for p in PREGUNTAS_HABILIDADES}
ID_A_TEXTO_PREGUNTA = {p['id']: p['texto'][:80] + '…' for p in PREGUNTAS_INTERESES + PREGUNTAS_HABILIDADES}

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

KNOWLEDGE_BASE = [
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

REQUISITOS_CARRERAS = {carrera: (interes, habilidad) for carrera, interes, habilidad in KNOWLEDGE_BASE}

METADATA_CARRERAS = {
    'Desarrollo de Software y Cloud': {'descripcion': 'Diseño, construcción e implementación de aplicaciones, arquitecturas en la nube y sistemas de software escalables.', 'area': 'Ingeniería y Tecnología', 'color': '#2563EB'},
    'Inteligencia Artificial y Ciencia de Datos': {'descripcion': 'Desarrollo de modelos de aprendizaje automático, procesamiento de grandes volúmenes de datos y algoritmos de inteligencia artificial.', 'area': 'Ingeniería y Ciencias Exactas', 'color': '#3B82F6'},
    'Ciberseguridad y Redes de Información': {'descripcion': 'Protección de infraestructuras críticas digitales, auditoría de vulnerabilidades y diseño de políticas de seguridad informática.', 'area': 'Ingeniería y Seguridad', 'color': '#1D4ED8'},
    'Medicina y Cirugía': {'descripcion': 'Diagnóstico, tratamiento y prevención de patologías humanas, combinando fundamentos científicos y prácticas clínicas quirúrgicas.', 'area': 'Ciencias de la Salud', 'color': '#DC2626'},
    'Psicología Clínica y Psicoterapia': {'descripcion': 'Evaluación, diagnóstico y terapia de la salud mental y el comportamiento, promoviendo el bienestar emocional.', 'area': 'Ciencias de la Salud y Sociales', 'color': '#DB2777'},
    'Enfermería y Salud Comunitaria': {'descripcion': 'Atención y cuidado integral del paciente, gestión hospitalaria y desarrollo de programas preventivos de salud pública.', 'area': 'Ciencias de la Salud', 'color': '#EC4899'},
    'Administración y Estrategia Corporativa': {'descripcion': 'Planificación, organización y toma de decisiones estratégicas para optimizar recursos financieros y liderar organizaciones.', 'area': 'Negocios y Administración', 'color': '#059669'},
    'Marketing Digital y E-Commerce': {'descripcion': 'Diseño de campañas de posicionamiento, análisis de comportamiento del consumidor en entornos digitales y comercio electrónico.', 'area': 'Negocios y Comunicación', 'color': '#10B981'},
    'Economía y Finanzas de Mercado': {'descripcion': 'Análisis de tendencias económicas globales, mercados de valores, modelado financiero y asignación estratégica de recursos.', 'area': 'Economía y Finanzas', 'color': '#047857'},
    'Derecho Corporativo y Fiscal': {'descripcion': 'Asesoría jurídica empresarial, cumplimiento de normativas fiscales, redacción de contratos y resolución de disputas legales.', 'area': 'Derecho y Ciencias Jurídicas', 'color': '#6D28D9'},
    'Relaciones Internacionales y Diplomacia': {'descripcion': 'Análisis de la política global, diplomacia, resolución de conflictos internacionales y gestión en organismos no gubernamentales.', 'area': 'Ciencias Sociales y Políticas', 'color': '#7C3AED'},
    'Ingeniería Civil y Estructuras': {'descripcion': 'Diseño estructural, supervisión y construcción de infraestructuras complejas como puentes, autopistas y edificaciones.', 'area': 'Ingeniería y Construcción', 'color': '#78350F'},
    'Arquitectura y Diseño Urbano': {'descripcion': 'Planificación de espacios habitables, diseño arquitectónico sostenible y ordenamiento urbano que armoniza estética y funcionalidad.', 'area': 'Artes y Construcción', 'color': '#92400E'},
    'Ingeniería Mecánica y Robótica': {'descripcion': 'Diseño, manufactura y automatización de sistemas mecánicos complejos, robótica industrial y maquinaria.', 'area': 'Ingeniería y Manufactura', 'color': '#374151'},
    'Biotecnología y Bioingeniería': {'descripcion': 'Manipulación genética y celular de organismos vivos para desarrollar soluciones aplicadas a la farmacia, medicina y agricultura.', 'area': 'Investigación y Ciencias Exactas', 'color': '#0369A1'},
    'Química y Farmacia': {'descripcion': 'Investigación y síntesis de compuestos químicos, diseño farmacológico y control de calidad de medicamentos.', 'area': 'Investigación y Salud', 'color': '#0891B2'},
    'Ciencias Ambientales y Energías Renovables': {'descripcion': 'Evaluación de impacto ambiental, conservación biológica y desarrollo de tecnologías de generación energética sostenible.', 'area': 'Ciencias de la Tierra y Ambientales', 'color': '#15803D'},
    'Geología y Recursos Naturales': {'descripcion': 'Estudio de la estructura terrestre, prospección de recursos minerales e hídricos, y mitigación de riesgos sísmicos.', 'area': 'Ciencias de la Tierra', 'color': '#166534'},
    'Diseño Gráfico y UX/UI': {'descripcion': 'Conceptualización visual, identidad de marca, tipografía y diseño de experiencias e interfaces digitales amigables.', 'area': 'Artes y Medios Digitales', 'color': '#EA580C'},
    'Artes Visuales y Animación Digital': {'descripcion': 'Producción artística, modelado tridimensional, ilustración digital y animación para cine, videojuegos y medios interactivos.', 'area': 'Artes y Entretenimiento', 'color': '#F97316'},
    'Periodismo Digital y Producción de Medios': {'descripcion': 'Investigación periodística, redacción de reportajes interactivos y dirección editorial en plataformas digitales multiplataforma.', 'area': 'Comunicación y Medios', 'color': '#0F172A'},
    'Música y Producción Musical': {'descripcion': 'Teoría e historia musical, composición, interpretación instrumental avanzada y mezcla o producción de audio digital.', 'area': 'Artes y Música', 'color': '#581C87'},
    'Artes Escénicas y Teatro': {'descripcion': 'Estudio del lenguaje corporal, actuación escénica y cinematográfica, dramaturgia y dirección teatral.', 'area': 'Artes y Espectáculo', 'color': '#9D174D'},
    'Gastronomía y Gestión Culinaria': {'descripcion': 'Técnicas culinarias globales, química de los alimentos y administración estratégica de negocios gastronómicos.', 'area': 'Artes Culinarias y Negocios', 'color': '#C2410C'},
}
