from django.db import models
from apps.courses.models import Course


class StandardQuestion(models.Model):
    """Pergunta-padrao reutilizada em todas as disciplinas.

    Funciona como um TEMPLATE. Quando uma disciplina e criada, o sistema
    copia estas perguntas para EvaluationQuestion (uma copia por curso),
    de modo que editar o template aqui nao impacta automaticamente
    disciplinas ja existentes. Para propagar, o admin clica em
    "Aplicar em todas as disciplinas" na tela de Perguntas Padrao.
    """

    QUESTION_TYPE_CHOICES = (
        ("scale", "Escala"),
        ("text", "Texto"),
    )

    text = models.TextField()
    question_type = models.CharField(
        max_length=20, choices=QUESTION_TYPE_CHOICES, default="scale"
    )
    order = models.PositiveIntegerField(unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Pergunta padrao"
        verbose_name_plural = "Perguntas padrao"

    def __str__(self):
        return f"Q{self.order} - {self.text[:60]}"


class EvaluationQuestion(models.Model):
    QUESTION_TYPE_CHOICES = (
        ("scale", "Escala"),
        ("text", "Texto"),
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES, default="scale")
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.course.name} - Q{self.order}"


class EvaluationResponse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="responses")
    submitted_at = models.DateTimeField(auto_now_add=True)
    external_response_id = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"Resposta #{self.id} - {self.course.name}"


class EvaluationAnswer(models.Model):
    response = models.ForeignKey(EvaluationResponse, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(EvaluationQuestion, on_delete=models.CASCADE, related_name="answers")
    scale_value = models.IntegerField(blank=True, null=True)
    text_value = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Resp {self.response_id} - Pergunta {self.question_id}"
