import math
import tempfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from django.conf import settings
from django.utils import timezone

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak,
    Table,
    TableStyle,
    KeepTogether,
)

from apps.evaluations.models import EvaluationAnswer


QUESTION_GROUPS = {
    "A) Infraestrutura e Suporte às aulas": [1, 2, 3, 4, 5],
    "B) Participação do estudante": [6, 7, 8, 9, 10, 11, 12],
    "C) Atuação Docente": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
    "D) Questões abertas": [23, 24, 25, 26],
}

SCALE_LABELS = ["Não sei avaliar", "DT", "DP", "Neutro", "CP", "CT"]

LEGEND_TEXT = (
    "Legenda: DT=Discordo totalmente; DP=Discordo parcialmente; "
    "CP=Concordo parcialmente; CT=Concordo totalmente."
)


def tamanho_amostral(matriculados, tipo="professor"):
    try:
        n_pop = int(matriculados)
    except (TypeError, ValueError):
        n_pop = 0

    if n_pop <= 0:
        return 0

    z = 1.96
    p = 0.5
    e = 0.15 if tipo == "professor" else 0.05
    aa = (z * z * p * (1 - p)) / (e * e)
    return aa / (1 + (aa / n_pop))


def safe_filename(value):
    chars = []
    for char in str(value):
        if char.isalnum() or char in ("-", "_"):
            chars.append(char)
    return "".join(chars) or "relatorio"


def get_course_enrollment(course):
    if hasattr(course, "enrollment_count") and course.enrollment_count:
        return int(course.enrollment_count)

    total = course.responses.count()
    return total if total > 0 else 0


def question_number(question):
    return int(question.order or question.id)


def find_group_title(order):
    for title, orders in QUESTION_GROUPS.items():
        if order in orders:
            return title
    return "Outras questões"


def get_scale_values(question):
    values = EvaluationAnswer.objects.filter(
        question=question,
        scale_value__isnull=False,
    ).values_list("scale_value", flat=True)

    return [int(v) for v in values if v is not None]


def get_text_values(question):
    values = EvaluationAnswer.objects.filter(
        question=question,
        text_value__isnull=False,
    ).exclude(text_value="").values_list("text_value", flat=True)

    return [str(v).strip() for v in values if str(v).strip()]


def calculate_mean_sd(values):
    valid = [v for v in values if v > 0]
    if not valid:
        return None, None

    mean = sum(valid) / len(valid)
    variance = sum((x - mean) ** 2 for x in valid) / len(valid)
    return mean, math.sqrt(variance)


def create_histogram(values, question_order, output_dir):
    counts = [0, 0, 0, 0, 0, 0]

    for value in values:
        if 0 <= value <= 5:
            counts[value] += 1

    total = sum(counts)
    percentages = [(c / total * 100) if total else 0 for c in counts]

    fig = plt.figure(figsize=(9.5, 5.4), dpi=120)
    ax = fig.add_subplot(111)

    x_positions = list(range(6))
    bars = ax.bar(x_positions, counts, alpha=0.8)

    max_count = max(counts) if counts else 0
    top_limit = max(max_count + 1, 1)

    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + top_limit * 0.025,
            f"{percentages[i]:.1f} %",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
        )

    ax.set_xlabel("Respostas", fontsize=11)
    ax.set_ylabel("Número de Alunos", fontsize=11)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(SCALE_LABELS, fontsize=8)
    ax.set_ylim(0, top_limit * 1.30)
    ax.grid(axis="y", alpha=0.25)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    path = Path(output_dir) / f"q{question_order}.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)

    return path


def footer(canvas, doc):
    canvas.saveState()

    width, height = A4
    canvas.setStrokeColor(colors.HexColor("#2F6F89"))
    canvas.setLineWidth(0.5)
    canvas.line(1.5 * cm, 1.15 * cm, width - 1.5 * cm, 1.15 * cm)

    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.drawString(1.5 * cm, 0.75 * cm, "Sistema Web de Avaliação de Disciplinas")
    canvas.drawRightString(width - 1.5 * cm, 0.75 * cm, f"Página {doc.page}")

    canvas.restoreState()


def header_block(styles, course, professor_name, respondentes, matriculados, razao, minimo, now):
    status_amostra = ""
    if matriculados:
        if respondentes < minimo:
            status_amostra = f"Número de respondentes menor que o tamanho amostral mínimo ({minimo})."
        else:
            status_amostra = f"Número de respondentes maior ou igual ao tamanho amostral mínimo ({minimo})."

    data = [
        ["Disciplina", course.name],
        ["Código", course.code],
        ["Professor", professor_name],
        ["Respondentes/matriculados", f"{respondentes}/{matriculados} = {razao} %"],
        ["Data de geração", now.strftime("%d/%m/%Y %H:%M")],
    ]

    table = Table(data, colWidths=[5 * cm, 11.2 * cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EAF3F7")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#1F4E5F")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#CCCCCC")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    block = [
        Paragraph("UNIVERSIDADE ESTADUAL DE CAMPINAS", styles["InstitutionTitle"]),
        Paragraph("Faculdade de Tecnologia", styles["InstitutionSubtitle"]),
        Spacer(1, 0.55 * cm),
        Paragraph("Relatório de Avaliação Docente", styles["ReportTitle"]),
        Spacer(1, 0.55 * cm),
        table,
        Spacer(1, 0.35 * cm),
    ]

    if status_amostra:
        block.append(Paragraph(status_amostra, styles["AlertText"]))
        block.append(Spacer(1, 0.25 * cm))

    block.append(Paragraph(
        "Observação: O tamanho amostral (n) foi calculado com z-score z=1,96 "
        "(nível de confiança de 95%), proporção p=0,5 e margem de erro e=0,15 "
        "(15%) para relatórios por professor. N representa o número de matriculados "
        "na disciplina.",
        styles["NoteText"],
    ))

    return block


