from django.db.models import Avg
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import EvaluationQuestion, EvaluationAnswer, StandardQuestion
from .serializers import (
    EvaluationQuestionSerializer,
    EvaluationResponseSerializer,
    StandardQuestionSerializer,
)
from apps.courses.models import Course
from apps.users.permissions import IsAdminRole, IsProfessorOrAdmin


class QuestionListCreateView(generics.ListCreateAPIView):
    serializer_class = EvaluationQuestionSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [IsAdminRole()]

    def get_queryset(self):
        course_id = self.request.query_params.get("course_id")

        qs = EvaluationQuestion.objects.select_related("course")

        if course_id:
            qs = qs.filter(course_id=course_id)

        # GET público: retorna perguntas do curso
        if self.request.method == "GET":
            return qs

        # POST só admin
        user = self.request.user
        if user.role == "admin":
            return qs

        return qs.none()


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EvaluationQuestionSerializer
    permission_classes = [IsAdminRole]
    queryset = EvaluationQuestion.objects.select_related("course").all()


class PublicEvaluationSubmitView(generics.CreateAPIView):
    serializer_class = EvaluationResponseSerializer
    permission_classes = [permissions.AllowAny]


class StandardQuestionListCreateView(generics.ListCreateAPIView):
    """Lista e cria perguntas-padrao. Apenas admin.

    Na primeira chamada (tabela vazia) faz auto-seed das 24 perguntas
    oficiais a partir de apps/evaluations/standard_questions.py, para
    que a tela do admin ja apareca com a lista pronta.
    """

    serializer_class = StandardQuestionSerializer
    permission_classes = [IsAdminRole]

    def get_queryset(self):
        # Dispara o seed automatico se a tabela estiver vazia.
        from apps.evaluations.standard_questions import _get_template_questions
        _get_template_questions()
        return StandardQuestion.objects.all().order_by("order")


class StandardQuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Edita/exclui uma pergunta-padrao. Apenas admin."""

    serializer_class = StandardQuestionSerializer
    permission_classes = [IsAdminRole]
    queryset = StandardQuestion.objects.all()


class StandardQuestionSyncView(APIView):
    """Aplica o template de perguntas-padrao em todas as disciplinas.

    Por default cria apenas as perguntas faltantes; com ?overwrite=1
    tambem atualiza o texto das perguntas existentes.
    """

    permission_classes = [IsAdminRole]

    def post(self, request):
        from apps.evaluations.standard_questions import sync_all_courses

        overwrite = request.query_params.get("overwrite") in ("1", "true", "True")
        cursos, criadas, atualizadas = sync_all_courses(overwrite_text=overwrite)

        return Response(
            {
                "detail": "Sincronizacao concluida.",
                "cursos_processados": cursos,
                "perguntas_criadas": criadas,
                "perguntas_atualizadas": atualizadas,
                "overwrite": overwrite,
            },
            status=status.HTTP_200_OK,
        )


class CourseReportView(APIView):
    permission_classes = [IsProfessorOrAdmin]

    def get(self, request, course_id):
        user = request.user

        try:
            if user.role == "admin":
                course = Course.objects.prefetch_related("questions", "responses").get(id=course_id)
            else:
                course = Course.objects.prefetch_related("questions", "responses").get(id=course_id, professor=user)
        except Course.DoesNotExist:
            return Response({"detail": "Disciplina não encontrada."}, status=404)

        questions_data = []
        questions = course.questions.all().order_by("order")

        for question in questions:
            item = {
                "question_id": question.id,
                "text": question.text,
                "question_type": question.question_type,
            }

            if question.question_type == "scale":
                answers = EvaluationAnswer.objects.filter(question=question, scale_value__isnull=False)
                avg_value = answers.aggregate(avg=Avg("scale_value"))["avg"]

                distribution = {}
                for answer in answers:
                    key = str(answer.scale_value)
                    distribution[key] = distribution.get(key, 0) + 1

                item["average"] = round(avg_value, 2) if avg_value is not None else None
                item["distribution"] = distribution
            else:
                comments = list(
                    EvaluationAnswer.objects.filter(
                        question=question,
                        text_value__isnull=False
                    ).exclude(text_value="").values_list("text_value", flat=True)
                )
                item["comments"] = comments

            questions_data.append(item)

        payload = {
            "course_id": course.id,
            "course_name": course.name,
            "course_code": course.code,
            "total_responses": course.responses.count(),
            "questions": questions_data,
        }

        return Response(payload)
