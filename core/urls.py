"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
<<<<<<< HEAD
    path("api/book_service", include("book_service.urls", namespace="book_service")),
    path("api/borrowing_service", include("borrowing_service.urls", namespace="borrowing_service")),
=======
    path("api/book_service", include("book_service.urls",
                                     namespace="book_service")),
>>>>>>> 7c77e26465b5e2afb037591098b4e432fb3b183b

]
