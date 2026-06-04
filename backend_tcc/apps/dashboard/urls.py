from django.urls import path
from .views import DashboardOverview, CourseDashboard

urlpatterns = [
    path("overview/", DashboardOverview.as_view()),
    path("course/<int:course_id>/", CourseDashboard.as_view()),
]