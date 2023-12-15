from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from borrowing_service.models import Borrowing


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
        if user.borrowings.filter(is_active=True).count():
            raise ValidationError("You must return your active borrowing!")
        borrowed_book.inventory -= 1
        borrowed_book.save()
        return Borrowing.objects.create(
            **validated_data
        )
