FRONTEND TCC - Sistema Web de Avaliação de Disciplinas

COMO RODAR

1. Entre na pasta do frontend:
   cd C:\Users\victo\OneDrive\Documentos\TCC\frontend_tcc

2. Instale dependências:
   npm install

3. Rode:
   npm run dev

4. Acesse:
   http://localhost:5173/

ROTAS
/                 Login
/admin            Dashboard do administrador
/professores      Cadastro/listagem de professores
/disciplinas      Cadastro/listagem de disciplinas + QR Code
/relatorios       Relatórios com gráfico e PDF
/professor        Tela do professor com QR Code
/formulario/1     Formulário público da disciplina 1

O backend deve estar rodando em http://127.0.0.1:8000/
