"""
=============================================================================
INTERFAZ DE COMBATE (HUD, MENÚS Y MINIJUEGO DE ATAQUE ESTILO UNDERTALE)
=============================================================================
Gestiona:
1. Los 4 botones principales: [LUCHAR], [ACTUAR], [OBJETO], [PIEDAD].
2. Barra de estado del jugador (Nombre, LV, Barra HP amarillo/rojo).
3. Navegación por teclado clásica (Z: Confirmar, X: Retroceder, Flechas).
4. Submenús interactivos para cada opción con posición del Alma.
5. Minijuego de precisión de Ataque [LUCHAR] con barra deslizante y daño crítico.
=============================================================================
"""

import math
import pygame
from constantes import (
    BLANCO, NEGRO, ROJO_ALMA, AMARILLO_HP, AMARILLO_PIEDAD,
    NARANJA_BOTON, GRIS_OSCURO, GRIS_MEDIO, NOMBRE_JUGADOR, LV_JUGADOR
)
from alma import crear_superficie_corazon

class InterfazCombate:
    def __init__(self):
        # Botones principales
        self.nombres_botones = ["LUCHAR", "ACTUAR", "OBJETO", "PIEDAD"]
        self.indice_boton = 0
        self.rects_botones = [
            pygame.Rect(70, 500, 140, 52),
            pygame.Rect(240, 500, 140, 52),
            pygame.Rect(410, 500, 140, 52),
            pygame.Rect(580, 500, 150, 52)
        ]

        # Mini-icono del alma para menús
        self.alma_icono = crear_superficie_corazon(escala=1)

        # Opciones de Submenús
        self.opciones_actuar = [
            ("Comprobar", "Inspeccionar atributos y descripción"),
            ("Contar Chiste", "Contarle un juego de palabras absurdo"),
            ("Halagar", "Decirle que su sábana es muy elegante"),
            ("Invitar Té", "Ofrecerle una taza imaginaria de infusión")
        ]
        self.inventario = [
            {"nombre": "Tarta Canela", "curacion": 20},
            {"nombre": "Fideo Héroe", "curacion": 15},
            {"nombre": "Té Fantasma", "curacion": 10}
        ]
        self.indice_subopcion = 0

        # Minijuego de [LUCHAR]
        self.ataque_activo = False
        self.cursor_ataque_x = 0.0
        self.cursor_ataque_vel = 480.0
        self.area_ataque_rect = pygame.Rect(120, 310, 560, 120)
        self.golpe_efectuado = False
        self.danio_infligido = 0
        self.anim_slash_timer = 0.0

    def reiniciar_subopcion(self):
        self.indice_subopcion = 0

    def navegar_botones(self, direccion, motor_audio=None):
        viejo = self.indice_boton
        if direccion == "IZQ":
            self.indice_boton = (self.indice_boton - 1) % len(self.nombres_botones)
        elif direccion == "DER":
            self.indice_boton = (self.indice_boton + 1) % len(self.nombres_botones)
        if viejo != self.indice_boton and motor_audio:
            motor_audio.reproducir("select")

    def navegar_subsubmenu(self, direccion, total_opciones, motor_audio=None):
        viejo = self.indice_subopcion
        if direccion == "ARRIBA":
            if self.indice_subopcion >= 2:
                self.indice_subopcion -= 2
        elif direccion == "ABAJO":
            if self.indice_subopcion + 2 < total_opciones:
                self.indice_subopcion += 2
        elif direccion == "IZQ":
            if self.indice_subopcion % 2 == 1:
                self.indice_subopcion -= 1
        elif direccion == "DER":
            if self.indice_subopcion % 2 == 0 and self.indice_subopcion + 1 < total_opciones:
                self.indice_subopcion += 1

        if viejo != self.indice_subopcion and motor_audio:
            motor_audio.reproducir("select")

    # -------------------------------------------------------------
    # MINIJUEGO DE ATAQUE CON BARRA DE PUNTERÍA
    # -------------------------------------------------------------
    def iniciar_minijuego_ataque(self):
        self.ataque_activo = True
        self.cursor_ataque_x = float(self.area_ataque_rect.left + 5)
        self.golpe_efectuado = False
        self.danio_infligido = 0
        self.anim_slash_timer = 0.0

    def actualizar_minijuego_ataque(self, dt):
        if not self.ataque_activo:
            return None

        # Si ya golpeó, reproducir animación de tajo
        if self.golpe_efectuado:
            self.anim_slash_timer += dt
            if self.anim_slash_timer >= 0.6:
                self.ataque_activo = False
                return self.danio_infligido
            return None

        # Mover barra de puntería hacia la derecha
        self.cursor_ataque_x += self.cursor_ataque_vel * dt

        # Si cruza el extremo derecho, es un fallo (MISS)
        if self.cursor_ataque_x >= self.area_ataque_rect.right - 10:
            self.golpe_efectuado = True
            self.danio_infligido = 0
            self.anim_slash_timer = 0.0

        return None

    def golpear_minijuego_ataque(self, motor_audio=None):
        if not self.ataque_activo or self.golpe_efectuado:
            return 0

        self.golpe_efectuado = True
        self.anim_slash_timer = 0.0

        # El centro óptimo del área de ataque
        centro_x = self.area_ataque_rect.centerx
        distancia = abs(self.cursor_ataque_x - centro_x)
        max_dist = self.area_ataque_rect.width / 2.0

        # Cálculo de daño: más cerca del centro = mayor daño (Crítico = 35)
        factor = max(0.0, 1.0 - (distancia / max_dist))
        if factor > 0.92:
            self.danio_infligido = 35  # ¡CRÍTICO!
        else:
            self.danio_infligido = int(12 + factor * 18)

        if motor_audio:
            motor_audio.reproducir("slash")

        return self.danio_infligido

    # -------------------------------------------------------------
    # RENDERIZADO DEL HUD Y ELEMENTOS
    # -------------------------------------------------------------
    def draw_hud(self, superficie, hp_actual, hp_max, fuentes):
        fuente_hud = fuentes["hud"]

        # 1. Nombre y Nivel
        texto_jugador = fuente_hud.render(f"{NOMBRE_JUGADOR}   LV {LV_JUGADOR}", True, BLANCO)
        superficie.blit(texto_jugador, (70, 475))

        # 2. Barra de HP estilo Undertale
        # Etiqueta HP
        texto_hp = fuentes["pequena"].render("HP", True, BLANCO)
        superficie.blit(texto_hp, (290, 478))

        # Caja de la barra
        ancho_barra = 120
        alto_barra = 20
        x_barra = 320
        y_barra = 476

        # Fondo rojo (vida perdida)
        pygame.draw.rect(superficie, ROJO_ALMA, (x_barra, y_barra, ancho_barra, alto_barra))

        # Porción amarilla (vida restante)
        ratio_hp = max(0.0, min(1.0, hp_actual / float(hp_max)))
        ancho_amarillo = int(ancho_barra * ratio_hp)
        pygame.draw.rect(superficie, AMARILLO_HP, (x_barra, y_barra, ancho_amarillo, alto_barra))

        # Texto numérico "HP / HP_MAX"
        texto_cifras = fuente_hud.render(f"{hp_actual} / {hp_max}", True, BLANCO)
        superficie.blit(texto_cifras, (x_barra + ancho_barra + 15, 475))

    def draw_botones(self, superficie, fuentes, estado_actual):
        fuente_btn = fuentes["boton"]
        esta_en_menu_principal = (estado_actual == "MENU_COMBATE")

        for i, nombre in enumerate(self.nombres_botones):
            rect = self.rects_botones[i]
            seleccionado = (i == self.indice_boton) and esta_en_menu_principal

            color_borde = NARANJA_BOTON if seleccionado else (180, 80, 0)
            color_texto = NARANJA_BOTON if seleccionado else (190, 190, 190)

            # Dibujar borde del botón
            pygame.draw.rect(superficie, color_borde, rect, width=3, border_radius=4)

            # Texto del botón
            txt_render = fuente_btn.render(nombre, True, color_texto)
            superficie.blit(txt_render, (rect.left + 35, rect.top + 14))

            # Dibujar corazón a la izquierda del botón si está seleccionado
            if seleccionado:
                superficie.blit(self.alma_icono, (rect.left + 12, rect.centery - 7))

    def draw_submenus(self, superficie, fuentes, boton_activo, enemigo):
        fuente_opc = fuentes["texto"]
        # Posiciones de la cuadrícula de 2 columnas dentro de la caja de diálogo
        posiciones = [
            (120, 310),  # Opción 0: Arriba Izquierda
            (420, 310),  # Opción 1: Arriba Derecha
            (120, 360),  # Opción 2: Abajo Izquierda
            (420, 360)   # Opción 3: Abajo Derecha
        ]

        if boton_activo == "LUCHAR":
            # Selección de objetivo (Bob)
            pos = posiciones[0]
            color = AMARILLO_PIEDAD if enemigo.perdonable else BLANCO
            txt = fuente_opc.render(f"* {enemigo.nombre}", True, color)
            superficie.blit(txt, (pos[0] + 30, pos[1]))
            # Alma señalando
            superficie.blit(self.alma_icono, (pos[0], pos[1] + 4))

            # Barra de HP del enemigo
            ancho_e = 160
            pygame.draw.rect(superficie, ROJO_ALMA, (pos[0] + 280, pos[1] + 6, ancho_e, 14))
            porc_e = enemigo.hp / enemigo.hp_max
            pygame.draw.rect(superficie, (0, 255, 64), (pos[0] + 280, pos[1] + 6, int(ancho_e * porc_e), 14))

        elif boton_activo == "ACTUAR":
            for i, (nombre_opc, _) in enumerate(self.opciones_actuar):
                pos = posiciones[i]
                txt = fuente_opc.render(f"* {nombre_opc}", True, BLANCO)
                superficie.blit(txt, (pos[0] + 30, pos[1]))

                if i == self.indice_subopcion:
                    superficie.blit(self.alma_icono, (pos[0], pos[1] + 4))

        elif boton_activo == "OBJETO":
            if not self.inventario:
                superficie.blit(fuente_opc.render("* (Inventario vacío)", True, GRIS_MEDIO), (120, 310))
            else:
                for i, item in enumerate(self.inventario):
                    pos = posiciones[i]
                    txt = fuente_opc.render(f"* {item['nombre']} (+{item['curacion']})", True, BLANCO)
                    superficie.blit(txt, (pos[0] + 30, pos[1]))

                    if i == self.indice_subopcion:
                        superficie.blit(self.alma_icono, (pos[0], pos[1] + 4))

        elif boton_activo == "PIEDAD":
            opciones_piedad = [
                ("Perdonar", AMARILLO_PIEDAD if enemigo.perdonable else BLANCO),
                ("Huir", BLANCO)
            ]
            for i, (nombre_opc, color) in enumerate(opciones_piedad):
                pos = posiciones[i]
                txt = fuente_opc.render(f"* {nombre_opc}", True, color)
                superficie.blit(txt, (pos[0] + 30, pos[1]))

                if i == self.indice_subopcion:
                    superficie.blit(self.alma_icono, (pos[0], pos[1] + 4))

    def draw_minijuego_ataque(self, superficie, fuentes, enemigo_x, enemigo_y):
        if not self.ataque_activo:
            return

        # 1. Dibujar el marco de puntería estilo Undertale
        r = self.area_ataque_rect
        pygame.draw.rect(superficie, NEGRO, r)
        pygame.draw.rect(superficie, BLANCO, r, width=3, border_radius=6)

        # Diana / Ojo central
        centro_x = r.centerx
        pygame.draw.ellipse(superficie, (70, 70, 80), (centro_x - 35, r.top + 8, 70, r.height - 16), width=2)
        pygame.draw.ellipse(superficie, (110, 110, 130), (centro_x - 14, r.top + 20, 28, r.height - 40), width=2)

        # Barra deslizante vertical
        color_barra = BLANCO if not self.golpe_efectuado else AMARILLO_HP
        pygame.draw.rect(superficie, color_barra, (int(self.cursor_ataque_x), r.top + 4, 12, r.height - 8), border_radius=3)

        # Animación del Tajo (Slash) sobre el enemigo
        if self.golpe_efectuado and self.anim_slash_timer < 0.5:
            progreso = self.anim_slash_timer / 0.5
            tam_slash = int(70 * math.sin(progreso * math.pi))
            pygame.draw.line(superficie, BLANCO, (enemigo_x - tam_slash, enemigo_y - tam_slash),
                             (enemigo_x + tam_slash, enemigo_y + tam_slash), 6)
            pygame.draw.line(superficie, (180, 240, 255), (enemigo_x - tam_slash, enemigo_y - tam_slash),
                             (enemigo_x + tam_slash, enemigo_y + tam_slash), 2)

            # Texto de daño flotante
            txt_danio = fuentes["boton"].render(str(self.danio_infligido) if self.danio_infligido > 0 else "MISS", True, ROJO_ALMA if self.danio_infligido > 0 else GRIS_MEDIO)
            superficie.blit(txt_danio, (enemigo_x - 20, enemigo_y - 85 - int(progreso * 20)))
