from django.db import models


#category model
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

#product model
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.name

#USer model
class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


#Order model #There could be many more things in Order like order_status,quantity,delivery_address

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user}"
