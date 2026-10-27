@echo off
title Lanzador de Ejemplos Pygame
:menu
cls
echo ========================================================
echo        LANZADOR DE EJEMPLOS DE PYGAME
echo ========================================================
echo  1. Ventana, Game Loop y Formas Geometricas
echo  2. Eventos, Teclado, Raton y Delta Time
echo  3. Sprites, Grupos y Animaciones Procedurales
echo  4. Deteccion y Resolucion de Colisiones 2D
echo  5. Interfaz de Usuario, Botones y Dialogo
echo  6. Sintetizador de Audio Chiptune y Osciloscopio
echo  7. Sistema de Particulas y Efecto Resplandor (Glow)
echo  8. JUGAR: Videojuego Inspirado en Undertale
echo  0. Salir
echo ========================================================
set /p opc="Selecciona un numero (0-8): "

if "%opc%"=="1" python ejemplos\01_ventana_y_formas.py
if "%opc%"=="2" python ejemplos\02_eventos_y_movimiento.py
if "%opc%"=="3" python ejemplos\03_sprites_y_animaciones.py
if "%opc%"=="4" python ejemplos\04_colisiones_y_fisicas.py
if "%opc%"=="5" python ejemplos\05_texto_interfaz_usuario.py
if "%opc%"=="6" python ejemplos\06_sonido_sintetizado.py
if "%opc%"=="7" python ejemplos\07_sistema_particulas.py
if "%opc%"=="8" python juego_undertale\main.py
if "%opc%"=="0" exit

goto menu
