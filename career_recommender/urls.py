# pyrefly: ignore [missing-import]
from django.urls import path
from recommender.controllers.career_controller import CareerController

controller = CareerController()

urlpatterns = [
    path("", controller.index, name="index"),
    path("recommend/", controller.recommend, name="recommend"),
]
