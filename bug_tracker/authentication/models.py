from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_developer = models.BooleanField("Is admin", default=False)
    is_project_manager = models.BooleanField("Is project manager", default=False)
