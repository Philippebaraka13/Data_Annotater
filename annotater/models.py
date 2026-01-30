from django.db import models

# Create your models here.

from django.db import models

class RetailRow(models.Model):
    class Segment(models.TextChoices):
        FIRST_PARTY = "FIRST_PARTY", "First Party"
        THIRD_PARTY = "THIRD_PARTY", "Third Party"

    # Raw fields
    merchant = models.TextField()
    sku = models.TextField()
    country = models.CharField(max_length=2)

    # Annotation fields
    retailer = models.TextField(blank=True, null=True)
    segment = models.CharField(
        max_length=20,
        choices=Segment.choices,
        blank=True,
        null=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["merchant", "sku", "country"],
                name="uniq_merchant_sku_country",
            )
        ]

    def __str__(self):
        return f"{self.merchant} | {self.sku} | {self.country}"
