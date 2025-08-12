"""Cloudflare Plugin Models definitions"""

from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    MinValueValidator,
    MaxValueValidator,
)
from netbox.models import NetBoxModel


class ZoneAccount(NetBoxModel):
    """Cloudflare DNS zone account definition class"""

    zone_name = models.CharField(
        unique=True,
        max_length=255,
        null=False,
        blank=False,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=255),
        ],
    )
    zone_id = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=255),
        ],
    )
    token = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=255),
        ],
    )

    class Meta:
        """Cloudflare DNS zone account Model Meta Class"""

        ordering = ("zone_name",)

    def __str__(self):
        return f"{self.zone_name}"

    def get_absolute_url(self):
        """override"""
        return reverse("plugins:netbox_cloudflare_plugin:zoneaccount", args=[self.pk])


class DnsRecord(NetBoxModel):
    """DNS entry definition class"""

    is_deleted_manually = False

    CNAME = "CNAME"
    A = "A"

    TYPE_CHOICE = (
        (CNAME, CNAME),
        (A, A),
    )

    zone = models.ForeignKey(
        ZoneAccount, on_delete=models.CASCADE, related_name="records"
    )
    record_id = name = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=32),
        ],
    )
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=255),
        ],
    )
    type = models.CharField(
        max_length=64,
        choices=TYPE_CHOICE,
        default=CNAME,
        null=False,
        blank=False,
    )
    content = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        validators=[
            MinLengthValidator(limit_value=1),
            MaxLengthValidator(limit_value=255),
        ],
    )
    ttl = models.IntegerField(
        default=3600,
        null=False,
        blank=False,
        validators=[
            MinValueValidator(limit_value=60),
            MaxValueValidator(limit_value=86400),
        ],
    )
    proxied = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        """DNS entry Meta Class"""

        ordering = (
            "zone",
            "name",
            "type",
        )
        constraints = (
            models.UniqueConstraint(
                fields=["zone", "name", "type", "content"],
                name="%(app_label)s_%(class)s_unique_zone_name_type_content"
            ),
            models.UniqueConstraint(
                fields=["zone", "name", "type"],
                name="%(app_label)s_%(class)s_unique_zone_name_type",
                condition=Q(proxied=True)
            ),
        )

    def __str__(self):
        return f"{self.name} {self.type} {self.content} {self.ttl}"

    def get_absolute_url(self):
        """override"""
        return reverse("plugins:netbox_cloudflare_plugin:dnsrecord", args=[self.pk])

    def delete(self, using=None, keep_parents=False):
        """override"""
        self.is_deleted_manually = True

        return super().delete(using, keep_parents)
