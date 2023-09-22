from django.test import TestCase
from products.models import Product
from users.models import *
from cart.models import *
from billing.models import *
from orders.models import *

class user_test(TestCase):
    def test_create_user(self):
        # Test creating a user
        user = User.objects.create_user(
            email='test@example.com',
            password='testpassword'
        )

        # Check if the user was created successfully
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpassword'))

    def test_create_superuser(self):
        # Test creating a superuser
        superuser = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword'
        )
        self.assertIsInstance(superuser, User)
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertTrue(superuser.check_password('adminpassword'))
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

    def test_user_soft_delete(self):
        user = User.objects.create_user(
            email='test@example.com',
            password='testpassword'
        )
        user.delete()
        self.assertTrue(user.is_deleted)
        self.assertEqual(0,len(User.objects.filter(id=user.id)))
        self.assertEqual(1,len(User.objects.filter_deleted()))
        self.assertEqual(user.id,User.objects.get_deleted(id=user.id).id)


        for i in User.objects.all():
            self.assertNotEqual(user.id,i.id)
        user.restore()
        self.assertFalse(user.is_deleted)










class adressModelTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )

        # Create an adress instance for testing
        self.adress = adress.objects.create(
            user=self.user,
            zipcode=12345,
            houseno=123,
            locality='Test Locality',
            city='Test City',
            state='Test State'
        )

    def test_adress_creation(self):
        # Test if the adress instance was created successfully
        self.assertIsInstance(self.adress, adress)
        self.assertEqual(self.adress.zipcode, 12345)
        self.assertEqual(self.adress.houseno, 123)
        self.assertEqual(self.adress.locality, 'Test Locality')
        self.assertEqual(self.adress.city, 'Test City')
        self.assertEqual(self.adress.state, 'Test State')

    def test_adress_user_relation(self):
        # Test the relationship between adress and User
        self.assertEqual(self.adress.user, self.user)

  # Replace 'myapp' with your actual app name
