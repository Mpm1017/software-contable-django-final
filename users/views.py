from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.messages import get_messages
from rest_framework_simplejwt.tokens import RefreshToken
from .forms import RegisterForm

def index(request):
    """
    Vista inicial - Redirige según el estado de autenticación
    """
    if request.user.is_authenticated:
        # Si es admin, va al dashboard de admin
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin_dashboard')
        # Si es usuario normal, va al dashboard de usuario
        return redirect('user_dashboard')
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
        return redirect('admin_dashboard')
    
    access_token = request.session.get('access_token', None)
    refresh_token = request.session.get('refresh_token', None)
    
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
        return redirect('user_dashboard')
    
    access_token = request.session.get('access_token', None)
    refresh_token = request.session.get('refresh_token', None)
    
    # Estadísticas para admin
    from django.contrib.auth.models import User
    from accounting.models import AsientoContable, CuentaContable
    
    total_usuarios = User.objects.count()
    total_asientos = AsientoContable.objects.count()
    total_cuentas = CuentaContable.objects.count()
    
    context = {
        'username': request.user.username,
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user_role': 'Administrador',
        'is_admin': True,
        'total_usuarios': total_usuarios,
        'total_asientos': total_asientos,
        'total_cuentas': total_cuentas,
    }
    return render(request, 'users/admin_dashboard.html', context)

# Vista de Registro (Se mantiene la lógica de formulario funcional)
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.')
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
                return render(request, 'registration/user_login.html')
            
            # Login y JWT
            auth_login(request, user)
            refresh = RefreshToken.for_user(user)
            request.session['access_token'] = str(refresh.access_token)
            request.session['refresh_token'] = str(refresh)
            request.session['user_role'] = 'user'
            
            messages.success(request, f'¡Bienvenido, {user.username}!')
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'registration/user_login.html')


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
            request.session['access_token'] = str(refresh.access_token)
            request.session['refresh_token'] = str(refresh)
            request.session['user_role'] = 'admin'
            
            messages.success(request, f'¡Bienvenido, Administrador {user.username}!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'registration/admin_login.html')


def custom_logout(request):
    """
    Vista de logout personalizada que limpia los tokens JWT.
    """
    # Limpiamos los tokens de la sesión
    if 'access_token' in request.session:
        del request.session['access_token']
    if 'refresh_token' in request.session:
        del request.session['refresh_token']
    if 'user_role' in request.session:
        del request.session['user_role']
    
    # Limpiar todos los mensajes anteriores
    storage = get_messages(request)
    for _ in storage:
        pass  # Esto consume/limpia todos los mensajes
    
    # Logout tradicional de Django
    auth_logout(request)
    
    # Agregar solo el mensaje de logout
    messages.success(request, '¡Has cerrado sesión exitosamente!')
    
    return redirect('user_login')
