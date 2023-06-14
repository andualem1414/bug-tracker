from django.db import models
from users.models import User

# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField()
    email = models.EmailField()
    personnels = models.ManyToManyField(User)

    def __str__(self):
        return self.name
