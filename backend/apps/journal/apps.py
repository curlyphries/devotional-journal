from django.apps import AppConfig


class JournalConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.journal"

    def ready(self):
        # Import signal handlers so they register on app load.
        from . import signals  # noqa: F401
