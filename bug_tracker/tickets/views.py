from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, CreateView
from .forms import TicketForm

from .models import Ticket

# Create your views here.


class TickerListView(ListView):
    template_name = "tickets/index.html"
    model = Ticket
    context_object_name = "tickets"


class CreateTicketView(CreateView):
    template_name = "tickets/create_ticket.html"
    form_class = TicketForm
    model = Ticket
    success_url = "/tickets"
