"""
Encryption utilities for journal entries.
Uses Fernet symmetric encryption with per-user derived keys.
"""
import base64
import hashlib
from typing import Optional

from cryptography.fernet import Fernet
from django.conf import settings
from django.db import models


def derive_user_key(user_salt: bytes) -> bytes:
    """
    Derive a user-specific encryption key from the root key and user salt.
    """
    root_key = settings.ENCRYPTION_ROOT_KEY.encode()
    derived = hashlib.pbkdf2_hmac(
        'sha256',
        root_key,
        user_salt,
        iterations=100000,
        dklen=32
    )
    return base64.urlsafe_b64encode(derived)


def encrypt_content(content: str, user_salt: bytes) -> bytes:
    """
    Encrypt content using the user's derived key.
    """
    key = derive_user_key(user_salt)
    fernet = Fernet(key)
    return fernet.encrypt(content.encode())


def decrypt_content(encrypted_content: bytes, user_salt: bytes) -> str:
    """
    Decrypt content using the user's derived key.
    """
    key = derive_user_key(user_salt)
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_content).decode()


class EncryptedTextField(models.BinaryField):
    """
    A Django model field that encrypts text content at rest.
    Requires the model instance to have access to the user's encryption salt.
    """
    description = "Encrypted text field"

    def __init__(self, *args, **kwargs):
        kwargs['editable'] = True
        super().__init__(*args, **kwargs)

    def get_user_salt(self, model_instance) -> Optional[bytes]:
        """
        Get the user's encryption salt from the model instance.
        Override this method if the user relationship is different.
        """
        if hasattr(model_instance, 'user') and model_instance.user:
            return model_instance.user.encryption_key_salt
        return None

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if value is not None and isinstance(value, str):
            user_salt = self.get_user_salt(model_instance)
            if user_salt:
                encrypted = encrypt_content(value, user_salt)
                setattr(model_instance, self.attname, encrypted)
                return encrypted
        return value

    def from_db_value(self, value, expression, connection):
        return value

    def to_python(self, value):
        return value
