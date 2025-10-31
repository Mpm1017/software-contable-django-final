# 🔐 Documentación: JWT y Recuperación de Contraseña

## Implementación Completada

Este documento explica las nuevas funcionalidades implementadas en el Software Contable Django.

---

## 1. Autenticación con JWT (JSON Web Tokens)

### ¿Qué es JWT?

JWT es un estándar de autenticación que permite crear tokens seguros para identificar usuarios. Cada vez que un usuario inicia sesión, se generan dos tokens:

- **Access Token**: Token de corta duración (5 horas) para acceder a recursos protegidos
- **Refresh Token**: Token de larga duración (1 día) para renovar el access token

### ¿Cómo Funciona?

#### 1. **Al Iniciar Sesión:**

Cuando un usuario (administrador o normal) inicia sesión:

```python
# En users/views.py - función custom_login()
user = authenticate(request, username=username, password=password)

if user is not None:
    # Login tradicional de Django
    auth_login(request, user)
    
    # Generamos tokens JWT
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)
    
    # Guardamos en la sesión
    request.session['access_token'] = access_token
    request.session['refresh_token'] = refresh_token
```

#### 2. **Diferenciación de Roles:**

El sistema detecta automáticamente si el usuario es administrador o usuario normal:

```python
user_role = 'Administrador' if user.is_staff or user.is_superuser else 'Usuario'
messages.success(request, f'¡Bienvenido, {user.username}! ({user_role})')
```

#### 3. **Tokens en la Sesión:**

Los tokens se almacenan en la sesión del usuario y están disponibles para:
- Autenticación en APIs REST
- Verificación de permisos
- Renovación automática de sesión

### Configuración JWT

En `config/settings.py`:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

### Ventajas de JWT

✅ **Seguridad**: Los tokens están firmados criptográficamente
✅ **Escalabilidad**: No requiere almacenamiento en servidor
✅ **Stateless**: Cada token contiene toda la información necesaria
✅ **Expiración**: Los tokens expiran automáticamente
✅ **Roles**: Diferencia entre administradores y usuarios normales

---

## 2. Sistema de Recuperación de Contraseña

### Flujo Completo

#### **Paso 1: Solicitar Recuperación**

1. El usuario hace clic en "¿Olvidaste tu contraseña?" en el login
2. Ingresa su correo electrónico
3. El sistema envía un email con un enlace único

**URL**: `/accounts/password_reset/`
**Template**: `password_reset_form.html`

#### **Paso 2: Email Enviado**

- Se muestra confirmación de que el email fue enviado
- En desarrollo, el enlace aparece en la consola del servidor

**URL**: `/accounts/password_reset/done/`
**Template**: `password_reset_done.html`

#### **Paso 3: Establecer Nueva Contraseña**

1. El usuario hace clic en el enlace del email
2. Ingresa su nueva contraseña dos veces
3. El sistema valida y guarda la nueva contraseña

**URL**: `/accounts/reset/<uidb64>/<token>/`
**Template**: `password_reset_confirm.html`

#### **Paso 4: Confirmación**

- Se muestra mensaje de éxito
- El usuario puede iniciar sesión con la nueva contraseña

**URL**: `/accounts/reset/done/`
**Template**: `password_reset_complete.html`

### Configuración de Email

#### **Desarrollo (Actual):**

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Los emails se muestran en la consola del servidor (terminal donde corre `python manage.py runserver`).

