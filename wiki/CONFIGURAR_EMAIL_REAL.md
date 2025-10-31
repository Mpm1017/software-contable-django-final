# 📧 Configurar Email Real para Recuperación de Contraseña

## Estado Actual: Modo Desarrollo ✅

Actualmente los emails se muestran en la **consola del servidor** (terminal).
Esto es perfecto para desarrollo y pruebas.

---

## 🚀 Para Enviar Emails Reales (Producción)

### Opción 1: Gmail (Recomendado para pruebas)

#### Paso 1: Crear Contraseña de Aplicación en Gmail

1. Ve a tu cuenta de Gmail
2. Configuración > Seguridad
3. Activa "Verificación en 2 pasos" (si no está activa)
4. Ve a "Contraseñas de aplicaciones"
5. Genera una nueva contraseña para "Correo"
6. Copia la contraseña generada (16 caracteres)

#### Paso 2: Actualizar .env

Agrega estas líneas a tu archivo `.env`:

```env
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx  # Contraseña de aplicación
DEFAULT_FROM_EMAIL=noreply@softwarecontable.com
```

#### Paso 3: Actualizar settings.py

En `config/settings.py`, reemplaza:

```python
# Para desarrollo
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Por:

```python
# Para producción con Gmail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@softwarecontable.com')
```

---

### Opción 2: SendGrid (Recomendado para producción)

SendGrid ofrece 100 emails gratis al día.

#### Paso 1: Crear Cuenta en SendGrid

1. Ve a https://sendgrid.com/
2. Crea una cuenta gratuita
3. Verifica tu email
4. Crea una API Key

#### Paso 2: Instalar Dependencia

```bash
pip install sendgrid
```

#### Paso 3: Actualizar .env

```env
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxxxxx
DEFAULT_FROM_EMAIL=noreply@softwarecontable.com
```

#### Paso 4: Actualizar settings.py

```python
EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
SENDGRID_API_KEY = config('SENDGRID_API_KEY', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@softwarecontable.com')
```

---

### Opción 3: Mailgun

Mailgun ofrece 5,000 emails gratis al mes.

#### Configuración:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('MAILGUN_SMTP_LOGIN', default='')
EMAIL_HOST_PASSWORD = config('MAILGUN_SMTP_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@softwarecontable.com')
```

---

## 🧪 Probar el Email Real

Una vez configurado:

1. Reinicia el servidor Django
2. Ve a la página de recuperación de contraseña
3. Ingresa tu email
4. **El email llegará a tu bandeja de entrada real**
5. Haz clic en el enlace del email
6. Establece tu nueva contraseña

---

## ⚠️ Importante para Desarrollo

**Recomendación:** Mantén el modo consola durante el desarrollo:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

**Ventajas:**
- ✅ No necesitas configurar nada
- ✅ Ves los emails inmediatamente en la terminal
- ✅ No gastas cuota de envío
- ✅ Más rápido para pruebas

**Solo cambia a email real cuando:**
- Estés en producción
- Necesites probar el flujo completo con usuarios reales
- Vayas a desplegar la aplicación

---

## 📋 Resumen

| Modo | Dónde aparece el email | Cuándo usar |
|---|---|---|
| **Console** (Actual) | Terminal del servidor | Desarrollo ✅ |
| **SMTP (Gmail)** | Bandeja de entrada real | Producción |
| **SendGrid** | Bandeja de entrada real | Producción profesional |
| **Mailgun** | Bandeja de entrada real | Producción profesional |

---

## 🎯 Para Ahora (Desarrollo)

1. Ve a la terminal donde corre el servidor
2. Busca el email con el enlace
3. Copia la URL completa
4. Pégala en el navegador
5. Establece tu nueva contraseña

¡Así de simple! No necesitas configurar email real para desarrollo.
