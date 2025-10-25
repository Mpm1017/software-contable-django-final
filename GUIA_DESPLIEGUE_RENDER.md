# 🚀 Guía Completa de Despliegue en Render

## ✅ Archivos Preparados

Todos los archivos necesarios ya están listos:

- ✅ `requirements.txt` - Dependencias del proyecto
- ✅ `runtime.txt` - Versión de Python
- ✅ `build.sh` - Script de construcción
- ✅ `settings.py` - Configurado para producción
- ✅ `.gitignore` - Archivos a ignorar

---

## 📋 PASO 1: Crear Cuenta en Render

1. Ve a: **https://render.com/**
2. Haz clic en **"Get Started"** o **"Sign Up"**
3. Regístrate con:
   - GitHub (Recomendado)
   - GitLab
   - Email

**Recomendación:** Usa GitHub para conectar fácilmente tu repositorio.

---

## 📋 PASO 2: Subir tu Proyecto a GitHub

### 2.1 Crear Repositorio en GitHub

1. Ve a: **https://github.com/new**
2. Nombre del repositorio: `software-contable-django`
3. Descripción: "Sistema de Software Contable con Django"
4. Selecciona: **Private** (para mantenerlo privado)
5. **NO** marques "Add a README file"
6. Haz clic en **"Create repository"**

### 2.2 Subir tu Código

Abre la terminal en tu proyecto y ejecuta:

```bash
# Inicializar git (si no está inicializado)
git init

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Preparado para despliegue en Render"

# Conectar con GitHub (reemplaza TU_USUARIO con tu usuario de GitHub)
git remote add origin https://github.com/TU_USUARIO/software-contable-django.git

# Subir el código
git branch -M main
git push -u origin main
```

**IMPORTANTE:** Reemplaza `TU_USUARIO` con tu nombre de usuario de GitHub.

---

## 📋 PASO 3: Crear Web Service en Render

1. Ve a tu dashboard de Render: **https://dashboard.render.com/**
2. Haz clic en **"New +"** (arriba a la derecha)
3. Selecciona **"Web Service"**

### 3.1 Conectar Repositorio

1. Si conectaste con GitHub, verás tus repositorios
2. Busca **"software-contable-django"**
3. Haz clic en **"Connect"**

### 3.2 Configurar el Servicio

Completa los siguientes campos:

**Name:**
```
software-contable
```

**Region:**
```
Oregon (US West) o el más cercano a ti
```

**Branch:**
```
main
```

**Root Directory:**
```
(déjalo vacío)
```

**Runtime:**
```
Python 3
```

**Build Command:**
```
./build.sh
```

**Start Command:**
```
gunicorn config.wsgi:application
```

**Instance Type:**
```
Free
```

---

## 📋 PASO 4: Configurar Variables de Entorno

En la misma página, baja hasta **"Environment Variables"** y agrega:

### Variables Requeridas:

| Key | Value |
|---|---|
| `SECRET_KEY` | (genera una nueva con el comando de abajo) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.onrender.com` |
| `DATABASE_URL` | (Render lo generará automáticamente) |
| `EMAIL_HOST_USER` | `tu_email@gmail.com` |
| `EMAIL_HOST_PASSWORD` | `tu_contraseña_de_aplicación` |
| `DEFAULT_FROM_EMAIL` | `Software Contable <noreply@softwarecontable.com>` |

### Generar SECRET_KEY:

Ejecuta en tu terminal local:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copia el resultado y úsalo como `SECRET_KEY`.

---

## 📋 PASO 5: Crear Base de Datos PostgreSQL

1. En el dashboard de Render, haz clic en **"New +"**
2. Selecciona **"PostgreSQL"**
3. Completa:

**Name:**
```
software-contable-db
```

**Database:**
```
software_contable
```

**User:**
```
software_contable_user
```

**Region:**
```
(El mismo que el Web Service)
```

**PostgreSQL Version:**
```
16
```

**Instance Type:**
```
Free
```

4. Haz clic en **"Create Database"**

### 5.1 Conectar la Base de Datos

1. Una vez creada, copia la **"Internal Database URL"**
2. Ve a tu Web Service
3. En **"Environment Variables"**, agrega:

| Key | Value |
|---|---|
| `DATABASE_URL` | (pega la Internal Database URL) |

---

## 📋 PASO 6: Desplegar

1. Haz clic en **"Create Web Service"** (al final de la página)
2. Render comenzará a construir y desplegar tu aplicación
3. **Espera 5-10 minutos** (la primera vez tarda más)

### Ver el Progreso:

En la pestaña **"Logs"** verás:
```
==> Building...
==> Installing dependencies...
==> Collecting static files...
==> Running migrations...
==> Deploy successful!
```

---

## 📋 PASO 7: Crear Superusuario

Una vez desplegado, necesitas crear un superusuario:

1. En tu Web Service, ve a la pestaña **"Shell"**
2. Haz clic en **"Launch Shell"**
3. Ejecuta:

```bash
python manage.py createsuperuser
```

4. Ingresa:
   - Username: `admin`
   - Email: `tu_email@gmail.com`
   - Password: (tu contraseña)

---

## 🎉 PASO 8: ¡Listo! Acceder a tu Aplicación

Tu aplicación estará disponible en:

```
https://software-contable.onrender.com
```

(Render te dará la URL exacta)

### URLs Importantes:

- **Página principal:** `https://tu-app.onrender.com/`
- **Admin:** `https://tu-app.onrender.com/admin/`
- **Recuperación:** `https://tu-app.onrender.com/accounts/password_reset/`

