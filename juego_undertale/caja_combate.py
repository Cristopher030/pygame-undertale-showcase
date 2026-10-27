"""
=============================================================================
CLASE CAJA DE COMBATE (BATTLE BOX)
=============================================================================
La emblemática caja delimitadora de Undertale.
Permite transiciones suaves (morfismo/interpolación) de tamaño y posición
entre la fase de menús y los diferentes tipos de ataque del enemigo, además
de soportar temblor de pantalla (Screen Shake) al recibir impactos.
=============================================================================
"""

import random
import pygame
from constantes import BLANCO, NEGRO, CAJA_MENU_RECT, CAJA_ESQUIVAR_RECT

class CajaCombate:
    def __init__(self):
        # Rectángulo actual (en coordenadas de coma flotante para Lerp suave)
        self.x = float(CAJA_MENU_RECT.x)
        self.y = float(CAJA_MENU_RECT.y)
        self.ancho = float(CAJA_MENU_RECT.width)
        self.alto = float(CAJA_MENU_RECT.height)

        # Rectángulo objetivo al que se interpola
        self.tar_x = self.x
        self.tar_y = self.y
        self.tar_w = self.ancho
        self.tar_h = self.alto

        self.grosor_borde = 5
        self.velocidad_transicion = 12.0  # Factor lerp

        # Efecto de sacudida (Screen Shake)
        self.intensidad_shake = 0.0
        self.offset_shake_x = 0
        self.offset_shake_y = 0

    @property
    def rect_actual(self):
        return pygame.Rect(
            int(self.x + self.offset_shake_x),
            int(self.y + self.offset_shake_y),
            int(self.ancho),
            int(self.alto)
        )

    def transformar_a_menu(self):
        """Muta la caja a sus proporciones amplias para leer menús y diálogos."""
        self.tar_x = float(CAJA_MENU_RECT.x)
        self.tar_y = float(CAJA_MENU_RECT.y)
        self.tar_w = float(CAJA_MENU_RECT.width)
        self.tar_h = float(CAJA_MENU_RECT.height)

    def transformar_a_esquivar(self, ancho=260, alto=200):
        """Muta la caja al centro de la pantalla para la fase de proyectiles."""
        # Centrado horizontalmente
        self.tar_w = float(ancho)
        self.tar_h = float(alto)
        self.tar_x = float(400 - ancho / 2)
        self.tar_y = float(355 - alto / 2)

    def aplicar_sacudida(self, intensidad=8.0):
        """Aplica temblor visual al recibir daño."""
        self.intensidad_shake = intensidad

    def update(self, dt):
        # Interpolación suave hacia las dimensiones deseadas
        f = min(1.0, self.velocidad_transicion * dt)
        self.x += (self.tar_x - self.x) * f
        self.y += (self.tar_y - self.y) * f
        self.ancho += (self.tar_w - self.ancho) * f
        self.alto += (self.tar_h - self.alto) * f

        # Disipación del temblor
        if self.intensidad_shake > 0.1:
            self.offset_shake_x = random.uniform(-self.intensidad_shake, self.intensidad_shake)
            self.offset_shake_y = random.uniform(-self.intensidad_shake, self.intensidad_shake)
            self.intensidad_shake = max(0.0, self.intensidad_shake - 25.0 * dt)
        else:
            self.intensidad_shake = 0.0
            self.offset_shake_x = 0
            self.offset_shake_y = 0

    def draw(self, superficie):
        r = self.rect_actual
        # Fondo interior negro
        pygame.draw.rect(superficie, NEGRO, r)
        # Borde exterior blanco característico
        pygame.draw.rect(superficie, BLANCO, r, width=self.grosor_borde)