#### **Producción (Configurar después):**

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu_email@gmail.com'
EMAIL_HOST_PASSWORD = 'tu_contraseña_de_aplicación'
DEFAULT_FROM_EMAIL = 'noreply@softwarecontable.com'
```

### Seguridad del Sistema

✅ **Tokens únicos**: Cada enlace es único y de un solo uso
✅ **Expiración**: Los enlaces expiran en 24 horas
✅ **Validación**: Se valida que el usuario exista
✅ **Encriptación**: Las contraseñas se hashean con algoritmos seguros
✅ **CSRF Protection**: Todos los formularios están protegidos

---

## 3. Cambios en el Registro

### Campo de Email Obligatorio

Ahora el registro requiere un email válido:

```python
class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Requerido. Ingresa un correo electrónico válido.'
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
```

### Validación

- Email único por usuario
- Formato de email válido
- Contraseña segura (mínimo 8 caracteres, no solo números)

---

## 4. Pruebas del Sistema

### Probar JWT

1. **Crear un usuario nuevo:**
   - Ve a `/register/`
   - Completa el formulario con username, email y contraseña
   - Haz clic en "Crear Cuenta"

2. **Iniciar sesión:**
   - Ve a `/login/`
   - Ingresa tus credenciales
   - Observa el mensaje: "¡Bienvenido, [usuario]! (Usuario/Administrador)"

3. **Verificar token en dashboard:**
   - Verás un mensaje azul: "🔐 Sesión segura con JWT activa"
   - Esto confirma que el token JWT fue generado

4. **Verificar en consola del navegador (opcional):**
   ```javascript
   // Abre la consola del navegador (F12)
   // Los tokens están en la sesión del servidor, no en cookies del cliente
   ```

### Probar Recuperación de Contraseña

1. **Solicitar recuperación:**
   - Ve a `/login/`
   - Haz clic en "¿Olvidaste tu contraseña?"
   - Ingresa el email del usuario
   - Haz clic en "Enviar Enlace de Recuperación"

2. **Verificar email en consola:**
   - Ve a la terminal donde corre el servidor
   - Busca el email con el enlace de recuperación
   - Copia la URL que aparece

3. **Restablecer contraseña:**
   - Pega la URL en el navegador
   - Ingresa la nueva contraseña dos veces
   - Haz clic en "Cambiar Contraseña"

4. **Iniciar sesión con nueva contraseña:**
   - Ve a `/login/`
   - Usa la nueva contraseña
   - Deberías poder acceder sin problemas

### Probar Roles (Admin vs Usuario)

1. **Crear superusuario:**
   ```bash
   python manage.py createsuperuser
   ```

2. **Iniciar sesión como admin:**
   - Usa las credenciales del superusuario
   - Verás: "¡Bienvenido, [usuario]! (Administrador)"

3. **Iniciar sesión como usuario normal:**
   - Usa un usuario creado con el registro
   - Verás: "¡Bienvenido, [usuario]! (Usuario)"

---

## 5. Archivos Modificados/Creados

### Archivos de Configuración:
- ✅ `requirements.txt` - Agregadas dependencias JWT
- ✅ `config/settings.py` - Configuración JWT y email

### Vistas y Formularios:
- ✅ `users/views.py` - Vista `custom_login()` con JWT
- ✅ `users/forms.py` - Campo email en registro
- ✅ `users/urls.py` - Ruta de login personalizada

### Templates:
- ✅ `templates/registration/login.html` - Actualizado para mensajes
- ✅ `templates/registration/register.html` - Campo email agregado
- ✅ `templates/registration/password_reset_form.html` - Nuevo
- ✅ `templates/registration/password_reset_done.html` - Nuevo
- ✅ `templates/registration/password_reset_confirm.html` - Nuevo
- ✅ `templates/registration/password_reset_complete.html` - Nuevo
- ✅ `templates/registration/password_reset_email.html` - Nuevo
- ✅ `templates/registration/password_reset_subject.txt` - Nuevo
- ✅ `templates/users/dashboard.html` - Indicador JWT

---

## 6. URLs del Sistema

### Autenticación:
- `/login/` - Login con JWT
- `/logout/` - Cerrar sesión
- `/register/` - Registro con email

### Recuperación de Contraseña:
- `/accounts/password_reset/` - Solicitar recuperación
- `/accounts/password_reset/done/` - Confirmación de envío
- `/accounts/reset/<uidb64>/<token>/` - Establecer nueva contraseña
- `/accounts/reset/done/` - Confirmación de cambio

### Dashboard y Módulos:
- `/dashboard/` - Panel principal
- `/accounting/transactions/` - Transacciones
- `/accounting/accounts/` - Cuentas
- `/accounting/categories/` - Categorías

---

## 7. Próximos Pasos (Opcional)

### Para Producción:

1. **Configurar Email Real:**
   - Crear cuenta de Gmail para la aplicación
   - Generar contraseña de aplicación
   - Actualizar settings.py con credenciales

2. **Blacklist de Tokens:**
   ```bash
   pip install djangorestframework-simplejwt[blacklist]
   python manage.py migrate
   ```

3. **API REST con JWT:**
   - Crear endpoints API
   - Usar JWT para autenticación de API
   - Documentar con Swagger/OpenAPI

4. **Renovación Automática de Tokens:**
   - Implementar refresh token endpoint
   - Renovar access token antes de expirar

---

## 8. Solución de Problemas

### El email no se envía:
- **Desarrollo**: Verifica la consola del servidor
- **Producción**: Verifica credenciales de email en settings.py

### Token JWT no aparece:
- Verifica que iniciaste sesión después de la implementación
- Cierra sesión y vuelve a iniciar sesión

### Enlace de recuperación inválido:
- Los enlaces expiran en 24 horas
- Solo se pueden usar una vez
- Solicita un nuevo enlace

### Error al cambiar contraseña:
- Verifica que las contraseñas coincidan
- Cumple los requisitos de seguridad (mínimo 8 caracteres)

---

## 9. Seguridad y Buenas Prácticas

✅ **Contraseñas hasheadas** con algoritmos seguros (PBKDF2)
✅ **Tokens firmados** criptográficamente
✅ **CSRF Protection** en todos los formularios
✅ **Validación de email** en registro
✅ **Expiración de tokens** automática
✅ **Enlaces de un solo uso** para recuperación
✅ **Mensajes de error genéricos** (no revelan si el usuario existe)

---

## 10. Resumen

### ✅ Implementado:

1. **JWT en Login**
   - Tokens generados al iniciar sesión
   - Diferenciación Admin/Usuario
   - Tokens almacenados en sesión

2. **Recuperación de Contraseña**
   - Flujo completo de 4 pasos
   - Templates profesionales
   - Email en consola (desarrollo)
   - Seguridad robusta

3. **Mejoras en Registro**
   - Campo email obligatorio
   - Validación mejorada
   - Mensajes de confirmación

### 🎯 Resultado:

Un sistema de autenticación profesional, seguro y completo que:
- Protege las sesiones con JWT
- Permite recuperar contraseñas fácilmente
- Diferencia entre administradores y usuarios
- Sigue las mejores prácticas de seguridad

---

**¡Sistema listo para usar!** 🚀
