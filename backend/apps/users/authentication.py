"""
JWT authentication for the API.
"""
import jwt
from datetime import datetime, timedelta

from django.conf import settings
from rest_framework import authentication, exceptions

from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    """
    JWT token authentication.
    """
    keyword = 'Bearer'

    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith(f'{self.keyword} '):
            return None

        token = auth_header[len(self.keyword) + 1:]
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')

        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('User is inactive')

        return (user, token)


def generate_tokens(user: User) -> dict:
    """
    Generate access and refresh tokens for a user.
    """
    now = datetime.utcnow()

    access_payload = {
        'user_id': str(user.id),
        'exp': now + timedelta(hours=1),
        'iat': now,
        'type': 'access'
    }

    refresh_payload = {
        'user_id': str(user.id),
        'exp': now + timedelta(days=7),
        'iat': now,
        'type': 'refresh'
    }

    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'expires_in': 3600
    }


def refresh_access_token(refresh_token: str) -> dict:
    """
    Generate a new access token from a refresh token.
    """
    try:
        payload = jwt.decode(
            refresh_token,
            settings.SECRET_KEY,
            algorithms=['HS256']
        )
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed('Refresh token has expired')
    except jwt.InvalidTokenError:
        raise exceptions.AuthenticationFailed('Invalid refresh token')

    if payload.get('type') != 'refresh':
        raise exceptions.AuthenticationFailed('Invalid token type')

    try:
        user = User.objects.get(id=payload['user_id'])
    except User.DoesNotExist:
        raise exceptions.AuthenticationFailed('User not found')

    return generate_tokens(user)
