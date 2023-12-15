from django.urls import path

from payment_service.views import CreateCheckoutSessionView

urlpatterns = [
    path(
        "create-checkout-session/<pk:int>/",
        CreateCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
]

app_name = "payment_service"
