from config.celery import app
from .models import order,Product,product_order
from django.db.models import F

@app.task
def check_order(order_id):
    print("task is running")
    Order=order.objects.get(order_id=order_id)
    if Order.order_placed==0:
        Order.expired=1
        Order.save()
        products=product_order.objects.filter(order=order_id)
        
        
        for product in products:
                print(product.product.id)
                print(Product.objects.filter(id=product.product.id).update(available_units=F('available_units')+product.quantity))
        




    



