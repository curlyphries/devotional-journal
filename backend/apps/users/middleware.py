"""
Middleware for Tailscale-only access restriction.
"""

from django.conf import settings
from django.http import HttpResponseForbidden


class TailscaleOnlyMiddleware:
    """
    Restrict access to Tailscale IP ranges only.
    Tailscale uses 100.64.0.0/10 (CGNAT range).
    """

    TAILSCALE_RANGES = [
        "100.",  # 100.64.0.0/10 - Tailscale CGNAT range
        "127.0.0.1",  # localhost for development
        "::1",  # IPv6 localhost
        "172.",  # Docker internal networks
        "192.168.",  # Local networks (for dev)
    ]

    def __init__(self, get_response):
        self.get_response = get_response
        self.enabled = getattr(settings, "TAILSCALE_ONLY", False)

    def __call__(self, request):
        if self.enabled:
            client_ip = self.get_client_ip(request)
            if not self.is_allowed_ip(client_ip):
                return HttpResponseForbidden(
                    f"Access denied. This service is only accessible via Tailscale. "
                    f"Your IP: {client_ip}"
                )

        return self.get_response(request)

    def get_client_ip(self, request):
        """
        Return the actual TCP connection IP (REMOTE_ADDR).
        X-Forwarded-For is intentionally ignored here because it can be
        trivially spoofed by any client, defeating the Tailscale IP check.
        If this service runs behind a trusted reverse proxy, configure
        Django's SECURE_PROXY_SSL_HEADER and NUM_PROXIES instead.
        """
        return request.META.get("REMOTE_ADDR", "")

    def is_allowed_ip(self, ip):
        """Check if IP is in allowed Tailscale/local ranges."""
        if not ip:
            return False

        for prefix in self.TAILSCALE_RANGES:
            if ip.startswith(prefix):
                return True

        return False
