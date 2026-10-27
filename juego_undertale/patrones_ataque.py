"""
=============================================================================
PATRONES DE ATAQUE (DANMAKU / BULLET HELL ESTILO UNDERTALE)
=============================================================================
Contiene las entidades de proyectiles y los generadores de oleadas de ataque
que el enemigo desata dentro de la caja de combate:
1. Lluvia de Lágrimas Espectrales (Caída vertical con aperturas).
2. Huesos Deslizantes Horizontales.
3. Anillo de Orbes Convergentes.
4. Esferas Rebotantes Caóticas.
5. Rayos Láser Telegrafiados con Línea de Advertencia.
=============================================================================
"""

import math
import random
import pygame
from constantes import BLANCO, ROJO_ALMA, AZUL_MAGIA, AMARILLO_HP

# =============================================================================
# CLASES DE PROYECTILES
# =============================================================================
class ProyectilLagrima:
    """Gotas espectrales alargadas que caen verticalmente."""
    def __init__(self, x, y, vy=140.0):
        self.x = float(x)
        self.y = float(y)
        self.vy = float(vy)
        self.radio = 5.0
        self.danio = 3

    def update(self, dt):
        self.y += self.vy * dt

    def colisiona_con_alma(self, alma):
        distancia = math.hypot(self.x - alma.x, self.y - alma.y)
        return distancia < (self.radio + alma.hitbox_radio)

    def draw(self, superficie):
        # Dibujar gota: círculo y triángulo hacia arriba
        px, py = int(self.x), int(self.y)
        pygame.draw.circle(superficie, BLANCO, (px, py), int(self.radio))
        puntos_cola = [(px - int(self.radio), py), (px + int(self.radio), py), (px, py - int(self.radio * 2))]
        pygame.draw.polygon(superficie, BLANCO, puntos_cola)

class ProyectilHueso:
    """Hueso rectangular blanco que se desplaza horizontalmente."""
    def __init__(self, x, y, ancho, alto, vx):
        self.x = float(x)
        self.y = float(y)
        self.ancho = ancho
        self.alto = alto
        self.vx = float(vx)
        self.danio = 4

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.ancho, self.alto)

    def update(self, dt):
        self.x += self.vx * dt

    def colisiona_con_alma(self, alma):
        return self.rect.colliderect(alma.rect)

    def draw(self, superficie):
        r = self.rect
        pygame.draw.rect(superficie, BLANCO, r, border_radius=3)
        # Nódulos del hueso en los extremos
        pygame.draw.circle(superficie, BLANCO, (r.left + 2, r.top + 2), 4)
        pygame.draw.circle(superficie, BLANCO, (r.right - 2, r.top + 2), 4)
        pygame.draw.circle(superficie, BLANCO, (r.left + 2, r.bottom - 2), 4)
        pygame.draw.circle(superficie, BLANCO, (r.right - 2, r.bottom - 2), 4)

class ProyectilOrbe:
    """Esfera que se mueve con dirección angular continua."""
    def __init__(self, x, y, vx, vy, radio=6.0, danio=3):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.radio = float(radio)
        self.danio = danio

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def colisiona_con_alma(self, alma):
        distancia = math.hypot(self.x - alma.x, self.y - alma.y)
        return distancia < (self.radio + alma.hitbox_radio)

    def draw(self, superficie):
        pygame.draw.circle(superficie, BLANCO, (int(self.x), int(self.y)), int(self.radio))
        pygame.draw.circle(superficie, (180, 220, 255), (int(self.x), int(self.y)), int(self.radio - 2))

class ProyectilRebote:
    """Esfera que rebota elásticamente en los bordes interiores de la caja."""
    def __init__(self, x, y, vx, vy, radio=7.0):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.radio = float(radio)
        self.danio = 3

    def update(self, dt, limites_caja):
        self.x += self.vx * dt
        self.y += self.vy * dt

        borde = 6
        if self.x - self.radio <= limites_caja.left + borde:
            self.x = limites_caja.left + borde + self.radio
            self.vx *= -1
        elif self.x + self.radio >= limites_caja.right - borde:
            self.x = limites_caja.right - borde - self.radio
            self.vx *= -1

        if self.y - self.radio <= limites_caja.top + borde:
            self.y = limites_caja.top + borde + self.radio
            self.vy *= -1
        elif self.y + self.radio >= limites_caja.bottom - borde:
            self.y = limites_caja.bottom - borde - self.radio
            self.vy *= -1

    def colisiona_con_alma(self, alma):
        distancia = math.hypot(self.x - alma.x, self.y - alma.y)
        return distancia < (self.radio + alma.hitbox_radio)

    def draw(self, superficie):
        pygame.draw.circle(superficie, BLANCO, (int(self.x), int(self.y)), int(self.radio))
        pygame.draw.circle(superficie, AMARILLO_HP, (int(self.x), int(self.y)), int(self.radio - 3))

