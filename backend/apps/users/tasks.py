"""
Celery tasks for user-related operations.
"""

import logging
import smtplib

from celery import shared_task
from django.conf import settings

from .emailing import diagnose, send_signin_email, signin_link

logger = logging.getLogger(__name__)

# Worth trying again: the server was busy or briefly unreachable. A rejected
# login or a refused address will not get better by retrying.
TRANSIENT = (
    smtplib.SMTPServerDisconnected,
    smtplib.SMTPConnectError,
    ConnectionError,
    TimeoutError,
)


def deliver_signin_link(user, raw_token: str) -> None:
    """
    Get a sign-in link to a person: by email when a mail server is configured,
    and into the server log when the operator asked for that.

    Raises if email was the only way and it failed.
    """
    link = signin_link(raw_token)

    # A sign-in link is a credential: whoever reads it can sign in as this
    # person. It is written to the log only when MAGIC_LINK_LOG is on (the
    # default when no mail server is configured).
    logged = getattr(settings, "MAGIC_LINK_LOG", False)
    if logged:
        print("\n" + "=" * 70)
        print("DEVOTIONAL JOURNAL - SIGN-IN LINK (MAGIC_LINK_LOG is on)")
        print(f"User: {user.email}")
        print(f"\n{link}\n")
        print("=" * 70 + "\n", flush=True)

    if not settings.EMAIL_CONFIGURED and not settings.EMAIL_BACKEND.endswith(
        ("console.EmailBackend", "locmem.EmailBackend")
    ):
        if not logged:
            logger.error(
                "A sign-in link was requested for user %s but there is no way to deliver "
                "it: no mail server is configured (EMAIL_HOST) and MAGIC_LINK_LOG is off. "
                "Configure EMAIL_*, or run `python manage.py signin_link <email>`.",
                user.id,
            )
        return

    try:
        send_signin_email(user, link)
        logger.info("Sign-in email sent for user %s", user.id)
    except Exception as exc:  # noqa: BLE001 - explained, then re-raised or tolerated
        problem = diagnose(exc)
        logger.error(
            "Sign-in email NOT sent for user %s [%s]: %s",
            user.id,
            problem.code,
            problem,
        )
        if logged:
            # The link is in the log, so the person can still sign in.
            return
        raise


@shared_task(
    bind=True,
    # Nobody reads this task's result. Not storing one also means queuing it
    # never waits on the result store when Redis is down.
    ignore_result=True,
    autoretry_for=TRANSIENT,
    retry_backoff=5,
    retry_backoff_max=60,
    max_retries=3,
)
def send_magic_link_email(self, user_id: str, token: str):
    """Deliver a sign-in link (email and/or server log). Retries brief outages."""
    from .models import User

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return
    deliver_signin_link(user, token)
