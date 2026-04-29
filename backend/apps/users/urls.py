"""
URL routes for authentication endpoints.
"""
from django.urls import path

from .views import (
    MagicLinkRequestView,
    MagicLinkVerifyView,
    RefreshTokenView,
    LogoutView,
    DevLoginView,
    TestAIConnectionView,
    GoogleOAuthInitView,
    GoogleOAuthCallbackView,
    GoogleOAuthTokenView,
)

urlpatterns = [
    path('magic-link/request/', MagicLinkRequestView.as_view(), name='magic-link-request'),
    path('magic-link/verify/', MagicLinkVerifyView.as_view(), name='magic-link-verify'),
    path('refresh/', RefreshTokenView.as_view(), name='token-refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dev-login/', DevLoginView.as_view(), name='dev-login'),
    path('test-ai/', TestAIConnectionView.as_view(), name='test-ai'),
    # Google OAuth
    path('google/login/', GoogleOAuthInitView.as_view(), name='google-login'),
    path('google/callback/', GoogleOAuthCallbackView.as_view(), name='google-callback'),
    path('google/token/', GoogleOAuthTokenView.as_view(), name='google-token'),
]
