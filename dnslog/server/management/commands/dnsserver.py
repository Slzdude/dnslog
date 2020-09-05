from django.conf import settings
from django.core.management.base import BaseCommand
from dnslib.server import DNSServer

from dnslog.server.dns_logger import DjangoDNSLogger
from dnslog.server.resolver import ZoneResolver


class Command(BaseCommand):
    help = "Run the dns log server"

    def handle(self, *args, **options):
        zone = """
*.{dnsdomain}.       IN      NS      {ns1domain}.
*.{dnsdomain}.       IN      NS      {ns2domain}.
*.{dnsdomain}.       IN      A       {serverip}
{dnsdomain}.       IN      A       {serverip}
""".format(
            dnsdomain=settings.DNS_DOMAIN,
            ns1domain=settings.NS1_DOMAIN,
            ns2domain=settings.NS2_DOMAIN,
            serverip=settings.SERVER_IP,
        )
        print("Starting Zone Resolver (%s:%d) [%s]" % ("*", 53, "UDP"))

        udp_server = DNSServer(
            ZoneResolver(zone, True), port=53, address="", logger=DjangoDNSLogger()
        )
        udp_server.start()
