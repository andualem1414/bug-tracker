from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class DashBoardView(TemplateView):
    template_name = "dashboard/dashboard.html"
