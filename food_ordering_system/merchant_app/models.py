from django.db import models
from user_app.models import User


# Create your models here.
class Merchant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='merchant_profile')
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
