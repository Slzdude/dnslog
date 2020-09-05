import json

from django.conf import settings
from django.conf.urls import url
from django.http import HttpResponse

from dnslog.logs.models import WebLog
from dnslog.users.models import UserProfile


def index(request):
    host = request.get_host()
    if ":" in host:
        host = host.split(":")[0]
    domains = host.replace(settings.DNS_DOMAIN, "").split(".")
    if len(domains) < 2:
        return HttpResponse("bad boy")
    profile = UserProfile.objects.filter(subdomain=domains[-2]).first()
    if not profile:
        return HttpResponse("bad boy")
    WebLog.objects.create(
        user=profile.user,
        ip=request.META.get("REMOTE_ADDR"),
        method=request.method,
        path=request.get_full_path(),
        header=json.dumps(dict(request.headers), indent=2),
        body=request.body,
    )
    return HttpResponse(host)


urlpatterns = [url("", index)]
