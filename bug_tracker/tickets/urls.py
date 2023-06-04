from django.urls import path
from . import views

urlpatterns = [
    path("", views.TickerListView.as_view(), name="tickets"),
    path("create", views.CreateTicketView.as_view(), name="create_ticket"),
]
