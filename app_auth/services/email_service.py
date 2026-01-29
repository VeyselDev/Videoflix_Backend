from dataclasses import dataclass
from enum import Enum
from typing import Optional
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from premailer import transform
from rq.job import Job

from app_auth.models.custom_user import CustomUser
from app_auth.services.user_service import get_user_or_404
from app_auth.utils.email_utils import get_email_local_part
from app_auth.utils.encoding_utils import encode_int_to_b64
from core.utils.queue_utils import enqueue_job


@dataclass(frozen=True)
class EmailSchema:
    template: str
    subject: str
    message: str
    frontend_path: Optional[str] = None


class EmailType(str, Enum):
    USER_ACTIVATION = "user_activation"
    PASSWORD_RESET = "password_reset"


EMAIL_SCHEMAS: dict[EmailType, EmailSchema] = {
    EmailType.USER_ACTIVATION: EmailSchema(
        template="app_auth/emails/confirm_email.html",
        subject="Confirm your email",
        message=(
            "Dear {name},\n\n"
            "Thank you for registering with Videoflix. To complete your registration and verify your email address, "
            "please click the link below:\n\n"
            "{url}\n\n"
            "Note that this link will expire in 24 hours.\n\n"
            "If you did not create an account, you can ignore this email.\n\n"
            "Best regards,\n"
            "Your Videoflix Team"
        ),
        frontend_path=settings.FRONTEND_USER_ACTIVATION_PATH,
    ),
    EmailType.PASSWORD_RESET: EmailSchema(
        template="app_auth/emails/reset_password.html",
        subject="Password reset",
        message=(
            "Dear {name},\n\n"
            "We recently received a request to reset your password. If you made this request, "
            "please click on the following link to reset your password:\n\n"
            "{url}\n\n"
            "Note that this link will expire in 24 hours.\n\n"
            "If you did not request a password reset, you can ignore this email.\n\n"
            "Best regards,\n"
            "Your Videoflix Team"
        ),
        frontend_path=settings.FRONTEND_PASSWORD_RESET_PATH,
    )
}


def _build_email_verification_url(user: CustomUser, path: str) -> str:
    query = urlencode({
        'uid': encode_int_to_b64(user.pk),
        'token': default_token_generator.make_token(user)
    })
    return f'{settings.FRONTEND_BASE_URL.rstrip("/")}/{path.lstrip("/")}?{query}'


def _build_email_context(user: CustomUser, schema: EmailSchema, extra_context: Optional[dict] = None) -> dict:
    context = {
        "user": user,
        "name": get_email_local_part(user.email),
        "frontend_base_url": settings.FRONTEND_BASE_URL,
        "logo_file_name": settings.FRONTEND_LOGO_FILE_NAME,
    }

    if schema.frontend_path:
        context["url"] = _build_email_verification_url(user, schema.frontend_path)

    if extra_context:
        context.update(extra_context)

    return context


def _build_email_message(email_type: EmailType, user: CustomUser, extra_context: dict | None = None) -> tuple[str, str, str]:
    schema = EMAIL_SCHEMAS[email_type]
    context = _build_email_context(user, schema, extra_context)
    message = schema.message.format(**context)
    html_message = _render_html_body(schema.template, context)
    return schema.subject, message, html_message


def enqueue_email(*, email_type: EmailType, user_id: int) -> Job:
    return enqueue_job(_process_email_job, email_type.value, user_id)


def _render_html_body(template_name: str, context: dict) -> str:
    return transform(render_to_string(template_name, context))


def _process_email_job(email_type: EmailType, user_id: int, extra_context: Optional[dict] = None) -> None:
    user = get_user_or_404(pk=user_id)
    subject, message, html_message = _build_email_message(email_type=email_type, user=user, extra_context=extra_context)

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False
    )