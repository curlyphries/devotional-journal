"""
User and authentication models.
"""
import secrets
import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication."""

    def create_user(self, email, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.create_user(email, **extra_fields)
        if password:
            user.set_password(password)
            user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with email authentication and encryption support.
    """
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('bilingual', 'Bilingual'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=100, blank=True)
    language_preference = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default='en'
    )
    timezone = models.CharField(max_length=50, default='UTC')
    
    # AI Provider Settings
    AI_PROVIDER_CHOICES = [
        ('none', 'None (Use System Default)'),
        ('openai', 'OpenAI'),
        ('anthropic', 'Anthropic (Claude)'),
        ('openrouter', 'OpenRouter'),
        ('ollama', 'Ollama (Local)'),
        ('custom', 'Custom OpenAI-Compatible'),
    ]
    
    ai_provider = models.CharField(
        max_length=20,
        choices=AI_PROVIDER_CHOICES,
        default='none'
    )
    ai_api_key = models.CharField(max_length=500, blank=True)
    ai_model = models.CharField(max_length=100, blank=True)
    ai_base_url = models.CharField(max_length=500, blank=True)
    encryption_key_salt = models.BinaryField(max_length=32, editable=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    last_active_at = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    def set_ai_api_key(self, raw_key: str):
        """Encrypt and store the user's AI API key."""
        from shared.encryption import encrypt_content
        if raw_key:
            self.ai_api_key = encrypt_content(raw_key, self.encryption_key_salt).decode('latin-1')
        else:
            self.ai_api_key = ''

    def get_ai_api_key(self) -> str:
        """Decrypt and return the user's AI API key."""
        from shared.encryption import decrypt_content
        if not self.ai_api_key:
            return ''
        try:
            return decrypt_content(self.ai_api_key.encode('latin-1'), self.encryption_key_salt)
        except Exception:
            return self.ai_api_key

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.encryption_key_salt:
            self.encryption_key_salt = secrets.token_bytes(32)
        super().save(*args, **kwargs)

    def update_last_active(self):
        self.last_active_at = timezone.now()
        self.save(update_fields=['last_active_at'])


class MagicLinkToken(models.Model):
    """
    Token for passwordless magic link authentication.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='magic_links')
    token_hash = models.CharField(max_length=64, unique=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'magic_link_tokens'

    @classmethod
    def create_for_user(cls, user: User) -> tuple['MagicLinkToken', str]:
        """
        Create a new magic link token for a user.
        Returns the token object and the raw token string.
        """
        import hashlib
        raw_token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        expiry_minutes = getattr(settings, 'MAGIC_LINK_EXPIRY_MINUTES', 15)

        token = cls.objects.create(
            user=user,
            token_hash=token_hash,
            expires_at=timezone.now() + timedelta(minutes=expiry_minutes)
        )
        return token, raw_token

    @classmethod
    def verify_token(cls, raw_token: str) -> 'MagicLinkToken | None':
        """
        Verify a raw token and return the token object if valid.
        """
        import hashlib
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        try:
            token = cls.objects.get(
                token_hash=token_hash,
                used_at__isnull=True,
                expires_at__gt=timezone.now()
            )
            return token
        except cls.DoesNotExist:
            return None

    def mark_used(self):
        self.used_at = timezone.now()
        self.save(update_fields=['used_at'])
