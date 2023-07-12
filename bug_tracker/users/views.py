from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.views.generic import View, ListView, UpdateView, TemplateView
from .models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, LoginForm, UserUpdateForm


# Create your views here.


class UsersListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = "users/login"
    redirect_field_name = "users"

    permission_required = "users.view_user"
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"
    permission_denied_message = "You do not have permission to View Users."
    paginate_by = 5

    def get_queryset(self):
        search = self.request.GET.get("search", "")
        projects = User.objects.filter(
            username__icontains=search
        ) | User.objects.filter(role__icontains=search)
        return projects

    def get_paginate_by(self, queryset):
        if self.request.GET.get("page_number"):
            self.request.session["page_number"] = self.request.GET.get("page_number")
        self.paginate_by = self.request.session.get("page_number", 5)
        return self.paginate_by


class UserUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    login_url = "users/login"
    redirect_field_name = "users/update"
    permission_required = "users.add_user"
    model = User
    template_name = "users/update_user.html"
    form_class = UserUpdateForm
    success_url = "/users/"
    success_message = "User successfully Updated!!!!"

    def form_valid(self, form):
        user = User.objects.get(username=form.cleaned_data.get("username"))
        user.groups.clear()
        group = Group.objects.get(name=form.cleaned_data.get("role").lower())
        user.groups.add(group)
        print(group)
        return super().form_valid(form)


class ProfileView(
    TemplateView,
    LoginRequiredMixin,
    PermissionRequiredMixin,
):
    login_url = "users/login"
    permission_required = "users.view_user"
    model = User
    template_name = "users/profile.html"


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)

            messages.success(request, "Login Successful")
            return redirect("projects")
        else:
            messages.error(request, "Invalid Username or Password")
            return render(request, "users/login.html", {"form": form})


def logout(request):
    auth.logout(request)
    messages.success(request, "You have been logged out")
    return redirect("/users/login")


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "users/register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=form.cleaned_data.get("username"))
            dev_groups = Group.objects.get(name="developer")
            user.groups.add(dev_groups)

            username = form.cleaned_data.get("username")

            messages.success(request, f"Account created for {username}")
            return redirect("login")
        else:
            return render(request, "users/register.html", {"form": form})
