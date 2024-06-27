from django.db import models


# Create your models here.
class Allergen(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name


class Dish(models.Model):
    merchant = models.ForeignKey('merchant_app.Merchant', on_delete=models.CASCADE, related_name='dishes')
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, db_index=True)
    image_url = models.URLField(blank=True)
    ingredients = models.TextField(blank=True)
    nutrition_info = models.TextField(blank=True)
    allergens = models.ManyToManyField(Allergen, blank=True, related_name='dished_with_allergen')

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey('user_app.User', on_delete=models.CASCADE, related_name='reviews', db_index=True)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='reviews', db_index=True)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.dish.name}'


class PriceHistory(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='price_history', db_index=True)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    changed_at = models.DateTimeField(auto_now_add=True)