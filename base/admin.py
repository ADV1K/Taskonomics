from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Project, Task, User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = [
        "username",
        "email",
        "timezone",
        "is_staff",
    ]


admin.site.register(User, CustomUserAdmin)
admin.site.register(Project)
admin.site.register(Task)
