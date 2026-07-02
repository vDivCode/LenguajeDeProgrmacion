from django.urls import path
from test_vocacional.views import HomeView, TestView, ResultadosView

app_name = 'test_vocacional'

urlpatterns = [
    path('',           HomeView.as_view(),      name='home'),
    path('test/',      TestView.as_view(),        name='test'),
    path('resultados/', ResultadosView.as_view(), name='resultados'),
]
