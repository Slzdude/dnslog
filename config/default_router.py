from django.conf import settings
from django.conf.urls import url
from django.http import HttpResponse

from dnslog.logs.models import WebLog
from dnslog.users.models import UserProfile


def index(request):
    host = request.get_host()
    if ":" in host:
        host = host.split(":")[0]

    headers = ""
    for header, value in request.META.items():
        if not header.startswith("HTTP"):
            continue
        header = "-".join([h.capitalize() for h in header[5:].lower().split("_")])
        headers += "{}: {}\n".format(header, value)
    path = request.get_full_path()
    body = request.body or " "
    realip = request.META.get("HTTP_X_REAL_IP") or request.META.get("REMOTE_ADDR")
    subdomain = host.replace(settings.DNS_DOMAIN, "")
    if not subdomain:
        return HttpResponse("bad boy")
    domains = subdomain.split(".")
    if len(domains) < 2:
        return HttpResponse("bad boy")
    # usersubdomain = domains[-2]
    user_profile = UserProfile.objects.filter(subdomain=domains[-2]).first()
    if not user_profile:
        return HttpResponse("bad boy")
    weblog = WebLog(
        user=user_profile.user,
        ip=realip,
        path=path,
        header=headers,
        body=body,
    )
    weblog.save()
    return HttpResponse("good boy")


urlpatterns = [url("", index)]
