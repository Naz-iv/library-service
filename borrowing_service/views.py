from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from borrowing_service.models import Borrowing
from borrowing_service.serializers import (
    BorrowingSerializer,
    BorrowingCreateSerializer,
)
from book_service.models import Book


class BorrowingViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Borrowing.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):

        if self.action == "create":
            return BorrowingCreateSerializer

        return BorrowingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
