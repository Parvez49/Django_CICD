from django.db import models
from django.utils import timezone

# Create your models here.


class OTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)  # Assuming OTP is a 6-digit code
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"OTP for {self.email}"
