"""
Lista oficial das perguntas do formulario de avaliacao de disciplinas
da Faculdade de Tecnologia (FT) da UNICAMP.

A organizacao em grupos (A, B, C, D) segue o mesmo padrao usado em
apps/reports/services.py (QUESTION_GROUPS).

Esta lista e a unica fonte da verdade. Toda disciplina nova nasce com
estas perguntas (ver Course.save() em apps/courses/models.py) e o
comando "python manage.py sincronizar_perguntas" garante que disciplinas
ja existentes tambem fiquem com este conjunto.
"""

STANDARD_QUESTIONS = [
    # A) Infraestrutura e Suporte as aulas
    {
        "order": 1,
        "question_type": "scale",
        "text": (
            "A infraestrutura da sala de aula (iluminacao, ventilacao, projetor, lousa, "
            "carteiras, etc) estava apropriada para o desenvolvimento da disciplina."
        ),
    },
    {
        "order": 2,
        "question_type": "scale",
        "text": (
            "A infraestrutura dos laboratorios (iluminacao, ventilacao, bancadas, mesas, "
            "experimentos, utensilios de laboratorio, etc) estava apropriada para o "
            "desenvolvimento da disciplina."
        ),
    },
    {
        "order": 3,
        "question_type": "scale",
        "text": (
            "A infraestrutura fisica da FT como um todo esta apropriada para o "
            "desenvolvimento academico de seus alunos."
        ),
    },
    {
        "order": 4,
        "question_type": "scale",
        "text": (
            "Materiais didaticos disponibilizados e indicados pelo professor como livros, "
            "manuais, videos e tutoriais eram de facil acesso."
        ),
    },
    {
        "order": 5,
        "question_type": "scale",
        "text": (
            "Esta disciplina se mostrou pertinente para o meu curso, abordando conteudos "
            "relevantes para minha formacao profissional."
        ),
    },
    # B) Participacao do estudante
    {
        "order": 6,
        "question_type": "scale",
        "text": "Acompanhei (de forma sincrona ou assincrona) a maior parte das aulas da disciplina.",
    },
    {
        "order": 7,
        "question_type": "scale",
        "text": "Busquei e estudei o material de apoio da disciplina indicado pelo professor.",
    },
    {
        "order": 8,
        "question_type": "scale",
        "text": "Empenhei-me em resolver os exercicios e atividades extraclasse propostos pelo professor.",
    },
    {
        "order": 9,
        "question_type": "scale",
        "text": "Planejei de forma eficiente meus estudos para esta disciplina.",
    },
    {
        "order": 10,
        "question_type": "scale",
        "text": (
            "Procurei regularmente o professor, o PAD ou o PED da disciplina para sanar "
            "minhas duvidas fora do horario de aula."
        ),
    },
    {
        "order": 11,
        "question_type": "scale",
        "text": "Estive motivado para cursar a disciplina.",
    },
    {
        "order": 12,
        "question_type": "scale",
        "text": "Meus conhecimentos previos me permitiram acompanhar a disciplina.",
    },
    # C) Atuacao Docente
    {
        "order": 13,
        "question_type": "scale",
        "text": (
            "As aulas sempre comecaram e terminaram em horarios que nao prejudicaram o "
            "desenvolvimento do conteudo."
        ),
    },
    {
        "order": 14,
        "question_type": "scale",
        "text": "As aulas foram planejadas e os conteudos abordados estavam organizados.",
    },
    {
        "order": 15,
        "question_type": "scale",
        "text": (
            "Os metodos de ensino, as tecnicas e atividades didaticas utilizados na "
            "disciplina facilitaram minha aprendizagem."
        ),
    },
    {
        "order": 16,
        "question_type": "scale",
        "text": (
            "O conteudo apresentado em aula continha tanto os aspectos basicos como "
            "exemplos mais aprofundados."
        ),
    },
    {
        "order": 17,
        "question_type": "scale",
        "text": "As avaliacoes de aprendizagem da disciplina foram coerentes.",
    },
    {
        "order": 18,
        "question_type": "scale",
        "text": "Entendi os criterios para aprovacao na disciplina apresentados no inicio da disciplina.",
    },
    {
        "order": 19,
        "question_type": "scale",
        "text": (
            "Recebi os resultados das avaliacoes (provas, testes, relatorios, projetos, etc) "
            "em um prazo adequado para que eu pudesse avaliar meu desempenho, tirar duvidas "
            "e me preparar para as proximas avaliacoes."
        ),
    },
    {
        "order": 20,
        "question_type": "scale",
        "text": (
            "A interacao entre os alunos e o professor na sala de aula assegurou um "
            "processo de ensino e aprendizagem de qualidade."
        ),
    },
    {
        "order": 21,
        "question_type": "scale",
        "text": "A participacao e expressao de ideias foram estimuladas durante as aulas.",
    },
    {
        "order": 22,
        "question_type": "scale",
        "text": "Quando precisei, consegui contatar o professor fora do horario da aula para tirar duvidas.",
    },
    # D) Questoes abertas
    {
        "order": 23,
        "question_type": "text",
        "text": "Comente os principais aspectos positivos da disciplina.",
    },
    {
        "order": 24,
        "question_type": "text",
        "text": "Indique algumas sugestoes para a melhoria da disciplina.",
    },
]


