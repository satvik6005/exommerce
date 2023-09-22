from django.test import TestCase
from rest_framework.test import APIClient as Client
from products.models import Product
from users.models import *
from cart.models import *
from billing.models import *
from orders.models import *
from rest_framework import status
from knox.models import AuthToken as Token
import json


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_registration_view(self):
        data = {"email": "satvik.goyal@scalereal.com", "password": "newuserpassword"}
        response = self.client.post("/register/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", json.loads(response.content))

    def test_login_view(self):
        data = {"email": "newuser@example.com", "password": "newuserpassword"}
        response = self.client.post("/register/", data, format="json")
        response = self.client.post("/login/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", json.loads(response.content))

    def test_update_user_view(self):
        data = {"email": "newuser@example.com", "password": "newuserpassword"}
        response = self.client.post("/register/", data, format="json")
        token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        data = {"first_name": "NewFirst", "last_name": "NewLast", "authorization": 1}
        response = self.client.put(
            "/users/update/" ,data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.user.refresh_from_db()
        # self.assertEqual(self.user.first_name, 'NewFirst')
        # self.assertEqual(self.user.last_name, 'NewLast')
        # self.assertEqual(self.user.authorization, 1)

    def test_retrieve_user_view(self):
        data = {"email": "newuser@example.com", "password": "newuserpassword"}
        response = self.client.post("/register/", data, format="json")
        user_id = response.data["id"]
        user_email = response.data["user"]["email"]
        token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response = self.client.get("/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], user_id)
        self.assertEqual(response.data["email"], user_email)

    def test_create_address_view(self):
        data = {"email": "newuser@example.com", "password": "newuserpassword"}
        response = self.client.post("/register/", data, format="json")
        token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        data = {
            "user": response.data["id"],
            "zipcode": 12345,
            "houseno": 123,
            "locality": "Test Locality",
            "city": "Test City",
            "state": "Test State",
        }
        response = self.client.post("/addresses/create/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Add additional assertions for the created address

    def test_retrieve_address_view(self):
        data = {"email": "newuser@example.com", "password": "newuserpassword"}
        response = self.client.post("/register/", data, format="json")
        token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response = self.client.get(
            "/addresses/"
        )  # Replace address_pk with an actual address ID
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add additional assertions for the retrieved address

    def test_create_product_view(self):
        data = {"email": "newuser@example.com", "password": "newuserpassword"}
        response = self.client.post("/register/", data, format="json")
        token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        data = {
            "name": "Test Product",
            "desc": "Description for Test Product",
            "available_units": 10,
            "price_per_unit": 50,
            "supplier": response.data["id"],
        }
        response = self.client.post("/products/create/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_product_view(self):
        data = {"email": "newuser@example.com", "password": "newuserpassword"}
        response = self.client.post("/register/", data, format="json")
        token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        product = Product.objects.create(
            name="Test Product",
            desc="Description for Test Product",
            available_units=10,
            price_per_unit=50,
            supplier=User.objects.get(pk=response.data["id"]),
        )
        response = self.client.get("/products/{}/".format(product.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_cart_view(self):
        data = {"email": "newuser@example.com", "password": "newuserpassword"}
        response = self.client.post("/register/", data, format="json")
        token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        product = Product.objects.create(
            name="Test Product",
            desc="Description for Test Product",
            available_units=10,
            price_per_unit=50,
            supplier=User.objects.get(pk=response.data["id"]),
        )
        data = {"product": product.pk, "user": response.data["id"], "quantity": 2}
        response = self.client.post("/carts/create/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_cart_view(self):
        data = {"email": "newuser@example.com", "password": "newuserpassword"}
        response = self.client.post("/register/", data, format="json")
        token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        product = Product.objects.create(
            name="Test Product",
            desc="Description for Test Product",
            available_units=10,
            price_per_unit=50,
            supplier=User.objects.get(pk=response.data["id"]),
        )
        cart_item = cart.objects.create(
            product=product, user=User.objects.get(pk=response.data["id"]), quantity=3
        )
        response = self.client.get("/carts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def order_test_no_cart(self):
        data = {"email": "newuser@example.com", "password": "newuserpassword"}
        response = self.client.post("/register/", data, format="json")
        token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        data = {
            "user": User.objects.get(pk=response.data["id"]),
            "zipcode": 12345,
            "houseno": 123,
            "locality": "Test Locality",
            "city": "Test City",
            "state": "Test State",
        }
        adres=adress.objects.create(**data)
        product = Product.objects.create(
            name="Test Product",
            desc="Description for Test Product",
            available_units=10,
            price_per_unit=50,
            supplier=User.objects.get(pk=response.data["id"]),
        )
        data={
        "cart":False,
        "product": product.id,
        "quantity": 2,
        "del_adress":adres.id
        }
        response=self.client.post("/order/",data=data,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1,order.objects.get(id=response.data['id']))

    def order_test_cart(self):
        data = {"email": "newuser@example.com", "password": "newuserpassword"}
        response = self.client.post("/register/", data, format="json")
        token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        data = {
            "user": User.objects.get(pk=response.data["id"]),
            "zipcode": 12345,
            "houseno": 123,
            "locality": "Test Locality",
            "city": "Test City",
            "state": "Test State",
        }
        adres=adress.objects.create(**data)
        product = Product.objects.create(
            name="Test Product",
            desc="Description for Test Product",
            available_units=10,
            price_per_unit=50,
            supplier=User.objects.get(pk=response.data["id"]),
        )
        cart_item = cart.objects.create(
            product=product, user=User.objects.get(pk=response.data["id"]), quantity=3
        )
        data={
        "cart":True,
        "del_adress":adres.id
        }
        response=self.client.post("/order/",data=data,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1,order.objects.get(id=response.data['id']))


    def checke_change_password(self):
        data = {"email": "newuser@example.com", "password": "newuserpassword"}
        response = self.client.post("/register/", data, format="json")
        token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        data={
    "current_password":"newuserpassword",
    "new_password":"hello",
    "re_new_password":"hello"
}
        self.client.post("/change_password/",data,format='json')
        self.assertEqual(response.status_code, 204)










    # def test_delete_user_view(self):
    #     data = {"email": "newuser@example.com", "password": "newuserpassword"}
    #     response = self.client.post("/register/", data, format="json")
    #     token = response.data["token"]

    #     self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
    #     response=self.client.delete("users/delete/",data={},format="json")
    #     self.assertEqual(response.status_code,status.HTTP_200_OK)
