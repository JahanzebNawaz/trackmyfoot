from django.db import models  # noqa: F401
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


def upload_profile(instance, filename):
    return "Profiles/{user}/{filename}".format(user='{0}_{1}'.format(instance.first_name, instance.last_name),
                                               filename=filename)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_image = models.ImageField(
                        upload_to=upload_profile,
                        default='Profiles/user/user.png',
                        null=True, blank=True
    )
    phone_no = models.CharField(max_length=14)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    def __str__(self):
        return self.email

