from django.db import models

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class UserProfileManager(BaseUserManager):
    """Work with custom user manager"""

    def create_user(self, email, name, password=None):
        """Creates new user object"""

        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Creates and saves a new super user"""

        user = self.create_user(email, name, password)

        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """User Profile in our system"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name'] # Since email is already set to username so by default it will be required field

    def get_full_name(self):
        """Used to get user full name"""

        return self.name

    def get_short_name(self):
        """Used to get short name of user"""

        return self.name


    def __str__(self):
        """When needed to object converted to string"""

        return self.email

# class ProfileFeedItem(models.Model):
#     """Profile status update"""
#
#     user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
#     status_text = models.CharField(max_length=255)
#     created_on = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         """Return as string"""
#
#         return self.status_text
