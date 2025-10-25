"""
Vistas personalizadas para recuperación de contraseña con email HTML
"""
from django.contrib.auth.views import PasswordResetView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class CustomPasswordResetView(PasswordResetView):
    """
    Vista personalizada para enviar emails HTML en recuperación de contraseña
    """
    
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Override del método send_mail para enviar emails HTML profesionales
        """
        # Renderizar el asunto
        subject = render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())  # Eliminar saltos de línea
        
        # Renderizar el contenido HTML
        html_content = render_to_string('registration/password_reset_email_html.html', context)
        
        # Versión texto plano (fallback)
        text_content = strip_tags(html_content)
        
        # Crear el email
        email_message = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[to_email]
        )
        
        # Adjuntar la versión HTML
        email_message.attach_alternative(html_content, "text/html")
        
        # Enviar
        email_message.send()
