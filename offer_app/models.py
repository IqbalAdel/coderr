from django.db import models
from django.conf import settings
from django.utils import timezone

class Offer(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='offers'
    )
    title = models.CharField(max_length=255, blank=False, null=False)
    image = models.FileField(blank=True, null=True, default='', upload_to='uploads/')
    description = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Offer: {self.title} by {self.user.username}"

class OfferDetail(models.Model):
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name='details'
    )
    title = models.CharField(max_length=255, blank=False, null=False)
    revisions = models.DecimalField(max_digits=2, decimal_places=0, blank=False, null=False)
    delivery_time_in_days = models.DecimalField(max_digits=2, decimal_places=0, blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=0, blank=False, null=False)
    features = models.JSONField(default=list, blank=True)
    offer_type = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return f"Details for Offer: {self.offer.title}"



