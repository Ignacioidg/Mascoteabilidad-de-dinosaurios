@echo off
setlocal enabledelayedexpansion
title DinoMascota Server - Bases de Datos UAI

:: 1. Posicionarse siempre en la carpeta donde esta este archivo bat
cd /d "%~dp0"

echo ==============================================================
echo     DinoMascota - Tablero de Control Paleontologico (UAI)
echo ==============================================================
echo.

:: 2. Deteccion automatica del ejecutable de Python
set "PYTHON_EXE="

if exist "%~dp0.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
    goto :python_found
)

if exist "%~dp0venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0venv\Scripts\python.exe"
    goto :python_found
)

if exist "C:\Ignacio\UAI\PythonEj\.venv\Scripts\python.exe" (
    set "PYTHON_EXE=C:\Ignacio\UAI\PythonEj\.venv\Scripts\python.exe"
    goto :python_found
)

:: Probar python en PATH del sistema
where python >nul 2>&1
if %errorlevel% equ 0 (
    python -c "import sys; sys.exit(0)" >nul 2>&1
    if !errorlevel! equ 0 (
        set "PYTHON_EXE=python"
        goto :python_found
    )
)

:: Probar lanzador py en Windows
where py >nul 2>&1
if %errorlevel% equ 0 (
    py -3 -c "import sys; sys.exit(0)" >nul 2>&1
    if !errorlevel! equ 0 (
        set "PYTHON_EXE=py -3"
        goto :python_found
    )
)

:python_not_found
echo [ERROR] No se encontro ninguna instalacion valida de Python.
echo Asegurate de tener Python 3 instalado o un entorno virtual (.venv).
echo Puedes descargarlo desde https://www.python.org/downloads/
echo.
pause
exit /b 1

:python_found
echo [*] Usando Python: !PYTHON_EXE!

:: 3. Verificar si uvicorn y fastapi estan instalados
!PYTHON_EXE! -c "import fastapi, uvicorn" >nul 2>&1
if !errorlevel! neq 0 (
    echo.
    echo [*] Faltan dependencias del proyecto. Instalando backend/requirements.txt...
    !PYTHON_EXE! -m pip install -r backend/requirements.txt
    if !errorlevel! neq 0 (
        echo [ERROR] No se pudieron instalar las dependencias automaticamente.
        pause
        exit /b 1
    )
)

:: 4. Verificar si la base de datos existe; si no, inicializarla
if not exist "backend\database\dinomascota.db" (
    echo.
    echo [*] Base de datos no encontrada. Inicializando dinomascota.db...
    !PYTHON_EXE! init_database.py
)

:: 5. Abrir navegador e iniciar Uvicorn
echo.
echo [*] Iniciando servidor web en http://localhost:8000 ...
start http://localhost:8000

!PYTHON_EXE! -m uvicorn backend.app:app --reload --port 8000
pause
