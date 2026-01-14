from dataclasses import dataclass
from enum import Enum
from typing import Optional
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from premailer import transform

from app_auth.models import CustomUser
from app_auth.services.user_service import get_user_or_fail
from app_auth.utils.email_utils import get_email_local_part
from app_auth.utils.encoding_utils import encode_int_to_b64


@dataclass(frozen=True)
class EmailSchema:
    template: str
    subject: str
    plain_text: str
    frontend_path: Optional[str] = None


class EmailType(str, Enum):
    USER_ACTIVATION = "user_activation"
    PASSWORD_RESET = "password_reset"


EMAIL_SCHEMAS: dict[EmailType, EmailSchema] = {
    EmailType.USER_ACTIVATION: EmailSchema(
        template="app_auth/emails/confirm_email.html",
        subject="Confirm your email",
        plain_text="Please activate your account by clicking the link.",
        frontend_path=settings.FRONTEND_USER_ACTIVATION_PATH,
    ),
    EmailType.PASSWORD_RESET: EmailSchema(
        template="app_auth/emails/reset_password.html",
        subject="Password reset",
        plain_text="Click the link to reset your password.",
        frontend_path=settings.FRONTEND_PASSWORD_RESET_PATH,
    )
}


def build_email_verification_url(user: CustomUser, path: str) -> str:
    query = urlencode({
        'uid': encode_int_to_b64(user.pk),
        'token': default_token_generator.make_token(user)
    })
    return f'{settings.FRONTEND_BASE_URL.rstrip("/")}/{path.lstrip("/")}?{query}'


def build_email_context(user: CustomUser, schema: EmailSchema, extra_context: Optional[dict] = None) -> dict:
    context = {
        "user": user,
        "name": get_email_local_part(user.email),
        "frontend_base_url": settings.FRONTEND_BASE_URL,
        "logo_file_name": settings.FRONTEND_LOGO_FILE_NAME,
    }

    if schema.frontend_path:
        context["url"] = build_email_verification_url(user, schema.frontend_path)

    if extra_context:
        context.update(extra_context)

    return context


def send_email(email_type_str: str, user_id: int, extra_context: Optional[dict] = None, *, mail_sender=send_mail) -> None:
    email_type = EmailType(email_type_str)
    user = get_user_or_fail(pk=user_id)
    schema = EMAIL_SCHEMAS[email_type]

    context = build_email_context(user, schema, extra_context)
    print("EMAIL CONTEXT:", context)
    html_message = transform(render_to_string(schema.template, context))

    mail_sender(
        subject=schema.subject,
        message=schema.plain_text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )