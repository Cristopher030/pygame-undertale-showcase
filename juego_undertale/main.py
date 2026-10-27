"""
=============================================================================
UNDERTALE: BATALLA ESPECTRAL (PROYECTO FINAL EN PYGAME)
=============================================================================
Recreación fiel y completa del sistema de combate por turnos y esquiva Danmaku
(Bullet Hell) inspirado en el legendario videojuego 'UNDERTALE' de Toby Fox.

Características implementadas:
- Menú de 4 botones: [LUCHAR], [ACTUAR], [OBJETO], [PIEDAD].
- Movimiento pixel-perfect del Alma (corazón rojo) con cuadros de invulnerabilidad.
- Minijuego de precisión de impacto con barra deslizante y golpes críticos.
- Caja de combate reactiva que se transforma fluidamente con interpolación (Lerp).
- 4 patrones de proyectiles dinámicos: lágrimas, huesos, orbes y láseres con aviso.
- Sistema de Diálogos con máquina de escribir y bocadillo de cómic reactivo.
- Rutas de desenlace: Pacifista (mediante ACTUAR y PERDONAR) o Combate (LUCHAR).
- Pantalla de Game Over con fractura del alma y determinación.
- Motor de sonido chiptune 8-bit procedural integrado (no requiere archivos externos).
=============================================================================
"""

import sys
import pygame

# Importaciones de los módulos del juego
from constantes import (
    ANCHO_PANTALLA, ALTO_PANTALLA, FPS, NEGRO, BLANCO, ROJO_ALMA,
    AMARILLO_HP, AMARILLO_PIEDAD, GRIS_CLARO, GRIS_MEDIO,
    ESTADO_MENU_COMBATE, ESTADO_SUBMENU_ACCION, ESTADO_MINIJUEGO_ATAQUE,
    ESTADO_DIALOGO_ENEMIGO, ESTADO_ESQUIVAR_ATAQUE, ESTADO_VICTORIA, ESTADO_GAME_OVER
)
from audio_retro import MotorAudio
from alma import Alma
from caja_combate import CajaCombate
from enemigo import Enemigo
from patrones_ataque import GestorAtaques
from interfaz_combate import InterfazCombate

