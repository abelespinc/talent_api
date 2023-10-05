from django.contrib.auth import get_user_model
from django.contrib.auth import login

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from talent.users.api.serializers import LoginSerializer
from talent.users.api.serializers import RegisterSerializer
from talent.users.api.serializers import UserSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class RegisterViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()


class LoginViewSet(ObtainAuthToken):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Login the user with the given username and password
        Return the user's authentication token
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)

        # Use the Django's login function to update the "last_login" field in User model
        login(request, user)

        return Response({"token": token.key})