class LaserAvisado:
    """Rayo telegrafiado: aviso con línea roja y disparo letal instantáneo."""
    def __init__(self, y, altura=28, tiempo_aviso=0.75, duracion_activo=0.4):
        self.y = float(y)
        self.altura = altura
        self.tiempo_aviso = tiempo_aviso
        self.duracion_activo = duracion_activo
        self.temporizador = 0.0
        self.activo = False
        self.terminado = False
        self.danio = 4

    def update(self, dt):
        self.temporizador += dt
        if not self.activo:
            if self.temporizador >= self.tiempo_aviso:
                self.activo = True
                self.temporizador = 0.0
        else:
            if self.temporizador >= self.duracion_activo:
                self.terminado = True

    def colisiona_con_alma(self, alma, limites_caja):
        if not self.activo or self.terminado:
            return False
        rect_laser = pygame.Rect(limites_caja.left, int(self.y - self.altura / 2), limites_caja.width, self.altura)
        return rect_laser.colliderect(alma.rect)

    def draw(self, superficie, limites_caja):
        if self.terminado:
            return

        x = limites_caja.left + 5
        w = limites_caja.width - 10

        if not self.activo:
            # Línea de advertencia parpadeante
            alfa = 180 if int(self.temporizador * 16) % 2 == 0 else 60
            surf_aviso = pygame.Surface((w, 4), pygame.SRCALPHA)
            surf_aviso.fill((255, 60, 60, alfa))
            superficie.blit(surf_aviso, (x, int(self.y - 2)))
            # Exclamaciones de peligro en los extremos
            pygame.draw.line(superficie, ROJO_ALMA, (x + 8, self.y - 8), (x + 8, self.y + 8), 2)
            pygame.draw.line(superficie, ROJO_ALMA, (x + w - 8, self.y - 8), (x + w - 8, self.y + 8), 2)
        else:
            # Rayo láser brillante
            rect_haz = pygame.Rect(x, int(self.y - self.altura / 2), w, self.altura)
            pygame.draw.rect(superficie, BLANCO, rect_haz, border_radius=4)
            pygame.draw.rect(superficie, (180, 240, 255), rect_haz.inflate(0, -6), border_radius=4)

