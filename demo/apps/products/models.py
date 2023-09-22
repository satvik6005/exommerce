from django.db import models
# Create your models here.
from django.utils.translation import gettext_lazy  as _
from users.models import User






class Product(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=200)
    desc=models.CharField(max_length=1000, default='',blank=True)
    available_units=models.PositiveIntegerField(default=0)
    price_per_unit=models.PositiveIntegerField(null=True)
    supplier=models.ForeignKey(User,null=True,on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.name)

    @staticmethod
    def get_products(key):

        return Product.objects.filter(id__in=key)




class Product_image(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    image_link=models.URLField()
