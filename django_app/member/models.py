from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=24, null=True, unique=True)

    def __str__(self):
        return self.nickname
