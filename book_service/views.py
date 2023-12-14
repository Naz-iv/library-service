from rest_framework import viewsets

from book_service.models import Book
from book_service.permissions import IsAdminOrReadOnly
from book_service.serializers import BookListSerializer, BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        return BookSerializer
