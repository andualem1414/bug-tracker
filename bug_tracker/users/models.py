from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ("Developer", "Developer"),
        ("Project Manager", "Project Manager"),
        ("Submitter", "Submitter"),
    )

    role = models.CharField(
        max_length=40, default="Developer", choices=ROLE_CHOICES, blank=True, null=True
    )
