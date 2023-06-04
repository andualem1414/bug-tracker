from django.db import models

# Create your models here.


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
