# ⚡ Configuración Rápida de Email (5 minutos)

## 🎯 Objetivo
Configurar el envío de emails reales para recuperación de contraseña.

---

## ✅ Paso 1: Gmail - Contraseña de Aplicación (2 min)

1. Ve a: https://myaccount.google.com/security
2. Activa **"Verificación en 2 pasos"** (si no está activa)
3. Busca **"Contraseñas de aplicaciones"**
4. Selecciona: **Correo** > **Otro** > Escribe: "Django"
5. Haz clic en **"Generar"**
6. **COPIA** la contraseña de 16 caracteres (ejemplo: `abcd efgh ijkl mnop`)

---

## ✅ Paso 2: Configurar .env (1 min)

Abre o crea el archivo `.env` en la raíz del proyecto y agrega:

```env
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
DEFAULT_FROM_EMAIL=Software Contable <noreply@softwarecontable.com>
```

**Reemplaza:**
- `tu_email@gmail.com` → Tu email de Gmail
- `abcd efgh ijkl mnop` → La contraseña de aplicación que copiaste

---

## ✅ Paso 3: Probar (2 min)

### Opción A: Script de Prueba

```bash
python test_email.py
```

Ingresa tu email y verifica que llegue el correo.

### Opción B: Flujo Completo

1. Reinicia el servidor:
   ```bash
   python manage.py runserver
   ```

2. Ve a: http://127.0.0.1:8000/accounts/password_reset/

3. Ingresa tu email y haz clic en "Enviar"

4. **Revisa tu bandeja de entrada** (debería llegar en menos de 1 minuto)

---

## ✅ ¡Listo!

Si el email llegó, **la configuración está completa** ✅

---

## ❌ ¿No funciona?

### Error común: "SMTPAuthenticationError"

**Causa:** Contraseña incorrecta

**Solución:**
1. Verifica que usaste la **contraseña de aplicación** (no tu contraseña normal)
2. Verifica que no haya espacios extra en el .env
3. Regenera una nueva contraseña de aplicación

### El email no llega

**Soluciones:**
1. Revisa la carpeta de **Spam**
2. Verifica que el email en .env sea correcto
3. Verifica tu conexión a internet
4. Espera 2-3 minutos (a veces Gmail tarda)

---

## 📖 Documentación Completa

Para más detalles, consulta: `GUIA_CONFIGURACION_EMAIL.md`

---

**Tiempo total:** ⏱️ 5 minutos
**Dificultad:** 🟢 Fácil
