import graphene

from graphene_django.types import DjangoObjectType
from accounts.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query:
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.Int(), email=graphene.String())

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')
        email = kwargs.get('email')

        if id is not None:
            return User.objects.get(id=id)

        if email is not None:
            return User.objects.get(email=email)
