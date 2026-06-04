from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("id", "institutional_email", "first_name", "last_name", "role", "is_active")
    ordering = ("institutional_email",)
    search_fields = ("institutional_email", "first_name", "last_name")

    fieldsets = (
        (None, {"fields": ("institutional_email", "password")}),
        ("Informações pessoais", {"fields": ("first_name", "last_name")}),
        ("Permissões", {"fields": ("role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Datas importantes", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("institutional_email", "first_name", "last_name", "role", "password1", "password2", "is_staff", "is_superuser"),
        }),
    )
