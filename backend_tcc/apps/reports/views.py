from django.http import FileResponse
from rest_framework.views import APIView

from apps.courses.models import Course
from apps.users.permissions import IsProfessorOrAdmin
from .services import generate_course_pdf_report


class CoursePdfReportView(APIView):
    permission_classes = [IsProfessorOrAdmin]

    def get(self, request, course_id):
        user = request.user

        if user.role == "admin":
            course = Course.objects.get(id=course_id)
        else:
            course = Course.objects.get(id=course_id, professor=user)

        pdf_path = generate_course_pdf_report(course=course)
        filename = f"relatorio-{course.code}-{course.id}.pdf"

        return FileResponse(
            open(pdf_path, "rb"),
            as_attachment=True,
            filename=filename,
            content_type="application/pdf",
        )
