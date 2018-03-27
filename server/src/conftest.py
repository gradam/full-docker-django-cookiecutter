import pytest

from common.generators import generate_user


@pytest.fixture
def normal_user(db):
    user = generate_user()
    user.save()
    return user
