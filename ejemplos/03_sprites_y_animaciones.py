"""
=============================================================================
EJEMPLO 03: Arquitectura con Sprites, Grupos y Animación por Fotogramas
=============================================================================
En este archivo aprenderás:
1. Cómo utilizar la clase base pygame.sprite.Sprite.
2. Cómo organizar y actualizar entidades con pygame.sprite.Group.
3. El ciclo de vida de un Sprite: inicialización, update(dt), renderizado y kill().
4. Cómo construir spritesheets y animaciones de varios fotogramas de forma
   procedimental sin depender de imágenes externas.
5. El manejo del reloj interno de animación para cambiar de fotograma suavemente.
=============================================================================
"""

import sys
import math
import random
import pygame

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("03 - Pygame: Sprites, Grupos y Animaciones")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("Consolas", 15)

# Paleta de colores
FONDO = (22, 27, 34)
BLANCO = (255, 255, 255)
AMARILLO = (255, 215, 0)
AZUL_CIELO = (70, 180, 255)

# =============================================================================
# GENERADOR PROCEDIMENTAL DE GRÁFICOS (Spritesheet procedural)
# =============================================================================
def generar_frames_limo():
    """Genera 4 fotogramas para una criatura gelatinosa (Slime) que salta y respira."""
    frames = []
    colores_cuerpo = (46, 204, 113)
    color_brillo = (168, 240, 201)

    dimensiones = [
        (48, 40),  # Frame 0: Reposo
        (44, 46),  # Frame 1: Estirándose hacia arriba
        (52, 34),  # Frame 2: Aplanándose al caer
        (46, 42)   # Frame 3: Volviendo al estado neutro
    ]

    for ancho, alto in dimensiones:
        surf = pygame.Surface((64, 64), pygame.SRCALPHA)
        offset_y = 64 - alto - 10
        rect_elipse = pygame.Rect((64 - ancho) // 2, offset_y, ancho, alto)
        
        # Cuerpo principal del slime
        pygame.draw.ellipse(surf, colores_cuerpo, rect_elipse)
        # Brillo reflejado
        pygame.draw.circle(surf, color_brillo, (rect_elipse.left + 12, rect_elipse.top + 10), 5)
        # Ojos
        pygame.draw.circle(surf, (10, 30, 20), (rect_elipse.centerx - 8, rect_elipse.centery - 2), 4)
        pygame.draw.circle(surf, (10, 30, 20), (rect_elipse.centerx + 8, rect_elipse.centery - 2), 4)
        # Pupilas blancas
        pygame.draw.circle(surf, (255, 255, 255), (rect_elipse.centerx - 7, rect_elipse.centery - 3), 1)
        pygame.draw.circle(surf, (255, 255, 255), (rect_elipse.centerx + 9, rect_elipse.centery - 3), 1)
        
        frames.append(surf)
    return frames

def generar_frames_estrella():
    """Genera 4 fotogramas de una estrella brillante que rota y parpadea."""
    frames = []
    for f in range(4):
        surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        angulo_base = f * (math.pi / 8)
        puntos = []
        for i in range(8):
            ang = angulo_base + i * (math.pi / 4)
            radio = 12 if i % 2 == 0 else 6
            px = 16 + math.cos(ang) * radio
            py = 16 + math.sin(ang) * radio
            puntos.append((px, py))
        pygame.draw.polygon(surf, AMARILLO, puntos)
        pygame.draw.circle(surf, (255, 255, 255), (16, 16), 3)
        frames.append(surf)
    return frames

# =============================================================================
# CLASE ENTIDAD: LIMO JUGADOR
# =============================================================================
class LimoJugador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = generar_frames_limo()
        self.indice_frame = 0
        self.image = self.frames[self.indice_frame]
        self.rect = self.image.get_rect(center=(x, y))

        # Parámetros de animación
        self.tiempo_frame = 0.15  # segundos por fotograma
        self.temporizador_animacion = 0.0

        # Parámetros de movimiento
        self.velocidad = 220.0
        self.mirando_izquierda = False

    def update(self, dt):
        # 1. Movimiento del jugador
        teclas = pygame.key.get_pressed()
        vx, vy = 0, 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            vx -= 1
            self.mirando_izquierda = True
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            vx += 1
            self.mirando_izquierda = False
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            vy -= 1
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            vy += 1

        # Normalización básica para no correr más rápido en diagonal
        if vx != 0 and vy != 0:
            vx *= 0.7071
            vy *= 0.7071

        self.rect.x += int(vx * self.velocidad * dt)
        self.rect.y += int(vy * self.velocidad * dt)

        # Restricción dentro de la ventana
        self.rect.clamp_ip(pygame.Rect(0, 0, ANCHO, ALTO))

        # 2. Control de animación
        se_mueve = (vx != 0 or vy != 0)
        # Si se mueve, la animación se reproduce más rápido
        velocidad_anim = 0.10 if se_mueve else 0.20
        self.temporizador_animacion += dt

        if self.temporizador_animacion >= velocidad_anim:
            self.temporizador_animacion = 0.0
            self.indice_frame = (self.indice_frame + 1) % len(self.frames)

        frame_actual = self.frames[self.indice_frame]
        # Si mira a la izquierda, invertimos el sprite horizontalmente
        if self.mirando_izquierda:
            self.image = pygame.transform.flip(frame_actual, True, False)
        else:
            self.image = frame_actual

# =============================================================================
# CLASE ENTIDAD: ESTRELLA COLECTABLE
# =============================================================================
class Estrella(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = generar_frames_estrella()
        self.indice_frame = random.randint(0, len(self.frames) - 1)
        self.image = self.frames[self.indice_frame]
        self.rect = self.image.get_rect(center=(x, y))
        self.temporizador = 0.0
        self.tiempo_frame = random.uniform(0.1, 0.2)

        # Flotación suave vertical
        self.y_original = float(y)
        self.tiempo_vida = random.uniform(0, 10)

    def update(self, dt):
        self.temporizador += dt
        self.tiempo_vida += dt

        if self.temporizador >= self.tiempo_frame:
            self.temporizador = 0.0
            self.indice_frame = (self.indice_frame + 1) % len(self.frames)
            self.image = self.frames[self.indice_frame]

        # Movimiento ondulante vertical
        self.rect.centery = int(self.y_original + math.sin(self.tiempo_vida * 3.0) * 8)

# =============================================================================
# BUCLE PRINCIPAL
# =============================================================================
def main():
    # Creación de los grupos de sprites
    # pygame.sprite.Group() administra colecciones de sprites
    grupo_todos = pygame.sprite.Group()
    grupo_estrellas = pygame.sprite.Group()

    # Instanciamos al jugador
    jugador = LimoJugador(ANCHO // 2, ALTO // 2)
    grupo_todos.add(jugador)

    # Generamos estrellas repartidas en la pantalla
    for _ in range(12):
        x = random.randint(50, ANCHO - 50)
        y = random.randint(50, ALTO - 100)
        estrella = Estrella(x, y)
        grupo_todos.add(estrella)
        grupo_estrellas.add(estrella)

    estrellas_recolectadas = 0
    ejecutando = True

    while ejecutando:
        dt = reloj.tick(60) / 1000.0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_r:
                    # Regenerar estrellas con la tecla R
                    for e in grupo_estrellas:
                        e.kill()
                    for _ in range(12):
                        nueva = Estrella(random.randint(50, ANCHO - 50), random.randint(50, ALTO - 100))
                        grupo_todos.add(nueva)
                        grupo_estrellas.add(nueva)

        # Actualiza TODOS los sprites en una sola llamada
        # Cada sprite ejecuta su método update(dt)
        grupo_todos.update(dt)

        # Colisión entre jugador y el grupo de estrellas
        # pygame.sprite.spritecollide: comprueba colisión y con dokill=True elimina las colisionadas
        colisiones = pygame.sprite.spritecollide(jugador, grupo_estrellas, dokill=True)
        if colisiones:
            estrellas_recolectadas += len(colisiones)

        # Dibujado
        pantalla.fill(FONDO)

        # Dibujar cuadrícula decorativa de fondo
        for x in range(0, ANCHO, 40):
            pygame.draw.line(pantalla, (28, 35, 45), (x, 0), (x, ALTO), 1)
        for y in range(0, ALTO, 40):
            pygame.draw.line(pantalla, (28, 35, 45), (0, y), (ANCHO, y), 1)

        # Dibuja todos los sprites del grupo en la pantalla
        grupo_todos.draw(pantalla)

        # Interfaz de usuario (HUD)
        texto_contador = fuente.render(f"Estrellas recolectadas: {estrellas_recolectadas} | Restantes: {len(grupo_estrellas)}", True, AMARILLO)
        texto_ayuda = fuente.render("Mover: Flechas / WASD | R: Regenerar estrellas | ESC: Salir", True, BLANCO)
        pantalla.blit(texto_contador, (20, 20))
        pantalla.blit(texto_ayuda, (20, 45))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
