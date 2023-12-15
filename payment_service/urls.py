from django.urls import path, include
from rest_framework import routers

from payment_service.views import CreateCheckoutSessionView, PaymentViewSet

router = routers.DefaultRouter()
router.register("payments", PaymentViewSet, basename="payments")

urlpatterns = [
    path(
        "create-checkout-session/<int:pk>/",
        CreateCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
    path("", include(router.urls))
]

app_name = "payment_service"
