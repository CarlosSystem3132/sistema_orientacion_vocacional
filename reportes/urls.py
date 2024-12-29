from django.urls import path
from . import views

urlpatterns = [
    path('solicitar/', views.solicitar_reporte, name='solicitar_reporte'),
]

