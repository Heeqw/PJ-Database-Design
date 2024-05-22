from django.contrib import admin
from .models import User, FavoriteMerchant, FavoriteDish

# Register your models here.
admin.site.register(User)
admin.site.register(FavoriteMerchant)
admin.site.register(FavoriteDish)
