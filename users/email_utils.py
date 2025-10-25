"""
Utilidades para envío de emails
"""
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_password_reset_email(user, reset_url, domain, protocol='http'):
    """
    Envía email de recuperación de contraseña con formato HTML
    
    Args:
        user: Usuario que solicita el reset
        reset_url: URL completa para resetear la contraseña
        domain: Dominio del sitio
        protocol: http o https
    """
    
    # Contexto para el template
    context = {
        'user': user,
        'reset_url': reset_url,
        'domain': domain,
        'protocol': protocol,
    }
    
    # Asunto del email
    subject = '🔐 Restablecer Contraseña - Software Contable'
    
    # Renderizar template HTML
    html_content = render_to_string('registration/password_reset_email_html.html', context)
    
    # Versión texto plano (fallback)
    text_content = strip_tags(html_content)
    
    # Crear email
    from_email = 'Software Contable <noreply@softwarecontable.com>'
    to_email = user.email
    
    # Crear mensaje con alternativas
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=[to_email]
    )
    
    # Adjuntar versión HTML
    email.attach_alternative(html_content, "text/html")
    
    # Enviar
    email.send(fail_silently=False)
    
    return True
