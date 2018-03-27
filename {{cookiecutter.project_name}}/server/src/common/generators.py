import delorean
from django.db.utils import IntegrityError
from faker import Faker

from accounts.models import User


def generate_user(is_superuser=False, password=None, save=True):
    fake = Faker()

    while True:
        first_name = fake.first_name()
        last_name = fake.last_name()
        simple_profile = fake.simple_profile()
        username = simple_profile['username']
        birth_date = simple_profile['birthdate']
        birth_date = delorean.parse(birth_date).datetime
        email = simple_profile['mail']
        gender = simple_profile['sex']
        password = password if password else 'haslo1234'
        user_data = dict(username=username, first_name=first_name, password=password,
                         last_name=last_name, email=email, is_superuser=is_superuser,
                         is_staff=is_superuser, birth_date=birth_date, gender=gender)
        if save:
            try:
                return User.objects.create(**user_data)
            except IntegrityError:
                pass
        else:
            return User(**user_data)
