from django_hosts import host, patterns

host_patterns = patterns(
    "",
    host(r"admin", "config.admin_router", name="admin"),
    host(r"api", "config.api_router", name="api"),
    host(r"\S+", "config.default_router", name="default"),
)
