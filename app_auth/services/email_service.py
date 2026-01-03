from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from premailer import transform

from app_auth.services.user_service import get_user_from_id_or_fail


def send_user_activation_email(user, activation_link):
    """
    Send account activation email to the specified user.
    """
    template_activation_email = 'emails/confirm_email.html'

    html_raw = render_to_string(template_activation_email, {
        'user': user,
        'activation_link': activation_link,
    })

    html_message = transform(html_raw)

    send_mail(
        subject='Confirm your email',
        message='Please activate your account by clicking the link.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )


def send_password_reset_email(user_id: int, reset_link):
    """
    Send password reset email.
    """
    user = get_user_from_id_or_fail(user_id)
    template_password_reset_email = 'emails/reset_password.html'


    html_raw = render_to_string(template_password_reset_email, {
        'user': user,
        'reset_link': reset_link,
    })

    html_message = transform(html_raw)

    send_mail(
        subject='Password reset',
        message='Click the link to reset your password.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )