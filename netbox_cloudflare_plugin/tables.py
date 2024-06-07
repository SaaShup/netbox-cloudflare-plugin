"""Tables definitions"""

import django_tables2 as tables
from netbox.tables import NetBoxTable, columns
from .models import ZoneAccount


class ZoneAccountTable(NetBoxTable):
    """ZoneAccount Table definition class"""

    zone_name = tables.Column(linkify=True)
    tags = columns.TagColumn()

    class Meta(NetBoxTable.Meta):
        """ZoneAccount Table definition Meta class"""

        model = ZoneAccount
        fields = (
            "pk",
            "id",
            "zone_name",
            "zone_id",
            "token",
            "tags",
        )
        default_columns = ("zone_name",)
