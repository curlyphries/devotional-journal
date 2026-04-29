"""
Views for user authentication and profile management.
"""

import logging
import secrets
from urllib.parse import urlencode

import httpx
from django.conf import settings
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from .authentication import generate_tokens, refresh_access_token
from .models import MagicLinkToken, User
from .serializers import (
    MagicLinkRequestSerializer,
    MagicLinkVerifySerializer,
    RefreshTokenSerializer,
    UserSerializer,
    UserUpdateSerializer,
)
from .tasks import send_magic_link_email

logger = logging.getLogger(__name__)


class MagicLinkThrottle(AnonRateThrottle):
    rate = "5/hour"
    scope = "magic_link"


class AuthThrottle(AnonRateThrottle):
    rate = "10/hour"
    scope = "auth"


class MagicLinkRequestView(APIView):
    """
    Request a magic link for passwordless authentication.
    """

    permission_classes = [AllowAny]
    throttle_classes = [MagicLinkThrottle]

    def post(self, request):
        serializer = MagicLinkRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        # Do NOT create accounts here — silently succeed for unknown emails
        # to prevent account enumeration and unsolicited magic link spam.
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"message": "Magic link sent to your email"}, status=status.HTTP_200_OK
            )

        token_obj, raw_token = MagicLinkToken.create_for_user(user)
        send_magic_link_email.delay(user.id, raw_token)

        return Response(
            {"message": "Magic link sent to your email"}, status=status.HTTP_200_OK
        )


