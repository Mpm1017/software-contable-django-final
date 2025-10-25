from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users.views_password_reset import CustomPasswordResetView

urlpatterns = [
    # 1. Ruta de Administración
    path('admin/', admin.site.urls),

    # 2. Ruta personalizada de recuperación de contraseña (con email HTML)
    path('accounts/password_reset/', 
         CustomPasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             email_template_name='registration/password_reset_email.html',
             subject_template_name='registration/password_reset_subject.txt',
             success_url='/accounts/password_reset/done/'
         ), 
         name='password_reset'),
    
    # 3. Resto de rutas de autenticación de Django
    path('accounts/', include('django.contrib.auth.urls')),

    # 4. Rutas del módulo de Contabilidad
    path('accounting/', include('accounting.urls')),

    # 5. Ruta base que apunta a nuestra aplicación 'users'
    path('', include('users.urls')),
]