"""
=============================================================================
VISTAS - views.py
=============================================================================
Paradigma: IMPERATIVO (manejo de eventos HTTP, flujo de solicitudes)

Las vistas Django actúan como coordinadores entre la interfaz web y el
controlador principal. Cada vista maneja un evento HTTP específico y
delega la lógica al TestVocacionalController.
=============================================================================
"""

import json
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from test_vocacional.controller import TestVocacionalController


# ---------------------------------------------------------------------------
# Vista: Página de inicio (Home)
# ---------------------------------------------------------------------------
class HomeView(View):
    """Vista de bienvenida. Muestra la portada del test vocacional."""

    def get(self, request):
        # Limpiar sesión anterior si existe
        if 'resultados' in request.session:
            del request.session['resultados']
        return render(request, 'test_vocacional/home.html')


# ---------------------------------------------------------------------------
# Vista: Test vocacional (cuestionario)
# ---------------------------------------------------------------------------
class TestView(View):
    """
    Vista del cuestionario.
    GET  → Muestra las preguntas.
    POST → Procesa respuestas y redirige a resultados.
    """

    def get(self, request):
        controlador = TestVocacionalController()
        estructura = controlador.obtener_estructura_test()
        return render(request, 'test_vocacional/test.html', {
            'preguntas_intereses':  estructura['preguntas_intereses'],
            'preguntas_habilidades': estructura['preguntas_habilidades'],
            'total_preguntas':     estructura['total_preguntas'],
            'total_intereses':     estructura['total_intereses'],
            'total_habilidades':   estructura['total_habilidades'],
        })

    def post(self, request):
        controlador = TestVocacionalController()

        # Ejecutar pipeline completo
        resultado = controlador.ejecutar_pipeline(request.POST)

        if not resultado['exito']:
            # Hay errores de validación, recargar test con errores
            estructura = controlador.obtener_estructura_test()
            return render(request, 'test_vocacional/test.html', {
                'preguntas_intereses':  estructura['preguntas_intereses'],
                'preguntas_habilidades': estructura['preguntas_habilidades'],
                'total_preguntas':     estructura['total_preguntas'],
                'total_intereses':     estructura['total_intereses'],
                'total_habilidades':   estructura['total_habilidades'],
                'errores':             resultado['errores'],
            })

        # Guardar resultados en sesión y redirigir
        request.session['resultados'] = json.dumps(resultado, ensure_ascii=False)
        return redirect('test_vocacional:resultados')


# ---------------------------------------------------------------------------
# Vista: Resultados
# ---------------------------------------------------------------------------
class ResultadosView(View):
    """Muestra las recomendaciones personalizadas generadas por el sistema."""

    def get(self, request):
        resultados_json = request.session.get('resultados', None)
        if not resultados_json:
            return redirect('test_vocacional:home')

        resultado = json.loads(resultados_json)
        perfil = resultado.get('perfil', {})

        # Serializar listas de radar a JSON para pasar al template JS
        radar_intereses_json   = json.dumps(perfil.get('radar_intereses', []),   ensure_ascii=False)
        radar_habilidades_json = json.dumps(perfil.get('radar_habilidades', []), ensure_ascii=False)

        return render(request, 'test_vocacional/results.html', {
            'recomendaciones':      resultado.get('recomendaciones', []),
            'perfil':               perfil,
            'advertencias':         resultado.get('advertencias', []),
            'total_candidatas':     resultado.get('total_candidatas_logicas', 0),
            'radar_intereses_json': radar_intereses_json,
            'radar_habilidades_json': radar_habilidades_json,
        })
