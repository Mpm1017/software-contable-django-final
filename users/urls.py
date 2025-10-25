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
]