BACKEND DJANGO - TCC

1) Ative o ambiente virtual:
   Windows CMD:
   venv\Scripts\activate

   Windows PowerShell:
   venv\Scripts\Activate.ps1

2) Instale as dependências:
   pip install -r requirements.txt

3) Renomeie o arquivo .env.exemplo para .env
   e preencha a senha correta do PostgreSQL.

4) Gere as migrações:
   python manage.py makemigrations

5) Aplique as migrações:
   python manage.py migrate

6) Crie um superusuário:
   python manage.py createsuperuser

   IMPORTANTE:
   Quando o Django pedir username, neste projeto o login é feito com institutional_email.
   Então informe o e-mail institucional.

7) Rode o servidor:
   python manage.py runserver

8) Endpoints principais:
   POST   /api/auth/login/
   POST   /api/auth/refresh/

   GET    /api/users/me/
   POST   /api/users/me/change-password/      <-- troca senha do logado
   POST   /api/users/password-reset/           <-- pedir e-mail de reset
   POST   /api/users/password-reset/confirm/   <-- redefinir com uid+token
   GET    /api/users/professores/
   POST   /api/users/professores/

   GET    /api/dashboard/overview/
   GET    /api/dashboard/course/<id>/

   GET    /api/courses/
   POST   /api/courses/

   GET    /api/evaluations/questions/?course_id=1
   POST   /api/evaluations/submit/
   GET    /api/evaluations/report/1/

   # Perguntas padrao (admin)
   GET    /api/evaluations/standard-questions/
   POST   /api/evaluations/standard-questions/
   PATCH  /api/evaluations/standard-questions/<id>/
   DELETE /api/evaluations/standard-questions/<id>/
   POST   /api/evaluations/standard-questions/sync/             <-- aplica nas existentes
   POST   /api/evaluations/standard-questions/sync/?overwrite=1 <-- sobrescreve textos

   GET    /api/reports/course/<id>/pdf/

   FLUXO DE PRIMEIRO LOGIN DO PROFESSOR:
   - Admin cadastra o professor com uma senha provisória.
   - Ao logar pela primeira vez, o professor recebe must_change_password=true
     no /api/users/me/ e é redirecionado para /trocar-senha no frontend.
   - Ele envia POST /api/users/me/change-password/ com {"new_password": "..."}.
   - Após sucesso, must_change_password volta para false e ele segue para o
     dashboard normal.

   FLUXO DE RECUPERACAO DE SENHA:
   - Usuario clica em "Esqueceu sua senha?" na tela de login.
   - Frontend chama POST /api/users/password-reset/ com o e-mail.
   - Backend gera token + uid e dispara e-mail com link
     <FRONTEND_URL>/reset-password/<uid>/<token>.
   - Em desenvolvimento o e-mail aparece no console do runserver
     (EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend).
   - Usuario clica no link, define nova senha; frontend posta em
     /api/users/password-reset/confirm/.
   - Para ativar SMTP real (Gmail, SendGrid), preencha no .env:
        EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
        EMAIL_HOST=smtp.gmail.com
        EMAIL_PORT=587
        EMAIL_USE_TLS=True
        EMAIL_HOST_USER=seu_email@gmail.com
        EMAIL_HOST_PASSWORD=sua_app_password
        DEFAULT_FROM_EMAIL="FT-UNICAMP <seu_email@gmail.com>"
        FRONTEND_URL=https://dominio-do-frontend

   PERGUNTAS PADRAO (template):
   - O admin gerencia o template na tela /perguntas-padrao.
   - Editar/excluir aqui NAO afeta disciplinas ja cadastradas.
   - O botao "Aplicar em todas as disciplinas" sincroniza o template com
     as disciplinas existentes (cria as faltantes). A variante "Aplicar
     e sobrescrever textos" atualiza o texto/tipo de perguntas existentes.
   - Toda nova disciplina ja nasce com as perguntas-padrao ativas.
   - Na primeira execucao apos a migracao, a tabela StandardQuestion e
     populada automaticamente a partir do arquivo apps/evaluations/standard_questions.py.

9) Exemplo de login:
   {
     "institutional_email": "admin@ft.unicamp.br",
     "password": "123456"
   }

   OBSERVAÇÃO:
   O endpoint padrão do simplejwt normalmente usa o campo definido em USERNAME_FIELD.
   Neste projeto, esse campo é institutional_email.
   Dependendo do cliente que você usar, envie:
   {
     "institutional_email": "admin@ft.unicamp.br",
     "password": "123456"
   }

10) Exemplo para criar professor:
   POST /api/users/professores/
   Authorization: Bearer SEU_TOKEN

   {
     "first_name": "Ana",
     "last_name": "Maria",
     "institutional_email": "ana@ft.unicamp.br",
     "role": "professor",
     "password": "123456"
   }

11) Exemplo para criar disciplina:
   POST /api/courses/
   Authorization: Bearer SEU_TOKEN

   {
     "name": "Estatística",
     "code": "EST001",
     "professor": 2,
     "google_form_link": "https://forms.gle/exemplo"
   }

12) Exemplo para criar perguntas:
   POST /api/evaluations/questions/
   Authorization: Bearer SEU_TOKEN

   {
     "course": 1,
     "text": "Como você avalia a didática do professor?",
     "question_type": "scale",
     "order": 1
   }

13) Exemplo para enviar avaliação anônima:
   POST /api/evaluations/submit/

   {
     "course": 1,
     "answers": [
       {
         "question": 1,
         "scale_value": 5
       },
       {
         "question": 2,
         "text_value": "A disciplina foi muito bem organizada."
       }
     ]
   }


============================================================
RELATÓRIO PDF
============================================================

Pacotes novos:
   matplotlib
   reportlab

Depois de substituir os arquivos, rode:
   pip install -r requirements.txt

Endpoint:
   GET /api/reports/course/1/pdf/

Header no Postman:
   Authorization: Bearer SEU_TOKEN

O PDF será gerado em:
   media/reports/

A versão atual usa os dados já cadastrados no banco:
disciplinas, perguntas e respostas.
