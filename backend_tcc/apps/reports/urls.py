from django.urls import path
from .views import CoursePdfReportView

urlpatterns = [
    path("course/<int:course_id>/pdf/", CoursePdfReportView.as_view(), name="course-pdf-report"),
]
