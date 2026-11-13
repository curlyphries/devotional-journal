"""
Create a one-time sign-in link without sending any email.

    python manage.py signin_link you@example.com
    python manage.py signin_link you@example.com --create --name "Your Name"

For servers with no mail server, or when a message has gone astray. The link
works once and expires like an emailed one. Anyone who has it can sign in as
that person, so pass it on privately.
"""

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.users.emailing import signin_link
from apps.users.models import MagicLinkToken, User


class Command(BaseCommand):
    help = "Print a one-time sign-in link for an account."

    def add_arguments(self, parser):
        parser.add_argument("email")
        parser.add_argument(
            "--create",
            action="store_true",
            help="Create the account if it does not exist",
        )
        parser.add_argument("--name", default="", help="Display name when creating")

    def handle(self, *args, **options):
        email = User.objects.normalize_email(options["email"].strip())
        user = User.objects.filter(email__iexact=email).first()
        if user is None:
            if not options["create"]:
                raise CommandError(
                    f"There is no account for {email}. Add --create to make one."
                )
            user = User.objects.create_user(email=email, display_name=options["name"])
            self.stdout.write(f"Created an account for {email}.")
        if not user.is_active:
            raise CommandError(f"The account for {email} is deactivated.")

        _token, raw = MagicLinkToken.create_for_user(user)
        minutes = getattr(settings, "MAGIC_LINK_EXPIRY_MINUTES", 15)
        self.stdout.write(
            f"Sign-in link for {email} (works once, expires in {minutes} minutes):"
        )
        self.stdout.write("")
        self.stdout.write(signin_link(raw))
        self.stdout.write("")
