from django.urls import path
from .views import (
    MeView,
    ChangePasswordView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    ProfessorListCreateView,
    ProfessorDetailView,
)

urlpatterns = [
    path("me/", MeView.as_view(), name="me"),
    path("me/change-password/", ChangePasswordView.as_view(), name="me-change-password"),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password-reset-request"),
    path("password-reset/confirm/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    path("professores/", ProfessorListCreateView.as_view(), name="professores-list-create"),
    path("professores/<int:pk>/", ProfessorDetailView.as_view(), name="professores-detail"),
]
