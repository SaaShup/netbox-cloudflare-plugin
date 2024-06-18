###################################################################
#  This file serves as a base configuration for testing purposes  #
#  only. It is not intended for production use.                   #
###################################################################

ALLOWED_HOSTS = ["*"]

DATABASE = {
    "NAME": "netbox",
    "USER": "netbox",
    "PASSWORD": "netbox",
    "HOST": "localhost",
    "PORT": "",
    "CONN_MAX_AGE": 300,
}

PLUGINS = [
    "netbox_cloudflare_plugin",
]

PLUGINS_CONFIG = {
    "netbox_cloudflare_plugin": {"cloudflare_base_url": "http://localhost:1080"}
}

REDIS = {
    "tasks": {
        "HOST": "localhost",
        "PORT": 6379,
        "USERNAME": "",
        "PASSWORD": "",
        "DATABASE": 0,
        "SSL": False,
    },
    "caching": {
        "HOST": "localhost",
        "PORT": 6379,
        "USERNAME": "",
        "PASSWORD": "",
        "DATABASE": 1,
        "SSL": False,
    },
}

SECRET_KEY = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

DJANGO_ADMIN_ENABLED = True

DEFAULT_PERMISSIONS = {}

LOGGING = {"version": 1, "disable_existing_loggers": True}