class MagicLinkVerifyView(APIView):
    """
    Verify a magic link token and return JWT tokens.
    """

    permission_classes = [AllowAny]
    throttle_classes = [AuthThrottle]

    def post(self, request):
        serializer = MagicLinkVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        raw_token = serializer.validated_data["token"]
        token_obj = MagicLinkToken.verify_token(raw_token)

        if not token_obj:
            return Response(
                {"error": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token_obj.mark_used()
        user = token_obj.user
        user.update_last_active()

        tokens = generate_tokens(user)
        return Response(tokens, status=status.HTTP_200_OK)


class RefreshTokenView(APIView):
    """
    Refresh an access token using a refresh token.
    """

    permission_classes = [AllowAny]
    throttle_classes = [AuthThrottle]

    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data["refresh_token"]
        tokens = refresh_access_token(refresh_token)
        return Response(tokens, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    Logout (client-side token invalidation).
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response(
            {"message": "Logged out successfully"}, status=status.HTTP_200_OK
        )


class DevLoginView(APIView):
    """
    Development-only login endpoint that bypasses email verification.
    Only available when DEBUG=True.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        from django.conf import settings

        if not settings.DEBUG:
            return Response(
                {"error": "Dev login only available in debug mode"},
                status=status.HTTP_403_FORBIDDEN,
            )

        email = request.data.get("email", "dev@homelab.local")
        user, created = User.objects.get_or_create(
            email=email, defaults={"display_name": "Dev User"}
        )
        user.update_last_active()

        tokens = generate_tokens(user)
        return Response(tokens, status=status.HTTP_200_OK)


class ProfileView(APIView):
    """
    Get or update the current user's profile.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserSerializer(request.user).data)

    def delete(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def _validate_external_url(url: str) -> bool:
    """
    Validate a user-supplied URL to prevent SSRF.
    Only permits http/https to non-private, non-loopback hosts.
    """
    import ipaddress
    from urllib.parse import urlparse

    if not url:
        return False
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False
    host = parsed.hostname or ""
    if not host:
        return False
    # Block loopback, link-local, private ranges, and cloud metadata
    blocked_hosts = {"localhost", "169.254.169.254", "metadata.google.internal"}
    if host in blocked_hosts:
        return False
    try:
        addr = ipaddress.ip_address(host)
        if (
            addr.is_loopback
            or addr.is_private
            or addr.is_link_local
            or addr.is_reserved
        ):
            return False
    except ValueError:
        pass  # host is a domain name, not an IP
    return True


class TestAIConnectionView(APIView):
    """
    Test the user's AI provider connection.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        import httpx

        provider = request.data.get("provider", "openai")
        api_key = request.data.get("api_key", "")
        request.data.get("model", "")
        base_url = request.data.get("base_url", "")

        if not api_key and provider not in ["none", "ollama"]:
            return Response(
                {"success": False, "error": "API key is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Test connection based on provider
            if provider == "openai":
                url = "https://api.openai.com/v1/models"
                headers = {"Authorization": f"Bearer {api_key}"}
                response = httpx.get(url, headers=headers, timeout=10)

            elif provider == "anthropic":
                url = "https://api.anthropic.com/v1/messages"
                headers = {
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                }
                # Just check if we can reach the API (will get 400 for empty body, but that's OK)
                response = httpx.post(url, headers=headers, json={}, timeout=10)
                # 400 means API key is valid but request is malformed (expected)
                if response.status_code == 400:
                    return Response(
                        {
                            "success": True,
                            "message": "Anthropic API connection successful",
                            "status_code": 200,
                        }
                    )

            elif provider == "openrouter":
                url = "https://openrouter.ai/api/v1/models"
                headers = {"Authorization": f"Bearer {api_key}"}
                response = httpx.get(url, headers=headers, timeout=10)

            elif provider == "ollama":
                ollama_url = base_url or settings.OLLAMA_BASE_URL
                if base_url and not _validate_external_url(base_url):
                    return Response(
                        {"success": False, "error": "Invalid or disallowed base URL"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                response = httpx.get(f"{ollama_url}/api/tags", timeout=10)

            elif provider == "custom":
                if not base_url:
                    return Response(
                        {
                            "success": False,
                            "error": "Base URL is required for custom provider",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if not _validate_external_url(base_url):
                    return Response(
                        {"success": False, "error": "Invalid or disallowed base URL"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                url = f'{base_url.rstrip("/")}/models'
                headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
                response = httpx.get(url, headers=headers, timeout=10)

            else:
                return Response(
                    {"success": False, "error": "Unknown provider"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if response.status_code == 200:
                return Response(
                    {
                        "success": True,
                        "message": f"{provider.title()} API connection successful",
                        "status_code": response.status_code,
                    }
                )
            else:
                return Response(
                    {
                        "success": False,
                        "error": f"API returned status {response.status_code}",
                        "status_code": response.status_code,
                    }
                )

        except httpx.TimeoutException:
            return Response(
                {"success": False, "error": "Connection timed out"},
                status=status.HTTP_408_REQUEST_TIMEOUT,
            )
        except httpx.ConnectError as e:
            return Response(
                {"success": False, "error": f"Connection failed: {str(e)}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except Exception as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GoogleOAuthInitView(APIView):
    """
    Initiate Google OAuth flow by redirecting to Google's authorization page.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        # Generate state token for CSRF protection
        state = secrets.token_urlsafe(32)
        request.session["google_oauth_state"] = state

        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "online",
            "state": state,
            "prompt": "select_account",
        }

        google_auth_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
        )
        return redirect(google_auth_url)


class GoogleOAuthCallbackView(APIView):
    """
    Handle Google OAuth callback and exchange code for tokens.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        code = request.query_params.get("code")
        state = request.query_params.get("state")
        error = request.query_params.get("error")

        frontend_url = settings.FRONTEND_URL

        # Handle errors from Google
        if error:
            logger.error(f"Google OAuth error: {error}")
            return redirect(f"{frontend_url}/login?error=google_auth_failed")

        if not code:
            return redirect(f"{frontend_url}/login?error=no_code")

        # Verify state (CSRF protection)
        stored_state = request.session.get("google_oauth_state")
        if state != stored_state:
            logger.warning("Google OAuth state mismatch")
            return redirect(f"{frontend_url}/login?error=invalid_state")

        try:
            # Exchange code for tokens
            token_response = httpx.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                },
                timeout=10,
            )

            if token_response.status_code != 200:
                logger.error(
                    "Google token exchange failed: status=%s",
                    token_response.status_code,
                )
                return redirect(f"{frontend_url}/login?error=token_exchange_failed")

            token_data = token_response.json()
            access_token = token_data.get("access_token")

            # Get user info from Google
            userinfo_response = httpx.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10,
            )

            if userinfo_response.status_code != 200:
                logger.error(
                    "Google userinfo failed: status=%s", userinfo_response.status_code
                )
                return redirect(f"{frontend_url}/login?error=userinfo_failed")

            userinfo = userinfo_response.json()
            email = userinfo.get("email")
            name = userinfo.get("name", "")
            userinfo.get("picture", "")

            if not email:
                return redirect(f"{frontend_url}/login?error=no_email")

            # Get or create user
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "display_name": name,
                },
            )

            # Update display name if user exists but has no name
            if not created and not user.display_name and name:
                user.display_name = name
                user.save(update_fields=["display_name"])

            user.update_last_active()

            # Generate JWT tokens
            tokens = generate_tokens(user)

            # Store tokens server-side under a short-lived one-time code.
            # The frontend redeems this code via POST /auth/exchange/ so that
            # tokens never appear in URLs, browser history, or server logs.
            one_time_code = secrets.token_urlsafe(32)
            request.session[f"oauth_code_{one_time_code}"] = {
                "access_token": tokens["access_token"],
                "refresh_token": tokens["refresh_token"],
                "new_user": created,
            }
            request.session.set_expiry(300)  # 5-minute window to redeem

            params = urlencode({"code": one_time_code})
            return redirect(f"{frontend_url}/auth/callback?{params}")

        except httpx.TimeoutException:
            logger.error("Google OAuth timeout")
            return redirect(f"{frontend_url}/login?error=timeout")
        except Exception as e:
            logger.error(f"Google OAuth error: {e}")
            return redirect(f"{frontend_url}/login?error=server_error")


class OAuthTokenExchangeView(APIView):
    """
    Redeem a one-time OAuth callback code for JWT tokens.
    The code is consumed on first use and expires after 5 minutes.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        code = request.data.get("code")
        if not code:
            return Response(
                {"error": "code is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        session_key = f"oauth_code_{code}"
        token_data = request.session.pop(session_key, None)

        if not token_data:
            return Response(
                {"error": "Invalid or expired code"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "access_token": token_data["access_token"],
                "refresh_token": token_data["refresh_token"],
                "new_user": token_data["new_user"],
            },
            status=status.HTTP_200_OK,
        )


class GoogleOAuthTokenView(APIView):
    """
    Alternative: Exchange Google ID token directly for JWT tokens.
    Used for frontend Google Sign-In button integration.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        id_token = request.data.get("id_token")

        if not id_token:
            return Response(
                {"error": "id_token is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Verify the ID token with Google
            response = httpx.get(
                f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}",
                timeout=10,
            )

            if response.status_code != 200:
                return Response(
                    {"error": "Invalid ID token"}, status=status.HTTP_401_UNAUTHORIZED
                )

            token_info = response.json()

            # Verify the token is for our app
            if token_info.get("aud") != settings.GOOGLE_CLIENT_ID:
                return Response(
                    {"error": "Token not issued for this application"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            email = token_info.get("email")
            name = token_info.get("name", "")

            if not email:
                return Response(
                    {"error": "Email not provided by Google"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Get or create user
            user, created = User.objects.get_or_create(
                email=email, defaults={"display_name": name}
            )

            if not created and not user.display_name and name:
                user.display_name = name
                user.save(update_fields=["display_name"])

            user.update_last_active()

            # Generate JWT tokens
            tokens = generate_tokens(user)
            tokens["new_user"] = created

            return Response(tokens, status=status.HTTP_200_OK)

        except httpx.TimeoutException:
            return Response(
                {"error": "Google verification timed out"},
                status=status.HTTP_408_REQUEST_TIMEOUT,
            )
        except Exception as e:
            logger.error(f"Google token verification error: {e}")
            return Response(
                {"error": "Authentication failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
