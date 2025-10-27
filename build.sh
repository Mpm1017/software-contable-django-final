#!/usr/bin/env bash
# Exit on error
set -o errexit

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

# Recolectar archivos estáticos
python manage.py collectstatic --no-input

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario si no existe (opcional)
# python manage.py createsuperuser --no-input --username admin --email admin@example.com || true
