from django.urls import path
from . import views

urlpatterns = [path("", views.DashBoardView.as_view(), name="dashboard")]
