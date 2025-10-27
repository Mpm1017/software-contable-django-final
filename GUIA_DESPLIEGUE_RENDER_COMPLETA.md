# 🚀 Guía Completa de Despliegue en Render

## ✅ Pre-requisitos Completados

Tu proyecto ya está **100% listo** para desplegar en Render. Todos los archivos necesarios están configurados:

- ✅ `requirements.txt` - Dependencias actualizadas con Brotli
- ✅ `build.sh` - Script de construcción mejorado
- ✅ `runtime.txt` - Python 3.11.9
- ✅ `render.yaml` - Configuración automática (opcional)
- ✅ `config/settings.py` - Seguridad para producción configurada
- ✅ Repositorio Git en GitHub

---

## 📋 Pasos para Desplegar

### **Paso 1: Crear Cuenta en Render**

1. Ve a [https://render.com](https://render.com)
2. Regístrate con tu cuenta de GitHub
3. Autoriza a Render para acceder a tus repositorios

---

### **Paso 2: Crear Base de Datos PostgreSQL**

1. En el dashboard de Render, haz clic en **"New +"**
2. Selecciona **"PostgreSQL"**
3. Configura:
   - **Name:** `software-contable-db`
   - **Database:** `software_contable`
   - **User:** `software_contable_user` (se genera automáticamente)
   - **Region:** Selecciona la más cercana (ej: Oregon, USA)
   - **Plan:** **Free** (para empezar)
4. Haz clic en **"Create Database"**
5. **IMPORTANTE:** Copia la **Internal Database URL** (la necesitarás en el siguiente paso)
   - Se ve así: `postgresql://user:password@host/database`

---

### **Paso 3: Crear Web Service**

1. En el dashboard, haz clic en **"New +"**
2. Selecciona **"Web Service"**
3. Conecta tu repositorio:
   - Busca: `Mpm1017/software-contable-django-final`
   - Haz clic en **"Connect"**

4. Configura el servicio:
   - **Name:** `software-contable-django` (o el nombre que prefieras)
   - **Region:** La misma que la base de datos
   - **Branch:** `master`
   - **Root Directory:** (dejar vacío)
   - **Runtime:** `Python 3`
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn config.wsgi:application`
   - **Plan:** **Free** (para empezar)

---

### **Paso 4: Configurar Variables de Entorno**

En la sección **"Environment Variables"**, agrega las siguientes variables:

#### **Variables Obligatorias:**

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `SECRET_KEY` | (generar nueva) | Clave secreta de Django |
| `DEBUG` | `False` | Modo producción |
| `DATABASE_URL` | (copiar de PostgreSQL) | URL de la base de datos |
| `ALLOWED_HOSTS` | `tu-app.onrender.com` | Dominio de tu app |
| `PYTHON_VERSION` | `3.11.9` | Versión de Python |

#### **Cómo generar SECRET_KEY:**
```python
# Ejecuta esto en tu terminal local:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### **Variables Opcionales (para email):**

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `EMAIL_HOST_USER` | `tu_email@gmail.com` | Tu email de Gmail |
| `EMAIL_HOST_PASSWORD` | `xxxx xxxx xxxx xxxx` | Contraseña de aplicación |
| `DEFAULT_FROM_EMAIL` | `Software Contable <noreply@tuapp.com>` | Email remitente |

**Nota:** Para configurar email, sigue la guía en `CONFIGURAR_EMAIL_REAL.md`

---

### **Paso 5: Desplegar**

1. Haz clic en **"Create Web Service"**
2. Render automáticamente:
   - Clonará tu repositorio
   - Ejecutará `build.sh`
   - Instalará dependencias
   - Ejecutará migraciones
   - Recolectará archivos estáticos
   - Iniciará el servidor con Gunicorn

3. **Espera 5-10 minutos** para el primer despliegue

---

### **Paso 6: Verificar el Despliegue**

1. Una vez completado, verás el estado **"Live"** en verde
2. Haz clic en la URL generada (ej: `https://software-contable-django.onrender.com`)
3. Deberías ver tu aplicación funcionando

---

### **Paso 7: Crear Superusuario**

Para acceder al admin de Django, necesitas crear un superusuario:

1. En el dashboard de Render, ve a tu Web Service
2. Haz clic en la pestaña **"Shell"**
3. Ejecuta:
   ```bash
   python manage.py createsuperuser
   ```
4. Sigue las instrucciones para crear el usuario admin

---

## 🔧 Configuración Adicional

### **Actualizar ALLOWED_HOSTS**

Después del primer despliegue, actualiza la variable de entorno:

```
ALLOWED_HOSTS=tu-app.onrender.com,www.tu-app.onrender.com
```

Si tienes un dominio personalizado:
```
ALLOWED_HOSTS=tu-app.onrender.com,tudominio.com,www.tudominio.com
```

---

## 🔄 Redespliegues Automáticos

Render se redesplegará automáticamente cuando:
- Hagas `git push` a la rama `master`
- Cambies variables de entorno
- Actualices la configuración del servicio

---

## 📊 Monitoreo

En el dashboard de Render puedes ver:
- **Logs:** Logs en tiempo real de tu aplicación
- **Metrics:** CPU, memoria, ancho de banda
- **Events:** Historial de despliegues
- **Shell:** Terminal para ejecutar comandos

---

## ⚠️ Limitaciones del Plan Free

- **Inactividad:** El servicio se duerme después de 15 minutos sin tráfico
- **Primer request:** Puede tardar 30-60 segundos en despertar
- **Horas mensuales:** 750 horas/mes (suficiente para un proyecto)
- **Base de datos:** 90 días de retención, luego se elimina

---

## 🆙 Actualizar a Plan Paid (Opcional)

Para eliminar las limitaciones:
1. Ve a tu Web Service
2. Haz clic en **"Upgrade"**
3. Selecciona el plan **Starter** ($7/mes)

Beneficios:
- Sin tiempo de inactividad
- Sin límite de horas
- Base de datos permanente
- Mejor rendimiento

---

## 🐛 Solución de Problemas

### **Error: "Application failed to respond"**
- Verifica que `gunicorn` esté en `requirements.txt`
- Revisa los logs en el dashboard
- Verifica que `ALLOWED_HOSTS` incluya tu dominio

### **Error: "Database connection failed"**
- Verifica que `DATABASE_URL` esté correctamente configurada
- Asegúrate de que la base de datos esté en la misma región

### **Error: "Static files not loading"**
- Ejecuta `python manage.py collectstatic` manualmente desde Shell
- Verifica que `STATIC_ROOT` esté configurado en `settings.py`

### **Error: "Bad Request (400)"**
- Agrega tu dominio a `ALLOWED_HOSTS`
- Reinicia el servicio

---

## 📝 Comandos Útiles

### **Ver logs en tiempo real:**
```bash
# En el dashboard > Shell
tail -f /var/log/render.log
```

### **Ejecutar migraciones manualmente:**
```bash
python manage.py migrate
```

### **Recolectar archivos estáticos:**
```bash
python manage.py collectstatic --no-input
```

### **Crear superusuario:**
```bash
python manage.py createsuperuser
```

### **Abrir shell de Django:**
```bash
python manage.py shell
```

---

## 🎉 ¡Listo!

Tu aplicación Django está desplegada en producción con:
- ✅ HTTPS automático
- ✅ Base de datos PostgreSQL
- ✅ Archivos estáticos optimizados con Whitenoise + Brotli
- ✅ Configuración de seguridad activada
- ✅ Redespliegues automáticos desde Git

---

## 📚 Recursos Adicionales

- [Documentación oficial de Render](https://render.com/docs)
- [Guía de Django en Render](https://render.com/docs/deploy-django)
- [Configuración de dominios personalizados](https://render.com/docs/custom-domains)

---

## 🆘 Soporte

Si encuentras problemas:
1. Revisa los logs en el dashboard de Render
2. Consulta la documentación oficial
3. Revisa los archivos de configuración en este repositorio

**¡Tu aplicación está lista para producción!** 🚀
