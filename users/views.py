from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required # Importación requerida para proteger la vista
from .forms import RegisterForm

def index(request):
    # Si el usuario está autenticado (logueado), lo enviamos al dashboard.
    # Esto evita el loop de redirección y es la lógica correcta.
    if request.user.is_authenticated:
        return redirect('dashboard') 
    # Si NO está autenticado, lo enviamos al login.
    return redirect('login') 

# FUNCIÓN NUEVA: El Dashboard (Página principal para usuarios logueados)
# Solo permite el acceso si el usuario está logueado.
@login_required
def dashboard(request):
    context = {
        'username': request.user.username,
    }
    # Renderiza la plantilla dashboard.html
    return render(request, 'users/dashboard.html', context)

# Vista de Registro (Se mantiene la lógica de formulario funcional)
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = RegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})
