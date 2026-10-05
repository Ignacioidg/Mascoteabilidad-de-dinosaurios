@echo off
title DinoMascota Server
cd /d "C:\Users\mdcom\.gemini\antigravity\scratch\dinomascota\Mascoteabilidad-de-dinosaurios"
echo ==============================================
echo   DinoMascota Server - Bases de Datos UAI
echo ==============================================
echo.
echo Iniciando servidor en http://localhost:8000 ...
start http://localhost:8000
"C:\Ignacio\UAI\PythonEj\.venv\Scripts\python.exe" -m uvicorn backend.app:app --reload --port 8000
pause
