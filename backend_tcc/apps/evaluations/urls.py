from django.urls import path
from .views import (
    QuestionListCreateView,
    QuestionDetailView,
    PublicEvaluationSubmitView,
    CourseReportView,
    StandardQuestionListCreateView,
    StandardQuestionDetailView,
    StandardQuestionSyncView,
)

urlpatterns = [
    path("questions/", QuestionListCreateView.as_view(), name="question-list-create"),
    path("questions/<int:pk>/", QuestionDetailView.as_view(), name="question-detail"),
    path("submit/", PublicEvaluationSubmitView.as_view(), name="public-evaluation-submit"),
    path("report/<int:course_id>/", CourseReportView.as_view(), name="course-report"),

    # Perguntas-padrao (template aplicado em toda disciplina nova)
    path("standard-questions/", StandardQuestionListCreateView.as_view(), name="standard-question-list-create"),
    path("standard-questions/<int:pk>/", StandardQuestionDetailView.as_view(), name="standard-question-detail"),
    path("standard-questions/sync/", StandardQuestionSyncView.as_view(), name="standard-question-sync"),
]
