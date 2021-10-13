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

GENDER = [('Male', 'Male'), ('Female', "Female")]
 

class User(AbstractUser):
    # username 
    # first_name
    # last_name
    # password
    # password2
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_image = models.ImageField(
                        upload_to=upload_profile,
                        default='Profiles/user/user.png',
                        null=True, blank=True
    )
    phone_no = models.CharField(max_length=14)
    gender = models.CharField(max_length=15, choices=GENDER, verbose_name='Gender')
    height = models.DecimalField(max_digits=3, decimal_places=2)
    weight = models.DecimalField(max_digits=3, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    def __str__(self):
        return self.email



class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    day = models.BooleanField()
    week = models.BooleanField()
    month = models.BooleanField()

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user


class GoalDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, verbose_name="Goal")

    daily_target = models.PositiveIntegerField()
    weekly_target = models.PositiveIntegerField()
    monthly_target = models.PositiveIntegerField()
