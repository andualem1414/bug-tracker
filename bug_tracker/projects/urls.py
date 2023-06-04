from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProjectsListView.as_view(), name="list_projects"),
    path("create", views.ProjectCreateView.as_view(), name="create_project"),
    path("<int:pk>/update", views.ProjectUpdateView.as_view(), name="edit_project"),
    path(
        "<int:pk>/delete",
        views.delete_project,
        name="delete_project",
    ),
    path(
        "<int:pk>/details",
        views.ProjectDetailView.as_view(),
        name="detail_project",
    ),
]
