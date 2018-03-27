import pytest
from django.core.exceptions import ValidationError

from accounts.models import User, username_validator


class TestUserNameValidator:
    def test_valid_username(self):
        username_validator('abcde234')

    def test_long_username(self):
        username_validator('a'*15)

    def test_short_username(self):
        username_validator('a'*3)

    def test_too_long_username(self):
        with pytest.raises(ValidationError):
            username_validator('a'*16)

    def test_too_short_username(self):
        with pytest.raises(ValidationError):
            username_validator('a')

    def test_not_alphanumeric_username(self):
        with pytest.raises(ValidationError):
            username_validator('hdfg#@$*&((@')


class TestUserModel:

    def test_user(self, normal_user):
        pass

    @pytest.mark.django_db
    def test_save_model(self, normal_user):
        normal_user.save()

    def test_short_name(self, normal_user):
        normal_user.first_name = None
        assert normal_user.get_short_name() == normal_user.username
        normal_user.first_name = 'someone'
        assert normal_user.get_short_name() == normal_user.first_name

    def test_full_name(self, normal_user):
        normal_user.first_name = None
        assert normal_user.get_full_name() == normal_user.username
        normal_user.first_name = 'someone'
        normal_user.last_name = 'someone'
        assert normal_user.get_full_name() == 'someone someone'


@pytest.mark.django_db
class TestUserManager:
    def test_create_user(self):
        email = 'something@c.c'
        user = User.objects.create_user(username='somehting', email=email)
        assert user == User.objects.get(email=email)

    def test_create_superuser(self):
        email = 'something@c.c'
        user = User.objects.create_superuser(username='somehting', email=email, password='test')
        assert user == User.objects.get(email=email)
        assert user.is_superuser
