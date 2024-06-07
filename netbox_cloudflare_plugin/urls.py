"""URL definitions"""

from django.urls import path
from netbox.views.generic import ObjectChangeLogView, ObjectJournalView
from . import models, views


urlpatterns = (
    # ZoneAccount
    path(
        "dns/account",
        views.ZoneAccountListView.as_view(),
        name="zoneaccount_list",
    ),
    path(
        "dns/account/add/",
        views.ZoneAccountEditView.as_view(),
        name="zoneaccount_add",
    ),
    path(
        "dns/account/delete/",
        views.ZoneAccountBulkDeleteView.as_view(),
        name="zoneaccount_bulk_delete",
    ),
    path(
        "dns/account/<int:pk>/",
        views.ZoneAccountView.as_view(),
        name="zoneaccount",
    ),
    path(
        "dns/account/<int:pk>/edit/",
        views.ZoneAccountEditView.as_view(),
        name="zoneaccount_edit",
    ),
    path(
        "dns/account/<int:pk>/delete/",
        views.ZoneAccountDeleteView.as_view(),
        name="zoneaccount_delete",
    ),
    path(
        "dns/account/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="zoneaccount_changelog",
        kwargs={"model": models.ZoneAccount},
    ),
    path(
        "dns/account/<int:pk>/journal/",
        ObjectJournalView.as_view(),
        name="zoneaccount_journal",
        kwargs={"model": models.ZoneAccount},
    ),
)
