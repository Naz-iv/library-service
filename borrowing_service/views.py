from django.utils import timezone
from django.db import transaction
from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrowing_service.models import Borrowing
from borrowing_service.serializers import (
    BorrowingSerializer,
    BorrowingCreateSerializer,
)


class BorrowingViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Borrowing.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if not self.request.user.is_superuser:
            queryset = self.queryset.filter(user=self.request.user)
        else:
            queryset = self.queryset
            user_id = self.request.query_params.get("user_id")
            if user_id:
                queryset = queryset.filter(user__id=user_id)
        is_active = str(self.request.query_params.get("is_active"))

        if is_active == "True":
            queryset = queryset.filter(is_active=True)
        elif is_active == "False":
            queryset = queryset.filter(is_active=False)
        return queryset

    def get_serializer_class(self):

        if self.action == "create":
            return BorrowingCreateSerializer
        return BorrowingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@transaction.atomic
def borrowing_return(request, pk):
    borrowing = Borrowing.objects.get(pk=pk)

    if request.method == "POST":
        if borrowing.is_active:
            borrowing.is_active = False
            borrowing.expected_return_date = timezone.now()
            borrowing.book.inventory += 1
            borrowing.book.save()
            borrowing.save()

            return Response(
                {"status": "success", "message":
                    "Thank you! The book is returned "},
                status=200
            )

        return Response(
            {"status": "fail", "message": "Book is already returned"},
            status=400
        )
