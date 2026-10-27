"""
=============================================================================
EJEMPLO 07: Sistema de Partículas y Efectos Visuales Avanzados
=============================================================================
En este archivo aprenderás:
1. Cómo diseñar un sistema de partículas modular (emisor y partículas individuales).
2. Manejo de ciclo de vida: tiempo de vida (lifespan), desvanecimiento alfa (Fade Out)
   y reducción de tamaño.
3. Simulación de fuerzas físicas simples: gravedad, resistencia del aire y dispersión.
4. Mezcla aditiva (pygame.BLEND_ADD) para conseguir un efecto brillante y resplandeciente (Glow).
5. Tres modos interactivos: Antorcha de Fuego, Estallido de Fuegos Artificiales y
   Polvo Mágico que sigue al cursor del ratón.
=============================================================================
"""

import sys
import math
import random
import pygame

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("07 - Pygame: Sistema de Partículas y Efectos de Resplandor")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("Consolas", 15)

FONDO = (10, 12, 16)

# =============================================================================
# CLASE PARTÍCULA
# =============================================================================
class Particula:
    def __init__(self, x, y, vx, vy, color, tam_inicial, vida_max, gravedad=0.0):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.color = color
        self.tam_inicial = tam_inicial
        self.vida_max = vida_max
        self.vida = vida_max
        self.gravedad = gravedad

    @property
    def viva(self):
        return self.vida > 0.0

    def update(self, dt):
        self.vida -= dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += self.gravedad * dt

    def draw(self, superficie):
        if not self.viva:
            return

        progreso = max(0.0, self.vida / self.vida_max)
        radio_actual = max(1, int(self.tam_inicial * progreso))
        alfa_actual = int(255 * progreso)

        # Para renderizar partículas con transparencia y brillo, usamos una superficie dedicada
        tam_surf = radio_actual * 4
        surf_particula = pygame.Surface((tam_surf, tam_surf), pygame.SRCALPHA)

        # Círculo central con alfa
        r, g, b = self.color
        pygame.draw.circle(surf_particula, (r, g, b, alfa_actual), (tam_surf // 2, tam_surf // 2), radio_actual)

        # Resplandor suave periférico
        pygame.draw.circle(surf_particula, (r, g, b, alfa_actual // 3), (tam_surf // 2, tam_surf // 2), radio_actual * 2)

        # Aplicamos con modo aditivo para que los colores se sumen e iluminen
        superficie.blit(surf_particula, (int(self.x - tam_surf // 2), int(self.y - tam_surf // 2)), special_flags=pygame.BLEND_ADD)

# =============================================================================
# EMISOR Y ADMINISTRADOR DE PARTÍCULAS
# =============================================================================
class SistemaParticulas:
    def __init__(self):
        self.particulas = []

    def emitir_fuego(self, x, y, cantidad=4):
        """Genera una llama ascendente con tonos rojizos, anaranjados y amarillos."""
        for _ in range(cantidad):
            vx = random.uniform(-25, 25)
            vy = random.uniform(-140, -60)
            vida = random.uniform(0.3, 0.8)
            tam = random.uniform(8, 16)
            # Gradiente de fuego
            color = random.choice([
                (255, 60, 20),   # Rojo vivo
                (255, 150, 30),  # Naranja
                (255, 220, 60),  # Amarillo incandescente
            ])
            self.particulas.append(Particula(x, y, vx, vy, color, tam, vida, gravedad=-20.0))

    def emitir_explosion(self, x, y, cantidad=60):
        """Genera un estallido omnidireccional con gravedad física."""
        for _ in range(cantidad):
            angulo = random.uniform(0, 2 * math.pi)
            velocidad = random.uniform(60, 280)
            vx = math.cos(angulo) * velocidad
            vy = math.sin(angulo) * velocidad
            vida = random.uniform(0.6, 1.4)
            tam = random.uniform(4, 9)
            color = random.choice([
                (0, 220, 255), (80, 255, 180), (255, 255, 255), (180, 100, 255)
            ])
            self.particulas.append(Particula(x, y, vx, vy, color, tam, vida, gravedad=220.0))

    def emitir_polvo_magico(self, x, y, cantidad=3):
        """Genera estela mágica flotante tras el cursor."""
        for _ in range(cantidad):
            vx = random.uniform(-30, 30)
            vy = random.uniform(-30, 30)
            vida = random.uniform(0.4, 0.9)
            tam = random.uniform(4, 7)
            color = (255, 120, 230)
            self.particulas.append(Particula(x, y, vx, vy, color, tam, vida, gravedad=10.0))

    def update(self, dt):
        for p in self.particulas:
            p.update(dt)
        # Eliminamos las partículas expiradas (filtrado in-place)
        self.particulas = [p for p in self.particulas if p.viva]

    def draw(self, superficie):
        for p in self.particulas:
            p.draw(superficie)

# =============================================================================
# BUCLE PRINCIPAL
# =============================================================================
def main():
    sistema = SistemaParticulas()
    modo_emision = "FUEGO"  # "FUEGO", "ESTELA"
    pos_antorcha = (ANCHO // 2, ALTO - 140)

    ejecutando = True
    while ejecutando:
        dt = reloj.tick(60) / 1000.0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_1:
                    modo_emision = "FUEGO"
                elif evento.key == pygame.K_2:
                    modo_emision = "ESTELA"
                elif evento.key == pygame.K_SPACE:
                    # Estallido en el centro de la pantalla
                    sistema.emitir_explosion(ANCHO // 2, ALTO // 2, cantidad=100)

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    # Clic izquierdo detona una explosión de chispas en las coordenadas del clic
                    sistema.emitir_explosion(evento.pos[0], evento.pos[1], cantidad=75)

        # Emisión continua según el modo activo
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if modo_emision == "FUEGO":
            sistema.emitir_fuego(pos_antorcha[0], pos_antorcha[1], cantidad=5)
        elif modo_emision == "ESTELA":
            sistema.emitir_polvo_magico(mouse_x, mouse_y, cantidad=3)

        sistema.update(dt)

        # Dibujado
        pantalla.fill(FONDO)

        # Si el fuego está activo, dibujamos un pedestal/antorcha
        if modo_emision == "FUEGO":
            rect_antorcha = pygame.Rect(pos_antorcha[0] - 20, pos_antorcha[1] + 10, 40, 70)
            pygame.draw.rect(pantalla, (60, 65, 75), rect_antorcha, border_radius=4)
            pygame.draw.circle(pantalla, (100, 110, 130), (pos_antorcha[0], pos_antorcha[1] + 10), 22)

        # Renderizamos todas las partículas
        sistema.draw(pantalla)

        # Interfaz de ayuda
        lineas_ayuda = [
            "--- CONTROLES DEL SISTEMA DE PARTÍCULAS ---",
            f"Modo actual: {modo_emision}  |  Partículas vivas: {len(sistema.particulas)}",
            "[1]: Modo Antorcha de Fuego Continua",
            "[2]: Modo Polvo Mágico en el Cursor",
            "[Clic Izquierdo] o [Espacio]: Provocar Estallido de Chispas",
            "Presiona ESC para salir"
        ]

        # Caja de texto
        pygame.draw.rect(pantalla, (15, 18, 24), (10, 10, 470, 155), border_radius=8)
        pygame.draw.rect(pantalla, (45, 52, 68), (10, 10, 470, 155), width=1, border_radius=8)

        for i, linea in enumerate(lineas_ayuda):
            color = (0, 230, 255) if i == 0 else (220, 225, 235)
            pantalla.blit(fuente.render(linea, True, color), (20, 20 + i * 22))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
