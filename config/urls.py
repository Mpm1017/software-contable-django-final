"""
URL configuration for config project.
... (Resto de comentarios de Django)
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 1. Ruta de Administración
    path('admin/', admin.site.urls),

    # 2. Rutas de Autenticación de Django (Login, Logout, Password Reset)
    path('accounts/', include('django.contrib.auth.urls')),

    # 3. Ruta base que apunta a nuestra aplicación 'users'
    path('', include('users.urls')),
]