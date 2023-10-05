from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "name", "is_superuser"]


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]


class LoginSerializer(AuthTokenSerializer):
    pass
