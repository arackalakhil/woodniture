from django.db import models
from products.models import products
from users.models import customuser

# Create your models here.
class cart(models.Model):
    cart_id = models.CharField(max_length=500, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class cart_item(models.Model): 
    user = models.ForeignKey(customuser, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    cart = models.ForeignKey(cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return (
            self.product.price * self.quantity
        )  # self means we are refering to the model cart_item ,product is the foreignkey of porduct model inside the product model we have the price

    def __str__(self):
        return self.product.name
