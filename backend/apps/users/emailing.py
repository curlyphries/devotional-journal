"""
Sending the sign-in email, and explaining plainly when it cannot be sent.

"I never got the email" has a handful of causes. Each one is recognised here
and turned into a sentence that says what went wrong and what to change, so
it shows up in the server log, in `manage.py send_test_email`, and (in
general terms) on the sign-in page.
"""

import logging
import smtplib
import socket
import ssl
from dataclasses import dataclass

from django.conf import settings
from django.core.mail import EmailMessage, get_connection

logger = logging.getLogger(__name__)


@dataclass
class MailProblem:
    code: str
    message: str
    suggestion: str

    def __str__(self):
        return f"{self.message} {self.suggestion}"


def describe_mail_settings() -> dict:
    """The mail settings in use, safe to print (never the password)."""
    if settings.EMAIL_USE_SSL:
        security = "TLS from the start (EMAIL_USE_SSL)"
    elif settings.EMAIL_USE_TLS:
        security = "STARTTLS (EMAIL_USE_TLS)"
    else:
        security = "none (plain text)"
    return {
        "configured": settings.EMAIL_CONFIGURED,
        "backend": settings.EMAIL_BACKEND.rsplit(".", 2)[-2],
        "host": settings.EMAIL_HOST or "(not set)",
        "port": settings.EMAIL_PORT,
        "security": security,
        "username": settings.EMAIL_HOST_USER or "(none - no login)",
        "password": "set" if settings.EMAIL_HOST_PASSWORD else "(none)",
        "from": settings.DEFAULT_FROM_EMAIL,
        "timeout_seconds": settings.EMAIL_TIMEOUT,
        "announces_itself_as": socket.getfqdn(),
    }


def diagnose(exc: BaseException) -> MailProblem:
    """Turn a mail failure into what went wrong and what to do about it."""
    host, port = settings.EMAIL_HOST, settings.EMAIL_PORT
    where = f"{host}:{port}"

    if isinstance(exc, smtplib.SMTPAuthenticationError):
        return MailProblem(
            "MAIL_LOGIN_REJECTED",
            f"The mail server at {where} rejected the username or password.",
            "Check EMAIL_HOST_USER and EMAIL_HOST_PASSWORD. Many servers want the full "
            "address as the username, and some need an app-specific password.",
        )
    if isinstance(exc, smtplib.SMTPRecipientsRefused):
        return MailProblem(
            "MAIL_RECIPIENT_REFUSED",
            f"The mail server at {where} refused to deliver to that address.",
            "It is probably refusing to relay: log in (EMAIL_HOST_USER / EMAIL_HOST_PASSWORD), "
            "or allow this server's address to relay, or send only to addresses it hosts.",
        )
    if isinstance(exc, smtplib.SMTPSenderRefused):
        return MailProblem(
            "MAIL_SENDER_REFUSED",
            f"The mail server at {where} refused the From address “{settings.DEFAULT_FROM_EMAIL}”.",
            "Set DEFAULT_FROM_EMAIL to an address this login is allowed to send as "
            "(usually the same address as EMAIL_HOST_USER).",
        )
    if isinstance(exc, smtplib.SMTPHeloError):
        return MailProblem(
            "MAIL_HELO_REJECTED",
            f"The mail server at {where} rejected this server's name “{socket.getfqdn()}”.",
            "Give the backend a fully qualified host name (MESH_HOSTNAME in .env.mesh, "
            "or `hostname:` in the compose file).",
        )
    if isinstance(exc, smtplib.SMTPNotSupportedError):
        return MailProblem(
            "MAIL_TLS_MISMATCH",
            f"The mail server at {where} does not offer what was asked of it: {exc}.",
            "If it says STARTTLS is not supported, use port 465 with EMAIL_USE_SSL=true, "
            "or set EMAIL_USE_TLS=false for a plain port-25 relay. If it says AUTH is not "
            "supported, clear EMAIL_HOST_USER and EMAIL_HOST_PASSWORD.",
        )
    if isinstance(exc, (ssl.SSLError, smtplib.SMTPServerDisconnected)):
        return MailProblem(
            "MAIL_TLS_MISMATCH",
            f"The secure connection to {where} could not be set up ({exc}).",
            "The port and the security setting probably do not match: port 465 needs "
            "EMAIL_USE_SSL=true; port 587 needs EMAIL_USE_TLS=true. A certificate error means "
            "EMAIL_HOST must be the name on the server's certificate.",
        )
    if isinstance(exc, socket.gaierror):
        return MailProblem(
            "MAIL_HOST_NOT_FOUND",
            f"The mail server name “{host}” could not be found.",
            "Check EMAIL_HOST for typos, and that this server can resolve that name "
            "(from inside the container, too).",
        )
    if isinstance(exc, ConnectionRefusedError):
        return MailProblem(
            "MAIL_CONNECTION_REFUSED",
            f"Nothing answered at {where}.",
            "Check EMAIL_HOST and EMAIL_PORT, and that the mail server accepts connections "
            "from this machine. Inside a container, “localhost” is the container itself.",
        )
    if isinstance(exc, (socket.timeout, TimeoutError)):
        return MailProblem(
            "MAIL_TIMEOUT",
            f"The mail server at {where} did not answer within {settings.EMAIL_TIMEOUT} seconds.",
            "A firewall is probably dropping the connection: allow outbound traffic to that "
            "port, or use the port your mail server actually listens on (587, 465 or 25).",
        )
    if isinstance(exc, smtplib.SMTPResponseException):
        detail = (
            exc.smtp_error.decode(errors="replace")
            if isinstance(exc.smtp_error, bytes)
            else exc.smtp_error
        )
        return MailProblem(
            "MAIL_REJECTED",
            f"The mail server at {where} answered {exc.smtp_code}: {detail}",
            "That is the server's own explanation; its log will say more.",
        )
    if isinstance(exc, OSError):
        return MailProblem(
            "MAIL_NETWORK_ERROR",
            f"Could not talk to the mail server at {where}: {exc}.",
            "Check the network path from this server to the mail server.",
        )
    return MailProblem(
        "MAIL_FAILED",
        f"Sending failed: {exc.__class__.__name__}: {exc}",
        "Run `python manage.py send_test_email you@example.com` on the server for details.",
    )


def signin_link(raw_token: str) -> str:
    base = getattr(settings, "FRONTEND_URL", "http://localhost:3001").rstrip("/")
    return f"{base}/auth/verify?token={raw_token}"


def build_signin_message(user, link: str) -> EmailMessage:
    minutes = getattr(settings, "MAGIC_LINK_EXPIRY_MINUTES", 15)
    greeting = f"Hello {user.display_name}," if user.display_name else "Hello,"
    body = f"""{greeting}

Open this link to sign in to Devotional Journal:

{link}

It works once and expires in {minutes} minutes.

If you did not ask for it, you can ignore this email.

- Devotional Journal
"""
    return EmailMessage(
        subject="Your Devotional Journal sign-in link",
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )


def send_signin_email(user, link: str) -> None:
    """Send the sign-in email. Raises the underlying error if it cannot be sent."""
    connection = get_connection(timeout=settings.EMAIL_TIMEOUT)
    message = build_signin_message(user, link)
    message.connection = connection
    message.send(fail_silently=False)
