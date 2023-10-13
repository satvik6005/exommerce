from django.test import TestCase
from users.models import User
from products.models import Product

class ProductTest(TestCase):
    def test_create_product_valid_data_superuser(self):
            # Create a valid product data
            data = {
                'name': 'Test Product',
                'price': 10.99,
                'description': 'Test description',
            }

            # Create a superuser
            user = User.objects.create_superuser(email='testuser', password='testpassword')
            self.client.force_authenticate(user=user)

            # Send a POST request to create a new product
            response = self.client.post('/create-product/', data=data)

            # Assert that the response status code is 201 (Created)
            assert response.status_code == 201
            # Assert that the product is created in the database
            assert Product.objects.filter(name='Test Product').exists()

        # Retrieve a product with valid ID and valid query parameters
    def test_retrieve_product_with_valid_id_and_valid_query_parameters(self):
        # Create a valid product ID and valid query parameters
        product_id = 1
        query_params = {
            'param1': 'value1',
            # Add more valid query parameters here
        }

        # Call the retrieve API view with the valid product ID and query parameters
        response = self.client.get(f'/products/{product_id}/', query_params)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the response data matches the expected data
        expected_data = {
            'id': 1000,
            # Add more expected fields here
        }
        self.assertEqual(response.data, expected_data)

        # Returns a list of all products when no search query is provided
    def test_no_search_query(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), len(Product.objects.all()))
