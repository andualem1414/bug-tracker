from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.views.generic import View

from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, LoginForm


# Create your views here.


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "authentication/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)

            messages.success(request, "Login Successful")
            return redirect("projects")
        else:
            messages.error(request, "Invalid Username or Password")
            return render(request, "authentication/login.html", {"form": form})

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
    return render(request, "dashboard/index.html")


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "authentication/register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}")
            return redirect("login")
        else:
            return render(request, "authentication/register.html", {"form": form})
