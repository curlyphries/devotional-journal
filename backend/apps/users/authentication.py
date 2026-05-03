"""
JWT authentication for the API.
"""

import uuid
from datetime import datetime, timedelta, timezone

import jwt
from django.conf import settings
from django.core.cache import cache
from rest_framework import authentication, exceptions

from .models import User

# Token blacklist TTL matches the longest token lifetime (refresh = 7 days)
_BLACKLIST_TTL = timedelta(days=7)
_BLACKLIST_PREFIX = "jwt_blacklist:"


def blacklist_token(jti: str, ttl: timedelta = _BLACKLIST_TTL) -> None:
    """Add a token's jti to the blacklist."""
    cache.set(f"{_BLACKLIST_PREFIX}{jti}", True, int(ttl.total_seconds()))


def is_token_blacklisted(jti: str) -> bool:
    """Check if a token's jti has been blacklisted."""
    return cache.get(f"{_BLACKLIST_PREFIX}{jti}") is True


class JWTAuthentication(authentication.BaseAuthentication):
    """
    JWT token authentication.
    """

    keyword = "Bearer"

    def authenticate_header(self, request):
        return self.keyword

    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if not auth_header:
            return None
        if not auth_header.startswith(f"{self.keyword} "):
            raise exceptions.AuthenticationFailed("Invalid authentication scheme")

        token = auth_header[len(self.keyword) + 1 :]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid token")

        jti = payload.get("jti")
        if jti and is_token_blacklisted(jti):
            raise exceptions.AuthenticationFailed("Token has been revoked")

        try:
            user = User.objects.get(id=payload["user_id"])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("User not found")

        if not user.is_active:
            raise exceptions.AuthenticationFailed("User is inactive")

        return (user, token)


def generate_tokens(user: User) -> dict:
    """
    Generate access and refresh tokens for a user.
    """
    now = datetime.now(timezone.utc)

    access_payload = {
        "user_id": str(user.id),
        "jti": uuid.uuid4().hex,
        "exp": now + timedelta(hours=1),
        "iat": now,
        "type": "access",
    }

    refresh_payload = {
        "user_id": str(user.id),
        "jti": uuid.uuid4().hex,
        "exp": now + timedelta(days=7),
        "iat": now,
        "type": "refresh",
    }

    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm="HS256")
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm="HS256")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": 3600,
    }


def refresh_access_token(refresh_token: str) -> dict:
    """
    Generate a new access token from a refresh token.
    Blacklists the old refresh token so it cannot be reused.
    """
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed("Refresh token has expired")
    except jwt.InvalidTokenError:
        raise exceptions.AuthenticationFailed("Invalid refresh token")

    if payload.get("type") != "refresh":
        raise exceptions.AuthenticationFailed("Invalid token type")

    old_jti = payload.get("jti")
    if old_jti and is_token_blacklisted(old_jti):
        raise exceptions.AuthenticationFailed("Refresh token has been revoked")

    try:
        user = User.objects.get(id=payload["user_id"])
    except User.DoesNotExist:
        raise exceptions.AuthenticationFailed("User not found")

    # Blacklist the old refresh token
    if old_jti:
        blacklist_token(old_jti)

    return generate_tokens(user)
