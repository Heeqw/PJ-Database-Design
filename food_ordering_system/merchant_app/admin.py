from django.contrib import admin
from .models import Merchant, MerchantLogin
from dish_app.models import Dish
from django import forms


# Register your models here.
class MerchantAdminForm(forms.ModelForm):
    class Meta:
        model = Merchant
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MerchantAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['featured_dish'].queryset = Dish.objects.filter(merchant=self.instance)


class MerchantAdmin(admin.ModelAdmin):
    form = MerchantAdminForm


admin.site.register(Merchant, MerchantAdmin)
admin.site.register(MerchantLogin)
