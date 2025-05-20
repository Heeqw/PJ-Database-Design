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

    class Meta:
        # Add composite indexes for common query patterns
        indexes = [
            # For merchant + category queries
            models.Index(fields=['merchant', 'category'], name='merchant_category_idx'),
            # For price range queries
            models.Index(fields=['price'], name='price_idx'),
            # For merchant + name search
            models.Index(fields=['merchant', 'name'], name='merchant_name_idx'),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Check if this is an update to an existing dish
        if self.pk:
            # Get the old price before saving
            try:
                old_dish = Dish.objects.get(pk=self.pk)
                old_price = old_dish.price

                # If price has changed, create a price history record
                if old_price != self.price:
                    PriceHistory.objects.create(
                        dish=self,
                        old_price=old_price,
                        new_price=self.price
                    )
            except Dish.DoesNotExist:
                pass  # This is a new dish, no price history needed

        # Call the original save method
        super().save(*args, **kwargs)


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