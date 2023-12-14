from django.urls import path, include
from rest_framework import routers

from borrowing_service import views

router = routers.DefaultRouter()
router.register("borrowings", views.BorrowingViewSet)

urlpatterns = [
    path("/", include(router.urls))
]

app_name = "borrowing_service"
