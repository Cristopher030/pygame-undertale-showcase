"""
=============================================================================
EJEMPLO 02: Manejo de Eventos, Entrada de Usuario y Movimiento Fluido
=============================================================================
En este archivo aprenderás:
1. La diferencia entre eventos discretos (KEYDOWN/KEYUP) y sondeo continuo
   (pygame.key.get_pressed()).
2. Captura de eventos del ratón (posición, clic, movimiento).
3. Movimiento independiente de los fotogramas usando Delta Time (dt).
4. Restricción del personaje dentro de los límites de la pantalla (Clamping).
5. Un objeto con física simple (una bola que rebota contra los bordes).
=============================================================================
"""

import sys
import pygame

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("02 - Pygame: Eventos, Teclado, Ratón y Delta Time")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("Consolas", 16)

# Paleta de colores
FONDO       = (28, 30, 38)
COLOR_JUGADOR = (52, 152, 219)
COLOR_BOLA   = (231, 76, 60)
COLOR_TEXTO  = (230, 230, 230)
COLOR_ACCENTO= (46, 204, 113)

def main():
    # Posición y velocidad del jugador (controlado con teclado)
    jugador_pos = [ANCHO // 4, ALTO // 2]
    jugador_tam = 40
    velocidad_jugador = 300.0  # Píxeles por segundo

    # Posición y velocidad de la bola que rebota
    bola_pos = [float(ANCHO // 2), float(ALTO // 2)]
    bola_vel = [220.0, 180.0]
    bola_radio = 18

    # Historial del último evento discreto registrado
    ultimo_evento = "Ninguno"
    modo_turbo = False

    ejecutando = True
    while ejecutando:
        # 1. Delta Time (dt): Tiempo transcurrido en segundos desde el último fotograma
        # Esto garantiza que la velocidad del juego sea idéntica a 30, 60 o 144 FPS.
        dt = reloj.tick(60) / 1000.0

        # -------------------------------------------------------------
        # A) PROCESAMIENTO DE EVENTOS DISCRETOS
        # Ideales para acciones únicas: pausar, disparar, cambiar de arma, etc.
        # -------------------------------------------------------------
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            elif evento.type == pygame.KEYDOWN:
                ultimo_evento = f"Tecla presionada: {pygame.key.name(evento.key)}"
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_SPACE:
                    modo_turbo = not modo_turbo

            elif evento.type == pygame.KEYUP:
                ultimo_evento = f"Tecla liberada: {pygame.key.name(evento.key)}"

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Clic izquierdo
                    ultimo_evento = f"Clic izquierdo en {evento.pos}"
                    # Teletransportar suavemente al jugador a la posición del ratón
                    jugador_pos[0] = evento.pos[0] - jugador_tam / 2
                    jugador_pos[1] = evento.pos[1] - jugador_tam / 2
                elif evento.button == 3:  # Clic derecho
                    ultimo_evento = f"Clic derecho en {evento.pos}"

        # -------------------------------------------------------------
        # B) SONDEO CONTINUO DE TECLADO (Continuous Polling)
        # Ideal para movimiento continuo y fluido de personajes o cámaras.
        # -------------------------------------------------------------
        teclas = pygame.key.get_pressed()
        velocidad_actual = velocidad_jugador * (2.0 if modo_turbo else 1.0)

        direccion_x = 0
        direccion_y = 0

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            direccion_x -= 1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            direccion_x += 1
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            direccion_y -= 1
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            direccion_y += 1

        # Aplicamos movimiento usando dt (velocidad * dt)
        jugador_pos[0] += direccion_x * velocidad_actual * dt
        jugador_pos[1] += direccion_y * velocidad_actual * dt

        # Mantener al jugador dentro de los límites de la ventana (Clamping)
        jugador_pos[0] = max(0, min(ANCHO - jugador_tam, jugador_pos[0]))
        jugador_pos[1] = max(0, min(ALTO - jugador_tam, jugador_pos[1]))

        # -------------------------------------------------------------
        # C) FÍSICA SIMPLE DE LA BOLA (Rebotes en bordes)
        # -------------------------------------------------------------
        bola_pos[0] += bola_vel[0] * dt
        bola_pos[1] += bola_vel[1] * dt

        # Rebote en eje X
        if bola_pos[0] - bola_radio <= 0:
            bola_pos[0] = bola_radio
            bola_vel[0] *= -1
        elif bola_pos[0] + bola_radio >= ANCHO:
            bola_pos[0] = ANCHO - bola_radio
            bola_vel[0] *= -1

        # Rebote en eje Y
        if bola_pos[1] - bola_radio <= 0:
            bola_pos[1] = bola_radio
            bola_vel[1] *= -1
        elif bola_pos[1] + bola_radio >= ALTO:
            bola_pos[1] = ALTO - bola_radio
            bola_vel[1] *= -1

        # -------------------------------------------------------------
        # D) RENDERIZADO
        # -------------------------------------------------------------
        pantalla.fill(FONDO)

        # Dibujar jugador (Cuadrado azul)
        rect_jugador = pygame.Rect(int(jugador_pos[0]), int(jugador_pos[1]), jugador_tam, jugador_tam)
        pygame.draw.rect(pantalla, COLOR_JUGADOR, rect_jugador, border_radius=6)
        pygame.draw.rect(pantalla, (255, 255, 255), rect_jugador, width=2, border_radius=6)

        # Dibujar bola rebotante (Círculo rojo)
        pygame.draw.circle(pantalla, COLOR_BOLA, (int(bola_pos[0]), int(bola_pos[1])), bola_radio)

        # Información del cursor del ratón
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.circle(pantalla, COLOR_ACCENTO, (mouse_x, mouse_y), 6, width=2)
        pygame.draw.line(pantalla, (100, 100, 120), (rect_jugador.centerx, rect_jugador.centery), (mouse_x, mouse_y), 1)

        # Panel de diagnóstico y textos informativos
        info_lineas = [
            "--- CONTROLES Y DIAGNÓSTICO ---",
            "Mover: Teclas Flechas o W, A, S, D",
            f"Espacio: Alternar Modo Turbo (Activo: {modo_turbo})",
            "Clic Izquierdo: Teletransportar personaje",
            f"Posición del Jugador: X={jugador_pos[0]:.1f}, Y={jugador_pos[1]:.1f}",
            f"Posición del Ratón: X={mouse_x}, Y={mouse_y}",
            f"Delta Time: {dt:.4f} s | FPS: {reloj.get_fps():.1f}",
            f"Último Evento: {ultimo_evento}",
            "Presiona ESC para salir"
        ]

        # Caja de fondo para texto
        pygame.draw.rect(pantalla, (15, 16, 22), (10, 10, 460, 210), border_radius=8)
        pygame.draw.rect(pantalla, (60, 65, 80), (10, 10, 460, 210), width=1, border_radius=8)

        for i, linea in enumerate(info_lineas):
            color = COLOR_ACCENTO if i == 0 else COLOR_TEXTO
            superficie_texto = fuente.render(linea, True, color)
            pantalla.blit(superficie_texto, (20, 20 + i * 20))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
