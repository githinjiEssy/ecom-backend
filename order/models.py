from django.db import models
from django.core.validators import MinLengthValidator
from user_auth.models import User
from product.models import Product

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    address_line_one = models.CharField(max_length=256, validators=[MinLengthValidator(4)])
    address_line_two = models.CharField(max_length=256, validators=[MinLengthValidator(4)])
    city = models.CharField(max_length=256, validators=[MinLengthValidator(4)])
    country = models.CharField(max_length=256, validators=[MinLengthValidator(3)])
    postal_code = models.IntegerField(blank=False, null=False)
    status = models.CharField(max_length=10, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status
