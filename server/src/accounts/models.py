import re

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


def username_validator(username):
    regex = re.compile(r'^[a-zA-Z0-9]{3,15}$')
    if not regex.match(username):
        raise ValidationError('3 to 15 characters. Letters and digits.')


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
        An abstract base class implementing a fully featured User model with
        admin-compliant permissions.

        Username and password are required. Other fields are optional.
        """

    GENDERS = [('F', 'Female'),
               ('M', 'Male')]

    # Base fields
    username = models.CharField(
        _('username'),
        max_length=30,
        unique=True,
        help_text=_('Required. 3 to 15 characters. Letters and digits.'),
        validators=[username_validator],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(
        _('email address'),
        blank=False,
        unique=True,
        error_messages={
            'unique': _('A user with that email already exists.'),
        },
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. Deselect this instead of deleting accounts.',
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    # Other fields
    gender = models.CharField(max_length=1, choices=GENDERS, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        if self.first_name and self.last_name:
            full_name = '{} {}'.format(self.first_name, self.last_name)
        else:
            full_name = self.username
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        if self.first_name:
            return self.first_name
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)
