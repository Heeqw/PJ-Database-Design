from django.contrib import admin
from .models import Allergen, Dish, Review

# Register your models here.
admin.site.register(Allergen)
admin.site.register(Dish)
admin.site.register(Review)
