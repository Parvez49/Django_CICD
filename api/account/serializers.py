from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User, UserMedia


class LoginSerializer(serializers.ModelSerializer):
    email_or_phone = serializers.CharField()

    class Meta:
        model = User
        fields = ("email_or_phone", "password")

    def validate(self, attrs):
        email_or_phone = attrs.get("email_or_phone")
        password = attrs.get("password")

        if not email_or_phone or not password:
            raise serializers.ValidationError(
                "Both email or phone and password are required."
            )

        # user = authenticate(email=email, password=password)
        user = User.get_by_email_or_phone(email_or_phone)
        if user is None:
            raise serializers.ValidationError("Invalid email or password.")

        attrs["user"] = user
        return attrs


class UserMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserMedia
        fields = ("id", "file")


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    media_files = UserMediaSerializer(many=True, read_only=True)
    files_input = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "phone_number",
            "receive_message",
            "fname",
            "lname",
            "date_of_birth",
            "city",
            "gender",
            "sexuality",
            "relationship",
            "education_level",
            "career_field",
            "income_range",
            "religious_status",
            "political_views",
            "smoke_status",
            "favourite_drink",
            "dietary_preferences",
            "exersize_week",
            "hobbies_interests",
            "like_traveling",
            "pet",
            "children_number",
            "live_place",
            "communication_style",
            "love_language",
            "personality",
            "culture",
            "media_files",
            "files_input",
        )
        extra_kwargs = {"password": {"write_only": True, "required": False}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()

        files = validated_data.pop("files_input", [])
        # user = super().create(validated_data)
        for file in files:
            UserMedia.objects.create(user=user, file=file)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password is not None:
            instance.set_password(password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        files = validated_data.pop("files_input", [])
        # instance = super().update(instance, validated_data)
        if files:
            instance.media_files.all().delete()
            for file in files:
                UserMedia.objects.create(user=instance, file=file)

        instance.save()
        return instance
