from django.shortcuts import render
from django.views.generic import TemplateView

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

# Create your views here.


class DashBoardView(LoginRequiredMixin, TemplateView):
    login_url = "users/login"
    redirect_field_name = ""
    template_name = "dashboard/index.html"
