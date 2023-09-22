from django.db import models
from products.models import Product
from users.models import User

# Create your models here.
class cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    @staticmethod
    def cart_product(id):
        return Product.get_products([i.product.id for i in cart.objects.filter(user=id)])
    @staticmethod
    def cart_objects(id):
        return cart.objects.filter(user=id)
