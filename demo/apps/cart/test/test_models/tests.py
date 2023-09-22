from django.test import TestCase
from products.models import Product
from users.models import *
from cart.models import *
from billing.models import *
from orders.models import *


class cartModelTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword'
        )

        # Create a product for testing
        self.product = Product.objects.create(
            name='Test Product',
            desc='Test Description',
            available_units=10,
            price_per_unit=50,
            supplier=self.user
        )

        # Create a cart item for testing
        self.cart_item = cart.objects.create(
            product=self.product,
            user=self.user,
            quantity=3
        )

    def test_cart_item_creation(self):
        # Test if the cart item instance was created successfully
        self.assertIsInstance(self.cart_item, cart)
        self.assertEqual(self.cart_item.product, self.product)
        self.assertEqual(self.cart_item.user, self.user)
        self.assertEqual(self.cart_item.quantity, 3)

    def test_cart_item_quantity_defaults_to_1(self):
        # Test if the 'quantity' field defaults to 1 when not specified
        cart_item_no_quantity = cart.objects.create(
            product=self.product,
            user=self.user
        )
        self.assertEqual(cart_item_no_quantity.quantity, 1)
