from django.contrib import admin
from .models import EvaluationQuestion, EvaluationResponse, EvaluationAnswer


@admin.register(EvaluationQuestion)
class EvaluationQuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "course", "question_type", "order")
    list_filter = ("question_type", "course")
    search_fields = ("text", "course__name", "course__code")


@admin.register(EvaluationResponse)
class EvaluationResponseAdmin(admin.ModelAdmin):
    list_display = ("id", "course", "submitted_at", "external_response_id")
    list_filter = ("course", "submitted_at")


@admin.register(EvaluationAnswer)
class EvaluationAnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "response", "question", "scale_value")
    list_filter = ("question",)
