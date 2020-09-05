import random
import string

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db.models import signals
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from dnslog.users.models import UserProfile

User = get_user_model()


@receiver(signals.post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if not created:
        return
    if not instance.is_superuser:
        instance.is_staff = True
    group = Group.objects.filter(name="普通用户").first()
    if not group:
        group = Group.objects.create(name="普通用户")
        group.save()
        group.permissions.set(Permission.objects.filter(codename__iendswith="log"))
    instance.groups.add(group)
    instance.save()
    subdomain = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    UserProfile(
        user=instance,
        subdomain=subdomain,
    ).save()
    token = Token.objects.create(user=instance)
    print("Create user: ", instance.username, subdomain, token.key)
