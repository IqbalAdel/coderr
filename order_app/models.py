from django.db import models
from offer_app.models import OfferDetail
from django.conf import settings
from django.utils import timezone

class Order(models.Model):
    customer_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='placed_orders'
    )
    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_orders'
    )
    status = models.CharField(max_length=20, blank=False, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    offer_detail = models.ForeignKey(OfferDetail, on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return f"Order: {self.customer_user.username} to {self.business_user.username} - Status: {self.status}"