class JuegoUndertale:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("Undertale: Batalla Espectral - Pygame Edition")
        self.reloj = pygame.time.Clock()

        # Cargar fuentes estilo retro
        self.fuentes = {
            "hud": pygame.font.SysFont("Lucida Console", 18, bold=True),
            "boton": pygame.font.SysFont("Lucida Console", 18, bold=True),
            "texto": pygame.font.SysFont("Lucida Console", 16),
            "dialogo_bocadillo": pygame.font.SysFont("Lucida Console", 14),
            "pequena": pygame.font.SysFont("Lucida Console", 12, bold=True),
            "game_over": pygame.font.SysFont("Lucida Console", 26, bold=True),
        }

        # Inicialización de subsistemas
        self.audio = MotorAudio()
        self.caja = CajaCombate()
        self.enemigo = Enemigo(x=400, y=140)
        self.alma = Alma(x=400, y=355)
        self.ataques = GestorAtaques()
        self.interfaz = InterfazCombate()

        # Datos del Jugador
        self.hp_max = 20
        self.hp = 20

        # Estado del juego
        self.estado = ESTADO_MENU_COMBATE
        self.mensaje_narrativo = "* ¡Un espectro flotante se interpone en tu camino!"
        self.mensaje_narrativo_visible = ""
        self.narrativo_indice = 0
        self.narrativo_timer = 0.0

        # Turno y conteo de oleadas
        self.numero_turno = 0
        self.tipo_victoria = ""

        # Iniciar música de batalla
        self.audio.reproducir_musica_combate()

    def reiniciar_batalla(self):
        """Reinicia el combate tras una victoria o Game Over."""
        self.hp = self.hp_max
        self.enemigo = Enemigo(x=400, y=140)
        self.alma = Alma(x=400, y=355)
        self.caja.transformar_a_menu()
        self.estado = ESTADO_MENU_COMBATE
        self.mensaje_narrativo = "* ¡Un espectro flotante se interpone en tu camino!"
        self.establecer_narracion(self.mensaje_narrativo)
        self.numero_turno = 0
        self.tipo_victoria = ""
        self.audio.reproducir_musica_combate()

    def establecer_narracion(self, texto):
        self.mensaje_narrativo = texto
        self.mensaje_narrativo_visible = ""
        self.narrativo_indice = 0
        self.narrativo_timer = 0.0

    def pasar_a_dialogo_enemigo(self, mensaje_caja, respuesta_bob):
        self.establecer_narracion(mensaje_caja)
        self.enemigo.decir(respuesta_bob)
        self.estado = ESTADO_DIALOGO_ENEMIGO

    def iniciar_fase_ataque_enemigo(self):
        """Transforma la caja y lanza la oleada de proyectiles."""
        self.enemigo.ocultar_dialogo()
        self.caja.transformar_a_esquivar(ancho=260, alto=200)

        # Posicionar el alma en el centro exacto de la nueva caja
        self.alma.x = 400.0
        self.alma.y = 355.0
        self.alma.tiempo_invulnerable = 0.5  # Pequeña gracia al iniciar el turno

        # Elegir patrón de proyectiles según el turno
        self.ataques.iniciar_oleada(numero_patron=self.numero_turno, duracion=6.5)
        self.numero_turno += 1
        self.estado = ESTADO_ESQUIVAR_ATAQUE

    # =========================================================================
    # MANEJO DE EVENTOS Y TECLADO
    # =========================================================================
    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return False

                # Reiniciar con tecla R en Victoria o Game Over
                if self.estado in (ESTADO_VICTORIA, ESTADO_GAME_OVER):
                    if evento.key == pygame.K_r:
                        self.reiniciar_batalla()
                    continue

                # 1. ESTADO: MENÚ PRINCIPAL
                if self.estado == ESTADO_MENU_COMBATE:
                    if evento.key in (pygame.K_LEFT, pygame.K_a):
                        self.interfaz.navegar_botones("IZQ", self.audio)
                    elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                        self.interfaz.navegar_botones("DER", self.audio)
                    elif evento.key in (pygame.K_z, pygame.K_RETURN, pygame.K_SPACE):
                        self.audio.reproducir("confirm")
                        self.interfaz.reiniciar_subopcion()
                        self.estado = ESTADO_SUBMENU_ACCION

                # 2. ESTADO: SUBMENÚ DE OPCIÓN
                elif self.estado == ESTADO_SUBMENU_ACCION:
                    boton_actual = self.interfaz.nombres_botones[self.interfaz.indice_boton]

                    if evento.key in (pygame.K_x, pygame.K_BACKSPACE):
                        # Cancelar / retroceder al menú principal
                        self.audio.reproducir("select")
                        self.estado = ESTADO_MENU_COMBATE

                    elif evento.key in (pygame.K_UP, pygame.K_w):
                        total = len(self.interfaz.opciones_actuar) if boton_actual == "ACTUAR" else 2
                        self.interfaz.navegar_subsubmenu("ARRIBA", total, self.audio)
                    elif evento.key in (pygame.K_DOWN, pygame.K_s):
                        total = len(self.interfaz.opciones_actuar) if boton_actual == "ACTUAR" else 2
                        self.interfaz.navegar_subsubmenu("ABAJO", total, self.audio)
                    elif evento.key in (pygame.K_LEFT, pygame.K_a):
                        total = len(self.interfaz.opciones_actuar) if boton_actual == "ACTUAR" else 2
                        self.interfaz.navegar_subsubmenu("IZQ", total, self.audio)
                    elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                        total = len(self.interfaz.opciones_actuar) if boton_actual == "ACTUAR" else 2
                        self.interfaz.navegar_subsubmenu("DER", total, self.audio)

                    elif evento.key in (pygame.K_z, pygame.K_RETURN, pygame.K_SPACE):
                        self.audio.reproducir("confirm")
                        self.ejecutar_accion_submenu(boton_actual)

                # 3. ESTADO: MINIJUEGO DE ATAQUE
                elif self.estado == ESTADO_MINIJUEGO_ATAQUE:
                    if evento.key in (pygame.K_z, pygame.K_RETURN, pygame.K_SPACE):
                        self.interfaz.golpear_minijuego_ataque(self.audio)

                # 4. ESTADO: DIÁLOGO DEL ENEMIGO
                elif self.estado == ESTADO_DIALOGO_ENEMIGO:
                    if evento.key in (pygame.K_z, pygame.K_RETURN, pygame.K_SPACE):
                        # Pasar a la fase de proyectiles
                        self.iniciar_fase_ataque_enemigo()

        return True

    def ejecutar_accion_submenu(self, boton):
        sub_idx = self.interfaz.indice_subopcion

        if boton == "LUCHAR":
            self.estado = ESTADO_MINIJUEGO_ATAQUE
            self.interfaz.iniciar_minijuego_ataque()

        elif boton == "ACTUAR":
            nombre_act, _ = self.interfaz.opciones_actuar[sub_idx]
            if nombre_act == "Comprobar":
                msg_caja = "* BOB - ATK 4 DEF 2.\n* Un fantasma melancólico al que le cuesta hacer amigos."
                bob_dijo = "...hola... gracias por mirarme."
            elif nombre_act == "Contar Chiste":
                msg_caja = "* Le contaste un chiste sobre fantasmas y sábanas.\n* ¡A Bob le pareció brillante!"
                bob_dijo = "...jeje... eres muy divertido."
                self.enemigo.aumentar_piedad(40)
            elif nombre_act == "Halagar":
                msg_caja = "* Le dijiste a Bob que su blancura es impecable.\n* Bob parece conmovido."
                bob_dijo = "...¿en serio? Qué amable..."
                self.enemigo.aumentar_piedad(35)
            elif nombre_act == "Invitar Té":
                msg_caja = "* Compartiste una merienda de té invisible.\n* ¡Bob siente una cálida felicidad!"
                bob_dijo = "...¡el mejor té que he probado!"
                self.enemigo.aumentar_piedad(50)

            self.pasar_a_dialogo_enemigo(msg_caja, bob_dijo)

        elif boton == "OBJETO":
            if not self.interfaz.inventario:
                return
            item = self.interfaz.inventario.pop(sub_idx)
            curacion = item["curacion"]
            self.hp = min(self.hp_max, self.hp + curacion)
            self.audio.reproducir("curar")
            msg_caja = f"* Usaste {item['nombre']}.\n* ¡Recuperaste {curacion} HP!"
            bob_dijo = "...eso se ve delicioso..."
            self.pasar_a_dialogo_enemigo(msg_caja, bob_dijo)

        elif boton == "PIEDAD":
            if sub_idx == 0:  # Perdonar
                if self.enemigo.perdonable:
                    self.audio.pausar_musica()
                    self.audio.reproducir("victoria")
                    self.tipo_victoria = "PACIFISTA"
                    self.estado = ESTADO_VICTORIA
                else:
                    msg_caja = "* Intentaste perdonar a Bob, pero aún está inseguro."
                    bob_dijo = "...¿ya nos vamos?... no sé..."
                    self.pasar_a_dialogo_enemigo(msg_caja, bob_dijo)
            elif sub_idx == 1:  # Huir
                msg_caja = "* Intentas alejarte, pero Bob flota suavemente a tu alrededor."
                bob_dijo = "...espera... no te vayas aún..."
                self.pasar_a_dialogo_enemigo(msg_caja, bob_dijo)

    # =========================================================================
    # ACTUALIZACIÓN DE LÓGICA (UPDATE)
    # =========================================================================
    def update(self, dt):
        # Actualización de la caja y sus dimensiones interpoladas
        self.caja.update(dt)

        # Actualización del enemigo y su animación senoidal
        self.enemigo.update(dt, self.audio)

        # Máquina de escribir del mensaje narrativo principal
        if self.narrativo_indice < len(self.mensaje_narrativo):
            self.narrativo_timer += dt
            if self.narrativo_timer >= 0.025:
                self.narrativo_timer = 0.0
                self.mensaje_narrativo_visible += self.mensaje_narrativo[self.narrativo_indice]
                self.narrativo_indice += 1

        # Lógica específica según el estado activo
        if self.estado == ESTADO_MINIJUEGO_ATAQUE:
            resultado_danio = self.interfaz.actualizar_minijuego_ataque(dt)
            if resultado_danio is not None:
                self.enemigo.recibir_ataque(resultado_danio)
                if self.enemigo.derrotado:
                    self.audio.pausar_musica()
                    self.audio.reproducir("victoria")
                    self.tipo_victoria = "NEUTRAL"
                    self.estado = ESTADO_VICTORIA
                else:
                    self.pasar_a_dialogo_enemigo(
                        f"* ¡Le hiciste {resultado_danio} de daño a Bob!",
                        "...ay... eso dolió un poco..."
                    )

        elif self.estado == ESTADO_ESQUIVAR_ATAQUE:
            # Movimiento del alma dentro de los bordes actuales de la caja
            self.alma.update(dt, self.caja.rect_actual)

            # Actualización de proyectiles y verificación de impactos
            danio_recibido = self.ataques.update(dt, self.caja.rect_actual, self.alma, self.audio)
            if danio_recibido > 0:
                self.hp = max(0, self.hp - danio_recibido)
                self.caja.aplicar_sacudida(10.0)

                # Si el jugador pierde toda la salud: GAME OVER
                if self.hp <= 0:
                    self.audio.pausar_musica()
                    self.audio.reproducir("romper")
                    self.alma.romper()
                    self.estado = ESTADO_GAME_OVER
                    return

            # Si se agotó el tiempo de la oleada de proyectiles, volver al turno del jugador
            if self.ataques.oleada_terminada:
                self.caja.transformar_a_menu()
                # Texto narrativo ambiental para el siguiente turno
                if self.enemigo.perdonable:
                    self.establecer_narracion("* ¡Bob parece completamente complacido!\n* Su nombre brilla con luz de PIEDAD.")
                else:
                    frases = [
                        "* Bob te observa tímidamente mientras flota.",
                        "* El aire se llena de un leve aroma a caramelo.",
                        "* Bob parece disfrutar de la compañía.",
                        "* Te mantienes firme y lleno de determinación."
                    ]
                    self.establecer_narracion(frases[self.numero_turno % len(frases)])
                self.estado = ESTADO_MENU_COMBATE

        elif self.estado == ESTADO_GAME_OVER:
            self.alma.update(dt)

    # =========================================================================
    # RENDERIZADO VISUAL (DRAW)
    # =========================================================================
    def draw(self):
        self.pantalla.fill(NEGRO)

        # 1. PANTALLA DE GAME OVER
        if self.estado == ESTADO_GAME_OVER:
            self.alma.draw(self.pantalla)
            # Texto emblemático de Undertale
            t1 = self.fuentes["game_over"].render("GAME OVER", True, BLANCO)
            self.pantalla.blit(t1, t1.get_rect(center=(ANCHO_PANTALLA // 2, 160)))

            t2 = self.fuentes["texto"].render("No puedes rendirte aquí...", True, BLANCO)
            t3 = self.fuentes["texto"].render(f"¡{self.enemigo.nombre.split()[0]} depende de ti! Mantén tu determinación.", True, BLANCO)
            self.pantalla.blit(t2, t2.get_rect(center=(ANCHO_PANTALLA // 2, 280)))
            self.pantalla.blit(t3, t3.get_rect(center=(ANCHO_PANTALLA // 2, 315)))

            t_retry = self.fuentes["hud"].render("[ Presiona R para reintentar | ESC para salir ]", True, AMARILLO_HP)
            self.pantalla.blit(t_retry, t_retry.get_rect(center=(ANCHO_PANTALLA // 2, 480)))

            pygame.display.flip()
            return

        # 2. PANTALLA DE VICTORIA
        if self.estado == ESTADO_VICTORIA:
            self.enemigo.draw(self.pantalla, self.fuentes["dialogo_bocadillo"])
            self.caja.draw(self.pantalla)

            r_caja = self.caja.rect_actual
            if self.tipo_victoria == "PACIFISTA":
                lineas = [
                    "* ¡HAS GANADO LA BATALLA!",
                    "* Perdonaste a Bob pacíficamente.",
                    "* Bob te sonríe y promete ser tu amigo por siempre.",
                    "* ¡Ganaste 0 EXP y 50 ORO!",
                    "",
                    "[ Presiona R para jugar de nuevo | ESC para salir ]"
                ]
            else:
                lineas = [
                    "* ¡HAS GANADO LA BATALLA!",
                    "* Bob se disipó en una suave niebla espectral...",
                    "* Ganaste 25 EXP y 10 ORO.",
                    "",
                    "[ Presiona R para jugar de nuevo | ESC para salir ]"
                ]

            for i, l in enumerate(lineas):
                col = AMARILLO_PIEDAD if i == 0 else (AMARILLO_HP if i == len(lineas) - 1 else BLANCO)
                superficie_l = self.fuentes["texto"].render(l, True, col)
                self.pantalla.blit(superficie_l, (r_caja.left + 30, r_caja.top + 20 + i * 26))

            self.interfaz.draw_hud(self.pantalla, self.hp, self.hp_max, self.fuentes)
            self.interfaz.draw_botones(self.pantalla, self.fuentes, self.estado)
            pygame.display.flip()
            return

        # 3. COMBATE NORMAL
        # A) Dibujar enemigo arriba
        self.enemigo.draw(self.pantalla, self.fuentes["dialogo_bocadillo"])

        # B) Dibujar Caja de Combate
        self.caja.draw(self.pantalla)
        rect_caja = self.caja.rect_actual

        # C) Contenido dentro de la caja según el estado
        if self.estado in (ESTADO_MENU_COMBATE, ESTADO_DIALOGO_ENEMIGO):
            # Dibujar texto narrativo con saltos de línea
            lineas = self.mensaje_narrativo_visible.split("\n")
            for i, lin in enumerate(lineas):
                txt_render = self.fuentes["texto"].render(lin, True, BLANCO)
                self.pantalla.blit(txt_render, (rect_caja.left + 30, rect_caja.top + 25 + i * 28))

            # Indicador de confirmación en diálogos
            if self.estado == ESTADO_DIALOGO_ENEMIGO and (pygame.time.get_ticks() // 400) % 2 == 0:
                txt_avanzar = self.fuentes["pequena"].render("[Z]", True, AMARILLO_HP)
                self.pantalla.blit(txt_avanzar, (rect_caja.right - 40, rect_caja.bottom - 25))

        elif self.estado == ESTADO_SUBMENU_ACCION:
            boton_actual = self.interfaz.nombres_botones[self.interfaz.indice_boton]
            self.interfaz.draw_submenus(self.pantalla, self.fuentes, boton_actual, self.enemigo)

        elif self.estado == ESTADO_MINIJUEGO_ATAQUE:
            self.interfaz.draw_minijuego_ataque(self.pantalla, self.fuentes, int(self.enemigo.x), int(self.enemigo.y))

        elif self.estado == ESTADO_ESQUIVAR_ATAQUE:
            # Proyectiles y Alma
            self.ataques.draw(self.pantalla, rect_caja)
            self.alma.draw(self.pantalla)

        # D) Barra de HUD (Nombre, LV, HP amarillo/rojo)
        self.interfaz.draw_hud(self.pantalla, self.hp, self.hp_max, self.fuentes)

        # E) Los 4 Botones inferiores [LUCHAR], [ACTUAR], [OBJETO], [PIEDAD]
        self.interfaz.draw_botones(self.pantalla, self.fuentes, self.estado)

        pygame.display.flip()

    # =========================================================================
    # BUCLE PRINCIPAL DE EJECUCIÓN
    # =========================================================================
    def ejecutar(self):
        ejecutando = True
        while ejecutando:
            dt = self.reloj.tick(FPS) / 1000.0

            ejecutando = self.manejar_eventos()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    juego = JuegoUndertale()
    juego.ejecutar()
