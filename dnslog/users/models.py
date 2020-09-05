from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for dnslog-server."""

    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None
    last_name = None


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    subdomain = models.CharField(db_index=True, max_length=128)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.subdomain + "." + settings.DNS_DOMAIN
