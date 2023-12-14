from rest_framework import serializers
from django.utils import timezone

from borrowing_service.models import Borrowing
from book_service.models import Book


RETURN_TERM = timezone.timedelta(days=14)


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "pk",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user"
        )

    def create(self, validated_data):
        return Borrowing.objects.create(
            **validated_data
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("book",)
