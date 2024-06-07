"""API URLs definition"""

from netbox.api.routers import NetBoxRouter
from .views import ZoneAccountViewSet


APP_NAME = "netbox_cloudflare_plugin"

router = NetBoxRouter()
router.register("dns/account", ZoneAccountViewSet)

urlpatterns = router.urls
