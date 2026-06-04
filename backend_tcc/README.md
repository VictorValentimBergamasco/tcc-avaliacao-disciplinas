# Backend — Sistema de Avaliação de Disciplinas

API REST em Django + Django REST Framework + PostgreSQL.

## Requisitos

- Python 3.11 ou superior
- PostgreSQL 14 ou superior (com um banco já criado)

## Instalação

1. Crie e ative o ambiente virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate          # Windows
   # ou
   source venv/bin/activate        # Linux/Mac
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Crie o arquivo `.env` a partir do exemplo e preencha:
   ```bash
   copy .env.example .env          # Windows
   cp .env.example .env            # Linux/Mac
   ```
   Variáveis principais: `SECRET_KEY`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `FRONTEND_URL`.
4. Aplique as migrações:
   ```bash
   python manage.py migrate
   ```
5. Crie um superusuário (admin):
   ```bash
   python manage.py createsuperuser
   ```
   Quando perguntar `Email`, informe o e-mail institucional — é ele que serve de login no sistema.
6. Suba o servidor:
   ```bash
   python manage.py runserver
   ```

API disponível em `http://127.0.0.1:8000/api/`.

## Estrutura dos apps

| App | Responsabilidade |
|-----|------------------|
| `users` | Usuário customizado (login por e-mail institucional), JWT, primeiro login com troca obrigatória de senha, recuperação por e-mail. |
| `courses` | Disciplinas e geração automática de QR Code no `save()`. |
| `evaluations` | Perguntas padrão (template), perguntas por disciplina, respostas anônimas, submissão pública via QR. |
| `dashboard` | Estatísticas para admin e médias por disciplina. |
| `reports` | Geração de PDF com gráficos via ReportLab + Matplotlib. |

## Endpoints principais

Veja [`README_INSTALACAO.txt`](README_INSTALACAO.txt) para a lista completa, incluindo exemplos de payload de login, criação de professor, criação de disciplina e submissão de avaliação.

## Comandos úteis

| Comando | O que faz |
|---------|-----------|
| `python manage.py sincronizar_perguntas` | Garante que toda disciplina existente tem as 24 perguntas-padrão. |
| `python manage.py sincronizar_perguntas --sobrescrever` | Idem, mas também atualiza o texto das perguntas existentes. |
| `python manage.py sincronizar_perguntas --disciplina EST001` | Roda apenas em uma disciplina. |
| `python manage.py createsuperuser` | Cria um admin. |
| `python manage.py migrate` | Aplica migrações. |

## Recuperação de senha em desenvolvimento

O `.env.example` deixa `EMAIL_BACKEND` apontando para o console — quando o usuário pede para recuperar a senha, o e-mail (com o link) é impresso no terminal onde o `runserver` está rodando. Para usar SMTP real (Gmail, SendGrid), descomente as variáveis correspondentes no `.env`.
