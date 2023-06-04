from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProjectsListView.as_view(), name="list_projects"),
    path("create", views.CreateProjectView.as_view(), name="create_project"),
    path("<int:pk>/update", views.UpdateProjectView.as_view(), name="edit_project"),
    path(
        "<int:pk>/delete",
        views.delete_project,
        name="delete_project",
    ),
]
