import random
import string

from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        user = super(CustomUserManager, self)._create_user(
            username, email, password, **extra_fields
        )
        UserProfile(
            user=user,
            subdomain="".join(
                random.choices(string.ascii_lowercase + string.digits, k=8)
            ),
        ).save()
        Token.objects.get_or_create(user=user)
        return user


class User(AbstractUser):
    """Default user for dnslog-server."""

    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None
    last_name = None
    objects = CustomUserManager()


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    subdomain = models.CharField(max_length=128)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.subdomain + "." + settings.DNS_DOMAIN
