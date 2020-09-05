import re

from django.conf import settings
from dnslib import QTYPE
from dnslib.server import DNSLogger

from dnslog.logs.models import DnsLog
from dnslog.users.models import UserProfile


class DjangoDNSLogger(DNSLogger):
    def log_data(self, dns_obj):
        pass

    def log_error(self, handler, e):
        pass

    def log_pass(self, *args):
        pass

    def log_prefix(self, handler):
        pass

    def log_recv(self, handler, data):
        pass

    def log_reply(self, handler, reply):
        pass

    def log_request(self, handler, request):
        domain = request.q.qname.__str__().lower()
        # self.default_logger.info(domain)
        if not domain.endswith(settings.DNS_DOMAIN + "."):
            return
        subdomain = re.search(r"\.?([^\.]+)\.%s\." % settings.DNS_DOMAIN, domain)
        if not subdomain:
            return
        user = UserProfile.objects.filter(subdomain__iexact=subdomain.group(1))
        if not user and domain.strip(".") != settings.ADMIN_DOMAIN:
            user = UserProfile.objects.filter(subdomain__exact="@")
        if not user:
            return
        print("Resolving", user[0].user.username, domain)
        DnsLog(
            user=user[0].user,
            host=domain,
            type=QTYPE[request.q.qtype],
            client_ip=handler.client_address[0],
        ).save()

    def log_send(self, handler, data):
        pass

    def log_truncated(self, handler, reply):
        pass
