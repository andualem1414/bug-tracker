from django.contrib import admin
from .models import User
from .forms import RegisterForm
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    add_form = RegisterForm

    fieldsets = (
        *UserAdmin.fieldsets,
        ("User role", {"fields": ["role"]}),
    )


admin.site.register(User, CustomUserAdmin)
