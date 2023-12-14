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

    def get_queryset(self):
        """Retrieve books with specific title or author"""

        title = self.request.query_params.get("title")
        author = self.request.query_params.get("author")

        if title:
            self.queryset = self.queryset.filter(title__icontains=title)

        if author:
            self.queryset = self.queryset.filter(author__icontains=author)

        return self.queryset
