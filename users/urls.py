from django.urls import path
from . import views

urlpatterns = [
    # Ruta base
    path('', views.index, name='index'),
    
    # Selección de rol
    path('role-selection/', views.role_selection, name='role_selection'),
    
    # Logins separados
    path('login/user/', views.user_login, name='user_login'),
    path('login/admin/', views.admin_login, name='admin_login'),
    path('login/', views.user_login, name='login'),  # Por compatibilidad
    
    # Dashboards separados
    path('dashboard/user/', views.user_dashboard, name='user_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/', views.user_dashboard, name='dashboard'),  # Por compatibilidad
    
    # Logout
    path('logout/', views.custom_logout, name='logout'),
    
    # Registro
    path('register/', views.register, name='register'),
    
    # Gestión de usuarios (admin)
    path('management/users/', views.admin_user_management, name='admin_user_management'),
    path('management/users/<int:user_id>/edit/', views.admin_user_edit, name='admin_user_edit'),
    path('management/users/<int:user_id>/delete/', views.admin_user_delete, name='admin_user_delete'),
    path('management/config/', views.admin_config, name='admin_config'),
]