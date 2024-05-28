from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('staff', 'Staff')
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    student_id = models.CharField(max_length=20, blank=True, null=True, unique=True)
    staff_id = models.CharField(max_length=20, blank=True, null=True, unique=True)
    full_name = models.CharField(max_length=100)
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female'), ('other', 'Other')]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    def save(self, *args, **kwargs):
        if self.role == 'student':
            self.staff_id = None
        elif self.role == 'staff':
            self.student_id = None
        super().save(*args, **kwargs)


class FavoriteMerchant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    merchant = models.ForeignKey('merchant_app.Merchant', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class FavoriteDish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey('dish_app.Dish', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