def _get_template_questions():
    """Retorna a lista de perguntas-padrao a serem usadas como base.

    Le primeiro do banco (modelo StandardQuestion). Se a tabela estiver
    vazia (primeira vez que o sistema roda apos a migracao), faz um
    auto-seed a partir da constante STANDARD_QUESTIONS e devolve os
    registros recem-criados. Assim a configuracao funciona "fora da caixa"
    sem precisar de comando manual.
    """
    from apps.evaluations.models import StandardQuestion

    qs = StandardQuestion.objects.filter(is_active=True).order_by("order")
    if qs.exists():
        return [
            {"order": q.order, "question_type": q.question_type, "text": q.text}
            for q in qs
        ]

    # Tabela vazia -> seed com a lista hardcoded e re-le.
    if not StandardQuestion.objects.exists():
        for item in STANDARD_QUESTIONS:
            StandardQuestion.objects.create(
                order=item["order"],
                question_type=item["question_type"],
                text=item["text"],
                is_active=True,
            )
        qs = StandardQuestion.objects.filter(is_active=True).order_by("order")
        return [
            {"order": q.order, "question_type": q.question_type, "text": q.text}
            for q in qs
        ]

    return []


def sync_standard_questions(course, *, overwrite_text=False):
    """Garante que `course` tem as perguntas padrao definidas no template
    (modelo StandardQuestion).

    - Se `overwrite_text=False` (default), apenas perguntas faltantes sao criadas.
      Perguntas que ja existem para aquele `order` nao sao alteradas, preservando
      qualquer resposta ja vinculada.
    - Se `overwrite_text=True`, atualiza tambem o texto e o tipo de perguntas
      existentes para coincidir com o padrao. Util para "consertar" disciplinas
      antigas que tem perguntas com texto fora do padrao.

    Retorna (criadas, atualizadas).
    """
    # Import lazy para evitar import circular (apps/courses importa este modulo)
    from apps.evaluations.models import EvaluationQuestion

    template = _get_template_questions()

    criadas = 0
    atualizadas = 0

    for q in template:
        defaults = {"text": q["text"], "question_type": q["question_type"]}
        existing = EvaluationQuestion.objects.filter(course=course, order=q["order"]).first()
        if existing is None:
            EvaluationQuestion.objects.create(course=course, order=q["order"], **defaults)
            criadas += 1
        elif overwrite_text:
            mudou = False
            if existing.text != defaults["text"]:
                existing.text = defaults["text"]
                mudou = True
            if existing.question_type != defaults["question_type"]:
                existing.question_type = defaults["question_type"]
                mudou = True
            if mudou:
                existing.save(update_fields=["text", "question_type"])
                atualizadas += 1

    return criadas, atualizadas


def sync_all_courses(*, overwrite_text=False):
    """Aplica o template em todas as disciplinas existentes. Usado pelo
    botao "Aplicar em todas as disciplinas" da tela de admin.

    Retorna (cursos_processados, total_criadas, total_atualizadas).
    """
    from apps.courses.models import Course

    cursos = list(Course.objects.all())
    total_criadas = 0
    total_atualizadas = 0

    for c in cursos:
        criadas, atualizadas = sync_standard_questions(c, overwrite_text=overwrite_text)
        total_criadas += criadas
        total_atualizadas += atualizadas

    return len(cursos), total_criadas, total_atualizadas
