from django.urls import path
from recommender import vistas

urlpatterns = [
    path("", vistas.inicio, name="index"),
    path("recommend/", vistas.recomendar, name="recommend"),
]
