from django.urls import path
from . import views

urlpatterns = [

    path('/send-otp', views.SendOTPView.as_view(), name='send-otp'),
    path('/verify-otp', views.VerifyOTPView.as_view(), name='verify-otp'),

    path('/send-email-otp',views.SendEmailOTPView.as_view(),name='send-gmail-otp'),
    path('/verify-email-otp',views.VerifyEmailOTPView.as_view(),name='verify-gmail-otp')
]
