from django.shortcuts import render, redirect
from django.http import HttpResponse 
from .forms import RegisterForm # Importamos el nuevo formulario

def index(request):
    # Redirigimos al login como punto de entrada principal
    return redirect('login') 

# FUNCIÓN ACTUALIZADA: Vista de Registro con lógica de formulario
def register(request):
    if request.method == 'POST':
        # 1. Crear formulario con los datos POST
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 2. Si es válido, guardar el usuario y hashear la contraseña
            form.save()
            # 3. Redirigir al login para que el nuevo usuario inicie sesión
            return redirect('login') 
    else:
        # Si es GET, creamos un formulario vacío para mostrarlo
        form = RegisterForm()
    
    # Renderiza la plantilla 'registration/register.html' y pasa el formulario
    return render(request, 'registration/register.html', {'form': form})

