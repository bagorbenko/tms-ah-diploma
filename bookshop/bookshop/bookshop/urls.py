from books.views import (
    AuthorAPIView,
    BookAPIView,
    CategoryAPIView,
    GenreAPIView,
    PublisherAPIView,
)
from cart.views import CartAPIView, CartItemAPIView
from django.contrib import admin
from django.urls import include, path, re_path
from django.http import JsonResponse
from order.views import OrderAPIView
from rest_framework.routers import DefaultRouter
from user.views import RegistrationAPIView, UserAPIView, LoginSuccessView

from .yasg import urlpatterns as doc_urls


def health_check(request):
    return JsonResponse({"service": "Bookshop", "status": "healthy"})

router = DefaultRouter()
router.register(r"books", BookAPIView, basename="books")
router.register(r"authors", AuthorAPIView, basename="author")
router.register(r"genres", GenreAPIView, basename="genres")
router.register(r"publishers", PublisherAPIView, basename="publishers")
router.register(r"categories", CategoryAPIView, basename="categories")
router.register(r"carts", CartAPIView, basename="carts")
router.register(r"cart_items", CartItemAPIView, basename="cartitems")
router.register(r"customers", UserAPIView, basename="customers")
router.register(r"orders", OrderAPIView, basename="orders")


urlpatterns = [
    path("", health_check, name="health_check"),
    path(
        "admin/",
        admin.site.urls,
    ),
    path("api/drf-auth/", include("rest_framework.urls")),
    path("api/login-success/", LoginSuccessView.as_view()),
    path("api/", include(router.urls)),
    path(r"api/auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
    path("api/registration/", RegistrationAPIView.as_view(), name="registration"),
]

urlpatterns += doc_urls
