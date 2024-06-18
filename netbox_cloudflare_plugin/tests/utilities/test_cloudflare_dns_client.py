"""Cloudflare DNS Client Test Case"""

import unittest
import requests_mock
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from netbox_cloudflare_plugin.utilities.cloudflare_dns_client import CloudflareDnsClient
from netbox_cloudflare_plugin.models import ZoneAccount


class CloudflareDnsClientTestCase(unittest.TestCase):
    """Cloudflare DNS Client Test Case"""

    def test_that_dns_records_can_be_fetched(self):
        """Test that DNS record can be fetched"""

        with requests_mock.Mocker(json_encoder=DjangoJSONEncoder) as m:
            zone_account = ZoneAccount(
                zone_name="test.cloud",
                token="secrettoken",
                zone_id="12345",
            )
            base_url = settings.PLUGINS_CONFIG["netbox_cloudflare_plugin"][
                "cloudflare_base_url"
            ]

            m.get(
                f"{base_url}/zones/{zone_account.zone_id}/dns_records?page=1&per_page=100",
                headers={
                    "Authorization": f"Bearer {zone_account.token}",
                    "Content-Type": "application/json",
                },
                json={
                    "errors": [],
                    "messages": [],
                    "success": True,
                    "result": [
                        {
                            "content": "198.51.100.4",
                            "name": "example.com",
                            "proxied": False,
                            "type": "A",
                            "comment": "Domain verification record",
                            "created_on": "2014-01-01T05:20:00.12345Z",
                            "id": "023e105f4ecef8ad9ca31a8372d0c353",
                            "locked": False,
                            "meta": {"auto_added": True, "source": "primary"},
                            "modified_on": "2014-01-01T05:20:00.12345Z",
                            "proxiable": True,
                            "tags": ["owner:dns-team"],
                            "ttl": 3600,
                            "zone_id": "023e105f4ecef8ad9ca31a8372d0c353",
                            "zone_name": "example.com",
                        },
                        {
                            "id": "60cd730cdfe330eb736d4c39cdb1d7c2",
                            "zone_id": "0ed0140310e7347c5ff41335d1d9918d",
                            "zone_name": "example.com",
                            "name": "mailjet._domainkey.portainer.cloud",
                            "type": "TXT",
                            "content": "k=rsa;p=jZyaYVVrOfOMBKLzb9fUBsmGwIDAQAB",
                            "proxiable": False,
                            "proxied": False,
                            "ttl": 1,
                            "locked": False,
                            "meta": {
                                "auto_added": False,
                                "managed_by_apps": False,
                                "managed_by_argo_tunnel": False,
                            },
                            "comment": None,
                            "tags": [],
                            "created_on": "2021-11-12T22:33:01.376568Z",
                            "modified_on": "2021-11-12T22:33:01.376568Z",
                        },
                    ],
                    "result_info": {
                        "count": 1,
                        "page": 1,
                        "per_page": 20,
                        "total_count": 2000,
                    },
                },
            )

            client = CloudflareDnsClient(
                zone_account=zone_account,
                base_url=settings.PLUGINS_CONFIG["netbox_cloudflare_plugin"][
                    "cloudflare_base_url"
                ],
            )

            result = client.get_dns_records()

            self.assertEqual(
                result["result_info"],
                {
                    "count": 1,
                    "page": 1,
                    "per_page": 20,
                    "total_count": 2000,
                },
            )
            self.assertEqual(len(result["records"]), 1)
            self.assertEqual(result["records"][0].zone.zone_name, "test.cloud")
            self.assertEqual(
                result["records"][0].record_id, "023e105f4ecef8ad9ca31a8372d0c353"
            )
            self.assertEqual(result["records"][0].name, "example.com")
            self.assertEqual(result["records"][0].type, "A")
            self.assertEqual(result["records"][0].content, "198.51.100.4")
            self.assertEqual(result["records"][0].ttl, 3600)
            self.assertEqual(result["records"][0].proxied, False)
