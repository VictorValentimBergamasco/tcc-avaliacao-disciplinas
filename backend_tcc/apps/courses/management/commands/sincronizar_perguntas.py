"""Comando para popular/sincronizar as perguntas padrao em todas as disciplinas.

Uso:
    python manage.py sincronizar_perguntas
        -> apenas cria perguntas faltantes; preserva perguntas existentes.

    python manage.py sincronizar_perguntas --sobrescrever
        -> tambem atualiza o texto/tipo de perguntas existentes para coincidir
           com o padrao oficial. Use isso para "consertar" disciplinas antigas
           cujo texto das perguntas estava fora do padrao.

    python manage.py sincronizar_perguntas --disciplina EST001
        -> roda apenas para a disciplina com aquele codigo.
"""

from django.core.management.base import BaseCommand, CommandError

from apps.courses.models import Course
from apps.evaluations.standard_questions import sync_standard_questions


class Command(BaseCommand):
    help = (
        "Garante que todas as disciplinas (ou uma especifica) tenham as 24 "
        "perguntas padrao da FT-UNICAMP."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--sobrescrever",
            action="store_true",
            help=(
                "Atualiza tambem o texto e o tipo das perguntas existentes "
                "para coincidir com o padrao oficial."
            ),
        )
        parser.add_argument(
            "--disciplina",
            type=str,
            default=None,
            help="Codigo da disciplina (ex.: EST001). Se omitido, roda em todas.",
        )

    def handle(self, *args, **options):
        overwrite = options["sobrescrever"]
        codigo = options["disciplina"]

        if codigo:
            try:
                courses = [Course.objects.get(code=codigo)]
            except Course.DoesNotExist:
                raise CommandError(f"Disciplina com codigo '{codigo}' nao encontrada.")
        else:
            courses = list(Course.objects.all())

        if not courses:
            self.stdout.write(self.style.WARNING("Nenhuma disciplina encontrada."))
            return

        total_criadas = 0
        total_atualizadas = 0

        for course in courses:
            criadas, atualizadas = sync_standard_questions(course, overwrite_text=overwrite)
            total_criadas += criadas
            total_atualizadas += atualizadas
            self.stdout.write(
                f"- {course.code} ({course.name}): "
                f"{criadas} criadas, {atualizadas} atualizadas."
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nConcluido. Disciplinas processadas: {len(courses)}. "
                f"Total: {total_criadas} criadas, {total_atualizadas} atualizadas."
            )
        )