---

## 🔧 Mantenimiento y Actualizaciones

### Para Actualizar el Código:

```bash
# Hacer cambios en tu código local
git add .
git commit -m "Descripción de los cambios"
git push origin main
```

Render detectará los cambios y desplegará automáticamente.

### Ver Logs:

1. Ve a tu Web Service en Render
2. Pestaña **"Logs"**
3. Verás todos los logs en tiempo real

---

## ⚠️ Solución de Problemas

### Error: "Build failed"

**Causa:** Problema con dependencias

**Solución:**
1. Verifica que `requirements.txt` esté correcto
2. Verifica que `runtime.txt` tenga una versión válida de Python

### Error: "Application failed to start"

**Causa:** Problema con el comando de inicio

**Solución:**
1. Verifica que el Start Command sea: `gunicorn config.wsgi:application`
2. Verifica que `gunicorn` esté en `requirements.txt`

### Error: "DisallowedHost"

**Causa:** ALLOWED_HOSTS no configurado

**Solución:**
1. Ve a Environment Variables
2. Agrega/actualiza: `ALLOWED_HOSTS=.onrender.com`
3. Redeploy manual

### La aplicación se "duerme"

**Causa:** Plan gratuito de Render

**Solución:**
- Es normal en el plan gratuito
- La app se "despierta" cuando alguien la visita (tarda 30-60 segundos)
- Para evitarlo, actualiza a plan de pago ($7/mes)

---

## 💰 Costos

### Plan Gratuito:
- ✅ Web Service: Gratis
- ✅ PostgreSQL: Gratis (hasta 1GB)
- ⚠️ La app se duerme después de 15 minutos de inactividad
- ⚠️ 750 horas gratis al mes

### Plan de Pago:
- 💰 Web Service: $7/mes
- 💰 PostgreSQL: $7/mes
- ✅ Sin límite de horas
- ✅ No se duerme

---

## 📊 Checklist de Despliegue

- [ ] Cuenta en Render creada
- [ ] Repositorio en GitHub creado
- [ ] Código subido a GitHub
- [ ] Web Service creado en Render
- [ ] Variables de entorno configuradas
- [ ] Base de datos PostgreSQL creada
- [ ] DATABASE_URL configurada
- [ ] Despliegue exitoso
- [ ] Superusuario creado
- [ ] Aplicación accesible

---

## 🎯 Próximos Pasos

1. ✅ Prueba todas las funcionalidades
2. ✅ Configura un dominio personalizado (opcional)
3. ✅ Configura backups de la base de datos
4. ✅ Monitorea los logs regularmente

---

## 📞 Soporte

- **Documentación Render:** https://render.com/docs
- **Comunidad Render:** https://community.render.com/
- **Django Docs:** https://docs.djangoproject.com/

---

**¡Tu Software Contable está listo para el mundo!** 🚀

---

**Última actualización:** 25 de Octubre, 2025
