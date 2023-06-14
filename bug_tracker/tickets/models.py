from django.db import models

# Create your models here.

from projects.models import Project
from users.models import User


class Ticket(models.Model):
    ORDER_STATUS = (
        ("new", "new"),
        ("open", "open"),
        ("inprogress", "inprogress"),
        ("resolved", "resolved"),
        ("additional information required", "additional information required"),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=40, choices=ORDER_STATUS)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    developer = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )


class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, blank=True)

    class Meta:
        ordering = ["created_at"]
