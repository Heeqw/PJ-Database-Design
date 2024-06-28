import random
from datetime import timedelta, datetime, time
from django.core.management.base import BaseCommand
from django.utils import timezone
from user_app.models import User
from merchant_app.models import Merchant
from dish_app.models import Dish
from order_app.models import Order, OrderDetail

class Command(BaseCommand):
    help = '插入大量Order和OrderDetail数据'

    def handle(self, *args, **kwargs):
        # 确保用户和商家存在
        user1, created1 = User.objects.get_or_create(username="test_user1", defaults={"password": "password"})
        user2, created2 = User.objects.get_or_create(username="test_user2", defaults={"password": "password"})

        merchants = [
            Merchant.objects.get_or_create(name="merchant_1", defaults={"address": "address_1"})[0],
            Merchant.objects.get_or_create(name="merchant_2", defaults={"address": "address_2"})[0]
        ]

        dishes = []
        for merchant in merchants:
            dishes.append(Dish.objects.get_or_create(merchant=merchant, name=f"{merchant.name}_dish1", defaults={"price": 10.00})[0])
            dishes.append(Dish.objects.get_or_create(merchant=merchant, name=f"{merchant.name}_dish2", defaults={"price": 15.00})[0])

        now = timezone.now()

        def create_order(user, merchant, dish, order_type, order_dining_status, date_offset, quantity, price):
            order_date = now - timedelta(days=date_offset)
            random_time = time(
                hour=random.randint(0, 23),
                minute=random.randint(0, 59),
                second=random.randint(0, 59)
            )
            order_datetime = timezone.make_aware(datetime.combine(order_date.date(), random_time))

            order = Order.objects.create(
                user=user,
                merchant=merchant,
                status='completed',
                order_type=order_type,
                order_dining_status=order_dining_status,
                date=order_datetime.date(),
                time=order_datetime.time(),
                total_price=price * quantity,
                created_at=order_datetime,
                updated_at=order_datetime
            )
            OrderDetail.objects.create(
                order=order,
                dish=dish,
                quantity=quantity,
                price=price,
                is_reviewed=False
            )

        # 基础数据
        for merchant in merchants:
            for dish in Dish.objects.filter(merchant=merchant):
                create_order(user1, merchant, dish, 'online', 'dines_in', random.randint(1, 5), random.randint(1, 3), dish.price)
                create_order(user1, merchant, dish, 'offline', 'reservation', random.randint(6, 10), random.randint(1, 5), dish.price)
                create_order(user1, merchant, dish, 'online', 'dines_in', random.randint(11, 30), random.randint(1, 2), dish.price)
                create_order(user1, merchant, dish, 'offline', 'reservation', random.randint(31, 365), random.randint(1, 5), dish.price)

                create_order(user2, merchant, dish, 'online', 'dines_in', random.randint(1, 5), random.randint(1, 3), dish.price)
                create_order(user2, merchant, dish, 'offline', 'reservation', random.randint(6, 10), random.randint(1, 5), dish.price)
                create_order(user2, merchant, dish, 'online', 'dines_in', random.randint(11, 30), random.randint(1, 2), dish.price)
                create_order(user2, merchant, dish, 'offline', 'reservation', random.randint(31, 365), random.randint(1, 5), dish.price)

        # 批量插入更多数据
        batch_size = 100
        total_batches = 20
        for _ in range(total_batches):
            for _ in range(batch_size):
                days_ago = random.randint(1, 365)
                dish = random.choice(dishes)
                order_type = random.choice(['online', 'offline'])
                order_dining_status = random.choice(['dines_in', 'reservation'])
                quantity = random.randint(1, 5)
                create_order(random.choice([user1, user2]), dish.merchant, dish, order_type, order_dining_status, days_ago, quantity, dish.price)

        self.stdout.write(self.style.SUCCESS('大量订单数据创建成功！'))