# =============================================================================
# GESTOR Y COORDINADOR DE OLEADAS DE ATAQUE
# =============================================================================
class GestorAtaques:
    def __init__(self):
        self.proyectiles = []
        self.laseres = []
        self.tiempo_oleada_restante = 0.0
        self.patron_actual = 0
        self.temporizador_spawn = 0.0
        self.total_patrones = 4

    def iniciar_oleada(self, numero_patron=None, duracion=6.5):
        self.proyectiles.clear()
        self.laseres.clear()
        self.tiempo_oleada_restante = duracion
        self.temporizador_spawn = 0.0

        if numero_patron is not None:
            self.patron_actual = numero_patron % self.total_patrones
        else:
            self.patron_actual = random.randint(0, self.total_patrones - 1)

    @property
    def oleada_terminada(self):
        return self.tiempo_oleada_restante <= 0.0

    def update(self, dt, limites_caja, alma, motor_audio=None):
        self.tiempo_oleada_restante -= dt
        self.temporizador_spawn += dt

        # -------------------------------------------------------------
        # GENERACIÓN DEL PATRÓN ACTUAL
        # -------------------------------------------------------------
        if self.patron_actual == 0:
            # PATRÓN 0: Lluvia de Lágrimas con aperturas
            if self.temporizador_spawn >= 0.22:
                self.temporizador_spawn = 0.0
                # Generar fila con un hueco seguro
                x_inicio = limites_caja.left + 15
                x_fin = limites_caja.right - 15
                hueco_x = random.randint(x_inicio + 30, x_fin - 30)

                for px in range(x_inicio, x_fin, 26):
                    if abs(px - hueco_x) > 35:
                        self.proyectiles.append(ProyectilLagrima(px, limites_caja.top - 10, vy=random.uniform(130, 170)))

        elif self.patron_actual == 1:
            # PATRÓN 1: Huesos horizontales alternados (arriba y abajo)
            if self.temporizador_spawn >= 0.85:
                self.temporizador_spawn = 0.0
                lado = random.choice(["IZQ", "DER"])
                alto_hueso = random.randint(50, 95)
                es_suelo = random.choice([True, False])

                y = limites_caja.bottom - 6 - alto_hueso if es_suelo else limites_caja.top + 6
                vx = 170.0 if lado == "IZQ" else -170.0
                x = limites_caja.left - 20 if lado == "IZQ" else limites_caja.right + 5
                self.proyectiles.append(ProyectilHueso(x, y, ancho=18, alto=alto_hueso, vx=vx))

        elif self.patron_actual == 2:
            # PATRÓN 2: Anillos de Orbes Convergentes
            if self.temporizador_spawn >= 1.4:
                self.temporizador_spawn = 0.0
                cx = limites_caja.centerx
                cy = limites_caja.centery
                radio_anillo = 160.0
                num_orbes = 7
                angulo_base = random.uniform(0, math.pi * 2)

                for i in range(num_orbes):
                    ang = angulo_base + (i * (math.pi * 2 / num_orbes))
                    ox = cx + math.cos(ang) * radio_anillo
                    oy = cy + math.sin(ang) * radio_anillo
                    # Velocidad hacia el alma
                    dir_ang = math.atan2(alma.y - oy, alma.x - ox)
                    vx = math.cos(dir_ang) * 90.0
                    vy = math.sin(dir_ang) * 90.0
                    self.proyectiles.append(ProyectilOrbe(ox, oy, vx, vy, radio=6.0))

        elif self.patron_actual == 3:
            # PATRÓN 3: Rebote caótico + Rayos Telegrafiados
            if len(self.proyectiles) < 4 and self.temporizador_spawn >= 0.4:
                self.temporizador_spawn = 0.0
                ang = random.uniform(0.3, math.pi - 0.3)
                vel = 140.0
                self.proyectiles.append(ProyectilRebote(
                    limites_caja.centerx, limites_caja.centery - 30,
                    math.cos(ang) * vel, math.sin(ang) * vel, radio=8.0
                ))

            # Cada 2 segundos lanza un aviso de rayo horizontal
            if int(self.tiempo_oleada_restante) % 2 == 0 and len(self.laseres) == 0:
                y_laser = random.choice([limites_caja.top + 45, limites_caja.centery, limites_caja.bottom - 45])
                self.laseres.append(LaserAvisado(y_laser, altura=26, tiempo_aviso=0.7, duracion_activo=0.35))

        # -------------------------------------------------------------
        # ACTUALIZACIÓN Y COLISIONES
        # -------------------------------------------------------------
        # Actualizar proyectiles normales
        for p in self.proyectiles:
            if isinstance(p, ProyectilRebote):
                p.update(dt, limites_caja)
            else:
                p.update(dt)

            if p.colisiona_con_alma(alma):
                if alma.recibir_impacto():
                    limites_caja = limites_caja  # referencia
                    if motor_audio:
                        motor_audio.reproducir("danio")
                    return p.danio

        # Actualizar láseres
        for l in self.laseres:
            l.update(dt)
            if l.colisiona_con_alma(alma, limites_caja):
                if alma.recibir_impacto():
                    if motor_audio:
                        motor_audio.reproducir("danio")
                    return l.danio

        # Filtrar proyectiles fuera de la caja (excepto rebotantes)
        margen = 80
        self.proyectiles = [
            p for p in self.proyectiles
            if isinstance(p, ProyectilRebote) or (
                limites_caja.left - margen <= p.x <= limites_caja.right + margen and
                limites_caja.top - margen <= p.y <= limites_caja.bottom + margen
            )
        ]
        self.laseres = [l for l in self.laseres if not l.terminado]

        return 0

    def draw(self, superficie, limites_caja):
        # Clip para no dibujar proyectiles saliendo de la caja de combate
        clip_original = superficie.get_clip()
        superficie.set_clip(limites_caja)

        for l in self.laseres:
            l.draw(superficie, limites_caja)

        for p in self.proyectiles:
            p.draw(superficie)

        superficie.set_clip(clip_original)
