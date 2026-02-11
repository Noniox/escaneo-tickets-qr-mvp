@echo off
cd /d "%~dp0"
title SISTEMA ACCESO - EVENTO

echo ===================================================
echo   INICIANDO SISTEMA
echo ===================================================
echo.

if not exist venv (
    echo [ERROR] Entorno virtual 'venv' no encontrado.
    echo Debe ejecutar _INSTALAR_PRIMERO.bat antes de usar el sistema.
    pause
    exit /b
)

echo 1. Activando entorno...
call venv\Scripts\activate

echo 2. Iniciando servidor...
echo    (Por favor permita el acceso en el Firewall si se le solicita)
echo.
echo Presione Ctrl+C para detener el servidor.
echo.

start http://localhost:8000

python app.py

pause
