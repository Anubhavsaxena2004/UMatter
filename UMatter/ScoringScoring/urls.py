from django.urls import path
from .views import get_questions, evaluate_test

urlpatterns = [
    path("questions/", get_questions),
    path("evaluate/", evaluate_test),
]
