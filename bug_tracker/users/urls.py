from django.urls import path
from . import views


urlpatterns = [
    path("", views.UsersListView.as_view(), name="users"),
    path("<int:pk>/update", views.UserUpdateView.as_view(), name="update_user"),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.RegisterView.as_view(), name="register"),
]
