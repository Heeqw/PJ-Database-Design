# Generated by Django 5.0.6 on 2024-06-28 01:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dish_app", "0004_pricehistory"),
    ]

    operations = [
        migrations.AlterField(
            model_name="allergen",
            name="name",
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name="dish",
            name="category",
            field=models.CharField(db_index=True, max_length=50),
        ),
        migrations.AlterField(
            model_name="dish",
            name="name",
            field=models.CharField(db_index=True, max_length=100),
        ),
    ]