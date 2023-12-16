from django.db import transaction
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from borrowing_service.models import Borrowing
from payment_service.models import Payment
from payment_service.serializers import (
    PaymentSerializer,
    PaymentListSerializer
)
from payment_service.services import get_payment


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "pk",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "is_active"
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("book",)

    @transaction.atomic
    def create(self, validated_data):
        user = validated_data.get("user")
        borrowed_book = validated_data.get("book")

        if borrowed_book.inventory == 0:
            raise ValidationError("Sorry no books available!")

        pending_payments = Payment.objects.filter(
            Q(borrowing__user_id=user.id)
            & Q(status=Payment.PaymentStatus.PENDING)
        ).count()
        if pending_payments:
            raise ValidationError(
                "You must complete your pending payments "
                "before borrowing new book!"
            )

        borrowed_book.inventory -= 1
        borrowed_book.save()
        borrowing = Borrowing.objects.create(
            **validated_data
        )
        get_payment(borrowing)
        return borrowing


class BorrowingListSerializer(BorrowingSerializer):
    payments = PaymentListSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = Borrowing
        fields = (
            "pk",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "is_active",
            "payments"
        )


class BorrowingDetailSerializer(BorrowingSerializer):
    payments = PaymentSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = Borrowing
        fields = (
            "pk",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "is_active",
            "payments"
        )
