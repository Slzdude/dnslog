from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class WebLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField("remote_addr")
    path = models.TextField("path")
    header = models.TextField("header")
    body = models.TextField("body")
    log_time = models.DateTimeField("time loged", auto_now_add=True)

    class Meta:
        ordering = ["-id"]


class DnsLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    host = models.TextField("host")
    type = models.TextField("dns type")
    client_ip = models.TextField(max_length=256, blank=True, help_text="客户端IP")
    log_time = models.DateTimeField("time loged", auto_now_add=True)

    class Meta:
        ordering = ["-id"]
