from django.urls import path
from . import views

urlpatterns = [
    path("", views.DashBoardView.as_view(), name="index"),
    path("projects", views.ProjectsListView.as_view(), name="list_projects"),
    path("create-project", views.CreateProjectView.as_view(), name="create_project"),
    path("projects/<int:pk>", views.UpdateProjectView.as_view(), name="edit_project"),
    path(
        "delete-project/<int:pk>",
        views.delete_project,
        name="delete_project",
    ),
]
