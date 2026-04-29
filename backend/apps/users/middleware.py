"""
Middleware for Tailscale-only access restriction.
"""
from django.http import HttpResponseForbidden
from django.conf import settings


class TailscaleOnlyMiddleware:
    """
    Restrict access to Tailscale IP ranges only.
    Tailscale uses 100.64.0.0/10 (CGNAT range).
    """
    
    TAILSCALE_RANGES = [
        '100.',  # 100.64.0.0/10 - Tailscale CGNAT range
        '127.0.0.1',  # localhost for development
        '::1',  # IPv6 localhost
        '172.',  # Docker internal networks
        '192.168.',  # Local networks (for dev)
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.enabled = getattr(settings, 'TAILSCALE_ONLY', False)
    
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
        """Get the real client IP, handling proxies."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        
        x_real_ip = request.META.get('HTTP_X_REAL_IP')
        if x_real_ip:
            return x_real_ip
        
        return request.META.get('REMOTE_ADDR', '')
    
    def is_allowed_ip(self, ip):
        """Check if IP is in allowed Tailscale/local ranges."""
        if not ip:
            return False
        
        for prefix in self.TAILSCALE_RANGES:
            if ip.startswith(prefix):
                return True
        
        return False
