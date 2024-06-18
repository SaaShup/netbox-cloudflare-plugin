"""Filtersets definitions"""

from django.db.models import Q
from django_filters import ModelMultipleChoiceFilter
from netbox.filtersets import NetBoxModelFilterSet
from .models import ZoneAccount, DnsRecord


class DnsRecordFilterSet(NetBoxModelFilterSet):
    """DnsRecord filterset definition class"""

    zone_id = ModelMultipleChoiceFilter(
        field_name="zone_id",
        queryset=ZoneAccount.objects.all(),
        label="Account (ID)",
    )

    class Meta:
        """DnsRecord filterset definition meta class"""

        model = DnsRecord
        fields = ("id", "type")

    def search(self, queryset, name, value):
        """override"""
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value))
