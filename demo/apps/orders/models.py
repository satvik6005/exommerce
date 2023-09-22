from django.db import models
from users.models import User,adress
from products.models import Product
from django.utils import timezone


del_status=(
    ("1","delieverd"),
    ("2","not delieverd")
)

# Create your models here.
class order(models.Model):
    secret_key=models.CharField(max_length=20)
    order_id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    del_adress=models.ForeignKey(adress,on_delete=models.DO_NOTHING)
    final_price=models.PositiveIntegerField()
    status=models.CharField(max_length=20,choices=del_status,default="2")
    date=models.DateTimeField(default=timezone.now())
    order_placed=models.BooleanField(default=0)
    expired=models.BooleanField(default=0)



class product_order(models.Model):
    order=models.ForeignKey(order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    price=models.PositiveBigIntegerField()
    quantity=models.PositiveIntegerField()
