""" Hooks on Django model signals. """

from django.conf import settings
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from utilities.exceptions import AbortRequest
from .models import ZoneAccount, DnsRecord
from .utilities.cloudflare_dns_client import CloudflareDnsClient


@receiver(post_save, sender=ZoneAccount)
def init_zoneaccount(instance, **_kwargs):
    """Init Zone Account by creating all dns record compatible"""

    if _kwargs.get("created") is True:
        client = CloudflareDnsClient(
            instance,
            settings.PLUGINS_CONFIG["netbox_cloudflare_plugin"]["cloudflare_base_url"],
        )

        page = 1

        while True:
            result = client.get_dns_records(page=page)
            DnsRecord.objects.bulk_create(result["records"])

            if page == result["result_info"]["total_pages"]:
                break

            page = page + 1


@receiver(pre_save, sender=DnsRecord)
def create_dnsrecord(instance, **_kwargs):
    """Create a DNS Record on Cloudflare"""

    if instance.pk is None:
        if not instance.name.endswith("." + instance.zone.zone_name):
            instance.name = instance.name + "." + instance.zone.zone_name

        if DnsRecord.objects.filter(
            zone_id=instance.zone_id,
            name=instance.name,
            type=instance.type,
            proxied=(not instance.proxied),
        ).exists():
            raise AbortRequest("Unable to create DNS Record on Cloudflare")

        client = CloudflareDnsClient(
            instance.zone,
            settings.PLUGINS_CONFIG["netbox_cloudflare_plugin"]["cloudflare_base_url"],
        )

        try:
            instance = client.create_dns_record(instance)
        except Exception as e:
            raise AbortRequest("Unable to create DNS Record on Cloudflare") from e


@receiver(pre_delete, sender=DnsRecord)
def delete_dnsrecord(instance, **_kwargs):
    """Delete a DNS Record on Cloudflare"""

    if instance.is_deleted_manually is True:
        client = CloudflareDnsClient(
            instance.zone,
            settings.PLUGINS_CONFIG["netbox_cloudflare_plugin"]["cloudflare_base_url"],
        )

        try:
            client.delete_dnsrecord(instance)
        except Exception as e:
            raise AbortRequest("Unable to delete DNS Record on Cloudflare") from e
