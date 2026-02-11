@echo off
rem Obtener directorio raiz (padre de scripts/)
cd /d "%~dp0.."
set ROOT_DIR=%CD%

echo ========================================================
echo MODO TUNEL - ACCESO REMOTO
echo ========================================================
echo.
echo Directorio Raiz detectado: %ROOT_DIR%
echo.

if not exist venv (
    echo [ERROR] No encuentro 'venv' en %ROOT_DIR%
    echo Ejecuta _INSTALAR_PRIMERO.bat primero.
    pause
    exit /b
)

echo 1. Iniciando servidor local (HTTP)...
rem Usamos /D para forzar el directorio de inicio del nuevo CMD
start "Servidor Ticket App" /D "%ROOT_DIR%" cmd /k "call venv\Scripts\activate && set NO_SSL=1 && python app.py"

echo.
echo Esperando servidor...
timeout /t 5 >nul

echo 2. Iniciando tunel...
echo.
echo ========================================================
echo IMPORTANTE - PASSWORD DEL TUNEL
echo ========================================================
echo Si al abrir el link te pide un PASSWORD:
echo 1. Entra a: https://loca.lt/mytunnelpassword
echo 2. Copia la IP que aparece ahi.
echo 3. Pegala en la pagina del tunel.
echo ========================================================
echo.
echo URL DEL TUNEL (Copia la de abajo):
call npx localtunnel --port 8000
pause
