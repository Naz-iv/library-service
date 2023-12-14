<<<<<<< HEAD:customer/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import CustomerSerializer


class CreateCustomerView(generics.CreateAPIView):
    serializer_class = CustomerSerializer


class ManageCustomerView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
=======
from django.shortcuts import render

# Create your views here.
>>>>>>> 7c77e26465b5e2afb037591098b4e432fb3b183b:borrowing_service/views.py
