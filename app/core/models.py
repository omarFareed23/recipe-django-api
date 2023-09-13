"""Database Moodels"""
from django.db import models
from django.contrib.auth.models import \
    AbstractBaseUser, BaseUserManager, PermissionsMixin
import re


class UserManager(BaseUserManager):
    """Manager for user profiles"""

    email_regex = re.compile(
        r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
    )

    def create_user(self, email, password=None, **extra_fields):
        """Create a new user"""
        if not email:
            raise ValueError('User must have an email address')
        # check if the email is valid using regex
        if not self.email_regex.fullmatch(email):
            raise ValueError('Email address is not valid')

        user = self.model(email=self.normalize_email(email), **extra_fields)

        # encrypting the password
        user.set_password(password)
        # saving the user model
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """custom user model"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # telling django that we are using email
    # instead of username for authentication
    USERNAME_FIELD = 'email'
    objects = UserManager()
