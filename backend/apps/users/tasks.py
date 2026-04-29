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

    # Always print the login URL prominently for Tailscale-only internal access
    print("\n" + "=" * 70)
    print("🔐 DEVOTIONAL JOURNAL - MAGIC LOGIN LINK")
    print("=" * 70)
    print(f"User: {user.email}")
    print(f"\n👉 LOGIN URL:\n{magic_link}\n")
    print("=" * 70 + "\n")
    logger.info(f"Magic link generated for {user.email}: {magic_link}")

    subject = "Your Devotional Journal Login Link"
    message = f"""
Hello{' ' + user.display_name if user.display_name else ''},

Click the link below to sign in to Devotional Journal:

{magic_link}

This link will expire in 15 minutes.

If you didn't request this link, you can safely ignore this email.

- Devotional Journal
"""

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
