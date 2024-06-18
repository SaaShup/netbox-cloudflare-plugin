"""URL definitions"""

from django.urls import path
from netbox.views.generic import ObjectChangeLogView
from . import models, views


urlpatterns = (
    # ZoneAccount
    path(
        "dns/accounts/",
        views.ZoneAccountListView.as_view(),
        name="zoneaccount_list",
    ),
    path(
        "dns/accounts/add/",
        views.ZoneAccountAddView.as_view(),
        name="zoneaccount_add",
    ),
    path(
        "dns/accounts/delete/",
        views.ZoneAccountBulkDeleteView.as_view(),
        name="zoneaccount_bulk_delete",
    ),
    path(
        "dns/accounts/<int:pk>/",
        views.ZoneAccountView.as_view(),
        name="zoneaccount",
    ),
    path(
        "dns/accounts/<int:pk>/delete/",
        views.ZoneAccountDeleteView.as_view(),
        name="zoneaccount_delete",
    ),
    path(
        "dns/accounts/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="zoneaccount_changelog",
        kwargs={"model": models.ZoneAccount},
    ),
    # DnsRecord
    path(
        "dns/records/",
        views.DnsRecordListView.as_view(),
        name="dnsrecord_list",
    ),
    path(
        "dns/records/add/",
        views.DnsRecordAddView.as_view(),
        name="dnsrecord_add",
    ),
    path(
        "dns/records/delete/",
        views.DnsRecordBulkDeleteView.as_view(),
        name="dnsrecord_bulk_delete",
    ),
    path(
        "dns/records/<int:pk>/",
        views.DnsRecordView.as_view(),
        name="dnsrecord",
    ),
    path(
        "dns/records/<int:pk>/delete/",
        views.DnsRecordDeleteView.as_view(),
        name="dnsrecord_delete",
    ),
    path(
        "dns/records/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="dnsrecord_changelog",
        kwargs={"model": models.DnsRecord},
    ),
)
