from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request

from common.exceptions import OwnerError

User = get_user_model()


class IsOwnerOrAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request: Request, view, obj) -> bool:
        if request.method in SAFE_METHODS:
            return True

        owner = get_object_owner(obj)
        return is_admin(request.user) or request.user == owner


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request: Request, view, obj) -> bool:
        owner = get_object_owner(obj)
        return is_admin(request.user) or request.user == owner


def get_object_owner(obj) -> User:
    if isinstance(obj, get_user_model()):
        return obj
    else:
        return obj.user
    raise OwnerError(f'Can\'t find the owner of {obj}')


def is_admin(user: User) -> bool:
    return user.is_superuser
