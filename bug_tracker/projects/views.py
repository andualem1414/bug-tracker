from django.shortcuts import redirect, render
from django.urls import reverse

from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import ProjectForm
from .models import Project

# Create your views here.


class DashBoardView(TemplateView):
    template_name = "projects/dashboard.html"


class ProjectsListView(ListView):
    template_name = "projects/projects_list.html"
    model = Project
    template_name = "projects/projects_list.html"
    context_object_name = "projects"


class CreateProjectView(CreateView):
    template_name = "projects/create_project.html"
    form_class = ProjectForm
    model = Project
    success_url = "/projects"


class UpdateProjectView(UpdateView):
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
    return redirect("list_projects")


# class AddProject(View):
#     catagories = Project.objects.all()
#     context = {

#         }
#     def get(request, *args, **kwargs):
#         return render(request, 'projects/projects_list.html' )

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
