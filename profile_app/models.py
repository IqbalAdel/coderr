from django.db import models
from django.conf import settings
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    username = models.CharField(max_length=150, blank=False, null=False)
    first_name = models.CharField(max_length=150, blank=True, default='', null=False)  
    last_name = models.CharField(max_length=150, blank=True, default='', null=False)   
    file = models.FileField(blank=True, null=True, default='', upload_to='uploads/')        
    location = models.CharField(max_length=255, blank=True, default='', null=False)    
    tel = models.CharField(max_length=50, blank=True, default='', null=False)         
    description = models.TextField(blank=True, default='', null=False)                 
    working_hours = models.CharField(max_length=100, blank=True,null=False, default='')  
    type = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    created_at = models.DateTimeField(default=timezone.now)

    def clean(self):
        super().clean()
        if not self.username.strip():
            raise ValueError("Username cannot be empty.")
        if not self.email.strip():
            raise ValueError("Email cannot be empty.")
        if not self.type.strip():
            raise ValueError("Type cannot be empty.")

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.user:
            if self.username and self.username != self.user.username:
                self.user.username = self.username
            if self.email and self.email != self.user.email:
                self.user.email = self.email
            self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Profile: {self.username or getattr(self.user, "username", "")}'