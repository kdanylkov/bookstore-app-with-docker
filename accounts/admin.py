from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .forms import CustomUserChangeForm, CustomUserCreationForm


CustomUser = get_user_model()


@admin.register(CustomUser)
class CustomAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
            'email',
            'username',
            'is_superuser',
            ]
    list_display_links = ('username',)
