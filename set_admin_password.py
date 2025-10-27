import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

try:
    user = User.objects.get(username='admin')
    user.set_password('admin123')
    user.save()
    print('✅ Contraseña establecida para el usuario: admin')
    print('📝 Usuario: admin')
    print('🔑 Contraseña: admin123')
except User.DoesNotExist:
    print('❌ Usuario admin no existe')
