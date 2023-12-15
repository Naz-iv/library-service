from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from payment_service.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class PaymentListSerializer(PaymentSerializer):
    borrowing = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = Payment
        fields = (
            "id",
            "borrowing",
            "money_to_be_paid",
            "payment_type",
            "status",
            "money_to_be_paid",
        )
