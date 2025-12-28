from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from app_auth.services.auth_service import build_password_reset_link


def send_user_activation_email(user, activation_link):
    """
    Send account activation email to the specified user.
    """
    template_activation_email = 'emails/account_activation.html'

    html_message = render_to_string(template_activation_email, {
        'user': user,
        'activation_link': activation_link,
    })

    send_mail(
        subject='Activate your account',
        message='Please activate your account by clicking the link.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )


def send_password_reset_email(request, user):
    """
    Send password reset email.
    """
    template_password_reset_email = 'emails/password_reset.html'

    reset_link = build_password_reset_link(request, user)
    html_message = render_to_string(template_password_reset_email, {
        'user': user,
        'reset_link': reset_link,
    })

    send_mail(
        subject='Password reset',
        message='Click the link to reset your password.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )