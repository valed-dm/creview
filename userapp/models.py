# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class MyUser(AbstractUser):
    email = models.EmailField(unique=True)
