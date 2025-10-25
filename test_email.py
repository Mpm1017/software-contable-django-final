"""
Script de Prueba para Verificar Configuración de Email

Ejecutar con: python test_email.py
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings


def test_email_configuration():
    """
    Prueba la configuración de email enviando un correo de prueba
    """
    print("=" * 60)
    print("🧪 PRUEBA DE CONFIGURACIÓN DE EMAIL")
    print("=" * 60)
    
    # Verificar configuración
    print("\n📋 Verificando configuración...")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'NO CONFIGURADO'}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
    # Validar que las credenciales estén configuradas
    if not settings.EMAIL_HOST_USER:
        print("\n❌ ERROR: EMAIL_HOST_USER no está configurado en .env")
        return False
    
    if not settings.EMAIL_HOST_PASSWORD:
        print("\n❌ ERROR: EMAIL_HOST_PASSWORD no está configurado en .env")
        return False
    
    print("\n✅ Configuración básica correcta")
    
    # Solicitar email de destino
    print("\n" + "=" * 60)
    email_destino = input("📧 Ingresa tu email para recibir el email de prueba: ").strip()
    
    if not email_destino:
        print("❌ Email no válido")
        return False
    
    # Enviar email de prueba
    print(f"\n📤 Enviando email de prueba a: {email_destino}")
    print("⏳ Espera un momento...")
    
    try:
        send_mail(
            subject='🧪 Prueba de Email - Software Contable',
            message='Este es un email de prueba del Software Contable.\n\nSi recibes este mensaje, la configuración de email está funcionando correctamente! ✅',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email_destino],
            fail_silently=False,
        )
        
        print("\n" + "=" * 60)
        print("✅ ¡EMAIL ENVIADO EXITOSAMENTE!")
        print("=" * 60)
        print(f"\n📬 Revisa tu bandeja de entrada: {email_destino}")
        print("💡 Si no lo ves, revisa la carpeta de Spam")
        print("\n✅ La configuración de email está funcionando correctamente")
        return True
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ ERROR AL ENVIAR EMAIL")
        print("=" * 60)
        print(f"\nError: {str(e)}")
        print("\n🔍 Posibles causas:")
        print("1. EMAIL_HOST_USER o EMAIL_HOST_PASSWORD incorrectos en .env")
        print("2. No has generado una contraseña de aplicación en Gmail")
        print("3. Verificación en 2 pasos no activada en Gmail")
        print("4. Problemas de conexión a internet")
        print("\n📖 Consulta GUIA_CONFIGURACION_EMAIL.md para más ayuda")
        return False


if __name__ == "__main__":
    test_email_configuration()
