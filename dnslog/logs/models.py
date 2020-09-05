from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class WebLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField("remote_addr", help_text="客户端地址")
    method = models.CharField(max_length=16, help_text="请求方法")
    host = models.CharField(max_length=300, help_text="请求域名")
    path = models.TextField("path", help_text="请求路径")
    header = models.TextField("header", help_text="请求头")
    body = models.TextField(blank=True, help_text="请求体")
    log_time = models.DateTimeField(auto_now_add=True, help_text="记录时间")

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
