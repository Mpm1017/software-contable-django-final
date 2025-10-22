from django.contrib.auth.forms import UserCreationForm

# Usamos UserCreationForm ya que estamos utilizando el modelo de usuario estándar de Django.
# Esto garantiza que el registro maneje las contraseñas de forma segura.
class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # No se añaden campos extra por ahora, solo usuario y doble contraseña.
        pass

