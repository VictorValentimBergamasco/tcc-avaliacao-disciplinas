from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.courses.models import Course
from apps.evaluations.models import (
    EvaluationAnswer,
    EvaluationQuestion,
    EvaluationResponse,
)
from apps.users.models import User
from apps.users.permissions import IsAdminRole, IsProfessorOrAdmin


class DashboardOverview(APIView):
    """Visão geral do administrador: totais de professores, disciplinas e respostas."""

    permission_classes = [IsAdminRole]

    def get(self, request):
        data = {
            "total_professors": User.objects.filter(role="professor").count(),
            "total_courses": Course.objects.count(),
            # total_responses = quantos formulários foram submetidos (respostas únicas).
            # Antes estava contando EvaluationAnswer (uma resposta por pergunta), o que
            # inflava muito o número exibido no card.
            "total_responses": EvaluationResponse.objects.count(),
        }
        return Response(data)


class CourseDashboard(APIView):
    """Resumo (médias por pergunta) das avaliações de uma disciplina."""

    permission_classes = [IsProfessorOrAdmin]

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)

        # Professores só podem ver o dashboard das próprias disciplinas.
        user = request.user
        if user.role == "professor" and course.professor_id != user.id:
            raise PermissionDenied(
                "Você não tem permissão para acessar esta disciplina."
            )

        questions = EvaluationQuestion.objects.filter(course=course).order_by("order")

        result = []
        for q in questions:
            answers = EvaluationAnswer.objects.filter(
                question=q, scale_value__isnull=False
            )
            avg = answers.aggregate(avg=Avg("scale_value"))["avg"]
            result.append({
                "question": q.text,
                "order": q.order,
                "average": round(avg, 2) if avg else 0,
                "total_answers": answers.count(),
            })

        return Response({
            "course": course.name,
            "course_code": course.code,
            "questions": result,
        })
