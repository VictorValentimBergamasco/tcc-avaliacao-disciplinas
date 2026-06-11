# Sistema Web de Avaliação de Disciplinas — FT/UNICAMP

Trabalho de Conclusão de Curso (TCC) desenvolvido como parte dos requisitos para obtenção do título de Bacharel em Sistemas de Informação pela Faculdade de Tecnologia (FT) da Universidade Estadual de Campinas (UNICAMP).

**Autor:** Victor Valentim Bergamasco
**Orientador:** Prof. Dr. Vitor Rafael Coluci
**Ano:** 2026

---

## Resumo do projeto

Sistema web que automatiza o processo de avaliação de disciplinas da FT-UNICAMP. Substitui o fluxo manual atual — onde os dados coletados por QR Code/Google Forms são entregues em formato bruto aos professores — por uma solução integrada que cadastra disciplinas, gera QR Codes únicos, coleta respostas de forma anônima e gera relatórios consolidados em PDF com gráficos, médias e desvio padrão.

## Arquitetura

Três camadas independentes que se comunicam via API REST (HTTP/JSON):

- **Frontend** — React 18 + Vite + React Router + Axios + Recharts
- **Backend** — Django 5 + Django REST Framework + SimpleJWT
- **Banco** — PostgreSQL

Geração de PDF (ReportLab + Matplotlib) e QR Code (biblioteca `qrcode`) ficam no servidor.

## Monografia

O documento completo do TCC (57 páginas, formato ABNT) está em [`Monografia_TCC_Victor.pdf`](Monografia_TCC_Victor.pdf). Inclui introdução, levantamento de requisitos, modelagem UML, arquitetura, implementação detalhada, segurança, testes, hospedagem, limitações e referências bibliográficas, além do Apêndice B com 21 listagens de código dos módulos principais.

## Estrutura do repositório

```
TCC/
├── backend_tcc/                 Servidor Django (porta 8000)
├── frontend_tcc/                Aplicação React (porta 5173)
├── typst/figuras/               Diagramas UML, ER e sequência (PNG)
├── Monografia_TCC_Victor.pdf    Monografia completa do TCC
├── Documentacao_Sistema_TCC.pdf Documentação técnica detalhada
├── unicamp.png                  Brasão da UNICAMP (usado nas capas)
├── iniciar-sistema.bat          Atalho para iniciar os dois servidores
└── README.md                    Este arquivo
```

Para instruções específicas, veja [`backend_tcc/README.md`](backend_tcc/README.md) e [`frontend_tcc/README.md`](frontend_tcc/README.md).

## Como rodar localmente (Windows)

**Pré-requisitos:** Python 3.11+, Node.js 18+, PostgreSQL 14+.

1. Clone o repositório:
   ```bash
   git clone https://github.com/<usuario>/<repo>.git
   cd <repo>
   ```
2. Configure o backend:
   ```bash
   cd backend_tcc
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   copy .env.example .env       # depois edite o .env com sua senha do Postgres
   python manage.py migrate
   python manage.py createsuperuser
   ```
3. Configure o frontend:
   ```bash
   cd ../frontend_tcc
   npm install
   ```
4. Em vez de subir manualmente, dê duplo clique em `iniciar-sistema.bat` na raiz — ele abre o backend e o frontend em janelas separadas e abre o navegador em `http://localhost:5173`.

## Funcionalidades principais

- Autenticação JWT por e-mail institucional, com papéis `admin` e `professor`.
- Primeiro login do professor força definição de senha pessoal.
- Recuperação de senha por e-mail (link com token expirável).
- Cadastro de professores e disciplinas pelo admin.
- Geração automática de QR Code único por disciplina.
- Formulário público de avaliação acessado via QR Code (sem login, anônimo).
- 24 perguntas-padrão da FT-UNICAMP aplicadas automaticamente a toda disciplina nova.
- Painel admin para editar/excluir perguntas-padrão e propagar mudanças para disciplinas existentes.
- Dashboard com totais e médias por pergunta.
- Geração de relatório consolidado em PDF (gráficos por pergunta, média ± desvio padrão, tamanho amostral, comentários abertos).
- Controle de acesso: cada professor visualiza apenas as próprias disciplinas e relatórios.
- Anonimato preservado: respostas não têm vínculo com nenhum usuário.

## Documentação técnica

Para detalhes de cada parte do código (modelos, views, fluxos), consulte o arquivo [`Documentacao_Sistema_TCC.pdf`](Documentacao_Sistema_TCC.pdf) — diagramas, endpoints e descrição de todos os fluxos, com trechos de código em syntax highlighting.

## Vídeo demonstrativo

Vídeo percorrendo o ciclo completo do sistema — login do admin, cadastro de professor e disciplina, primeiro login do professor com troca de senha, escaneamento do QR Code, submissão anônima e geração do relatório PDF.

Disponível em: [https://youtu.be/Vi92iTVklQ8](https://youtu.be/Vi92iTVklQ8)

## Licença

Trabalho acadêmico. Uso livre para fins educacionais. Para uso institucional ou comercial, consultar o autor.
