from django.shortcuts import redirect, render
from django.urls import reverse

from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DetailView,
)

from tickets.models import Ticket

from .forms import ProjectForm
from .models import Project
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from users.models import User

# Create your views here.


def is_member(user):
    return user.groups.filter(name="developer").exists()


class ProjectsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = "/users/login"
    redirect_field_name = "/projects"

    permission_required = "projects.view_project"
    template_name = "projects/index.html"
    model = Project
    context_object_name = "projects"

    def get_paginate_by(self, queryset):
        if self.request.GET.get("page_number"):
            self.request.session["page_number"] = self.request.GET.get("page_number")
        self.paginate_by = self.request.session.get("page_number", 5)
        return self.paginate_by

    def get_queryset(self):
        search = self.request.GET.get("search", "")
        projects = Project.objects.filter(
            name__icontains=search
        ) | Project.objects.filter(description__icontains=search)
        return projects


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


# class AddProject(View):
#     catagories = Project.objects.all()
#     context = {

#         }
#     def get(request, *args, **kwargs):
#         return render(request, 'projects/index.html' )

#     def post(request, *args, **kwargs):
#         name = request.POST["name"]
#         description = request.POST["description"]


#         # if not amount:
#         #     messages.error(request, "Amount is required")
#         #     return render(request, 'expenses/add_expense.html' , context)
#         # if not description:
#         #     messages.error(request, "description")
#         #     return render(request, 'expenses/add_expense.html' , context)

#         Expense.objects.create(owner= request.user, amount=amount, description=description, catagory=catagory, date=date)
#         messages.success(request, "Expense saved successfully")


#         return redirect('expenses')
