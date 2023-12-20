import stripe
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets

from core.permissions import IsAdminOrReadOnly
from payment_service.serializers import (
    PaymentListSerializer,
    PaymentSerializer
)

from payment_service.models import Payment
from payment_service.services import (
    get_checkout_session,
    successful_payment_notification
)

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        queryset = self.queryset.select_related(
            "borrowing", "borrowing__book", "borrowing__user"
        )
        if (not self.request.user.is_staff
                or not self.request.user.is_superuser):
            return self.queryset.filter(borrowing__user=self.request.user)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PaymentListSerializer
        return PaymentSerializer

    @action(methods=["GET"], url_path="success", detail=True)
    def payment_successful(self, request, pk: None):
        """Endpoint for redirection after successful payment"""
        if not request.user.is_authenticated:
            return Response(
                {"status": "Unauthorized",
                 "message": "Please authenticate to access resource!"},
                status=401,
            )

        payment = self.get_object()
        session = stripe.checkout.Session.retrieve(payment.session_id)

        status = session.status
        if status != "complete":

            return Response(
                {"status": "fail",
                 "message": "Payment failed, please complete payment "
                            "within 24 hours from book borrowing time!"},
                status=400,
            )
        payment.status = payment.PaymentStatus.PAID
        payment.save()

        successful_payment_notification(payment)

        return Response(
            {
                "status": "success",
                "message": "Payment was completed successfully",
            },
            status=200,
        )

    @action(methods=["GET"], url_path="cancel", detail=True)
    def payment_canceled(self, request, pk: None):
        """Endpoint for redirection after payment was canceled or failed"""
        return Response(
            {"status": "fail",
             "message": "Payment was canceled. Please complete payment "
                        "within 24 hours from book borrowing time!"},
            status=400,
        )

    @action(methods=["POST"], url_path="renew-session", detail=True)
    def renew_checkout(self, request, pk: None):
        """Endpoint for renewing checkout session if it expired"""
        payment = self.get_object()
        new_session = get_checkout_session(payment.borrowing, payment.id)

        if new_session.status != "open":
            raise stripe.error.StripeError

        payment.session_id = new_session.id
        payment.url = new_session.url
