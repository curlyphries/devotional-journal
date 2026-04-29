"""
URL routes for authentication endpoints.
"""
from django.urls import path

from django.conf import settings

from .views import (
    MagicLinkRequestView,
    MagicLinkVerifyView,
    RefreshTokenView,
    LogoutView,
    DevLoginView,
    TestAIConnectionView,
    GoogleOAuthInitView,
    GoogleOAuthCallbackView,
    OAuthTokenExchangeView,
    GoogleOAuthTokenView,
    ProfileView,
)

urlpatterns = [
    path('magic-link/request/', MagicLinkRequestView.as_view(), name='magic-link-request'),
    path('magic-link/verify/', MagicLinkVerifyView.as_view(), name='magic-link-verify'),
    path('refresh/', RefreshTokenView.as_view(), name='token-refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('test-ai/', TestAIConnectionView.as_view(), name='test-ai'),
    path('profile/', ProfileView.as_view(), name='profile'),
    # Google OAuth
    path('google/login/', GoogleOAuthInitView.as_view(), name='google-login'),
    path('google/callback/', GoogleOAuthCallbackView.as_view(), name='google-callback'),
    path('google/exchange/', OAuthTokenExchangeView.as_view(), name='oauth-token-exchange'),
    path('google/token/', GoogleOAuthTokenView.as_view(), name='google-token'),
]

if settings.DEBUG:
    urlpatterns += [
        path('dev-login/', DevLoginView.as_view(), name='dev-login'),
    ]
