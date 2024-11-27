import random
from faker import Faker
from recommendations.models import Product, Order, User, Category
from django.utils.timezone import make_aware, now
from datetime import timedelta

# initialize Faker
fake = Faker()

# create 15 categories
categories = [Category.objects.create(name=fake.word()) for _ in range(15)]

# create 150 products
products = [Product.objects.create(
    name=fake.word(),
    category=random.choice(categories),
    description=fake.text(),
) for _ in range(150)]

# create 70 users
users = [User.objects.create(
    username=fake.user_name(),
    email=fake.email(),
) for _ in range(70)]

# create 450 orders and multiple orders per user
order_count = 450
for _ in range(order_count):
    user = random.choice(users)
    
    # spread orders over time
    days_offset = random.randint(1, 30)  # random days for order spread
    order_date = now() - timedelta(days=days_offset)
    order = Order.objects.create(
        user=user,
        created_at=order_date
    )

    # select random products (1 to 5 per order)
    num_products = random.randint(1, 5)
    order_products = random.sample(products, num_products)
    order.products.set(order_products)
    order.save()

print(f"Categories created: {len(categories)}")
print(f"Products created: {len(products)}")
print(f"Users created: {len(users)}")
print(f"Orders created: {Order.objects.count()}")
