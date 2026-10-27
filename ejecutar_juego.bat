@echo off
title Undertale: Batalla Espectral
echo Iniciando juego inspirado en Undertale...
python juego_undertale\main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Probando con lanzador py...
    py juego_undertale\main.py
)
pause
