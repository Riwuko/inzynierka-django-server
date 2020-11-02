from django.urls import include, path
from users.api import views

urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]