from datetime import timedelta

from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from app_authentication.models import CustomUser


def send_activation_email(user, html_message):
    send_mail(
        subject='Activate your account',
        message='Please activate your account by clicking the link.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )

def delete_inactive_users():
    cutoff = timezone.now() - timedelta(hours=24)
    users_to_delete = CustomUser.objects.filter(is_active=False, created_at__lte=cutoff)
    users_to_delete.delete()