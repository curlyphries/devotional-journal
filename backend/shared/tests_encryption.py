"""
Tests for shared encryption utilities.
Covers key derivation, encrypt/decrypt round-trips, and tamper detection.
"""
import pytest
from cryptography.fernet import InvalidToken
from django.test import override_settings


ENCRYPTION_SETTINGS = {
    'ENCRYPTION_ROOT_KEY': 'test-encryption-root-key-32bytes!'
}


@pytest.fixture
def salt():
    import secrets
    return secrets.token_bytes(32)


@pytest.fixture
def alt_salt():
    import secrets
    return secrets.token_bytes(32)


# ---------------------------------------------------------------------------
# Key Derivation
# ---------------------------------------------------------------------------

class TestDeriveUserKey:
    def test_derive_key_returns_bytes(self, salt):
        with override_settings(**ENCRYPTION_SETTINGS):
            from shared.encryption import derive_user_key
            key = derive_user_key(salt)
        assert isinstance(key, bytes)

    def test_derive_key_is_44_bytes(self, salt):
        """Fernet requires a 32-byte key, which is 44 bytes when base64url-encoded."""
        with override_settings(**ENCRYPTION_SETTINGS):
            from shared.encryption import derive_user_key
            key = derive_user_key(salt)
        assert len(key) == 44

    def test_same_salt_same_key(self, salt):
        """Key derivation must be deterministic for the same salt + root key."""
        with override_settings(**ENCRYPTION_SETTINGS):
            from shared.encryption import derive_user_key
            k1 = derive_user_key(salt)
            k2 = derive_user_key(salt)
        assert k1 == k2

    def test_different_salts_different_keys(self, salt, alt_salt):
        """Different salts must produce different derived keys."""
        with override_settings(**ENCRYPTION_SETTINGS):
            from shared.encryption import derive_user_key
            k1 = derive_user_key(salt)
            k2 = derive_user_key(alt_salt)
        assert k1 != k2

    def test_different_root_keys_different_derived_keys(self, salt):
        """A different root key must produce a different derived key for the same salt."""
        with override_settings(ENCRYPTION_ROOT_KEY='root-key-one-32-chars-padded!!'):
            from shared.encryption import derive_user_key
            import importlib, shared.encryption
            importlib.reload(shared.encryption)
            k1 = shared.encryption.derive_user_key(salt)

        with override_settings(ENCRYPTION_ROOT_KEY='root-key-two-32-chars-padded!!'):
            importlib.reload(shared.encryption)
            k2 = shared.encryption.derive_user_key(salt)

        assert k1 != k2

    def test_pbkdf2_iteration_count(self):
        """Confirm the iteration count meets NIST SP 800-132 minimum."""
        with override_settings(**ENCRYPTION_SETTINGS):
            from shared.encryption import PBKDF2_ITERATIONS
        assert PBKDF2_ITERATIONS >= 600_000


# ---------------------------------------------------------------------------
# Encrypt / Decrypt Round-Trip
# ---------------------------------------------------------------------------

class TestEncryptDecrypt:
    def test_basic_roundtrip(self, salt):
        with override_settings(**ENCRYPTION_SETTINGS):
            from shared.encryption import encrypt_content, decrypt_content
            plaintext = 'Today I am grateful for my family.'
            ciphertext = encrypt_content(plaintext, salt)
            result = decrypt_content(ciphertext, salt)
        assert result == plaintext

    def test_empty_string_roundtrip(self, salt):
        with override_settings(**ENCRYPTION_SETTINGS):
            from shared.encryption import encrypt_content, decrypt_content
            ciphertext = encrypt_content('', salt)
            assert decrypt_content(ciphertext, salt) == ''

    def test_unicode_content_roundtrip(self, salt):
        with override_settings(**ENCRYPTION_SETTINGS):
            from shared.encryption import encrypt_content, decrypt_content
            plaintext = 'Hoy estoy agradecido por mi familia. 🙏'
            ciphertext = encrypt_content(plaintext, salt)
            assert decrypt_content(ciphertext, salt) == plaintext

    def test_long_content_roundtrip(self, salt):
        with override_settings(**ENCRYPTION_SETTINGS):
            from shared.encryption import encrypt_content, decrypt_content
            plaintext = 'A' * 10_000
            ciphertext = encrypt_content(plaintext, salt)
            assert decrypt_content(ciphertext, salt) == plaintext

    def test_ciphertext_is_not_plaintext(self, salt):
        with override_settings(**ENCRYPTION_SETTINGS):
            from shared.encryption import encrypt_content
            plaintext = 'do not store me in plaintext'
            ciphertext = encrypt_content(plaintext, salt)
        assert plaintext.encode() not in ciphertext

    def test_encrypt_same_content_twice_produces_different_ciphertext(self, salt):
        """Fernet uses a random IV — identical plaintexts must not produce identical ciphertext."""
        with override_settings(**ENCRYPTION_SETTINGS):
            from shared.encryption import encrypt_content
            c1 = encrypt_content('same content', salt)
            c2 = encrypt_content('same content', salt)
        assert c1 != c2

    def test_wrong_salt_raises_on_decrypt(self, salt, alt_salt):
        """Decrypting with a different salt must fail (wrong key)."""
        with override_settings(**ENCRYPTION_SETTINGS):
            from shared.encryption import encrypt_content, decrypt_content
            ciphertext = encrypt_content('secret text', salt)
            with pytest.raises(Exception):
                decrypt_content(ciphertext, alt_salt)

    def test_tampered_ciphertext_raises(self, salt):
        """Any modification to the ciphertext must cause decryption to fail."""
        with override_settings(**ENCRYPTION_SETTINGS):
            from shared.encryption import encrypt_content, decrypt_content
            ciphertext = encrypt_content('untampered', salt)
            tampered = bytes([b ^ 0xFF for b in ciphertext])
            with pytest.raises(Exception):
                decrypt_content(tampered, salt)

    def test_truncated_ciphertext_raises(self, salt):
        with override_settings(**ENCRYPTION_SETTINGS):
            from shared.encryption import encrypt_content, decrypt_content
            ciphertext = encrypt_content('some text', salt)
            with pytest.raises(Exception):
                decrypt_content(ciphertext[:10], salt)


# ---------------------------------------------------------------------------
# Cross-user isolation
# ---------------------------------------------------------------------------

class TestCrossUserIsolation:
    def test_user_a_cannot_decrypt_user_b_content(self, salt, alt_salt):
        """Content encrypted with user A's salt must not be readable by user B."""
        with override_settings(**ENCRYPTION_SETTINGS):
            from shared.encryption import encrypt_content, decrypt_content
            ciphertext_a = encrypt_content("User A private thought", salt)
            with pytest.raises(Exception):
                decrypt_content(ciphertext_a, alt_salt)

    def test_same_content_different_users_different_ciphertext(self, salt, alt_salt):
        with override_settings(**ENCRYPTION_SETTINGS):
            from shared.encryption import encrypt_content
            c1 = encrypt_content('identical text', salt)
            c2 = encrypt_content('identical text', alt_salt)
        assert c1 != c2
