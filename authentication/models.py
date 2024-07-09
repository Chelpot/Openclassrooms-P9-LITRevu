from django.contrib.auth.models import AbstractUser, Group
from django.db import models

class User(AbstractUser):
    profile_photo = models.ImageField(verbose_name='Photo de profil')