"""
Create an account by email (sign-in is by emailed/logged link, so no password).

    python manage.py create_user you@example.com --name "Your Name"

Needed on a private instance without Google sign-in: requesting a sign-in link
never creates an account on its own.
"""

from django.core.management.base import BaseCommand, CommandError
from django.core.validators import validate_email

from apps.users.models import User


class Command(BaseCommand):
    help = "Create a user who can then sign in with a magic link."

    def add_arguments(self, parser):
        parser.add_argument("email")
        parser.add_argument("--name", default="", help="Display name")
        parser.add_argument(
            "--language", default="en", choices=["en", "es", "bilingual"]
        )
        parser.add_argument(
            "--staff", action="store_true", help="Allow Django admin access"
        )

    def handle(self, *args, **options):
        email = User.objects.normalize_email(options["email"].strip())
        try:
            validate_email(email)
        except Exception:
            raise CommandError(f"'{email}' is not a valid email address.")
        if User.objects.filter(email__iexact=email).exists():
            raise CommandError(f"An account for {email} already exists.")

        User.objects.create_user(
            email=email,
            display_name=options["name"],
            language_preference=options["language"],
            is_staff=options["staff"],
        )
        self.stdout.write(
            self.style.SUCCESS(f"Created {email}. They can now request a sign-in link.")
        )
