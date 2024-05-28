from django.contrib import admin
from .models import Merchant, MerchantLogin

# Register your models here.

admin.site.register(Merchant)
admin.site.register(MerchantLogin)
