from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Usamos UserCreationForm ya que estamos utilizando el modelo de usuario estándar de Django.
# Esto garantiza que el registro maneje las contraseñas de forma segura.
class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com'
        }),
        help_text='Requerido. Ingresa un correo electrónico válido.'
    )
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

