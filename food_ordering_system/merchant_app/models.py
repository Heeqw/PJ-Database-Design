from django.db import models
from rest_framework.authtoken.models import Token as DefaultToken
import uuid


class Merchant(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    featured_dish = models.ForeignKey('dish_app.Dish', on_delete=models.SET_NULL,null=True,blank=True,related_name='featured_by')

    def __str__(self):
        return self.name


class MerchantLogin(models.Model):
    merchant = models.OneToOneField(Merchant, on_delete=models.CASCADE, related_name='login')
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username


class MerchantToken(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    user = models.OneToOneField(MerchantLogin, related_name='auth_token', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @staticmethod
    def generate_key():
        return uuid.uuid4().hex
