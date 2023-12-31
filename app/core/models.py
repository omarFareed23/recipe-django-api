"""Database Moodels"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import \
    AbstractBaseUser, BaseUserManager, PermissionsMixin
import re


class UserManager(BaseUserManager):
    """Manager for user profiles"""

    __email_regex = re.compile(
        r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
    )

    def __validate_email(self, email):
        """Check if the email exist and valid"""
        if not email:
            raise ValueError('User must have an email address')
        if not self.__email_regex.fullmatch(email):
            raise ValueError('Email address is not valid')

    def __create_user(self, email, password=None, **extra_fields):
        """Create and save a new user"""
        self.__validate_email(email)
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # encrypting the password
        user.set_password(password)
        # saving the user model
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create a new user"""
        extra_fields['is_superuser'] = False
        extra_fields['is_staff'] = False
        return self.__create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create a new superuser"""
        extra_fields['is_superuser'] = True
        extra_fields['is_staff'] = True
        return self.__create_user(email, password, **extra_fields)


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


class Recipe(models.Model):
    """Recipe object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Tag object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return self.name
