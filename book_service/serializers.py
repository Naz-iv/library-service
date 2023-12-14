from rest_framework import serializers

from book_service.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "title", "author", "available"
        )


RETURN_TERM = timezone.timedelta(days=14)


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "borrow_date", "expected_return_date", "actual_return_date", "book", "user")

    def create(self, validated_data):
        book_id = validated_data.pop("book")
        return Borrowing.objects.create(
            borrow_date=timezone.now().date,
            expected_return_date=timezone.now().date + RETURN_TERM,
            book=Book.objects.get(pk=book_id),
            **validated_data
        )

