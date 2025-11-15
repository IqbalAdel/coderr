from django.db import models
from django.conf import settings
from django.utils import timezone

class Review(models.Model):
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='made_reviews'
    )
    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_reviews'
    )
    rating = models.DecimalField(max_digits=1, decimal_places=0, default=0, blank=False, null=False)
    description = models.TextField(max_length=2000, blank=True, null=False, default='')
    def __str__(self):
        return f"Review: {self.reviewer_user.username} to {self.business_user.username}"