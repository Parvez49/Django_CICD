from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from rest_framework_simplejwt.tokens import RefreshToken
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    receive_message = models.BooleanField(default=False)

    fname = models.CharField(max_length=50, blank=True, null=True)
    lname = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)  # unchangeable later
    city = models.CharField(max_length=100, blank=True, null=True)
    gender = models.JSONField(null=True, blank=True)
    sexuality = models.JSONField(null=True, blank=True)
    relationship = models.JSONField(null=True, blank=True)
    education_level = models.JSONField(null=True, blank=True)
    career_field = models.JSONField(null=True, blank=True)
    income_range = models.JSONField(null=True, blank=True)
    religious_status = models.JSONField(null=True, blank=True)
    political_views = models.JSONField(null=True, blank=True)
    smoke_status = models.JSONField(null=True, blank=True)
    favourite_drink = models.JSONField(null=True, blank=True)
    dietary_preferences = models.JSONField(null=True, blank=True)
    exersize_week = models.JSONField(null=True, blank=True)
    hobbies_interests = models.JSONField(null=True, blank=True)
    like_traveling = models.JSONField(null=True, blank=True)
    pet = models.JSONField(null=True, blank=True)
    children_number = models.JSONField(null=True, blank=True)
    live_place = models.JSONField(null=True, blank=True)
    communication_style = models.JSONField(null=True, blank=True)
    love_language = models.JSONField(null=True, blank=True)
    personality = models.JSONField(null=True, blank=True)
    culture = models.JSONField(null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    @staticmethod
    def get_by_email_or_phone(email_or_phone):
        try:
            return User.objects.get(
                Q(email=email_or_phone) | Q(phone_number=email_or_phone)
            )
        except ObjectDoesNotExist:
            return None


class UserMedia(models.Model):
    MEDIA_TYPE_CHOICES = (
        ("image", "Image"),
        ("video", "Video"),
    )

    user = models.ForeignKey(User, related_name="media_files", on_delete=models.CASCADE)
    media_type = models.CharField(
        max_length=10, choices=MEDIA_TYPE_CHOICES, blank=True, null=True
    )
    file = models.FileField(upload_to="user_file/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.media_type} - {self.created_at}"
