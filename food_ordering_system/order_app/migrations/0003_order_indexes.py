from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('order_app', '0004_order_date_order_order_dining_status_order_time_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['merchant', 'date'], name='merchant_date_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['user', 'date'], name='user_date_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['merchant', 'status'], name='merchant_status_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['order_type', 'date'], name='order_type_date_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['merchant', 'status', 'order_type'], name='merchant_status_type_idx'),
        ),
        migrations.AddIndex(
            model_name='orderdetail',
            index=models.Index(fields=['dish', 'order'], name='dish_order_idx'),
        ),
        migrations.AddIndex(
            model_name='orderdetail',
            index=models.Index(fields=['is_reviewed', 'dish'], name='review_dish_idx'),
        ),
        migrations.AddIndex(
            model_name='orderdetail',
            index=models.Index(fields=['order', 'dish'], name='order_dish_idx'),
        ),
    ]
