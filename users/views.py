from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .forms import RegisterForm

# Constantes para evitar duplicación de cadenas
DASHBOARD_USER = 'user_dashboard'
DASHBOARD_ADMIN = 'admin_dashboard'
TEMPLATE_USER_LOGIN = 'registration/user_login.html'
TEMPLATE_ADMIN_LOGIN = 'registration/admin_login.html'
TEMPLATE_ADMIN_USER_MANAGEMENT = 'users/admin_user_management.html'
TEMPLATE_ADMIN_USER_EDIT = 'users/admin_user_edit.html'
TEMPLATE_ADMIN_USER_DELETE = 'users/admin_user_delete.html'
TEMPLATE_ADMIN_CONFIG = 'users/admin_config.html'
URL_ADMIN_USER_MANAGEMENT = 'admin_user_management'
SESSION_ACCESS_TOKEN = 'access_token'
SESSION_REFRESH_TOKEN = 'refresh_token'
SESSION_USER_ROLE = 'user_role'
POST_USERNAME = 'username'
POST_PASSWORD = 'password'
MSG_NO_PERMISOS = 'No tienes permisos para acceder a esta sección.'
MSG_CREDENCIALES_INCORRECTAS = 'Usuario o contraseña incorrectos.'

def index(request):
    """
    Vista inicial - Redirige según el estado de autenticación
    """
    if request.user.is_authenticated:
        # Si es admin, va al dashboard de admin
        if request.user.is_staff or request.user.is_superuser:
            return redirect(DASHBOARD_ADMIN)
        # Si es usuario normal, va al dashboard de usuario
        return redirect(DASHBOARD_USER)
    # Si NO está autenticado, muestra selección de rol
    return redirect('role_selection')

def role_selection(request):
    """
    Vista de selección de rol (Usuario/Administrador)
    """
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'users/role_selection.html') 

@login_required
def user_dashboard(request):
    """
    Dashboard para USUARIOS NORMALES
    Funcionalidades limitadas
    """
    # Verificar que NO sea admin
    if request.user.is_staff or request.user.is_superuser:
        return redirect(DASHBOARD_ADMIN)
    
    access_token = request.session.get(SESSION_ACCESS_TOKEN, None)
    refresh_token = request.session.get(SESSION_REFRESH_TOKEN, None)
    
    context = {
        'username': request.user.username,
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user_role': 'Usuario',
        'is_admin': False,
    }
    return render(request, 'users/user_dashboard.html', context)


@login_required
def admin_dashboard(request):
    """
    Dashboard para ADMINISTRADORES
    Funcionalidades completas
    """
    # Verificar que SÍ sea admin
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect(DASHBOARD_USER)
    
    access_token = request.session.get(SESSION_ACCESS_TOKEN, None)
    refresh_token = request.session.get(SESSION_REFRESH_TOKEN, None)
    
    # Estadísticas para admin
    total_usuarios = User.objects.count()
    
    context = {
        'username': request.user.username,
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user_role': 'Administrador',
        'is_admin': True,
        'total_usuarios': total_usuarios,
    }
    return render(request, 'users/admin_dashboard.html', context)

