from django.urls import path, include
from rest_framework import routers

from book_service import views

router = routers.DefaultRouter()
router.register("books", views.BookViewSet)

urlpatterns = [
    path("/", include(router.urls))
]

app_name = "book_service"
