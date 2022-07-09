
from django.db import models

# Create your models here.
class categories(models.Model):
    category_name = models.CharField(max_length = 300)
    des = models.TextField()
    stock = models.IntegerField(null=True)

    def __str__(self):
        return self.category_name

class products(models.Model):
    name = models.CharField(max_length=300)
    des = models.TextField()
    img = models.CharField(max_length=3000)
    price = models.IntegerField()
    stock = models.IntegerField(null=True)
    cats = models.ForeignKey(categories,on_delete=models.CASCADE,null=True,blank=True)
    



