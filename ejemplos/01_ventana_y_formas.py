"""
=============================================================================
EJEMPLO 01: Creación de Ventana y Dibujo de Formas Geométricas
=============================================================================
En este archivo aprenderás:
1. Cómo inicializar la librería Pygame (pygame.init()).
2. Cómo crear una ventana con resolución personalizada y título.
3. El funcionamiento del "Game Loop" (Bucle de Juego) esencial.
4. El control de cuadros por segundo (FPS) con pygame.time.Clock.
5. El sistema de coordenadas (origen (0,0) en la esquina superior izquierda).
6. Dibujo de primitivas geométricas: rectángulos, círculos, polígonos,
   líneas, elipses y figuras con transparencia (canal Alpha).
=============================================================================
"""

import sys
import math
import pygame

# 1. Inicialización obligatoria de todos los submódulos de Pygame
pygame.init()

# 2. Configuración de dimensiones de pantalla y título
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("01 - Pygame: Ventana y Formas Geométricas")

# 3. Reloj para controlar la tasa de refresco (FPS)
reloj = pygame.time.Clock()
FPS = 60

# 4. Definición de colores en formato RGB (Rojo, Verde, Azul) de 0 a 255
NEGRO       = (20, 24, 30)
BLANCO      = (245, 245, 245)
ROJO        = (231, 76, 60)
VERDE       = (46, 204, 113)
AZUL        = (52, 152, 219)
AMARILLO    = (241, 196, 15)
MORADO      = (155, 89, 182)
TURQUESA    = (26, 188, 156)
GRIS_OSCURO = (44, 62, 80)

# Fuente para mostrar instrucciones en pantalla
fuente = pygame.font.SysFont("Arial", 16)

def main():
    ejecutando = True
    angulo_animacion = 0.0

    while ejecutando:
        # A) PROCESAMIENTO DE EVENTOS
        # pygame.event.get() obtiene todos los eventos ocurridos desde el último ciclo
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False

        # B) ACTUALIZACIÓN DE ESTADO
        # Hacemos oscilar un ángulo para ver dinamismo en las formas
        angulo_animacion += 0.03
        oscilacion = math.sin(angulo_animacion) * 20

        # C) RENDERIZADO / DIBUJADO
        # Limpiamos la pantalla rellenándola con el color de fondo
        pantalla.fill(NEGRO)

        # -------------------------------------------------------------
        # 1. Rectángulos (pygame.draw.rect)
        # -------------------------------------------------------------
        # Rectángulo sólido: (pantalla, color, (x, y, ancho, alto))
        rect_solido = pygame.Rect(50, 60, 140, 90)
        pygame.draw.rect(pantalla, ROJO, rect_solido, border_radius=8)

        # Rectángulo con solo borde (especificando width=3)
        rect_borde = pygame.Rect(50, 170, 140, 90)
        pygame.draw.rect(pantalla, AMARILLO, rect_borde, width=3, border_radius=8)

        # -------------------------------------------------------------
        # 2. Círculos (pygame.draw.circle)
        # -------------------------------------------------------------
        # Círculo relleno: (pantalla, color, centro(x, y), radio)
        centro_x = int(300 + oscilacion)
        pygame.draw.circle(pantalla, VERDE, (centro_x, 105), 45)

        # Círculo hueco con grosor de línea
        pygame.draw.circle(pantalla, TURQUESA, (300, 215), 45, width=4)

        # -------------------------------------------------------------
        # 3. Elipses (pygame.draw.ellipse)
        # -------------------------------------------------------------
        rect_elipse = pygame.Rect(440, 70, 160, 70)
        pygame.draw.ellipse(pantalla, MORADO, rect_elipse)

        # -------------------------------------------------------------
        # 4. Polígonos (pygame.draw.polygon)
        # -------------------------------------------------------------
        # Estrella o triángulo conectando una serie de puntos [(x1,y1), (x2,y2), ...]
        puntos_triangulo = [
            (520, 170),
            (460, 260),
            (580, 260)
        ]
        pygame.draw.polygon(pantalla, AZUL, puntos_triangulo)

        # -------------------------------------------------------------
        # 5. Líneas simples y continuas (pygame.draw.line / lines)
        # -------------------------------------------------------------
        # Línea simple con grosor
        pygame.draw.line(pantalla, BLANCO, (650, 60), (750, 150), width=4)

        # Líneas continuas (cadena de puntos)
        puntos_zig_zag = [
            (650, 180), (680, 230), (710, 190), (740, 240), (770, 200)
        ]
        pygame.draw.lines(pantalla, AMARILLO, False, puntos_zig_zag, width=3)

        # -------------------------------------------------------------
        # 6. Superficie con Transparencia (Canal Alfa RGBA)
        # -------------------------------------------------------------
        # Para transparencias reales en Pygame se crea una Surface independiente
        # con la bandera pygame.SRCALPHA
        surf_transparente = pygame.Surface((300, 120), pygame.SRCALPHA)
        # Color RGBA: el 4to valor (130) es la opacidad (0 transparente, 255 opaco)
        surf_transparente.fill((52, 152, 219, 130))
        # Dibujamos un círculo brillante encima de la superficie transparente
        pygame.draw.circle(surf_transparente, (255, 255, 255, 180), (60, 60), 40)
        # Trasladamos ("blit") la superficie sobre la pantalla principal
        pantalla.blit(surf_transparente, (50, 320))

        # -------------------------------------------------------------
        # Textos informativos
        # -------------------------------------------------------------
        etiquetas = [
            ("Rectángulos (fill / border)", (50, 35)),
            ("Círculos (animado / grosor)", (240, 35)),
            ("Elipses y Polígonos", (470, 35)),
            ("Líneas vectoriales", (660, 35)),
            ("Superficie con canal Alfa (Transparencia RGBA)", (50, 295)),
            ("Presiona ESC o cierra la ventana para salir", (260, 560))
        ]
        for texto, pos in etiquetas:
            render = fuente.render(texto, True, BLANCO)
            pantalla.blit(render, pos)

        # D) ACTUALIZACIÓN DE PANTALLA
        # Intercambia los buffers de video (Double Buffering)
        pygame.display.flip()

        # Limitar la ejecución a la velocidad deseada
        reloj.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
