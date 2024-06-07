"""Forms definitions"""

from netbox.forms import NetBoxModelForm
from .models import ZoneAccount


class ZoneAccountForm(NetBoxModelForm):
    """ZoneAccount form definition class"""

    class Meta:
        """ZoneAccount form definition Meta class"""

        model = ZoneAccount
        fields = (
            "zone_name",
            "zone_id",
            "token",
            "tags",
        )
