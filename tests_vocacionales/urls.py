from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_vocacional, name='test_vocacional'),
    path('resultados/', views.resultados, name='resultados'),
]

