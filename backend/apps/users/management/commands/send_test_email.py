"""
Find out why sign-in emails are not arriving.

    python manage.py send_test_email you@example.com

Prints the mail settings in use (never the password), sends one test message,
and - if that fails - says what went wrong and what to change.
"""

from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from django.core.management.base import BaseCommand, CommandError

from apps.users.emailing import describe_mail_settings, diagnose
from apps.users.models import User


class Command(BaseCommand):
    help = "Send a test email and explain any failure in plain words."

    def add_arguments(self, parser):
        parser.add_argument("to", help="Address to send the test message to")

    def handle(self, *args, **options):
        to = options["to"].strip()
        info = describe_mail_settings()

        self.stdout.write("Mail settings in use")
        for label, key in (
            ("  Mail server", "host"),
            ("  Port", "port"),
            ("  Security", "security"),
            ("  Login", "username"),
            ("  Password", "password"),
            ("  From", "from"),
            ("  This server calls itself", "announces_itself_as"),
        ):
            self.stdout.write(f"{label}: {info[key]}")
        self.stdout.write(
            f"  Sign-in links also written to the log: {'yes' if settings.MAGIC_LINK_LOG else 'no'}"
        )
        self.stdout.write("")

        if settings.EMAIL_BACKEND.endswith(
            ("console.EmailBackend", "locmem.EmailBackend")
        ):
            self.stdout.write(
                self.style.WARNING(
                    "This is the development configuration: mail is printed, not sent. "
                    "Nothing will arrive in an inbox."
                )
            )
        elif not info["configured"]:
            raise CommandError(
                "No mail server is configured, so no sign-in email can be sent.\n"
                "Set EMAIL_HOST (and usually EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, "
                "DEFAULT_FROM_EMAIL) in the environment file and restart the backend and worker.\n"
                "Until then, create a sign-in link with:  python manage.py signin_link <email>"
            )

        if not User.objects.filter(email__iexact=to).exists():
            self.stdout.write(
                self.style.WARNING(
                    f"Note: there is no account for {to}. Requesting a sign-in link for it "
                    + (
                        "will create one (ALLOW_EMAIL_SIGNUP is on)."
                        if settings.ALLOW_EMAIL_SIGNUP
                        else "sends nothing. Create the account first:  "
                        f"python manage.py create_user {to}"
                    )
                )
            )

        self.stdout.write(f"Sending a test message to {to} ...")
        message = EmailMessage(
            subject="Devotional Journal test message",
            body=(
                "This is a test from your Devotional Journal server.\n\n"
                "If you are reading it, sign-in emails will arrive too."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to],
            connection=get_connection(timeout=settings.EMAIL_TIMEOUT),
        )
        try:
            message.send(fail_silently=False)
        except Exception as exc:  # noqa: BLE001 - every failure is explained
            problem = diagnose(exc)
            raise CommandError(
                f"NOT SENT [{problem.code}]\n  What happened: {problem.message}\n"
                f"  What to do: {problem.suggestion}"
            )
        self.stdout.write(
            self.style.SUCCESS(
                "The mail server accepted the message. If it does not reach the inbox, look in "
                "the spam folder, then in the mail server's own log: from here on it is the "
                "mail server's job."
            )
        )
