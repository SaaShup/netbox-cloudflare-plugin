"""API views definitions"""

from netbox.api.viewsets import NetBoxModelViewSet
from .serializers import ZoneAccountSerializer
from ..models import ZoneAccount


class ZoneAccountViewSet(NetBoxModelViewSet):
    """ZoneAccount view set class"""

    queryset = ZoneAccount.objects.all()
    serializer_class = ZoneAccountSerializer
    http_method_names = ["get", "post", "patch", "delete", "options"]
