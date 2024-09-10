from django.urls import path
from . import views

urlpatterns = [
    path("/hello", views.HelloWorldAPIView.as_view(), name="hello-word"),
    path("/login", views.UserLoginAPIView.as_view(), name="user-login"),
    path("/sign-up", views.UserSignUpAPIView.as_view(), name="user-register"),
    path("/list", views.UserListAPIView.as_view(), name="user-list"),
    path(
        "/<int:id>", views.UserUpdateDestroyAPIView.as_view(), name="user-update-delete"
    ),
]
