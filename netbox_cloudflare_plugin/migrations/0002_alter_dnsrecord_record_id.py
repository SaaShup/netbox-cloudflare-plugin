# pylint: disable=C0103
"""Migration file"""

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration file"""

    dependencies = [
        ("netbox_cloudflare_plugin", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dnsrecord",
            name="record_id",
            field=models.CharField(
                blank=True,
                max_length=32,
                null=True,
                validators=[
                    django.core.validators.MinLengthValidator(limit_value=1),
                    django.core.validators.MaxLengthValidator(limit_value=32),
                ],
            ),
        ),
    ]
