from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from merchant_app.models import Merchant, MerchantLogin, MerchantToken
from dish_app.models import Dish, Allergen
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
import random
from decimal import Decimal

User = get_user_model()

class Command(BaseCommand):
    help = 'Initialize database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting data initialization...'))

        # Create allergens
        self.create_allergens()

        # Create users
        self.create_users()

        # Create merchants
        merchants = self.create_merchants()

        # Create dishes
        self.create_dishes(merchants)

        self.stdout.write(self.style.SUCCESS('Data initialization completed successfully!'))

    def create_allergens(self):
        allergens = ['Gluten', 'Dairy', 'Nuts', 'Eggs', 'Soy', 'Fish', 'Shellfish', 'Wheat']

        for allergen_name in allergens:
            Allergen.objects.get_or_create(name=allergen_name)

        self.stdout.write(self.style.SUCCESS(f'Created {len(allergens)} allergens'))

    def create_users(self):
        # Create admin user
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'full_name': 'Admin User',
                'role': 'admin',
                'gender': 'male',
                'is_staff': True,
                'is_superuser': True
            }
        )

        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Created admin user: admin/admin123'))

        # Create student users
        students = []
        for i in range(1, 4):
            student, created = User.objects.get_or_create(
                username=f'student{i}',
                defaults={
                    'email': f'student{i}@example.com',
                    'full_name': f'Student {i}',
                    'role': 'student',
                    'student_id': f'S{10000+i}',
                    'gender': random.choice(['male', 'female']),
                }
            )

            if created:
                student.set_password('password123')
                student.save()
                students.append(student)

        self.stdout.write(self.style.SUCCESS(f'Created {len(students)} student users'))

        # Create staff users
        staff_users = []
        for i in range(1, 3):
            staff, created = User.objects.get_or_create(
                username=f'staff{i}',
                defaults={
                    'email': f'staff{i}@example.com',
                    'full_name': f'Staff {i}',
                    'role': 'staff',
                    'staff_id': f'E{20000+i}',
                    'gender': random.choice(['male', 'female']),
                }
            )

            if created:
                staff.set_password('password123')
                staff.save()
                staff_users.append(staff)

        self.stdout.write(self.style.SUCCESS(f'Created {len(staff_users)} staff users'))

    def create_merchants(self):
        merchant_data = [
            {
                'name': '校园餐厅',
                'address': '大学校园中心',
                'phone': '123-456-7890',
            },
            {
                'name': '快乐食堂',
                'address': '大学校园东区',
                'phone': '123-456-7891',
            },
            {
                'name': '美味小厨',
                'address': '大学校园西区',
                'phone': '123-456-7892',
            }
        ]

        merchants = []
        for data in merchant_data:
            merchant, created = Merchant.objects.get_or_create(
                name=data['name'],
                defaults={
                    'address': data['address'],
                    'phone': data['phone'],
                }
            )
            merchants.append(merchant)

            # Create merchant login
            username = data['name'].replace(' ', '_').lower()
            merchant_login, login_created = MerchantLogin.objects.get_or_create(
                merchant=merchant,
                defaults={
                    'username': username,
                    'password': make_password('merchant123')  # 使用make_password直接加密密码
                }
            )

            if login_created:
                # 创建商家令牌
                token, _ = MerchantToken.objects.get_or_create(user=merchant_login)
                self.stdout.write(self.style.SUCCESS(f'Created merchant login: {username}/merchant123 with token: {token.key}'))

        self.stdout.write(self.style.SUCCESS(f'Created {len(merchants)} merchants'))
        return merchants

    def create_dishes(self, merchants):
        categories = ['主食', '小吃', '饮料', '甜点']
        dish_data = [
            {
                'name': '红烧牛肉面',
                'description': '美味的红烧牛肉面，配以新鲜蔬菜和嫩滑牛肉',
                'price': Decimal('15.99'),
                'category': '主食',
                'image_url': 'https://example.com/beef_noodle.jpg',
                'ingredients': '面条, 牛肉, 葱, 姜, 蒜, 辣椒',
                'nutrition_info': '热量: 450卡路里, 蛋白质: 25克, 脂肪: 15克, 碳水化合物: 60克',
            },
            {
                'name': '宫保鸡丁',
                'description': '经典川菜，鸡肉与花生的完美搭配',
                'price': Decimal('18.50'),
                'category': '主食',
                'image_url': 'https://example.com/kungpao_chicken.jpg',
                'ingredients': '鸡肉, 花生, 干辣椒, 葱, 姜, 蒜',
                'nutrition_info': '热量: 380卡路里, 蛋白质: 28克, 脂肪: 18克, 碳水化合物: 22克',
            },
            {
                'name': '蛋炒饭',
                'description': '简单美味的蛋炒饭，适合任何时候享用',
                'price': Decimal('12.00'),
                'category': '主食',
                'image_url': 'https://example.com/egg_fried_rice.jpg',
                'ingredients': '米饭, 鸡蛋, 葱, 胡萝卜, 豌豆',
                'nutrition_info': '热量: 320卡路里, 蛋白质: 10克, 脂肪: 8克, 碳水化合物: 55克',
            },
            {
                'name': '水饺',
                'description': '手工制作的美味水饺，多种馅料可选',
                'price': Decimal('16.00'),
                'category': '小吃',
                'image_url': 'https://example.com/dumplings.jpg',
                'ingredients': '面粉, 猪肉, 白菜, 葱, 姜',
                'nutrition_info': '热量: 280卡路里, 蛋白质: 15克, 脂肪: 10克, 碳水化合物: 35克',
            },
            {
                'name': '奶茶',
                'description': '香浓奶茶，可选添加珍珠',
                'price': Decimal('8.00'),
                'category': '饮料',
                'image_url': 'https://example.com/milk_tea.jpg',
                'ingredients': '红茶, 牛奶, 糖',
                'nutrition_info': '热量: 180卡路里, 蛋白质: 3克, 脂肪: 5克, 碳水化合物: 30克',
            },
            {
                'name': '提拉米苏',
                'description': '经典意大利甜点，口感丰富',
                'price': Decimal('12.50'),
                'category': '甜点',
                'image_url': 'https://example.com/tiramisu.jpg',
                'ingredients': '马斯卡彭奶酪, 咖啡, 手指饼干, 可可粉',
                'nutrition_info': '热量: 350卡路里, 蛋白质: 6克, 脂肪: 22克, 碳水化合物: 32克',
            },
        ]

        dishes = []
        allergens = list(Allergen.objects.all())

        for data in dish_data:
            # Randomly assign to a merchant
            merchant = random.choice(merchants)

            dish, created = Dish.objects.get_or_create(
                name=data['name'],
                merchant=merchant,
                defaults={
                    'description': data['description'],
                    'price': data['price'],
                    'category': data['category'],
                    'image_url': data['image_url'],
                    'ingredients': data['ingredients'],
                    'nutrition_info': data['nutrition_info'],
                }
            )

            if created:
                # Randomly assign some allergens
                dish_allergens = random.sample(allergens, random.randint(0, 3))
                dish.allergens.set(dish_allergens)
                dishes.append(dish)

        self.stdout.write(self.style.SUCCESS(f'Created {len(dishes)} dishes'))
