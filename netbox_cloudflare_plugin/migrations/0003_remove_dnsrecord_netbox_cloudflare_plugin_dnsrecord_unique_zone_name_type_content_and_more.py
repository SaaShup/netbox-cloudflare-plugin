# pylint: disable=C0103
"""Migration file"""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        ("netbox_cloudflare_plugin", "0002_alter_dnsrecord_record_id"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="dnsrecord",
            name="netbox_cloudflare_plugin_dnsrecord_unique_zone_name_type_content",
        ),
        migrations.AddConstraint(
            model_name="dnsrecord",
            constraint=models.UniqueConstraint(
                fields=("zone", "name", "type", "content"),
                name="netbox_cloudflare_plugin_dnsrecord_unique_zone_name_type_content",
            ),
        ),
        migrations.AddConstraint(
            model_name="dnsrecord",
            constraint=models.UniqueConstraint(
                condition=models.Q(("proxied", True)),
                fields=("zone", "name", "type"),
                name="netbox_cloudflare_plugin_dnsrecord_unique_zone_name_type",
            ),
        ),
    ]
