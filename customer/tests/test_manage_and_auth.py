from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


class ManageCustomerViewTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@example.com",
            password="testpassword"
        )
        self.client = APIClient()
        self.refresh_token = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh_token.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_retrieve_customer_profile(self):
        response = self.client.get('/api/users/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_update_customer_profile(self):
        new_data = {"first_name": "New", "last_name": "Name"}
        response = self.client.patch('/api/users/me/', new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, new_data["first_name"])
        self.assertEqual(self.user.last_name, new_data["last_name"])

    def test_update_customer_profile_unauthenticated(self):
        unauthenticated_client = APIClient()
        response = unauthenticated_client.patch('/api/users/me/', {"first_name": "New"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
