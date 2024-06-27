from datetime import date

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('staff', 'Staff')
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, db_index=True)
    student_id = models.CharField(max_length=20, blank=True, null=True, unique=True)
    staff_id = models.CharField(max_length=20, blank=True, null=True, unique=True)
    full_name = models.CharField(max_length=100)
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female'), ('other', 'Other')]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, db_index=True)
    date_of_birth = models.DateField(default='2000-01-01', db_index=True)

    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    def save(self, *args, **kwargs):
        if self.role == 'student':
            self.staff_id = None
        elif self.role == 'staff':
            self.student_id = None
        super().save(*args, **kwargs)


class FavoriteMerchant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    merchant = models.ForeignKey('merchant_app.Merchant', on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)


class FavoriteDish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    dish = models.ForeignKey('dish_app.Dish', on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
