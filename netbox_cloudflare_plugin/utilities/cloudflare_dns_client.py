"""Cloudflare DNS Client"""

import requests
from ..models import DnsRecord


class CloudflareDnsClient:
    """Cloudflare DNS Client"""

    zone_account = None
    base_url = None

    def __init__(self, zone_account, base_url):
        self.zone_account = zone_account
        self.base_url = base_url

    def get_dns_records(self, page=1, per_page=100):
        """Get DNS Record from Cloudflare"""

        url = f"{self.base_url}/zones/{self.zone_account.zone_id}/dns_records"
        headers = {
            "Authorization": f"Bearer {self.zone_account.token}",
            "Content-Type": "application/json",
        }

        response = requests.get(
            url, headers=headers, timeout=5, params={"page": page, "per_page": per_page}
        )

        response.raise_for_status()

        content = response.json()

        result = {"result_info": content["result_info"]}

        result["records"] = []

        for record in content["result"]:
            if record["type"] in (DnsRecord.A, DnsRecord.CNAME):
                result["records"].append(
                    DnsRecord(
                        zone=self.zone_account,
                        record_id=record["id"],
                        name=record["name"],
                        type=record["type"],
                        content=record["content"],
                        ttl=record["ttl"],
                        proxied=record["proxied"],
                    )
                )

        return result

    def create_dns_record(self, dns_record):
        """Add DNS Record to Cloudflare"""

        url = f"{self.base_url}/zones/{self.zone_account.zone_id}/dns_records"
        headers = {
            "Authorization": f"Bearer {self.zone_account.token}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            url,
            headers=headers,
            timeout=5,
            json={
                "content": dns_record.content,
                "name": dns_record.name,
                "proxied": dns_record.proxied,
                "type": dns_record.type,
                "ttl": dns_record.ttl,
            },
        )

        response.raise_for_status()

        content = response.json()

        dns_record.record_id = content["result"]["id"]

        return dns_record

    def delete_dnsrecord(self, dns_record):
        """Delete DNS Record to from"""

        url = (f"{self.base_url}/zones/{self.zone_account.zone_id}/dns_records/"
            + dns_record.record_id)

        headers = {
            "Authorization": f"Bearer {self.zone_account.token}",
            "Content-Type": "application/json",
        }

        response = requests.delete(url, headers=headers, timeout=5)

        response.raise_for_status()
