from django.urls import path
from . import views

urlpatterns = [
    path("", views.DashBoardView.as_view(), name="dashboard"),
    path("ticket_count/", views.tickets_count, name="ticket_count"),
]
