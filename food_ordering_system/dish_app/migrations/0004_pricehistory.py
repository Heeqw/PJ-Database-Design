# Generated manually to fix migration dependency issue

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dish_app', '0003_alter_dish_merchant'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('new_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('changed_at', models.DateTimeField(auto_now_add=True, default='2024-05-01 00:00:00')),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_history', to='dish_app.dish')),
            ],
            options={
                'verbose_name': 'Price History',
                'verbose_name_plural': 'Price Histories',
                'ordering': ['-changed_at'],
            },
        ),
    ]
