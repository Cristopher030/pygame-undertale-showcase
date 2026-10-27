"""
=============================================================================
CLASE ENEMIGO: BOB EL ESPECTRO (Inspirado en Napstablook / Froggit)
=============================================================================
Entidad enemiga que interactúa con el jugador. Incluye:
1. Renderizado procedimental en blanco y negro característico de Undertale.
2. Animación de flotación y balanceo senoidal continuo.
3. Expresiones faciales reactivas (Neutro, Feliz/Sonrojado, Herido).
4. Sistema de Diálogo en Bocadillo estilo cómic.
5. Estadísticas de Combate: Puntos de Vida (HP) y Medidor de Piedad (Mercy).
=============================================================================
"""

import math
import random
import pygame
from constantes import BLANCO, NEGRO, GRIS_CLARO, GRIS_MEDIO, AMARILLO_HP, ROJO_ALMA

class Enemigo:
    def __init__(self, x=400, y=140):
        self.x = float(x)
        self.y = float(y)
        self.y_base = float(y)
        self.tiempo_animacion = 0.0

        # Estadísticas
        self.nombre = "Bob el Espectro"
        self.hp_max = 100
        self.hp = 100
        self.piedad = 0  # 0 a 100
        self.perdonable = False

        # Estados visuales: "NEUTRO", "FELIZ", "HERIDO"
        self.estado_emocional = "NEUTRO"
        self.tiempo_emocion = 0.0

        # Bocadillo de diálogo
        self.mostrar_bocadillo = False
        self.texto_dialogo = ""
        self.texto_dialogo_visible = ""
        self.indice_letra = 0
        self.temporizador_letra = 0.0
        self.bocadillo_terminado = False

    @property
    def derrotado(self):
        return self.hp <= 0

    def recibir_ataque(self, danio):
        self.hp = max(0, self.hp - danio)
        self.estado_emocional = "HERIDO"
        self.tiempo_emocion = 1.0

    def aumentar_piedad(self, cantidad):
        self.piedad = min(100, self.piedad + cantidad)
        if self.piedad >= 100:
            self.perdonable = True
        self.estado_emocional = "FELIZ"
        self.tiempo_emocion = 3.0

    def decir(self, mensaje):
        """Activa el bocadillo de diálogo con el mensaje indicado."""
        self.mostrar_bocadillo = True
        self.texto_dialogo = mensaje
        self.texto_dialogo_visible = ""
        self.indice_letra = 0
        self.temporizador_letra = 0.0
        self.bocadillo_terminado = False

    def ocultar_dialogo(self):
        self.mostrar_bocadillo = False
        self.texto_dialogo_visible = ""

    def update(self, dt, motor_audio=None):
        self.tiempo_animacion += dt

        # Flotación suave vertical y ligera oscilación horizontal
        self.y = self.y_base + math.sin(self.tiempo_animacion * 2.5) * 8
        offset_x = math.cos(self.tiempo_animacion * 1.8) * 3

        # Temporizador de emoción
        if self.tiempo_emocion > 0.0:
            self.tiempo_emocion -= dt
            if self.tiempo_emocion <= 0.0:
                self.estado_emocional = "NEUTRO"

        # Máquina de escribir del bocadillo de diálogo
        if self.mostrar_bocadillo and not self.bocadillo_terminado:
            self.temporizador_letra += dt
            if self.temporizador_letra >= 0.04:
                self.temporizador_letra = 0.0
                if self.indice_letra < len(self.texto_dialogo):
                    char = self.texto_dialogo[self.indice_letra]
                    self.texto_dialogo_visible += char
                    self.indice_letra += 1
                    # Reproducir bip de texto en caracteres no vacíos
                    if char not in (" ", "\n", ".", ",") and motor_audio:
                        motor_audio.reproducir("bip")
                else:
                    self.bocadillo_terminado = True

    def draw(self, superficie, fuente_dialogo):
        # 1. Dibujar el cuerpo del fantasma (Estilo monocromático retro)
        cx = int(self.x)
        cy = int(self.y)

        # Superficie del fantasma
        surf_fantasma = pygame.Surface((140, 140), pygame.SRCALPHA)
        fcx, fcy = 70, 70

        # Color base del cuerpo
        color_cuerpo = BLANCO if self.estado_emocional != "HERIDO" else (220, 220, 220)

        # Cabeza abovedada y cuerpo en forma de campana
        puntos_cuerpo = [
            (fcx - 40, fcy + 35),
            (fcx - 42, fcy),
            (fcx - 35, fcy - 25),
            (fcx - 20, fcy - 45),
            (fcx, fcy - 50),
            (fcx + 20, fcy - 45),
            (fcx + 35, fcy - 25),
            (fcx + 42, fcy),
            (fcx + 40, fcy + 35),
            # Ondulaciones inferiores de la sábana espectral
            (fcx + 25, fcy + 25),
            (fcx + 10, fcy + 38),
            (fcx - 5, fcy + 24),
            (fcx - 20, fcy + 36),
            (fcx - 35, fcy + 25),
        ]
        pygame.draw.polygon(surf_fantasma, color_cuerpo, puntos_cuerpo)
        pygame.draw.lines(surf_fantasma, (40, 40, 40), True, puntos_cuerpo, 2)

        # Ojos y expresión facial
        if self.estado_emocional == "FELIZ":
            # Ojos cerrados sonrientes (arcos hacia arriba)
            pygame.draw.arc(surf_fantasma, NEGRO, (fcx - 24, fcy - 22, 16, 14), 0, math.pi, 3)
            pygame.draw.arc(surf_fantasma, NEGRO, (fcx + 8, fcy - 22, 16, 14), 0, math.pi, 3)
            # Pequeña boca sonriente
            pygame.draw.arc(surf_fantasma, NEGRO, (fcx - 8, fcy - 4, 16, 10), math.pi, 2 * math.pi, 2)
            # Sonrojo en mejillas (puntos grises claros)
            pygame.draw.circle(surf_fantasma, (190, 190, 190), (fcx - 26, fcy - 4), 5)
            pygame.draw.circle(surf_fantasma, (190, 190, 190), (fcx + 26, fcy - 4), 5)

        elif self.estado_emocional == "HERIDO":
            # Ojos entrecerrados en forma de X o líneas
            pygame.draw.line(surf_fantasma, NEGRO, (fcx - 22, fcy - 18), (fcx - 10, fcy - 10), 3)
            pygame.draw.line(surf_fantasma, NEGRO, (fcx - 22, fcy - 10), (fcx - 10, fcy - 18), 3)
            pygame.draw.line(surf_fantasma, NEGRO, (fcx + 10, fcy - 18), (fcx + 22, fcy - 10), 3)
            pygame.draw.line(surf_fantasma, NEGRO, (fcx + 10, fcy - 10), (fcx + 22, fcy - 18), 3)
            # Boca ondulada de dolor
            pygame.draw.line(surf_fantasma, NEGRO, (fcx - 10, fcy - 2), (fcx + 10, fcy - 2), 2)

        else: # NEUTRO
            # Grandes ojos ovalados negros con lágrimas o pupilas
            pygame.draw.ellipse(surf_fantasma, NEGRO, (fcx - 24, fcy - 25, 14, 20))
            pygame.draw.ellipse(surf_fantasma, NEGRO, (fcx + 10, fcy - 25, 14, 20))
            # Pupilas blancas
            pygame.draw.circle(surf_fantasma, BLANCO, (fcx - 17, fcy - 18), 3)
            pygame.draw.circle(surf_fantasma, BLANCO, (fcx + 17, fcy - 18), 3)
            # Boca pequeña tímida
            pygame.draw.ellipse(surf_fantasma, NEGRO, (fcx - 4, fcy - 2, 8, 5))

        superficie.blit(surf_fantasma, (cx - 70, cy - 70))

        # 2. Dibujar Bocadillo de Diálogo estilo Undertale
        if self.mostrar_bocadillo and self.texto_dialogo_visible:
            # Posición a la derecha de la cabeza del enemigo
            rect_bocadillo = pygame.Rect(cx + 65, cy - 65, 230, 85)
            # Fondo blanco con borde negro
            pygame.draw.rect(superficie, BLANCO, rect_bocadillo, border_radius=10)
            pygame.draw.rect(superficie, NEGRO, rect_bocadillo, width=3, border_radius=10)

            # Puntero triangular que apunta hacia la boca de Bob
            triangulo = [
                (rect_bocadillo.left + 2, cy - 15),
                (rect_bocadillo.left - 14, cy - 8),
                (rect_bocadillo.left + 2, cy - 1)
            ]
            pygame.draw.polygon(superficie, BLANCO, triangulo)
            pygame.draw.line(superficie, NEGRO, triangulo[0], triangulo[1], 3)
            pygame.draw.line(superficie, NEGRO, triangulo[1], triangulo[2], 3)

            # Dividir texto en líneas para ajustarse al bocadillo
            palabras = self.texto_dialogo_visible.split(" ")
            lineas = []
            linea_act = ""
            for p in palabras:
                prueba = f"{linea_act} {p}".strip()
                if fuente_dialogo.size(prueba)[0] < rect_bocadillo.width - 24:
                    linea_act = prueba
                else:
                    lineas.append(linea_act)
                    linea_act = p
            if linea_act:
                lineas.append(linea_act)

            for i, l in enumerate(lineas):
                txt_render = fuente_dialogo.render(l, True, NEGRO)
                superficie.blit(txt_render, (rect_bocadillo.left + 12, rect_bocadillo.top + 10 + i * 22))
