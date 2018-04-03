{%- if cookiecutter.drf == 'yes' %}
from rest_framework import mixins, generics, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.serializers import CreateUserSerializer, UserSerializer, ChangePasswordSerializer


class Users(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Implements an endpoint for retrieving users
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    lookup_field = 'username'


class CreateAccount(generics.CreateAPIView):
    """
    Implements an endpoint for creating new account
    """
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


class MyAccount(generics.RetrieveUpdateDestroyAPIView):
    """
    Implements an endpoint for retrieving, updating and deleting own account
    """
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj


class ChangePassword(generics.UpdateAPIView):
    """
    Implements an endpoint for changing password
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs) -> Response:
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response("Success.", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ValidateUniqueFields(APIView):
    """
    View to check the uniqueness of user fields passed as query params

    * No authentication is required to access this view.

    """

    permission_classes = (AllowAny,)

    def get(self, request, format=None) -> Response:
        """
        Implements an endpoint to check if the given user field values are unique

        Use query parameters to specify filter criteria. If multiple values are associated
        with one field, it takes only the first one. The check is case insensitive.

        Returns:
            (Response): Response that wraps a dict of str: str. Each key corresponds to a field,
                value is either 'valid' if the field is unique or 'invalid' otherwise.

        """
        params = dict(self.request.query_params)

        if not params:
            return Response('[BAD REQUEST] No query parameters were specified',
                            status=status.HTTP_400_BAD_REQUEST)

        response = {}
        for field, values in params.items():
            value = values[0]  # validate only the first value associated with a field
            kwarg = f'{field}__iexact'  # case insensitive

            response[field] = ['valid', 'invalid'][User.objects.filter(**{kwarg: value}).exists()]

        return Response(response)
{%- endif %}
