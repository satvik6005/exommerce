from django.test import TestCase
from products.models import User,adress,cart,Product

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
    


class order:
    pass

