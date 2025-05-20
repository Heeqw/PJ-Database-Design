from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dish_app', '0003_alter_dish_merchant'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='dish',
            index=models.Index(fields=['merchant', 'category'], name='merchant_category_idx'),
        ),
        migrations.AddIndex(
            model_name='dish',
            index=models.Index(fields=['price'], name='price_idx'),
        ),
        migrations.AddIndex(
            model_name='dish',
            index=models.Index(fields=['merchant', 'name'], name='merchant_name_idx'),
        ),
        migrations.CreateModel(
            name='PriceHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('new_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('changed_at', models.DateTimeField(auto_now_add=True)),
                ('dish', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='price_history', to='dish_app.dish', db_index=True)),
            ],
        ),
    ]
