from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core import mail
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import MyTokenSerializer, SignUpSerializer, UserSerializer


class MyTokenObtainPairView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = MyTokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get("username")
            email = serializer.data.get("email")
            user, created = User.objects.get_or_create(username=username, email=email)
            data = self.get_tokens_for_user(user)
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class ApiUserViewSet(viewsets.ModelViewSet):
    """
    List all users, or create a new user.
    Retrieve, update or delete selected user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAdminUser]
    lookup_field = "username"

    def partial_update(self, request, username):
        user = User.objects.get(username=username)
        role = request.data.get("role", None)
        if role is not None:
            # create user or admin depending on role
            if role == "admin":
                user.is_staff = True
                user.is_superuser = True
            else:
                user.is_staff = False
                user.is_superuser = False
            user.save()
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(APIView):
    """
    Get and patch your profile
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = self.request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, format=None):
        # Do not allow to change username, email and role in profile
        for item in request.data.keys():
            if item in ["username", "email", "role"]:
                raise ValidationError(
                    "You cannot change username, email and role in profile"
                )
        user = self.request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUpEmail(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get("email")
            username = serializer.data.get("username")
            self.send_mail(email, username)
            return Response(
                {"detail": "Confirmation code was sent to your email"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_mail(self, email, username):
        # confirmation code generation using user's email and username
        password = email + username
        confirmation_code = make_password(
            password=password, salt="settings.SECRET_KEY", hasher="default"
        ).split("$")[-1]
        mail.send_mail(
            "Sign up new user",
            f"Your confirmation code is {confirmation_code}",
            "yatube@mail.ru",
            [email],
            fail_silently=False,
        )
