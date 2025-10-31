# 📧 Guía de Configuración de Email Real

## ✅ Paso 1: Crear Contraseña de Aplicación en Gmail

### 1.1 Activar Verificación en 2 Pasos

1. Ve a tu cuenta de Gmail: https://myaccount.google.com/
2. En el menú lateral, selecciona **"Seguridad"**
3. Busca la sección **"Cómo inicias sesión en Google"**
4. Haz clic en **"Verificación en 2 pasos"**
5. Sigue los pasos para activarla (necesitarás tu teléfono)

### 1.2 Generar Contraseña de Aplicación

1. Una vez activada la verificación en 2 pasos, regresa a **"Seguridad"**
2. Busca **"Contraseñas de aplicaciones"** (aparece después de activar 2FA)
3. Haz clic en **"Contraseñas de aplicaciones"**
4. En "Selecciona la app", elige **"Correo"**
5. En "Selecciona el dispositivo", elige **"Otro (nombre personalizado)"**
6. Escribe: **"Software Contable Django"**
7. Haz clic en **"Generar"**
8. **COPIA LA CONTRASEÑA DE 16 CARACTERES** (aparece como: `xxxx xxxx xxxx xxxx`)

---

## ✅ Paso 2: Configurar Variables de Entorno

### 2.1 Crear archivo .env

Si no existe, crea un archivo llamado `.env` en la raíz del proyecto:

```
c:\Users\Maribel Posada Mira\Desktop\software contable django final\.env
```

### 2.2 Agregar Configuración de Email

Abre el archivo `.env` y agrega estas líneas (reemplaza con tus datos):

```env
# Django
SECRET_KEY=tu-secret-key-actual
DEBUG=True

# Base de Datos
DATABASE_URL=sqlite:///db.sqlite3

# ================================================
# CONFIGURACIÓN DE EMAIL
# ================================================
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx
DEFAULT_FROM_EMAIL=Software Contable <noreply@softwarecontable.com>
```

**IMPORTANTE:** 
- Reemplaza `tu_email@gmail.com` con tu email de Gmail
- Reemplaza `xxxx xxxx xxxx xxxx` con la contraseña de aplicación que copiaste

### Ejemplo Real:

```env
EMAIL_HOST_USER=miempresa@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
DEFAULT_FROM_EMAIL=Software Contable <noreply@miempresa.com>
```

---

## ✅ Paso 3: Verificar Configuración en settings.py

El archivo `config/settings.py` ya está configurado correctamente con:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='Software Contable <noreply@softwarecontable.com>')
```

✅ **No necesitas modificar nada aquí**, ya está listo.

---

## ✅ Paso 4: Reiniciar el Servidor

1. Detén el servidor Django (Ctrl + C en la terminal)
2. Reinicia el servidor:

```bash
python manage.py runserver
```

---

## ✅ Paso 5: Probar el Sistema

### 5.1 Ir a Recuperación de Contraseña

1. Abre tu navegador
2. Ve a: http://127.0.0.1:8000/accounts/password_reset/
3. Ingresa tu email (debe ser un email real que puedas revisar)
4. Haz clic en "Enviar"

### 5.2 Revisar tu Email

1. Ve a tu bandeja de entrada de Gmail
2. Busca el email de "Software Contable"
3. **El email debería llegar en menos de 1 minuto**
4. Abre el email
5. Haz clic en el botón "Restablecer Contraseña"
6. Establece tu nueva contraseña

---

## 🔍 Solución de Problemas

### Problema 1: No llega el email

**Posibles causas:**

1. **Email incorrecto en .env**
   - Verifica que `EMAIL_HOST_USER` sea tu email de Gmail correcto

2. **Contraseña incorrecta**
   - Verifica que `EMAIL_HOST_PASSWORD` sea la contraseña de aplicación (16 caracteres)
   - NO uses tu contraseña normal de Gmail

3. **Verificación en 2 pasos no activada**
   - Debes tener activada la verificación en 2 pasos en Gmail

4. **Revisa la carpeta de Spam**
   - A veces Gmail envía el email a Spam la primera vez

### Problema 2: Error "SMTPAuthenticationError"

**Solución:**
- Verifica que la contraseña de aplicación esté correcta
- Asegúrate de NO tener espacios extra en el .env
- Regenera una nueva contraseña de aplicación

### Problema 3: Error "SMTPServerDisconnected"

**Solución:**
- Verifica tu conexión a internet
- Intenta reiniciar el servidor Django

### Problema 4: El email llega pero sin formato

**Solución:**
- Algunos clientes de email no soportan HTML
- El email también incluye una versión de texto plano

---

## 📊 Verificar que Funciona

### En la Terminal del Servidor

Cuando envíes un email, deberías ver algo como:

```
[25/Oct/2025 10:30:15] "POST /accounts/password_reset/ HTTP/1.1" 302 0
Email enviado a: usuario@example.com
```

### En tu Email

Deberías recibir un email con:
- ✅ Diseño profesional con colores del sistema
- ✅ Botón "Restablecer Contraseña"
- ✅ Enlace alternativo por si el botón no funciona
- ✅ Advertencias de seguridad

---

## 🎯 Checklist de Verificación

Antes de probar, asegúrate de:

- [ ] Verificación en 2 pasos activada en Gmail
- [ ] Contraseña de aplicación generada
- [ ] Archivo .env creado con las credenciales
- [ ] EMAIL_HOST_USER configurado
- [ ] EMAIL_HOST_PASSWORD configurado
- [ ] Servidor Django reiniciado
- [ ] Email de prueba es un email real que puedes revisar

---

## 🔐 Seguridad

### ⚠️ IMPORTANTE:

1. **NUNCA** compartas tu contraseña de aplicación
2. **NUNCA** subas el archivo .env a GitHub
3. El archivo .env ya está en .gitignore (protegido)
4. Si crees que tu contraseña fue comprometida:
   - Ve a Google > Seguridad > Contraseñas de aplicaciones
   - Revoca la contraseña comprometida
   - Genera una nueva

---

## 📝 Notas Adicionales

### Límites de Gmail

Gmail tiene límites de envío:
- **500 emails por día** para cuentas gratuitas
- **2000 emails por día** para Google Workspace

Para este proyecto, es más que suficiente.

### Para Producción

Si vas a producción, considera:
- **SendGrid** (100 emails gratis/día, más profesional)
- **Mailgun** (5000 emails gratis/mes)
- **Amazon SES** (62,000 emails gratis/mes)

---

## ✅ Resumen

1. ✅ Activa verificación en 2 pasos en Gmail
2. ✅ Genera contraseña de aplicación
3. ✅ Configura .env con tus credenciales
4. ✅ Reinicia el servidor
5. ✅ Prueba enviando un email de recuperación
6. ✅ Revisa tu bandeja de entrada

**¡Listo!** Ahora los usuarios recibirán emails reales para recuperar su contraseña.

---

## 🆘 ¿Necesitas Ayuda?

Si tienes problemas:
1. Revisa la sección "Solución de Problemas"
2. Verifica el checklist de verificación
3. Revisa los logs del servidor Django
4. Asegúrate de que tu conexión a internet funcione

---

**Última actualización:** 25 de Octubre, 2025
