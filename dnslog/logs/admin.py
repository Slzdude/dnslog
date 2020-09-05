from django.contrib import admin

from dnslog.logs.models import DnsLog, WebLog


@admin.register(WebLog)
class WebLogAdmin(admin.ModelAdmin):
    list_display = ["id", "ip", "method", "host", "path", "log_time"]
    readonly_fields = ["method", "user", "host", "ip", "path", "log_time"]
    save_as = False
    save_as_continue = False
    search_fields = ["ip", "path"]
    list_filter = ["method", "host", "ip", "path"]

    def get_queryset(self, request):
        qs = super(WebLogAdmin, self).get_queryset(request)
        if request.user:
            return qs.filter(user=request.user)
        else:
            return qs


@admin.register(DnsLog)
class DnsLogAdmin(admin.ModelAdmin):
    list_display = ["id", "host", "type", "client_ip", "log_time"]
    readonly_fields = ["user", "host", "type", "client_ip", "log_time"]
    save_as = False
    save_as_continue = False
    search_fields = ["host", "client_ip"]
    list_filter = ("host", "client_ip")

    def get_queryset(self, request):
        qs = super(DnsLogAdmin, self).get_queryset(request)
        if request.user:
            return qs.filter(user=request.user)
        else:
            return qs
