# ⚡ Despliegue Rápido en Render (15 minutos)

## ✅ Archivos Ya Preparados

Todos los archivos necesarios están listos. Solo sigue estos pasos:

---

## 🚀 PASO 1: Subir a GitHub (5 min)

```bash
# En la terminal de tu proyecto:
git init
git add .
git commit -m "Preparado para despliegue"
git remote add origin https://github.com/TU_USUARIO/software-contable.git
git push -u origin main
```

**Reemplaza `TU_USUARIO`** con tu usuario de GitHub.

---

## 🚀 PASO 2: Crear Cuenta en Render (2 min)

1. Ve a: **https://render.com/**
2. Regístrate con GitHub
3. Autoriza el acceso

---

## 🚀 PASO 3: Crear Web Service (3 min)

1. Dashboard > **New +** > **Web Service**
2. Conecta tu repositorio `software-contable`
3. Configuración:
   - **Name:** `software-contable`
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn config.wsgi:application`
   - **Instance Type:** Free

---

## 🚀 PASO 4: Variables de Entorno (3 min)

Agrega estas variables:

```
SECRET_KEY=genera_una_nueva_con_el_comando_de_abajo
DEBUG=False
ALLOWED_HOSTS=.onrender.com
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_contraseña_de_aplicación
DEFAULT_FROM_EMAIL=Software Contable <noreply@softwarecontable.com>
```

**Generar SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 🚀 PASO 5: Crear Base de Datos (2 min)

1. Dashboard > **New +** > **PostgreSQL**
2. **Name:** `software-contable-db`
3. **Instance Type:** Free
4. Copia la **Internal Database URL**
5. Agrégala como variable: `DATABASE_URL=...`

---

## 🚀 PASO 6: Desplegar

1. Haz clic en **"Create Web Service"**
2. Espera 5-10 minutos
3. ✅ ¡Listo!

---

## 🚀 PASO 7: Crear Superusuario

1. En Render > Shell
2. Ejecuta:
```bash
python manage.py createsuperuser
```

---

## ✅ Tu App Está en:

```
https://software-contable.onrender.com
```

---

## 📖 Guía Completa:

Para más detalles, consulta: `GUIA_DESPLIEGUE_RENDER.md`

---

**Tiempo total:** ⏱️ 15 minutos
**Costo:** 💰 Gratis
