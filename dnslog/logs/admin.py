from django.contrib import admin

from dnslog.logs.models import DnsLog, WebLog


@admin.register(WebLog)
class WebLogAdmin(admin.ModelAdmin):
    list_display = ["id", "ip", "path", "log_time"]

    def get_queryset(self, request):
        qs = super(WebLogAdmin, self).get_queryset(request)
        if request.user:
            return qs.filter(user=request.user)
        else:
            return qs


@admin.register(DnsLog)
class DnsLogAdmin(admin.ModelAdmin):
    list_display = ["id", "host", "type", "client_ip", "log_time"]
