from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name", "professor", "is_active", "created_at")
    search_fields = ("name", "code", "professor__first_name", "professor__last_name", "professor__institutional_email")
    list_filter = ("is_active", "created_at")
