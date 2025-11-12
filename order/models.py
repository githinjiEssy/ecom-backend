from django.db import models
from django.core.validators import MinLengthValidator
from user_auth.models import User
from product.models import Product

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status
