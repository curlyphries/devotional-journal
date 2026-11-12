"""
Restrict the whole site to a private mesh network (e.g. a Tailscale tailnet).

This is the second lock, not the first. The first is network-level: publish
the service only on the mesh interface (see docs/MESH_DEPLOYMENT.md). This
middleware makes sure that, if a port is ever exposed by mistake, requests
from outside the mesh are still refused.
"""

import ipaddress
import logging

from django.conf import settings
from django.http import JsonResponse

logger = logging.getLogger(__name__)


def _networks(cidrs):
    networks = []
    for cidr in cidrs:
        try:
            networks.append(ipaddress.ip_network(cidr, strict=False))
        except ValueError:
            logger.error("Ignoring invalid CIDR in mesh settings: %r", cidr)
    return networks


def _in(ip, networks) -> bool:
    try:
        addr = ipaddress.ip_address((ip or "").strip())
    except ValueError:
        return False
    # ::ffff:100.64.0.1 -> 100.64.0.1
    mapped = getattr(addr, "ipv4_mapped", None)
    if mapped:
        addr = mapped
    return any(
        addr in network for network in networks if network.version == addr.version
    )


class MeshOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.enabled = getattr(settings, "MESH_ONLY", False)
        self.allowed = _networks(getattr(settings, "MESH_ALLOWED_CIDRS", []))
        self.trusted_proxies = _networks(
            getattr(settings, "MESH_TRUSTED_PROXY_CIDRS", [])
        )

    def __call__(self, request):
        # The health probe returns booleans only and is called from the host.
        if self.enabled and not request.path.endswith("/api/v1/health/"):
            client_ip = self.get_client_ip(request)
            if not _in(client_ip, self.allowed):
                logger.warning("Refused request from outside the mesh: %s", client_ip)
                return JsonResponse(
                    {
                        "error": "This journal is only available on the private network.",
                        "code": "MESH_ONLY",
                        "suggestion": "Connect to the mesh (VPN) and try again.",
                    },
                    status=403,
                )
        return self.get_response(request)

    def get_client_ip(self, request) -> str:
        """
        The address of the real client.

        The TCP peer (REMOTE_ADDR) is authoritative. Only when that peer is
        one of our own reverse proxies do we believe the X-Real-IP it set -
        a header sent by an arbitrary client is never trusted.
        """
        peer = request.META.get("REMOTE_ADDR", "")
        if _in(peer, self.trusted_proxies):
            forwarded = request.META.get("HTTP_X_REAL_IP", "")
            if forwarded:
                return forwarded
        return peer


# Backwards-compatible name.
TailscaleOnlyMiddleware = MeshOnlyMiddleware
