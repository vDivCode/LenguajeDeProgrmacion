from unittest.mock import patch

MOCK_DATOS = {
    'preguntas': [
        {'id': 'int_tecnologia', 'texto': '¿Qué tanto te interesa el desarrollo de software y la tecnología?', 'tipo': 'interes', 'categoria': 'Tecnología y Programación', 'ordem': 1},
        {'id': 'int_salud', 'texto': 'Salud', 'tipo': 'interes', 'categoria': 'Ciencias de la Salud', 'ordem': 2},
        {'id': 'int_liderazgo', 'texto': 'Liderazgo', 'tipo': 'interes', 'categoria': 'Negocios y Liderazgo', 'ordem': 3},
        {'id': 'int_arte_diseno', 'texto': 'Arte', 'tipo': 'interes', 'categoria': 'Arte y Creatividad', 'ordem': 4},
        {'id': 'int_leyes', 'texto': 'Leyes', 'tipo': 'interes', 'categoria': 'Leyes y Política', 'ordem': 5},
        {'id': 'int_construccion', 'texto': 'Construcción', 'tipo': 'interes', 'categoria': 'Construcción e Ingeniería', 'ordem': 6},
        {'id': 'int_naturaleza', 'texto': 'Naturaleza', 'tipo': 'interes', 'categoria': 'Ciencias de la Tierra', 'ordem': 7},
        {'id': 'int_comunicacion', 'texto': 'Comunicacion', 'tipo': 'interes', 'categoria': 'Comunicación y Medios', 'ordem': 8},
        {'id': 'int_economia', 'texto': 'Economia', 'tipo': 'interes', 'categoria': 'Finanzas y Economía', 'ordem': 9},
        {'id': 'int_musica', 'texto': 'Musica', 'tipo': 'interes', 'categoria': 'Expresión Musical', 'ordem': 10},
        {'id': 'int_ciencias', 'texto': 'Ciencias', 'tipo': 'interes', 'categoria': 'Investigación Científica', 'ordem': 11},
        {'id': 'int_persuasion', 'texto': 'Persuasion', 'tipo': 'interes', 'categoria': 'Persuasión y Ventas', 'ordem': 12},
        {'id': 'hab_logica_matematica', 'texto': 'Lógica', 'tipo': 'habilidad', 'categoria': 'Lógica y Matemática', 'ordem': 13},
        {'id': 'hab_empatia', 'texto': 'Empatía', 'tipo': 'habilidad', 'categoria': 'Empatía y Relación Social', 'ordem': 14},
        {'id': 'hab_espacial', 'texto': 'Espacial', 'tipo': 'habilidad', 'categoria': 'Habilidad Espacial y Visual', 'ordem': 15},
        {'id': 'hab_destreza_manual', 'texto': 'Manual', 'tipo': 'habilidad', 'categoria': 'Destreza Manual e Instrumental', 'ordem': 16},
        {'id': 'hab_verbal', 'texto': 'Verbal', 'tipo': 'habilidad', 'categoria': 'Razonamiento Verbal y Análisis', 'ordem': 17},
        {'id': 'hab_critico', 'texto': 'Critico', 'tipo': 'habilidad', 'categoria': 'Pensamiento Crítico e Investigación', 'ordem': 18},
    ],
    'carreras': [
        {'nombre': 'Desarrollo de Software y Cloud', 'activa': True, 'descripcion': 'Dev', 'area': 'Tech', 'color': '#000'},
        {'nombre': 'Economía y Finanzas de Mercado', 'activa': True, 'descripcion': 'Econ', 'area': 'Biz', 'color': '#111'},
        {'nombre': 'Biotecnología y Bioingeniería', 'activa': True, 'descripcion': 'Bio', 'area': 'Sci', 'color': '#222'}
    ],
    'reglas': [
        {'carrera': 'Desarrollo de Software y Cloud', 'interes': 'Tecnología y Programación', 'habilidad': 'Lógica y Matemática'},
        {'carrera': 'Economía y Finanzas de Mercado', 'interes': 'Finanzas y Economía', 'habilidad': 'Lógica y Matemática'},
        {'carrera': 'Biotecnología y Bioingeniería', 'interes': 'Investigación Científica', 'habilidad': 'Pensamiento Crítico e Investigación'}
    ],
    'config': [
        {'clave': 'UMBRAL_MINIMO', 'valor_numerico': 3},
        {'clave': 'PESO_PRIMARIO', 'valor_numerico': 0.70},
        {'clave': 'PESO_SECUNDARIO', 'valor_numerico': 0.30}
    ],
    'relacionados': []
}

def _mock_datos():
    return MOCK_DATOS

def patch_loader():
    return patch('test_vocacional.datos.loader._datos', new=_mock_datos)