def generate_course_pdf_report(course):
    output_dir = Path(settings.MEDIA_ROOT) / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)

    temp_dir = Path(tempfile.mkdtemp(prefix="report_charts_"))
    filename = f"relatorio-{safe_filename(course.code)}-{course.id}.pdf"
    pdf_path = output_dir / filename

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        rightMargin=1.45 * cm,
        leftMargin=1.45 * cm,
        topMargin=1.15 * cm,
        bottomMargin=1.35 * cm,
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="InstitutionTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#1F4E5F"),
        spaceAfter=2,
    ))

    styles.add(ParagraphStyle(
        name="InstitutionSubtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontName="Helvetica",
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#333333"),
    ))

    styles.add(ParagraphStyle(
        name="ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#000000"),
    ))

    styles.add(ParagraphStyle(
        name="SectionTitle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12.5,
        leading=16,
        textColor=colors.HexColor("#1F4E5F"),
        spaceBefore=8,
        spaceAfter=8,
    ))

    styles.add(ParagraphStyle(
        name="Question",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
    ))

    styles.add(ParagraphStyle(
        name="NoteText",
        parent=styles["Normal"],
        fontSize=8.5,
        leading=11.5,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor("#333333"),
    ))

    styles.add(ParagraphStyle(
        name="AlertText",
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
        fontName="Helvetica-Bold",
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor("#8A4B00"),
    ))

    styles.add(ParagraphStyle(
        name="Caption",
        parent=styles["Normal"],
        fontSize=8.5,
        leading=11.5,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#333333"),
    ))

    styles.add(ParagraphStyle(
        name="Legend",
        parent=styles["Normal"],
        fontSize=8.5,
        leading=11.5,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor("#1F4E5F"),
    ))

    styles.add(ParagraphStyle(
        name="Comment",
        parent=styles["Normal"],
        fontSize=9.5,
        leading=13.5,
        alignment=TA_JUSTIFY,
        leftIndent=0.25 * cm,
        spaceAfter=5,
    ))

    story = []

    now = timezone.localtime()
    matriculados = get_course_enrollment(course)
    respondentes = course.responses.count()
    razao = round((respondentes / matriculados) * 100, 2) if matriculados else 0
    minimo = int(round(tamanho_amostral(matriculados, "professor"), 0)) if matriculados else 0
    professor_name = (
        f"{course.professor.first_name} {course.professor.last_name}".strip()
        or course.professor.institutional_email
    )

    story.extend(
        header_block(
            styles=styles,
            course=course,
            professor_name=professor_name,
            respondentes=respondentes,
            matriculados=matriculados,
            razao=razao,
            minimo=minimo,
            now=now,
        )
    )
    story.append(PageBreak())

    questions = list(course.questions.all().order_by("order", "id"))
    current_section = None
    figure_count = 0

    for question in questions:
        order = question_number(question)
        section = find_group_title(order)

        if section != current_section:
            current_section = section
            story.append(Paragraph(section, styles["SectionTitle"]))

        if question.question_type == "scale":
            values = get_scale_values(question)
            mean, sd = calculate_mean_sd(values)
            figure_count += 1

            chart_path = create_histogram(values, order, temp_dir)

            if mean is None:
                caption = f"Figura {figure_count}: Não há respostas válidas para esta questão."
            else:
                caption = (
                    f"Figura {figure_count}: Média da sua questão = "
                    f"{mean:.2f} ± {sd:.2f}. (Máximo da questão = 5,0)"
                )

            content = [
                Paragraph(f"{order}) {question.text}", styles["Question"]),
                Spacer(1, 0.12 * cm),
                Image(str(chart_path), width=16.2 * cm, height=8.8 * cm),
                Spacer(1, 0.10 * cm),
                Paragraph(caption, styles["Caption"]),
            ]

            if figure_count == 1:
                content.append(Spacer(1, 0.15 * cm))
                content.append(Paragraph(LEGEND_TEXT, styles["Legend"]))

            story.append(KeepTogether(content))
            story.append(PageBreak())

        else:
            comments = get_text_values(question)
            story.append(Paragraph(f"{order}) {question.text}", styles["Question"]))
            story.append(Spacer(1, 0.15 * cm))

            if comments:
                for idx, comment in enumerate(comments, start=1):
                    story.append(Paragraph(f"{idx}) {comment}", styles["Comment"]))
            else:
                story.append(Paragraph("Não houve nenhum comentário.", styles["Comment"]))

            story.append(PageBreak())

    if not questions:
        story.append(Paragraph("Ainda não há perguntas cadastradas para esta disciplina.", styles["Question"]))

    doc.build(story, onFirstPage=footer, onLaterPages=footer)

    return str(pdf_path)
