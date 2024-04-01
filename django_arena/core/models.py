from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    rating = models.IntegerField(default=1000)
    views = models.PositiveIntegerField(default=0)


__all__ = [User]
