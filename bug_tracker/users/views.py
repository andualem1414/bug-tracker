from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.views.generic import View, ListView, UpdateView
from .models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, LoginForm, UserUpdateForm


# Create your views here.


class UsersListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_denied_message = "You do not have permission to View Users."

    login_url = "users/login"
    redirect_field_name = "users"

    permission_required = "users.view_user"
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"
    permission_denied_message = "You do not have permission to View Users."


class UserUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    login_url = "users/login"
    redirect_field_name = "users/update"
    permission_required = "users.add_user"
    model = User
    template_name = "users/update_user.html"
    form_class = UserUpdateForm
    success_url = "/users"
    success_message = "User successfully Updated!!!!"

    def form_valid(self, form):
        user = User.objects.get(username=form.cleaned_data.get("username"))
        user.groups.clear()
        group = Group.objects.get(name=form.cleaned_data.get("role").lower())
        user.groups.add(group)
        print(group)
        return super().form_valid(form)


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

        # username = form.cleaned_data.get("username")
        # password = form.cleaned_data.get("password")
        # user = auth.authenticate(username=username, password=password)
        # if user is not None:
        #     auth.login(request, user)
        #     messages.success(request, "Login Successful")
        #     return redirect("projects")


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