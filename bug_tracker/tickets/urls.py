from django.urls import path
from . import views

urlpatterns = [
    path("", views.TicketListView.as_view(), name="tickets"),
    path("<int:pk>/update", views.TicketUpdateView.as_view(), name="update_ticket"),
    path(
        "<int:project_id>/create",
        views.CreateTicketView.as_view(),
        name="create_ticket",
    ),
    path(
        "<int:pk>/details",
        views.TicketDetailView.as_view(),
        name="ticket_detail",
    ),
]
