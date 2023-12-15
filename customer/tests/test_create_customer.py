from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient


class CustomerTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_customer(self):
        url = "/api/users/"
        data = {
            "email": "testuser@example.com",
            "password": "testpass",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["email"], "testuser@example.com")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="adminuser@example.com", password="adminpass"
        )
        self.assertTrue(admin_user.is_superuser)
