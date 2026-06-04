from rest_framework import generics
from .models import Course
from .serializers import CourseSerializer
from apps.users.permissions import IsAdminRole, IsProfessorOrAdmin


class CourseListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsProfessorOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Course.objects.select_related("professor").all()
        return Course.objects.select_related("professor").filter(professor=user)

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminRole()]
        return super().get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsProfessorOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Course.objects.select_related("professor").all()
        return Course.objects.select_related("professor").filter(professor=user)

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            if self.request.user.role == "admin":
                return [IsAdminRole()]
        return super().get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
