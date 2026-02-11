@echo off
cd /d "%~dp0"
title INSTALADOR

echo ===================================================
echo   BIENVENIDO AL INSTALADOR
echo ===================================================
echo.
echo Presiona cualquier tecla para comenzar...
pause >nul

echo.
echo [PASO 1] Buscando Python...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ERROR CRITICO]
    echo No se encontro 'python'. Es necesario instalarlo.
    echo Asegurate de marcar "Add Python to PATH" al instalarlo.
    echo Descarga: python.org
    echo.
    echo Presiona una tecla para salir...
    pause >nul
    exit
)
python --version

echo.
echo [PASO 2] Creando entorno virtual 'venv'...
if not exist venv (
    python -m venv venv
    if not exist venv (
        echo.
        echo [ERROR] No se pudo crear la carpeta venv.
        echo Verifica si tienes permisos de escritura.
        pause
        exit
    )
) else (
    echo (Carpeta venv ya existe, continuando...)
)

echo.
echo [PASO 3] Instalando librerias...
call venv\Scripts\activate
python -m pip install -r requirements.txt

echo.
echo [PASO 4] Configurando base de datos...
if exist "scripts\setup_db.py" (
    python scripts/setup_db.py
) else (
    echo [ADVERTENCIA] No se encontro scripts\setup_db.py
)

echo.
echo ===================================================
echo   INSTALACION FINALIZADA CORRECTAMENTE
echo ===================================================
pause
