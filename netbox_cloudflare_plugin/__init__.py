"""Netbox Plugin Configuration"""

from netbox.plugins import PluginConfig

class NetBoxCloudflareConfig(PluginConfig):
    """Plugin Config Class"""

    name = "netbox_cloudflare_plugin"
    verbose_name = " NetBox Cloudflare Plugin"
    description = "Manage Cloudflare"
    version = "0.1.0"
    base_url = "cloudflare"
    min_version = "4.0.0"
    author= "Vincent Simonin <vincent@saashup.com>"
    author_email= "vincent@saashup.com"
    default_settings = {
        'cloudflare_base_url': 'https://api.cloudflare.com/client/v4',
    }


# pylint: disable=C0103
config = NetBoxCloudflareConfig
