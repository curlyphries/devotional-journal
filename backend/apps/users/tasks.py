"""
Celery tasks for user-related operations.
"""

import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


@shared_task
def send_magic_link_email(user_id: str, token: str):
    """
    Send a magic link email to the user.
    In dev mode with console backend, also prints a prominent login URL.
    """
    from .models import User

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return

    base_url = getattr(settings, "FRONTEND_URL", "http://localhost:3001")
    magic_link = f"{base_url}/auth/verify?token={token}"

    # A sign-in link is a credential: whoever reads it can sign in as this
    # person. It is written to the log only when the operator asked for that
    # (MAGIC_LINK_LOG=true — a private instance with no mail server).
    if getattr(settings, "MAGIC_LINK_LOG", False):
        print("\n" + "=" * 70)
        print("DEVOTIONAL JOURNAL - SIGN-IN LINK (MAGIC_LINK_LOG is on)")
        print(f"User: {user.email}")
        print(f"\n{magic_link}\n")
        print("=" * 70 + "\n", flush=True)
    else:
        logger.info("Sign-in link generated for user %s", user.id)

    subject = "Your Devotional Journal Login Link"
    message = f"""
Hello{' ' + user.display_name if user.display_name else ''},

Click the link below to sign in to Devotional Journal:

{magic_link}

This link will expire in 15 minutes.

If you didn't request this link, you can safely ignore this email.

- Devotional Journal
"""

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception:
        if getattr(settings, "MAGIC_LINK_LOG", False):
            # The link is in the log, so sign-in still works without mail.
            logger.warning("Sign-in email could not be sent; the link is in the log.")
            return
        logger.exception(
            "Sign-in email could not be sent to user %s. Check EMAIL_* settings.",
            user.id,
        )
        raise
