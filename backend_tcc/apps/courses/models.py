from io import BytesIO
import qrcode
from django.conf import settings
from django.core.files import File
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    professor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="courses",
        limit_choices_to={"role": "professor"},
    )
    enrollment_count = models.PositiveIntegerField(
    default=0,
    verbose_name="Número de matriculados"
    )
    google_form_link = models.URLField()
    qr_code_image = models.ImageField(upload_to="qrcodes/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.code} - {self.name}"

    def generate_qr_code(self):
        qr = qrcode.make(self.google_form_link)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        filename = f"qr_course_{self.code}.png"
        self.qr_code_image.save(filename, File(buffer), save=False)

    def save(self, *args, **kwargs):
        creating = self._state.adding  # True quando a disciplina ainda nao tem pk

        should_generate = False
        if self.google_form_link:
            if not self.pk or not self.qr_code_image:
                should_generate = True
            else:
                old = Course.objects.filter(pk=self.pk).first()
                if old and old.google_form_link != self.google_form_link:
                    should_generate = True

        if should_generate:
            self.generate_qr_code()

        super().save(*args, **kwargs)

        # Toda disciplina nova ja nasce com as 24 perguntas padrao da FT-UNICAMP.
        # Import lazy aqui para evitar import circular (evaluations -> courses).
        if creating:
            from apps.evaluations.standard_questions import sync_standard_questions
            sync_standard_questions(self)
