from django import forms
from .models import Ticket, Comment
from django.utils.translation import gettext_lazy as _
from django.db import models
from projects.models import Project

from users.models import User


class TicketForm(forms.ModelForm):
    # project = Project.objects.get(pk=initials.pk)
    # developer = forms.ModelChoiceField(queryset=project.personnels.all())

    class Meta:
        model = Ticket
        fields = [
            "title",
            "description",
            "developer",
            "priority",
            "type",
            "status",
        ]
        labels = {"developer": "List of developers for this Ticket"}

    # ORDER_STATUS = (
    #     ("new", "new"),
    #     ("open", "open"),
    #     ("inprogress", "inprogress"),
    #     ("resolved", "resolved"),
    #     ("additional information required", "additional information required"),
    # )
    # title = forms.CharField(max_length=10)
    # description = forms.Textarea()
    # status = forms.ChoiceField(choices=ORDER_STATUS)
    # developer = forms.ModelChoiceField(queryset=User.objects.filter(role="Developer"))

    def __init__(self, *args, **kwargs):
        project_id = kwargs.pop("project_id", None)

        super(TicketForm, self).__init__(*args, **kwargs)
        if project_id:
            project = Project.objects.get(pk=project_id)

            self.fields["developer"] = forms.ModelChoiceField(
                queryset=project.personnels.all()
            )

        self.fields["developer"].label = "List of developers for this Ticket"

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]

    def __init__(self, *args, **kwargs):
        """Save the request with the form so it can be accessed in clean_*()"""
        self.request = kwargs.pop("request", None)
        super(CommentForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            visible.field.widget.attrs["rows"] = "0"
