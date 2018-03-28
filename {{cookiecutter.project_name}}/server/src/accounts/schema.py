import graphene

from graphene_django.types import DjangoObjectType
from accounts.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query:
    all_users = graphene.List(UserType)

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()
