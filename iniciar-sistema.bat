@echo off
title Iniciador - Sistema de Avaliacao de Disciplinas (FT/UNICAMP)

echo.
echo ============================================================
echo  Sistema Web de Avaliacao de Disciplinas - FT/UNICAMP
echo ============================================================
echo.

REM Verifica se o venv do backend existe
if not exist "%~dp0backend_tcc\venv\Scripts\activate.bat" (
    echo [ERRO] Ambiente virtual nao encontrado em backend_tcc\venv
    echo.
    echo Para criar o ambiente, rode:
    echo   cd backend_tcc
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Verifica se as dependencias do frontend estao instaladas
if not exist "%~dp0frontend_tcc\node_modules" (
    echo [AVISO] node_modules nao encontrado em frontend_tcc.
    echo Vou rodar 'npm install' antes de subir os servidores...
    echo.
    pushd "%~dp0frontend_tcc"
    call npm install
    popd
    echo.
)

echo Iniciando os servidores em janelas separadas...
echo    - Backend  (Django) -^> http://127.0.0.1:8000
echo    - Frontend (React)  -^> http://localhost:5173
echo.

REM === BACKEND (Django) ===
start "Backend Django (TCC)" cmd /k "cd /d %~dp0backend_tcc && call venv\Scripts\activate && python manage.py runserver"

REM Da tempo do Django subir antes do Vite tentar usar a API
timeout /t 4 /nobreak >nul

REM === FRONTEND (Vite + React) ===
start "Frontend React (TCC)" cmd /k "cd /d %~dp0frontend_tcc && npm run dev"

REM Aguarda o Vite ficar pronto antes de abrir o navegador
timeout /t 6 /nobreak >nul

REM Abre o navegador padrao na pagina de login
start "" http://localhost:5173

echo.
echo Pronto! Duas janelas foram abertas:
echo    - "Backend Django (TCC)"  - mantenha aberta enquanto usa o sistema
echo    - "Frontend React (TCC)"  - idem
echo.
echo Para encerrar o sistema, basta fechar as duas janelas.
echo.
timeout /t 5 >nul
exit
