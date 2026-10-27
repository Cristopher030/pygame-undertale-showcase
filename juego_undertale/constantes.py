"""
=============================================================================
CONSTANTES DEL JUEGO INSPIRADO EN UNDERTALE
=============================================================================
Definición de resoluciones, paletas de colores clásicas de Undertale,
fuentes y estados de la máquina de combate.
=============================================================================
"""

import pygame

# Dimensiones de la pantalla retro
ANCHO_PANTALLA = 800
ALTO_PANTALLA  = 600
FPS = 60

# Paleta de colores Undertale
NEGRO       = (0, 0, 0)
BLANCO      = (255, 255, 255)
ROJO_ALMA   = (255, 0, 0)
AMARILLO_HP = (255, 255, 0)
AMARILLO_PIEDAD = (255, 240, 0)
NARANJA_BOTON = (255, 127, 39)
VERDE_CURAR = (0, 255, 64)
GRIS_OSCURO = (40, 40, 40)
GRIS_MEDIO  = (120, 120, 120)
GRIS_CLARO  = (200, 200, 200)
AZUL_MAGIA  = (66, 135, 245)

# Estados del juego
ESTADO_MENU_COMBATE      = "MENU_COMBATE"
ESTADO_SUBMENU_ACCION    = "SUBMENU_ACCION"
ESTADO_MINIJUEGO_ATAQUE  = "MINIJUEGO_ATAQUE"
ESTADO_DIALOGO_ENEMIGO   = "DIALOGO_ENEMIGO"
ESTADO_ESQUIVAR_ATAQUE   = "ESQUIVAR_ATAQUE"
ESTADO_VICTORIA          = "VICTORIA"
ESTADO_GAME_OVER         = "GAME_OVER"

# Dimensiones estándar de la Caja de Batalla
CAJA_MENU_RECT = pygame.Rect(70, 280, 660, 190)
CAJA_ESQUIVAR_RECT = pygame.Rect(275, 260, 250, 190)

# Datos del Jugador
HP_MAXIMO_INICIAL = 20
NOMBRE_JUGADOR = "FRISK"
LV_JUGADOR = 1
