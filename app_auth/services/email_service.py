from typing import Optional, Dict

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from premailer import transform

from app_auth.services.user_service import get_user_or_fail


EMAIL_CONFIG: Dict[str, Dict[str, str]] = {
    "user_activation": {
        "template": "emails/confirm_email.html",
        "subject": "Confirm your email",
        "plain_text": "Please activate your account by clicking the link.",
    },
    "password_reset": {
        "template": "emails/reset_password.html",
        "subject": "Password reset",
        "plain_text": "Click the link to reset your password.",
    },
}

EMAIL_LINK_PATHS = {
    'user_activation': settings.FRONTEND_USER_ACTIVATION_PATH,
    'password_reset': settings.FRONTEND_PASSWORD_RESET_PATH,
}


def send_email(email_type: str, user_id: int, link: Optional[str] = None, context: Optional[dict] = None) -> None:
    user = get_user_or_fail(user_id=user_id)
    context = context or {}
    context.setdefault("user", user)
    context["link"] = link

    config = EMAIL_CONFIG[email_type]

    html_raw = render_to_string(config["template"], context)
    html_message = transform(html_raw)

    send_mail(
        subject=config["subject"],
        message=config["plain_text"],
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )