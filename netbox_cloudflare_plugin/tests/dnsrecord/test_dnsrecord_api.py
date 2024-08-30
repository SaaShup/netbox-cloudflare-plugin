"""Host API Test Case"""

from django.urls import reverse
from rest_framework import status
from utilities.testing import APIViewTestCases
from core.models import ObjectType
from users.models import ObjectPermission
from netbox_cloudflare_plugin.models import ZoneAccount, DnsRecord
from netbox_cloudflare_plugin.tests.base import BaseAPITestCase


class DnsRecordApiTestCase(
    BaseAPITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    """ZoneAccount API Test Case Class"""

    model = DnsRecord
    brief_fields = [
        "content",
        "display",
        "id",
        "name",
        "proxied",
        "record_id",
        "ttl",
        "type",
        "url",
    ]
    validation_excluded_fields = ["name"]

    @classmethod
    def setUpTestData(cls) -> None:
        zone1 = ZoneAccount.objects.create(
            zone_name="test1.cloud", zone_id="1001", token="token1"
        )

        DnsRecord.objects.create(
            zone=zone1, name="test1", type=DnsRecord.A, content="10.10.10.10", ttl=60
        )

        DnsRecord.objects.create(
            zone=zone1,
            name="test2",
            type=DnsRecord.CNAME,
            content="test1.test1.cloud",
            ttl=60,
        )

        DnsRecord.objects.create(
            zone=zone1, name="test3", type=DnsRecord.A, content="10.10.10.11", ttl=60
        )

        cls.create_data = [
            {
                "zone": zone1.pk,
                "name": "test4",
                "type": DnsRecord.A,
                "content": "10.10.10.12",
            },
            {
                "zone": zone1.pk,
                "name": "test5",
                "type": DnsRecord.A,
                "content": "10.10.10.13",
            },
            {
                "zone": zone1.pk,
                "name": "test6",
                "type": DnsRecord.A,
                "content": "10.10.10.14",
            },
        ]

    def test_that_record_name_is_set_according_convention(self):
        """Test that record's name is set according convention"""

        # Assign model-level permission
        obj_perm = ObjectPermission(
            name="Test permission", actions=["add", "change", "view"]
        )
        obj_perm.save()
        # pylint: disable=E1101
        obj_perm.users.add(self.user)
        # pylint: disable=E1101
        obj_perm.object_types.add(ObjectType.objects.get_for_model(self.model))
        obj_perm.object_types.add(ObjectType.objects.get_for_model(DnsRecord))

        zone2 = ZoneAccount.objects.create(
            zone_name="test2.cloud", zone_id="1002", token="token2"
        )

        response = self.client.post(
            reverse(f"plugins-api:{self._get_view_namespace()}:dnsrecord-list"),
            [
                {
                    "zone": zone2.pk,
                    "name": "test7",
                    "type": DnsRecord.A,
                    "content": "10.10.10.14",
                },
            ],
            format="json",
            **self.header,
        )

        self.assertHttpStatus(response, status.HTTP_201_CREATED)

        content = response.json()

        self.assertEqual(content[0]["name"], "test7.test2.cloud")

        response = self.client.post(
            reverse(f"plugins-api:{self._get_view_namespace()}:dnsrecord-list"),
            [
                {
                    "zone": zone2.pk,
                    "name": "test8.test2.cloud",
                    "type": DnsRecord.A,
                    "content": "10.10.10.15",
                },
            ],
            format="json",
            **self.header,
        )

        self.assertHttpStatus(response, status.HTTP_201_CREATED)

        content = response.json()

        self.assertEqual(content[0]["name"], "test8.test2.cloud")

    def test_that_record_must_be_unique(self):
        """Test that record must be unique"""

        # Assign model-level permission
        obj_perm = ObjectPermission(
            name="Test permission", actions=["add", "change", "view"]
        )
        obj_perm.save()
        # pylint: disable=E1101
        obj_perm.users.add(self.user)
        # pylint: disable=E1101
        obj_perm.object_types.add(ObjectType.objects.get_for_model(self.model))
        obj_perm.object_types.add(ObjectType.objects.get_for_model(DnsRecord))

        zone3 = ZoneAccount.objects.create(
            zone_name="test3.cloud", zone_id="1003", token="token3"
        )

        response = self.client.post(
            reverse(f"plugins-api:{self._get_view_namespace()}:dnsrecord-list"),
            [
                {
                    "zone": zone3.pk,
                    "name": "test9",
                    "type": DnsRecord.A,
                    "content": "10.10.10.16",
                    "proxied": True,
                },
            ],
            format="json",
            **self.header,
        )

        self.assertHttpStatus(response, status.HTTP_201_CREATED)

        content = response.json()

        self.assertEqual(content[0]["name"], "test9.test3.cloud")

        response = self.client.post(
            reverse(f"plugins-api:{self._get_view_namespace()}:dnsrecord-list"),
            [
                {
                    "zone": zone3.pk,
                    "name": "test9",
                    "type": DnsRecord.A,
                    "content": "10.10.10.17",
                    "proxied": True,
                },
            ],
            format="json",
            **self.header,
        )

        self.assertHttpStatus(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

        content = response.json()

        self.assertEqual(content["exception"], "IntegrityError")

    def test_that_record_can_be_use_for_round_robin(self):
        """Test that record must be unique"""

        # Assign model-level permission
        obj_perm = ObjectPermission(
            name="Test permission", actions=["add", "change", "view"]
        )
        obj_perm.save()
        # pylint: disable=E1101
        obj_perm.users.add(self.user)
        # pylint: disable=E1101
        obj_perm.object_types.add(ObjectType.objects.get_for_model(self.model))
        obj_perm.object_types.add(ObjectType.objects.get_for_model(DnsRecord))

        zone4 = ZoneAccount.objects.create(
            zone_name="test4.cloud", zone_id="1004", token="token4"
        )

        response = self.client.post(
            reverse(f"plugins-api:{self._get_view_namespace()}:dnsrecord-list"),
            [
                {
                    "zone": zone4.pk,
                    "name": "test10",
                    "type": DnsRecord.A,
                    "content": "10.10.10.18",
                    "proxied": False,
                },
            ],
            format="json",
            **self.header,
        )

        self.assertHttpStatus(response, status.HTTP_201_CREATED)

        content = response.json()

        self.assertEqual(content[0]["name"], "test10.test4.cloud")

        response = self.client.post(
            reverse(f"plugins-api:{self._get_view_namespace()}:dnsrecord-list"),
            [
                {
                    "zone": zone4.pk,
                    "name": "test10",
                    "type": DnsRecord.A,
                    "content": "10.10.10.19",
                    "proxied": False,
                },
            ],
            format="json",
            **self.header,
        )

        self.assertHttpStatus(response, status.HTTP_201_CREATED)

        content = response.json()

        self.assertEqual(content[0]["name"], "test10.test4.cloud")

    def test_that_record_must_be_unique_with_not_proxied(self):
        """Test that record must be unique with not proxied"""

        # Assign model-level permission
        obj_perm = ObjectPermission(
            name="Test permission", actions=["add", "change", "view"]
        )
        obj_perm.save()
        # pylint: disable=E1101
        obj_perm.users.add(self.user)
        # pylint: disable=E1101
        obj_perm.object_types.add(ObjectType.objects.get_for_model(self.model))
        obj_perm.object_types.add(ObjectType.objects.get_for_model(DnsRecord))

        zone5 = ZoneAccount.objects.create(
            zone_name="test5.cloud", zone_id="1005", token="token5"
        )

        response = self.client.post(
            reverse(f"plugins-api:{self._get_view_namespace()}:dnsrecord-list"),
            [
                {
                    "zone": zone5.pk,
                    "name": "test11",
                    "type": DnsRecord.A,
                    "content": "10.10.10.20",
                    "proxied": False,
                },
            ],
            format="json",
            **self.header,
        )

        self.assertHttpStatus(response, status.HTTP_201_CREATED)

        content = response.json()

        self.assertEqual(content[0]["name"], "test11.test5.cloud")

        response = self.client.post(
            reverse(f"plugins-api:{self._get_view_namespace()}:dnsrecord-list"),
            [
                {
                    "zone": zone5.pk,
                    "name": "test11",
                    "type": DnsRecord.A,
                    "content": "10.10.10.21",
                    "proxied": True,
                },
            ],
            format="json",
            **self.header,
        )

        self.assertHttpStatus(response, status.HTTP_400_BAD_REQUEST)

        content = response.json()

        self.assertEqual(content["detail"], "Unable to create DNS Record on Cloudflare")
