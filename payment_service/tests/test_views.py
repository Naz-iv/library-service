from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from payment_service.views import PaymentViewSet


class ViewsTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="testpassword"
        )
        self.client = APIClient()
        self.refresh_token = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh_token.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_payment_successful(self):
        factory = APIRequestFactory()
        view = PaymentViewSet.as_view({"get": "payment_successful"})
        request = factory.get("/payments/success/1/")
        request.user = self.user
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 200)

    def test_payment_canceled(self):
        factory = APIRequestFactory()
        view = PaymentViewSet.as_view({"get": "payment_canceled"})
        request = factory.get("/payments/cancel/1/")
        request.user = self.user
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 400)
