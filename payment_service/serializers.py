from rest_framework.serializers import ModelSerializer

from borrowing_service.serializers import BorrowingSerializer
from payment_service.models import Payment


class PaymentSerializer(ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"


class PaymentListSerializer(PaymentSerializer):
    borrowing = BorrowingSerializer()

    class Meta:
        model = Payment
        fields = (
            "borrowing",
            "money_to_be_paid",
            "payment_type",
            "money_to_be_paid"
        )
