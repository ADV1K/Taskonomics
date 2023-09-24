from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"timezone": {"required": True}}


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"
