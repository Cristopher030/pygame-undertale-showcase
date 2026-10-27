"""
=============================================================================
EJEMPLO 04: Detección y Resolución de Colisiones (Físicas 2D)
=============================================================================
En este archivo aprenderás:
1. Detección de colisiones Rectángulo contra Rectángulo (AABB - colliderect).
2. Detección de colisiones Círculo contra Círculo mediante distancia vectorial.
3. Detección de punto contra rectángulo (collidepoint).
4. Resolución de colisiones: cómo evitar que un personaje atraviese paredes
   separando los ejes X e Y de manera independiente.
5. Visualización del estado de colisión en tiempo real con cambios de color.
=============================================================================
"""

import sys
import math
import pygame

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("04 - Pygame: Detección y Resolución de Colisiones")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("Consolas", 15)

# Colores
FONDO       = (25, 26, 32)
COLOR_LIBRE = (46, 204, 113)
COLOR_CHOQUE= (231, 76, 60)
COLOR_MURO  = (108, 122, 137)
COLOR_JUGADOR = (52, 152, 219)
BLANCO      = (240, 240, 240)

def main():
    # -------------------------------------------------------------
    # 1. Jugador con resolución de colisiones contra paredes
    # -------------------------------------------------------------
    jugador_rect = pygame.Rect(100, 450, 40, 40)
    velocidad_jugador = 240.0

    # Obstáculos estáticos (paredes)
    paredes = [
        pygame.Rect(250, 380, 40, 180),
        pygame.Rect(380, 440, 180, 40),
        pygame.Rect(620, 350, 40, 210)
    ]

    # -------------------------------------------------------------
    # 2. Círculos interactivos (Colisión radial)
    # -------------------------------------------------------------
    circulo_fijo_pos = pygame.math.Vector2(250, 180)
    circulo_fijo_radio = 50

    # -------------------------------------------------------------
    # 3. Rectángulo de prueba que sigue al cursor
    # -------------------------------------------------------------
    rect_objetivo = pygame.Rect(520, 120, 120, 100)

    ejecutando = True
    while ejecutando:
        dt = reloj.tick(60) / 1000.0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False

        # -------------------------------------------------------------
        # A) MOVIMIENTO Y RESOLUCIÓN DE COLISIONES CON PAREDES
        # -------------------------------------------------------------
        # Técnica clave en videojuegos 2D:
        # Se mueve primero en el eje X y se corrigen colisiones en X.
        # Luego se mueve en el eje Y y se corrigen colisiones en Y.
        # Esto permite que el personaje "deslice" suavemente por las paredes.
        teclas = pygame.key.get_pressed()
        dx, dy = 0, 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dx -= 1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dx += 1
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            dy -= 1
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            dy += 1

        desplazamiento_x = int(dx * velocidad_jugador * dt)
        desplazamiento_y = int(dy * velocidad_jugador * dt)

        # 1. Movimiento en X y resolución
        jugador_rect.x += desplazamiento_x
        for pared in paredes:
            if jugador_rect.colliderect(pared):
                if desplazamiento_x > 0:  # Moviéndose a la derecha
                    jugador_rect.right = pared.left
                elif desplazamiento_x < 0: # Moviéndose a la izquierda
                    jugador_rect.left = pared.right

        # 2. Movimiento en Y y resolución
        jugador_rect.y += desplazamiento_y
        for pared in paredes:
            if jugador_rect.colliderect(pared):
                if desplazamiento_y > 0:  # Cayendo / moviéndose hacia abajo
                    jugador_rect.bottom = pared.top
                elif desplazamiento_y < 0: # Saltando / moviéndose hacia arriba
                    jugador_rect.top = pared.bottom

        # Límites de la ventana
        jugador_rect.clamp_ip(pygame.Rect(0, 300, ANCHO, 300))

        # -------------------------------------------------------------
        # B) COLISIÓN CÍRCULO CONTRA CÍRCULO (Basada en Distancia)
        # -------------------------------------------------------------
        mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
        circulo_mouse_radio = 30
        distancia = mouse_pos.distance_to(circulo_fijo_pos)
        suma_radios = circulo_fijo_radio + circulo_mouse_radio
        colision_circulos = distancia < suma_radios

        # -------------------------------------------------------------
        # C) COLISIÓN PUNTO CONTRA RECTÁNGULO (collidepoint)
        # -------------------------------------------------------------
        colision_mouse_rect = rect_objetivo.collidepoint((int(mouse_pos.x), int(mouse_pos.y)))

        # -------------------------------------------------------------
        # RENDERIZADO
        # -------------------------------------------------------------
        pantalla.fill(FONDO)

        # Línea divisoria de zonas de demostración
        pygame.draw.line(pantalla, (45, 50, 65), (0, 300), (ANCHO, 300), 2)

        # SECCIÓN SUPERIOR: Colisiones Matemáticas y Mouse
        titulo_sup = fuente.render("ZONA 1: Detección Radial (Círculos) y Punto en Rectángulo (Mouse)", True, BLANCO)
        pantalla.blit(titulo_sup, (20, 15))

        # Dibujar círculo fijo
        color_circulo = COLOR_CHOQUE if colision_circulos else COLOR_LIBRE
        pygame.draw.circle(pantalla, color_circulo, (int(circulo_fijo_pos.x), int(circulo_fijo_pos.y)), circulo_fijo_radio, width=3)
        pygame.draw.circle(pantalla, (color_circulo[0]//2, color_circulo[1]//2, color_circulo[2]//2),
                           (int(circulo_fijo_pos.x), int(circulo_fijo_pos.y)), circulo_fijo_radio - 4)

        # Dibujar círculo que sigue al mouse
        pygame.draw.circle(pantalla, color_circulo, (int(mouse_pos.x), int(mouse_pos.y)), circulo_mouse_radio, width=2)
        # Línea de distancia entre centros
        pygame.draw.line(pantalla, BLANCO, (int(circulo_fijo_pos.x), int(circulo_fijo_pos.y)), (int(mouse_pos.x), int(mouse_pos.y)), 1)
        texto_dist = fuente.render(f"Distancia: {distancia:.1f}px (Umbral: {suma_radios}px)", True, BLANCO)
        pantalla.blit(texto_dist, (int((circulo_fijo_pos.x + mouse_pos.x) / 2), int((circulo_fijo_pos.y + mouse_pos.y) / 2) - 15))

        # Dibujar rectángulo interactivo de prueba
        color_rect = COLOR_CHOQUE if colision_mouse_rect else (155, 89, 182)
        pygame.draw.rect(pantalla, color_rect, rect_objetivo, border_radius=6)
        texto_rect = fuente.render("¡Mouse sobre mí!" if colision_mouse_rect else "Pasa el mouse aquí", True, BLANCO)
        pantalla.blit(texto_rect, (rect_objetivo.x + 8, rect_objetivo.y + 40))

        # SECCIÓN INFERIOR: Colisión con Paredes y Deslizamiento
        titulo_inf = fuente.render("ZONA 2: Resolución de Colisiones en Paredes (Mover con Flechas / WASD)", True, BLANCO)
        pantalla.blit(titulo_inf, (20, 315))

        # Dibujar paredes
        for pared in paredes:
            pygame.draw.rect(pantalla, COLOR_MURO, pared, border_radius=4)
            pygame.draw.rect(pantalla, (180, 190, 200), pared, width=2, border_radius=4)

        # Dibujar jugador
        pygame.draw.rect(pantalla, COLOR_JUGADOR, jugador_rect, border_radius=4)
        pygame.draw.rect(pantalla, BLANCO, jugador_rect, width=2, border_radius=4)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
