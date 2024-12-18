# Product_Recommendation_System

Product Recommendation System
Overview

This is a Product Recommendation System built using Django and Docker. The system uses machine learning techniques to recommend products to users based on their purchase history and product categories. The backend API is built using Django Rest Framework, and the entire application is containerized using Docker and Docker Compose.

The system consists of the following models:

    Category: Represents product categories.
    Product: Represents products, each linked to a category.
    User: Represents a user who can place orders.
    Order: Represents an order made by a user, containing multiple products.

Features

    Product List: View a list of all available products.
    Order Management: Place new orders and view existing ones.
    Product Recommendations: Get product recommendations based on the user's past orders and similar product categories.

Tech Stack

    Backend: Django 5.x
    Database: SQLite (used for simplicity in this project)
    Docker: For containerization
    Django Rest Framework: For building RESTful APIs

Setup Instructions
1. Clone the Repository

Start by cloning the repository to your local machine:

git clone https://github.com/sarkarhd12/Product_Recommendation_System.git
cd product-recommendation

2. Build and Run with Docker

Ensure you have Docker and Docker Compose installed. Then, use the following command to build and run the application in Docker:

docker-compose up --build

This command will:

    Build the Docker image for the Django app.
    Set up the necessary containers for the application.
    Start the Django development server at http://localhost:8000.

3. Access the Application

Once the containers are up, you can access the API endpoints at:

    Product List: http://localhost:8000/api/products/
    Order List: http://localhost:8000/api/orders/
    Create Order: POST request to http://localhost:8000/api/orders/create/
    Product Recommendations: GET request to http://localhost:8000/api/recommendations/{product_id}/

4. Stop the Application

To stop the Docker containers, press Ctrl + C or run the following command in a new terminal window:

docker-compose down

5. Running Migrations

If you haven't run the migrations yet, you can do so manually by running the following command in the container:

docker-compose exec web python manage.py migrate

This will apply all the necessary database migrations to set up your application.
Application Structure

Here’s a brief overview of the key parts of the code:

Models
Category

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

Product

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.name

User

class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

Represents a user who can place orders.
Order

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user}"

Represents an order placed by a user, containing multiple products.
Data Population Script

The script to populate the database with fake data using the Faker library is as follows:

fake = Faker()

# Create 15 categories
categories = [Category.objects.create(name=fake.word()) for _ in range(15)]

# Create 150 products
products = [Product.objects.create(
    name=fake.word(),
    category=random.choice(categories),
    description=fake.text(),
) for _ in range(150)]

# Create 70 users
users = [User.objects.create(
    username=fake.user_name(),
    email=fake.email(),
) for _ in range(70)]

# Create 450 orders and multiple orders per user
order_count = 450
for _ in range(order_count):
    user = random.choice(users)
    days_offset = random.randint(1, 30)  # Random days for order spread
    order_date = now() - timedelta(days=days_offset)
    order = Order.objects.create(user=user, created_at=order_date)
    num_products = random.randint(1, 5)
    order_products = random.sample(products, num_products)
    order.products.set(order_products)
    order.save()

API Endpoints

    Product List: A simple endpoint to fetch all products:

class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

Order List: Fetches all orders:

class OrderListView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

Product Recommendations: Recommends products based on the category and purchase history:

@api_view(['GET'])
def recommend_products(request, product_id):
    # Logic for fetching related products

Create Order: Allows users to place orders:

    class CreateOrderView(APIView):
        def post(self, request):
            # Logic for creating an order

Docker Configuration

The Dockerfile sets up the environment and runs the Django app inside a container:

FROM python:3.12-alpine

WORKDIR /recommend_product

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

docker-compose.yml handles the orchestration of multiple containers:

version: '3.8'

services:
  web:
    build: .
    command: python manage.py migrate && python manage.py runserver 0.0.0.0:8000
    container_name: recommend_product
    volumes:
      - .:/recommend_product
    ports:
      - "8000:8000"