from django.urls import path
from . import views

urlpatterns = [
    path('/login',views.UserLoginAPIView.as_view(),name='user-login'),
    path('/sign-up', views.UserSignUpAPIView.as_view(), name='user-register'),
    path('/list',views.UserListAPIView.as_view(),name='user-list'),
    path('/<int:id>',views.UserUpdateDestroyAPIView.as_view(),name='user-update-delete'),
]
