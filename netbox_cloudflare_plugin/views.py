"""View definitions"""

from netbox.views import generic
from .models import ZoneAccount, DnsRecord
from .tables import ZoneAccountTable
from .forms import ZoneAccountForm


class ZoneAccountListView(generic.ObjectListView):
    """ZoneAccount list view definition"""

    queryset = ZoneAccount.objects.all()
    table = ZoneAccountTable


class ZoneAccountView(generic.ObjectView):
    """ZoneAccount view definition"""

    queryset = ZoneAccount.objects.prefetch_related("records")

    def get_extra_context(self, request, instance):
        related_models = (
            (
                DnsRecord.objects.filter(zone=instance),
                "host_id",
            ),
        )

        return {
            "related_models": related_models,
        }


class ZoneAccountEditView(generic.ObjectEditView):
    """ZoneAccount edition view definition"""

    queryset = ZoneAccount.objects.all()
    form = ZoneAccountForm


class ZoneAccountBulkDeleteView(generic.BulkDeleteView):
    """ZoneAccount bulk delete view definition"""


class ZoneAccountDeleteView(generic.ObjectDeleteView):
    """ZoneAccount delete view definition"""
