"""Navigation Menu definitions"""

from netbox.plugins import (
    PluginMenu,
    PluginMenuItem,
    PluginMenuButton,
)

zoneaccount_buttons = [
    PluginMenuButton(
        link="plugins:netbox_cloudflare_plugin:zoneaccount_add",
        title="Add",
        icon_class="mdi mdi-plus-thick"
    )
]

dnsrecord_buttons = [
    PluginMenuButton(
        link="plugins:netbox_cloudflare_plugin:dnsrecord_add",
        title="Add",
        icon_class="mdi mdi-plus-thick"
    )
]

dns_item = [
    PluginMenuItem(
        link="plugins:netbox_cloudflare_plugin:zoneaccount_list",
        link_text="Accounts",
        buttons=zoneaccount_buttons,
        permissions=["netbox_cloudflare_plugin.view_zoneaccount"],
    ),
    PluginMenuItem(
        link="plugins:netbox_cloudflare_plugin:dnsrecord_list",
        link_text="Records",
        buttons=dnsrecord_buttons,
        permissions=["netbox_cloudflare_plugin.view_dnsrecord"],
    ),
]

menu = PluginMenu(
    label="Cloudflare",
    groups=(("DNS ZONE", dns_item),),
    icon_class="mdi mdi-cloud",
)
