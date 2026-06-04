# Frontend — Sistema de Avaliação de Disciplinas

Aplicação React + Vite + React Router + Axios + Recharts.

## Requisitos

- Node.js 18 ou superior

## Instalação

```bash
npm install
npm run dev
```

A aplicação abre em `http://localhost:5173/`.

> Antes de rodar o frontend, o backend deve estar em execução em `http://127.0.0.1:8000/`. Para iniciar os dois automaticamente, use o `iniciar-sistema.bat` na raiz do projeto.

## Estrutura

```
src/
├── main.jsx              Entry point
├── App.jsx               Rotas e proteção de rotas (PrivateRoute)
├── services/
│   └── api.js            Cliente Axios com interceptor JWT
├── components/
│   ├── Layout.jsx        Casca padrão (Sidebar + main)
│   ├── Sidebar.jsx       Menu lateral (admin vs professor)
│   └── StatCard.jsx      Card de número grande
├── pages/
│   ├── Login.jsx                Tela de login
│   ├── ForgotPassword.jsx       Pedido de recuperação de senha
│   ├── ResetPassword.jsx        Definição de nova senha via link
│   ├── SetPassword.jsx          Troca obrigatória no primeiro login
│   ├── AdminDashboard.jsx       Início do admin (totais)
│   ├── Professores.jsx          CRUD de professores
│   ├── Disciplinas.jsx          CRUD de disciplinas
│   ├── PerguntasPadrao.jsx      CRUD do template das perguntas
│   ├── Relatorios.jsx           Gráfico de médias + download PDF
│   ├── ProfessorDashboard.jsx   Início do professor (QR + relatório)
│   └── EvaluationForm.jsx       Formulário público acessado via QR
└── styles/               CSS global
```

## Rotas

| URL | Tela | Acesso |
|-----|------|--------|
| `/` | Login | público |
| `/esqueci-senha` | Pedir recuperação | público |
| `/reset-password/:uid/:token` | Definir nova senha | público (via link do e-mail) |
| `/trocar-senha` | Trocar senha (primeiro login) | logado |
| `/admin` | Dashboard do admin | admin |
| `/professores` | CRUD de professores | admin |
| `/disciplinas` | CRUD de disciplinas | admin |
| `/perguntas-padrao` | Template de perguntas | admin |
| `/relatorios` | Gráficos e PDF | admin/professor |
| `/professor` | Dashboard do professor | professor |
| `/formulario/:courseId` | Formulário de avaliação | público (via QR) |

## Build de produção

```bash
npm run build
```

Os arquivos gerados em `dist/` podem ser servidos por qualquer CDN ou servidor estático (Vercel, Render Static, Nginx).
