from django.urls import path
from . import views

urlpatterns = [
    # Ruta base: Ya existía, apunta a la vista index
    path('', views.index, name='index'),
    
    # RUTA AÑADIDA: Define la ruta 'register' que faltaba
    path('register/', views.register, name='register'),
]