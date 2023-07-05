from django.db import models

from auditlog.registry import auditlog

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
    PRIORITY = {
        ("None", "None"),
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    }
    TYPE = {
        ("Bugs/Errors", "Bugs/Errors"),
        ("Feature request", "Feature Request"),
        ("Other Comments", "Other Comments"),
        ("Traning/documents request", "Traning/documents Request"),
    }

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=40, choices=ORDER_STATUS)
    priority = models.CharField(max_length=40, choices=PRIORITY)
    type = models.CharField(max_length=40, choices=TYPE)

    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    submitter = models.ForeignKey(
        to=User, related_name="submitter", on_delete=models.CASCADE
    )
    developer = models.ForeignKey(
        to=User,
        related_name="developer",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    commenter = models.ForeignKey(to=User, null=True, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, blank=True)

    class Meta:
        ordering = ["created_at"]


auditlog.register(Ticket)