# Vista de Registro (Se mantiene la lógica de formulario funcional)
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Guardar el nuevo usuario
            user = form.save()
            
            # Crear categorías predeterminadas para el nuevo usuario
            from accounting.utils import crear_categorias_predeterminadas
            try:
                categorias_creadas = crear_categorias_predeterminadas(user)
                messages.success(
                    request, 
                    f'¡Cuenta creada exitosamente! Se han creado {categorias_creadas} categorías predeterminadas para ti. Ahora puedes iniciar sesión.'
                )
            except Exception:
                messages.success(
                    request,
                    '¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.'
                )
            
            return redirect('login') 
    else:
        form = RegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    """
    Vista de login para USUARIOS NORMALES con JWT.
    """
    if request.user.is_authenticated:
        return redirect('user_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Verificar que NO sea admin
            if user.is_staff or user.is_superuser:
                messages.error(request, 'Esta área es solo para usuarios. Los administradores deben usar el login de administrador.')
                return render(request, TEMPLATE_USER_LOGIN)
            
            # Login y JWT
            auth_login(request, user)
            refresh = RefreshToken.for_user(user)
            request.session[SESSION_ACCESS_TOKEN] = str(refresh.access_token)
            request.session[SESSION_REFRESH_TOKEN] = str(refresh)
            request.session[SESSION_USER_ROLE] = 'user'
            
            messages.success(request, f'¡Bienvenido, {user.username}!')
            return redirect(DASHBOARD_USER)
        else:
            messages.error(request, MSG_CREDENCIALES_INCORRECTAS)
    
    return render(request, TEMPLATE_USER_LOGIN)


def admin_login(request):
    """
    Vista de login para ADMINISTRADORES con JWT.
    """
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Verificar que SÍ sea admin
            if not (user.is_staff or user.is_superuser):
                messages.error(request, 'Acceso denegado. Esta área es solo para administradores.')
                return render(request, 'registration/admin_login.html')
            
            # Login y JWT
            auth_login(request, user)
            refresh = RefreshToken.for_user(user)
            request.session[SESSION_ACCESS_TOKEN] = str(refresh.access_token)
            request.session[SESSION_REFRESH_TOKEN] = str(refresh)
            request.session[SESSION_USER_ROLE] = 'admin'
            
            messages.success(request, f'¡Bienvenido, Administrador {user.username}!')
            return redirect(DASHBOARD_ADMIN)
        else:
            messages.error(request, MSG_CREDENCIALES_INCORRECTAS)
    
    return render(request, TEMPLATE_ADMIN_LOGIN)


def custom_logout(request):
    """
    Vista de logout personalizada que limpia los tokens JWT.
    """
    # Limpiamos los tokens de la sesión
    if SESSION_ACCESS_TOKEN in request.session:
        del request.session[SESSION_ACCESS_TOKEN]
    if SESSION_REFRESH_TOKEN in request.session:
        del request.session[SESSION_REFRESH_TOKEN]
    if SESSION_USER_ROLE in request.session:
        del request.session[SESSION_USER_ROLE]
    
    # Limpiar todos los mensajes anteriores
    storage = get_messages(request)
    for _ in storage:
        pass  # Esto consume/limpia todos los mensajes
    
    # Logout tradicional de Django
    auth_logout(request)
    
    # Agregar solo el mensaje de logout
    messages.success(request, '¡Has cerrado sesión exitosamente!')
    
    return redirect('user_login')


# ================================================
# GESTIÓN DE USUARIOS (ADMIN)
# ================================================

@login_required
def admin_user_management(request):
    """Vista para gestionar usuarios (solo administradores)"""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, MSG_NO_PERMISOS)
        return redirect(DASHBOARD_USER)
    
    users = User.objects.all().order_by('-date_joined')
    
    context = {
        'users': users,
        'total_users': users.count(),
        'active_users': users.filter(is_active=True).count(),
        'admin_users': users.filter(is_staff=True).count(),
    }
    
    return render(request, 'users/admin_user_management.html', context)


@login_required
def admin_user_edit(request, user_id):
    """Vista para editar un usuario"""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, MSG_NO_PERMISOS)
        return redirect(DASHBOARD_USER)
    
    user_to_edit = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        # Actualizar datos del usuario
        user_to_edit.username = request.POST.get('username')
        user_to_edit.email = request.POST.get('email')
        user_to_edit.first_name = request.POST.get('first_name')
        user_to_edit.last_name = request.POST.get('last_name')
        user_to_edit.is_active = request.POST.get('is_active') == 'on'
        # is_staff se gestiona desde la terminal con manage.py createsuperuser
        
        # Cambiar contraseña si se proporciona
        new_password = request.POST.get('new_password')
        if new_password:
            user_to_edit.set_password(new_password)
        
        user_to_edit.save()
        messages.success(request, f'Usuario {user_to_edit.username} actualizado exitosamente.')
        return redirect('admin_user_management')
    
    context = {
        'user_to_edit': user_to_edit,
    }
    
    return render(request, 'users/admin_user_edit.html', context)


@login_required
def admin_user_delete(request, user_id):
    """Vista para eliminar un usuario"""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, MSG_NO_PERMISOS)
        return redirect(DASHBOARD_USER)
    
    user_to_delete = get_object_or_404(User, id=user_id)
    
    # No permitir que se elimine a sí mismo
    if user_to_delete == request.user:
        messages.error(request, 'No puedes eliminar tu propia cuenta.')
        return redirect('admin_user_management')
    
    if request.method == 'POST':
        username = user_to_delete.username
        user_to_delete.delete()
        messages.success(request, f'Usuario {username} eliminado exitosamente.')
        return redirect('admin_user_management')
    
    context = {
        'user_to_delete': user_to_delete,
    }
    
    return render(request, 'users/admin_user_delete.html', context)


@login_required
def admin_config(request):
    """Vista de configuración del sistema (admin)"""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, MSG_NO_PERMISOS)
        return redirect(DASHBOARD_USER)
    
    from accounting.models import Transaction, Account, Category
    
    # Estadísticas del sistema
    stats = {
        'total_transactions': Transaction.objects.count(),
        'total_accounts': Account.objects.count(),
        'total_categories': Category.objects.count(),
        'total_users': User.objects.count(),
    }
    
    context = {
        'stats': stats,
    }
    
    return render(request, 'users/admin_config.html', context)
