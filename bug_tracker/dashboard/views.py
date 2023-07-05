from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from tickets.models import Ticket
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

# Create your views here.


class DashBoardView(LoginRequiredMixin, TemplateView):
    login_url = "users/login"
    redirect_field_name = ""
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["no_tickets"] = Ticket.objects.all().count()

        return context


def tickets_count(request):
    tickets = Ticket.objects.all()
    tickets_type_count = {
        "Bugs/Errors": 20,
        "Other Comments": 70,
        "Feature request": 50,
        "Traning/documents request": 10,
    }
    tickets_status_count = {
        "new": 40,
        "open": 100,
        "inprogress": 60,
        "resolved": 70,
        "additional information required": 90,
    }
    tickets_priority_count = {"None": 40, "Low": 100, "Medium": 60, "High": 70}

    limit = max(tickets_status_count.values())

    for ticket in tickets:
        tickets_type_count[ticket.type] += 1
        tickets_status_count[ticket.status] += 1
        tickets_priority_count[ticket.priority] += 1

    return JsonResponse(
        {
            "tickets_type_count": tickets_type_count,
            "tickets_status_count": tickets_status_count,
            "tickets_priority_count": tickets_priority_count,
            "limit": limit,
        },
        safe=False,
    )
