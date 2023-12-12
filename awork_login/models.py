from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import hashlib
import requests

 
class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("The username is not given.")
        user = self.model(username=username, **extra_fields)
        user.is_active = True
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff = True")

        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser = True")
        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=128, unique=True)  # Set unique=True
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128, null=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_pro = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['is_pro']

    objects = UserManager()

    def __str__(self):
        return self.username
    

