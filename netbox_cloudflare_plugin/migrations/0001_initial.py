# pylint: disable=C0103
"""Migration file"""

import django.core.validators
import django.db.models.deletion
import taggit.managers
import utilities.json
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration file"""

    initial = True

    dependencies = [
        ("extras", "0115_convert_dashboard_widgets"),
    ]

    operations = [
        migrations.CreateModel(
            name="ZoneAccount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder,
                    ),
                ),
                (
                    "zone_name",
                    models.CharField(
                        max_length=255,
                        unique=True,
                        validators=[
                            django.core.validators.MinLengthValidator(limit_value=1),
                            django.core.validators.MaxLengthValidator(limit_value=255),
                        ],
                    ),
                ),
                (
                    "zone_id",
                    models.CharField(
                        max_length=255,
                        validators=[
                            django.core.validators.MinLengthValidator(limit_value=1),
                            django.core.validators.MaxLengthValidator(limit_value=255),
                        ],
                    ),
                ),
                (
                    "token",
                    models.CharField(
                        max_length=255,
                        validators=[
                            django.core.validators.MinLengthValidator(limit_value=1),
                            django.core.validators.MaxLengthValidator(limit_value=255),
                        ],
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        through="extras.TaggedItem", to="extras.Tag"
                    ),
                ),
            ],
            options={
                "ordering": ("zone_name",),
            },
        ),
        migrations.CreateModel(
            name="DnsRecord",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder,
                    ),
                ),
                (
                    "record_id",
                    models.CharField(
                        max_length=32,
                        validators=[
                            django.core.validators.MinLengthValidator(limit_value=1),
                            django.core.validators.MaxLengthValidator(limit_value=32),
                        ],
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=255,
                        validators=[
                            django.core.validators.MinLengthValidator(limit_value=1),
                            django.core.validators.MaxLengthValidator(limit_value=255),
                        ],
                    ),
                ),
                ("type", models.CharField(default="CNAME", max_length=64)),
                (
                    "content",
                    models.CharField(
                        max_length=255,
                        validators=[
                            django.core.validators.MinLengthValidator(limit_value=1),
                            django.core.validators.MaxLengthValidator(limit_value=255),
                        ],
                    ),
                ),
                (
                    "ttl",
                    models.IntegerField(
                        default=3600,
                        validators=[
                            django.core.validators.MinValueValidator(limit_value=60),
                            django.core.validators.MaxValueValidator(limit_value=86400),
                        ],
                    ),
                ),
                ("proxied", models.BooleanField(default=False)),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        through="extras.TaggedItem", to="extras.Tag"
                    ),
                ),
                (
                    "zone",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="records",
                        to="netbox_cloudflare_plugin.zoneaccount",
                    ),
                ),
            ],
            options={
                "ordering": ("zone", "name", "type"),
            },
        ),
        migrations.AddConstraint(
            model_name="dnsrecord",
            constraint=models.UniqueConstraint(
                fields=("zone", "name"),
                name="netbox_cloudflare_plugin_dnsrecord_unique_zone_name_type_content",
            ),
        ),
    ]
