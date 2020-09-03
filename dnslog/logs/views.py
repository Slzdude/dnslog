from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from dnslog.logs.models import WebLog

User = get_user_model()


class WebLogViewSet(ModelViewSet):
    queryset = WebLog.objects.all()
