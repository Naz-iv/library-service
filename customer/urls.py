from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CreateCustomerView, ManageCustomerView

urlpatterns = [
    path("", CreateCustomerView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", ManageCustomerView.as_view(), name="manage"),
]

app_name = "customer"
