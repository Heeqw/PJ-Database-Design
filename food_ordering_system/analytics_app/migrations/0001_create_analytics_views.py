from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        # Use a more generic dependency that should exist
        ('dish_app', '0003_alter_dish_merchant'),
        ('order_app', '0002_initial'),
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql='''
            CREATE TABLE IF NOT EXISTS dish_sales_view (
                dish_id INTEGER PRIMARY KEY,
                total_sales INTEGER NOT NULL,
                online_sales INTEGER NOT NULL,
                offline_sales INTEGER NOT NULL,
                total_revenue REAL NOT NULL,
                avg_rating REAL NULL
            );
            ''',
            reverse_sql='DROP TABLE IF EXISTS dish_sales_view;'
        ),
        migrations.RunSQL(
            sql='''
            CREATE TABLE IF NOT EXISTS merchant_sales_view (
                merchant_id INTEGER PRIMARY KEY,
                merchant_name TEXT NOT NULL,
                total_orders INTEGER NOT NULL,
                total_revenue REAL NOT NULL,
                avg_order_value REAL NOT NULL,
                online_orders INTEGER NOT NULL,
                offline_orders INTEGER NOT NULL
            );
            ''',
            reverse_sql='DROP TABLE IF EXISTS merchant_sales_view;'
        ),
        migrations.RunSQL(
            sql='''
            CREATE TABLE IF NOT EXISTS user_activity_view (
                user_id INTEGER PRIMARY KEY,
                total_orders INTEGER NOT NULL,
                total_spent REAL NOT NULL,
                avg_order_value REAL NULL,
                favorite_dishes_count INTEGER NOT NULL,
                reviews_count INTEGER NOT NULL
            );
            ''',
            reverse_sql='DROP TABLE IF EXISTS user_activity_view;'
        ),
    ]
