"""
=============================================================================
CLASE ALMA (SOUL) - El icónico Corazón Rojo de Undertale
=============================================================================
Gestiona:
1. Renderizado pixel-perfect del corazón rojo.
2. Movimiento suave en 8 direcciones con restricción dentro de la caja.
3. Modo de precisión (Focus) manteniendo presionada la tecla X / SHIFT.
4. Frames de invulnerabilidad temporal (i-frames) con parpadeo visual.
5. Animación de ruptura al perder toda la vida (Game Over).
=============================================================================
"""

import math
import random
import pygame
from constantes import ROJO_ALMA, BLANCO

def crear_superficie_corazon(escala=1):
    """Genera la textura pixel art del corazón rojo de Undertale."""
    # Matriz binaria 16x16 del corazón clásico
    matriz = [
        "....XX.....XX...",
        "..XXXXXX.XXXXXX.",
        ".XXXXXXXXXXXXXXX",
        "XXXXXXXXXXXXXXXX",
        "XXXXXXXXXXXXXXXX",
        "XXXXXXXXXXXXXXXX",
        ".XXXXXXXXXXXXXX.",
        "..XXXXXXXXXXXX..",
        "...XXXXXXXXXX...",
        "....XXXXXXXX....",
        ".....XXXXXX.....",
        "......XXXX......",
        ".......XX.......",
        "................"
    ]
    alto_matriz = len(matriz)
    ancho_matriz = len(matriz[0])

    surf = pygame.Surface((ancho_matriz * escala, alto_matriz * escala), pygame.SRCALPHA)
    for y, fila in enumerate(matriz):
        for x, char in enumerate(fila):
            if char == 'X':
                rect_pixel = pygame.Rect(x * escala, y * escala, escala, escala)
                surf.fill(ROJO_ALMA, rect_pixel)
    return surf

class Alma:
    def __init__(self, x, y):
        self.escala = 1
        self.image = crear_superficie_corazon(escala=1)
        self.ancho = self.image.get_width()
        self.alto = self.image.get_height()

        self.x = float(x)
        self.y = float(y)
        self.velocidad_base = 150.0  # px/s
        self.velocidad_focus = 85.0   # px/s en modo precisión

        # Hitbox precisa en el centro
        self.hitbox_radio = 5.0

        # Invulnerabilidad
        self.tiempo_invulnerable = 0.0
        self.duracion_invulnerable = 1.2
        self.visible_parpadeo = True

        # Animación de muerte
        self.esta_roto = False
        self.fragmentos = []

    @property
    def rect(self):
        return pygame.Rect(int(self.x - self.ancho / 2), int(self.y - self.alto / 2), self.ancho, self.alto)

    @property
    def invulnerable(self):
        return self.tiempo_invulnerable > 0.0

    def romper(self):
        """Inicia la animación de fractura en pedazos."""
        self.esta_roto = True
        self.fragmentos = []
        for _ in range(6):
            vx = random.uniform(-180, 180)
            vy = random.uniform(-220, -60)
            self.fragmentos.append({
                "x": self.x,
                "y": self.y,
                "vx": vx,
                "vy": vy,
                "gravedad": 400.0,
                "rot": random.uniform(0, 360),
                "v_rot": random.uniform(-300, 300)
            })

    def recibir_impacto(self):
        """Activa los cuadros de invulnerabilidad."""
        if not self.invulnerable and not self.esta_roto:
            self.tiempo_invulnerable = self.duracion_invulnerable
            return True
        return False

    def update(self, dt, limites_caja=None):
        if self.esta_roto:
            for frag in self.fragmentos:
                frag["x"] += frag["vx"] * dt
                frag["y"] += frag["vy"] * dt
                frag["vy"] += frag["gravedad"] * dt
                frag["rot"] += frag["v_rot"] * dt
            return

        # Temporizador de invulnerabilidad y parpadeo
        if self.tiempo_invulnerable > 0.0:
            self.tiempo_invulnerable -= dt
            # Parpadeo cada 0.08 segundos
            self.visible_parpadeo = (int(self.tiempo_invulnerable * 14) % 2 == 0)
        else:
            self.visible_parpadeo = True

        # Movimiento del alma
        teclas = pygame.key.get_pressed()
        velocidad = self.velocidad_focus if (teclas[pygame.K_x] or teclas[pygame.K_LSHIFT]) else self.velocidad_base

        dx, dy = 0, 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dx -= 1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dx += 1
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            dy -= 1
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            dy += 1

        # Normalización diagonal
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        self.x += dx * velocidad * dt
        self.y += dy * velocidad * dt

        # Confinamiento dentro de los bordes interiores de la caja de combate
        if limites_caja:
            borde_interior = 6  # Grosor del muro
            min_x = limites_caja.left + borde_interior + self.ancho / 2
            max_x = limites_caja.right - borde_interior - self.ancho / 2
            min_y = limites_caja.top + borde_interior + self.alto / 2
            max_y = limites_caja.bottom - borde_interior - self.alto / 2

            self.x = max(min_x, min(max_x, self.x))
            self.y = max(min_y, min(max_y, self.y))

    def draw(self, superficie):
        if self.esta_roto:
            # Dibujar fragmentos disparados
            for frag in self.fragmentos:
                surf_frag = pygame.Surface((6, 6), pygame.SRCALPHA)
                surf_frag.fill(ROJO_ALMA)
                rotada = pygame.transform.rotate(surf_frag, frag["rot"])
                superficie.blit(rotada, (int(frag["x"]), int(frag["y"])))
            return

        if self.visible_parpadeo:
            superficie.blit(self.image, (int(self.x - self.ancho / 2), int(self.y - self.alto / 2)))
