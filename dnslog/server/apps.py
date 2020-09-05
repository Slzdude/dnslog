from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ServerConfig(AppConfig):
    name = "dnslog.server"
    verbose_name = _("DNSServer")
