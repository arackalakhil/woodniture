from telnetlib import STATUS
from tkinter import CASCADE
from django.db import models
from carts.models import cart_item
from products.models import products

from users.models import address, customuser

# Create your models here.
class payment(models.Model):
    user = models.ForeignKey(customuser,on_delete=models.CASCADE, null=True)
    payment_id = models.CharField(max_length=100, null=True)
    payment_method = models.CharField(max_length=100, null=True)
    amount =models.CharField(max_length=100, null=True)
    date =models.DateField(auto_now_add=True)
    status =models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return str(self.user)


 


class order(models.Model):
    STATUS =(('order conformed','order Confirmed'),
                ("shipped","shipped"),
                ("out for delivery","out for delivery"),
                ("delivered","delivered"),
                ("cancelled","cancelled"),
                ("returned","returned"))

    user = models.ForeignKey(customuser, on_delete=models.CASCADE, null=True)
    payment= models.ForeignKey(payment, on_delete=models.SET_NULL, blank=True, null=True)
    total = models.IntegerField(null=True)
    address = models.ForeignKey(address, on_delete=models.CASCADE, null=True)
    order_id = models.CharField(max_length=30000,null=True)
    date =models.DateField(null=True)
    status = models.CharField(max_length=100,choices=STATUS,default="order conformed",null=True)
    is_ordered = models.BooleanField(default=False)
    

    def __str__(self):
        return str(self.user) 






class order_product (models.Model):
    order =models.ForeignKey(order,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(customuser,on_delete=models.CASCADE,null=True)
    payment = models.ForeignKey(payment,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(products, on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(null=True)
    product_price = models.FloatField(null=True)
   
   
   
    def __str__(self):
        return str(self.product)
