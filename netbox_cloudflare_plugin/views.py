"""View definitions"""

from utilities.query import count_related
from netbox.views import generic
from .models import ZoneAccount, DnsRecord
from .tables import ZoneAccountTable, DnsRecordTable
from .forms import ZoneAccountForm, DnsRecordFilterForm, DnsRecordForm
from .filtersets import DnsRecordFilterSet


class ZoneAccountListView(generic.ObjectListView):
    """ZoneAccount list view definition"""

    queryset = ZoneAccount.objects.annotate(
        dnsrecord_count=count_related(DnsRecord, "zone")
    )
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


class ZoneAccountAddView(generic.ObjectEditView):
    """ZoneAccount edition view definition"""

    queryset = ZoneAccount.objects.all()
    form = ZoneAccountForm


class ZoneAccountBulkDeleteView(generic.BulkDeleteView):
    """ZoneAccount bulk delete view definition"""

    queryset = ZoneAccount.objects.all()
    table = ZoneAccountTable


class ZoneAccountDeleteView(generic.ObjectDeleteView):
    """ZoneAccount delete view definition"""

    default_return_url = "plugins:netbox_cloudflare_plugin:zoneaccount_list"
    queryset = ZoneAccount.objects.all()


class DnsRecordListView(generic.ObjectListView):
    """DnsRecord list view definition"""

    queryset = DnsRecord.objects.all()
    table = DnsRecordTable
    filterset = DnsRecordFilterSet
    filterset_form = DnsRecordFilterForm


class DnsRecordView(generic.ObjectView):
    """DnsRecord view definition"""

    queryset = DnsRecord.objects.all()


class DnsRecordAddView(generic.ObjectEditView):
    """DnsRecord edition view definition"""

    queryset = DnsRecord.objects.all()
    form = DnsRecordForm


class DnsRecordBulkDeleteView(generic.BulkDeleteView):
    """ZoneAccount bulk delete view definition"""

    queryset = DnsRecord.objects.all()
    table = DnsRecordTable
    filterset = DnsRecordFilterSet


class DnsRecordDeleteView(generic.ObjectDeleteView):
    """ZoneAccount delete view definition"""

    default_return_url = "plugins:netbox_cloudflare_plugin:dnsrecord_list"
    queryset = DnsRecord.objects.all()
