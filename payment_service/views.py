import stripe
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
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


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.prefetch_related("borrowing")

    def get_queryset(self):
        if not self.request.user.is_staff or not self.request.user.is_superuser:
            return self.queryset.filter(borrowing__user=self.request.user.id)
        return self.queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PaymentListSerializer
        return PaymentSerializer

    @action(
        methods=["GET"],
        url_path="success",
        detail=True
    )
    def payment_successful(self, request, pk: None):
        payment = get_object_or_404(Payment, id=pk)
        payment.status = "paid"
        payment.save()
        return Response(
            {"status": "success",
             "message": f"Payment was completed successfully. Payment ID: {pk}"},
            status=200
        )

    @action(
        methods=["GET"],
        url_path="cancel",
        detail=True
    )
    def payment_canceled(self, request, pk: None):
        return Response(
            {"status": "fail",
             "message": f"Payment was canceled. Payment id: {pk}"},
            status=400
        )
