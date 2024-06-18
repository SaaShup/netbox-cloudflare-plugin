"""Host API Test Case"""

from utilities.testing import APIViewTestCases
from netbox_cloudflare_plugin.models import ZoneAccount
from netbox_cloudflare_plugin.tests.base import BaseAPITestCase


class ZoneAccountApiTestCase(
    BaseAPITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    """ZoneAccount API Test Case Class"""

    model = ZoneAccount
    brief_fields = ["display", "id", "token", "url", "zone_id", "zone_name"]
    create_data = [
        {"zone_name": "test4.cloud", "zone_id": "1004", "token": "token4"},
        {"zone_name": "test5.cloud", "zone_id": "1005", "token": "token5"},
        {"zone_name": "test6.cloud", "zone_id": "1006", "token": "token6"},
    ]

    @classmethod
    def setUpTestData(cls) -> None:
        ZoneAccount.objects.create(
            zone_name="test1.cloud", zone_id="1001", token="token1"
        )
        ZoneAccount.objects.create(
            zone_name="test2.cloud", zone_id="1002", token="token2"
        )
        ZoneAccount.objects.create(
            zone_name="test3.cloud", zone_id="1003", token="token3"
        )
