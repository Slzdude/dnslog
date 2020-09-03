from django.conf import settings
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter, SimpleRouter

from dnslog.users.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)

app_name = "dnslog"
urlpatterns = router.urls + [
    # allauth api user
    path("", include("rest_auth.urls")),
    path("", include("rest_auth.registration.urls")),
    # DRF auth token
    path("token/", obtain_auth_token),
]
