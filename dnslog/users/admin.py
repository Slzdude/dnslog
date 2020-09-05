from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from dnslog.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = list(
        {
            _("User"): {"fields": ("name", "email")},
            None: {"fields": ("username", "password")},
            _("Permissions"): {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
            _("Important dates"): {"fields": ("last_login", "date_joined")},
        }.items()
    )
    list_display = ["username", "profile", "is_superuser", "auth_token"]
    search_fields = ["name", "email"]
