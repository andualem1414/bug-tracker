from django.shortcuts import redirect, render
from django.urls import reverse

from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
)
from .forms import ProjectForm

from tickets.models import Ticket
from .models import Project
from users.models import User

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

# Create your views here.


def is_member(user):
    return user.groups.filter(name="developer").exists()


class ProjectsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = "/users/login"
    permission_required = "projects.view_project"
    redirect_field_name = "/projects"
    template_name = "projects/index.html"
    model = Project
    context_object_name = "projects"

    def get_queryset(self):
        search = self.request.GET.get("search", "")
        projects = Project.objects.filter(
            name__icontains=search
        ) | Project.objects.filter(description__icontains=search)
        return projects

    def get_paginate_by(self, queryset):
        if self.request.GET.get("page_number"):
            self.request.session["page_number"] = self.request.GET.get("page_number")
        self.paginate_by = self.request.session.get("page_number", 5)
        return self.paginate_by


class ProjectCreateView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = "projects.add_project"
    template_name = "projects/create_project.html"
    form_class = ProjectForm
    model = Project
    success_url = "/projects"
    success_message = "%(name)s was created successfully"


class ProjectDetailView(DetailView):
    template_name = "projects/detail_project.html"
    model = Project
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tickets"] = Ticket.objects.filter(project=context["project"])
        context["users"] = User.objects.all()
        return context


class ProjectUpdateView(SuccessMessageMixin, UpdateView):
    template_name = "projects/update_project.html"
    form_class = ProjectForm
    model = Project
    success_url = "/projects"
    context_object_name = "project"
    success_message = "Project successfully Updated!!!!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context


def delete_project(request, pk):
    project = Project.objects.get(pk=pk)
    project.delete()
    return redirect("projects")


def addPersonel(request, pk):
    project = Project.objects.get(pk=pk)

    for user in request.POST.getlist("users_list"):
        project.personnels.add(User.objects.get(username=user))

    return redirect("detail_project", pk)
