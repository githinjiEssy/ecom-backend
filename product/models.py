from django.db import models
from django.core.validators import MinLengthValidator
from user_auth.models import User


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    product_title = models.CharField( max_length=256 ,validators=[MinLengthValidator(10)])
    product_description = models.TextField(max_length=256, validators=[MinLengthValidator(30)])
    product_price = models.CharField(max_length=6)
    product_qty = models.IntegerField(default=0)
    product_image_url = models.CharField(max_length=256, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.product_title
