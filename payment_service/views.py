import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework import viewsets
from payment_service.serializers import (
    PaymentListSerializer,
    PaymentSerializer
)

from payment_service.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        payment_id = self.kwargs["pk"]
        payment = get_object_or_404(Payment, id=payment_id)
        return JsonResponse({
            "id": payment.session_id
        })


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return PaymentListSerializer
        return PaymentSerializer
