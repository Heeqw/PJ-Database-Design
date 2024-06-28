# Generated by Django 5.0.6 on 2024-06-28 01:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order_app", "0003_order_date_order_order_dining_status_order_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="date",
            field=models.DateField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name="order",
            name="order_dining_status",
            field=models.CharField(
                choices=[("dines_in", "Dines In"), ("reservation", "Reservation")],
                db_index=True,
                default="dines_in",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="order_type",
            field=models.CharField(
                choices=[("online", "Online"), ("offline", "Offline")],
                db_index=True,
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[("preparing", "Preparing"), ("completed", "Completed")],
                db_index=True,
                max_length=10,
            ),
        ),
    ]