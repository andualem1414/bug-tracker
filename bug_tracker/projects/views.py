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

# Create your views here.


class ProjectsListView(ListView):
    template_name = "projects/index.html"
    model = Project
    context_object_name = "projects"


class ProjectCreateView(CreateView):
    template_name = "projects/create_project.html"
    form_class = ProjectForm
    model = Project
    success_url = "/projects"
    success_message = "Project was created successfully"


class ProjectDetailView(DetailView):
    template_name = "projects/detail_project.html"
    model = Project
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tickets"] = Ticket.objects.filter(project=context["project"])
        return context


class ProjectUpdateView(UpdateView):
    template_name = "projects/update_project.html"
    form_class = ProjectForm
    model = Project
    success_url = "/projects"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context


def delete_project(request, pk):
    project = Project.objects.get(pk=pk)
    project.delete()
    return redirect("projects")


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
