from django.test import TestCase
from products.models import Product
from users.models import *
from cart.models import *
from billing.models import *
from orders.models import *


class ProductModelTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword'
        )

        # Create a product instance for testing
        self.product = Product.objects.create(
            name='Test Product',
            desc='Test Description',
            available_units=10,
            price_per_unit=50,
            supplier=self.user
        )

    def test_product_creation(self):
        # Test if the product instance was created successfully
        self.assertIsInstance(self.product, Product)
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.desc, 'Test Description')
        self.assertEqual(self.product.available_units, 10)
        self.assertEqual(self.product.price_per_unit, 50)
        self.assertEqual(self.product.supplier, self.user)

    def test_get_product(self):
        keys=[]
        for i in range(0,10):
            keys.append(Product.objects.create(
            name='Test Product',
            desc='Test Description',
            available_units=10,
            price_per_unit=50,
            supplier=self.user
        ).id)
        res=Product.get_products(keys)
        self.assertEqual(len(res),len(keys))
        for i in range(0,len(res)):
            self.assertEqual(keys[i],res[i].id)
            self.assertEqual('Test Product',res[i].name)
            self.assertEqual('Test Description',res[i].desc)
