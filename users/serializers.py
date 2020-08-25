from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(required=False)
    role = serializers.CharField(required=False)
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def validate_role(self, value):
        """
        Check if user's role is in ROLE_CHOICES('user' or 'moderator' or 'admin')
        """
        if value not in ["admin", "moderator", "user"]:
            raise ValidationError(
                "Allowed value for role is 'user' or 'moderator' or 'admin'"
            )
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            bio=validated_data.get("bio", ""),
            role=validated_data.get("role", "user"),
        )
        # create user or admin depending on role
        if validated_data.get("role") == "admin":
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = False
            user.is_superuser = False
        user.save()
        return user

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "bio", "role",]


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField()

    # for validation of uniqueness of email and username do not use built-in validators
    # because it will constraint users created by admin
    def validate_email(self, value):
        """
        Check uniqueness of email
        """
        username = self.initial_data.get("username")
        if User.objects.filter(email=value).exists():
            if not User.objects.filter(username=username, email=value).exists():
                raise ValidationError("The email must be unique")
        return value

    def validate_username(self, value):
        """
        Check uniqueness of username
        """
        email = self.initial_data.get("email")
        if User.objects.filter(username=value).exists():
            if not User.objects.filter(username=value, email=email).exists():
                raise ValidationError("The username must be unique")
        if value == "me":
            raise ValidationError("You cannot use 'me' as a username")
        return value

    class Meta:
        model = User
        fields = ["email", "username"]


class MyTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
    email = serializers.EmailField()

    def validate_confirmation_code(self, value):
        """
        Check confirmation code returned from user
        """
        # confirmation code generation using user's email and username
        email = self.initial_data.get("email", "")
        username = self.initial_data.get("username", "")
        if email and username:
            password = email + username
            response_code = make_password(
                password=password, salt="settings.SECRET_KEY", hasher="default"
            ).split("$")[-1]
            if response_code != value:
                raise ValidationError("The confirmation code is not correct.")
            return value
