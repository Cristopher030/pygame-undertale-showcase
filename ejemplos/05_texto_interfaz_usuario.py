"""
=============================================================================
EJEMPLO 05: Renderizado de Texto, Botones Interactivos y Componentes UI
=============================================================================
En este archivo aprenderás:
1. Carga y renderizado de texto nítido con pygame.font.
2. Creación de una clase Boton con estados: Normal, Hover (encima) y Clic.
3. Cambio dinámico del cursor del sistema (SYSTEM_CURSOR_HAND).
4. Barra de vida / progreso con interpolación suave (Lerp).
5. Efecto de texto progresivo estilo máquina de escribir (tecleado continuo),
   fundamental para juegos narrativos y RPGs tipo Undertale.
=============================================================================
"""

import sys
import pygame

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("05 - Pygame: Interfaz de Usuario (UI), Texto y Botones")
reloj = pygame.time.Clock()

# Fuentes
fuente_titulo = pygame.font.SysFont("Arial", 22, bold=True)
fuente_ui     = pygame.font.SysFont("Arial", 16, bold=True)
fuente_retro  = pygame.font.SysFont("Consolas", 15)

# Colores
FONDO       = (20, 22, 28)
BLANCO      = (255, 255, 255)
VERDE       = (46, 204, 113)
ROJO        = (231, 76, 60)
AZUL        = (52, 152, 219)
GRIS_CLARO  = (180, 185, 200)

# =============================================================================
# COMPONENTE: BOTÓN INTERACTIVO
# =============================================================================
class Boton:
    def __init__(self, x, y, ancho, alto, texto, color_base, color_hover, accion=None):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color_base = color_base
        self.color_hover = color_hover
        self.color_actual = color_base
        self.accion = accion
        self.hover = False
        self.presionado = False

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(evento.pos)
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.collidepoint(evento.pos):
                self.presionado = True
        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            if self.presionado and self.rect.collidepoint(evento.pos):
                if self.accion:
                    self.accion()
            self.presionado = False

    def update(self):
        # Color dinámico según estado
        if self.presionado:
            self.color_actual = (max(0, self.color_hover[0]-40), max(0, self.color_hover[1]-40), max(0, self.color_hover[2]-40))
        elif self.hover:
            self.color_actual = self.color_hover
        else:
            self.color_actual = self.color_base

    def draw(self, superficie):
        # Fondo del botón
        pygame.draw.rect(superficie, self.color_actual, self.rect, border_radius=8)
        # Borde exterior
        color_borde = (255, 255, 255) if self.hover else (80, 90, 110)
        pygame.draw.rect(superficie, color_borde, self.rect, width=2, border_radius=8)

        # Texto centrado dentro del botón
        render_texto = fuente_ui.render(self.texto, True, BLANCO)
        rect_texto = render_texto.get_rect(center=self.rect.center)
        superficie.blit(render_texto, rect_texto)

# =============================================================================
# COMPONENTE: BARRA DE PROGRESO / VIDA (Con Lerp Suave)
# =============================================================================
class BarraVida:
    def __init__(self, x, y, ancho, alto, valor_max=100):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.valor_max = valor_max
        self.valor_actual = valor_max
        self.valor_visual = float(valor_max)  # Se interpola suavemente

    def cambiar_vida(self, delta):
        self.valor_actual = max(0, min(self.valor_max, self.valor_actual + delta))

    def update(self, dt):
        # Interpolación lineal (Lerp) para transición suave
        velocidad_lerp = 8.0
        self.valor_visual += (self.valor_actual - self.valor_visual) * velocidad_lerp * dt

    def draw(self, superficie):
        # Fondo oscuro de la barra
        pygame.draw.rect(superficie, (40, 44, 52), self.rect, border_radius=6)

        # Ancho proporcional actual
        ancho_vida = int((self.valor_visual / self.valor_max) * self.rect.width)
        rect_vida = pygame.Rect(self.rect.x, self.rect.y, max(0, ancho_vida), self.rect.height)

        # Color gradual: Verde -> Amarillo -> Rojo según el porcentaje
        porcentaje = self.valor_visual / self.valor_max
        if porcentaje > 0.5:
            color = VERDE
        elif porcentaje > 0.25:
            color = (241, 196, 15)
        else:
            color = ROJO

        pygame.draw.rect(superficie, color, rect_vida, border_radius=6)
        pygame.draw.rect(superficie, (120, 130, 150), self.rect, width=2, border_radius=6)

        # Texto indicativo encima
        etiqueta = fuente_retro.render(f"HP: {int(self.valor_visual)} / {self.valor_max}", True, BLANCO)
        superficie.blit(etiqueta, (self.rect.x, self.rect.y - 22))

# =============================================================================
# EFECTO: CAJA DE DIÁLOGO TIPO MÁQUINA DE ESCRIBIR
# =============================================================================
class DialogoEscribiendo:
    def __init__(self, x, y, ancho, alto):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto_completo = ""
        self.texto_visible = ""
        self.indice_letra = 0
        self.temporizador = 0.0
        self.velocidad_letras = 0.03  # segundos por caracter

    def establecer_mensaje(self, mensaje):
        self.texto_completo = mensaje
        self.texto_visible = ""
        self.indice_letra = 0
        self.temporizador = 0.0

    def update(self, dt):
        if self.indice_letra < len(self.texto_completo):
            self.temporizador += dt
            if self.temporizador >= self.velocidad_letras:
                self.temporizador = 0.0
                self.texto_visible += self.texto_completo[self.indice_letra]
                self.indice_letra += 1

    def draw(self, superficie):
        # Marco del diálogo estilo RPG retro
        pygame.draw.rect(superficie, (10, 10, 15), self.rect, border_radius=8)
        pygame.draw.rect(superficie, BLANCO, self.rect, width=3, border_radius=8)

        # Dividir texto en líneas para no desbordar
        palabras = self.texto_visible.split(" ")
        lineas = []
        linea_actual = ""
        for palabra in palabras:
            prueba = f"{linea_actual} {palabra}".strip()
            if fuente_retro.size(prueba)[0] < self.rect.width - 30:
                linea_actual = prueba
            else:
                lineas.append(linea_actual)
                linea_actual = palabra
        if linea_actual:
            lineas.append(linea_actual)

        # Renderizar cada línea
        for i, lin in enumerate(lineas):
            render = fuente_retro.render(lin, True, BLANCO)
            superficie.blit(render, (self.rect.x + 15, self.rect.y + 15 + i * 24))

# =============================================================================
# PROGRAMA PRINCIPAL
# =============================================================================
def main():
    barra_hp = BarraVida(50, 80, 320, 26, valor_max=100)
    dialogo = DialogoEscribiendo(50, 360, 700, 160)
    dialogo.establecer_mensaje(
        "* ¡Has entrado en el mundo de Pygame! "
        "* Los botones superiores permiten alterar la barra de vida en tiempo real. "
        "* Este cuadro muestra cómo crear cinemáticas y diálogos tecleados progresivamente."
    )

    # Funciones para los botones
    def curar():
        barra_hp.cambiar_vida(20)
        dialogo.establecer_mensaje("* Usaste una Poción. ¡Recuperaste 20 puntos de salud!")

    def danar():
        barra_hp.cambiar_vida(-25)
        dialogo.establecer_mensaje("* ¡Recibiste un impacto sorpresa! Perdiste 25 de salud.")

    def reiniciar_dialogo():
        dialogo.establecer_mensaje(
            "* Las fuentes y botones en Pygame permiten crear interfaces completamente "
            "personalizadas para menús de inicio, inventarios y pantallas de combate."
        )

    # Crear lista de botones
    botones = [
        Boton(50, 130, 140, 42, "+ Curar (+20)", (39, 174, 96), (46, 204, 113), accion=curar),
        Boton(210, 130, 140, 42, "- Daño (-25)", (192, 57, 43), (231, 76, 60), accion=danar),
        Boton(50, 190, 300, 42, "Reiniciar Mensaje", (41, 128, 185), (52, 152, 219), accion=reiniciar_dialogo)
    ]

    ejecutando = True
    while ejecutando:
        dt = reloj.tick(60) / 1000.0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                ejecutando = False

            for b in botones:
                b.manejar_evento(evento)

        # Cambiar cursor si el mouse está sobre algún botón
        algun_hover = any(b.hover for b in botones)
        cursor_actual = pygame.SYSTEM_CURSOR_HAND if algun_hover else pygame.SYSTEM_CURSOR_ARROW
        pygame.mouse.set_cursor(cursor_actual)

        # Actualizaciones
        barra_hp.update(dt)
        dialogo.update(dt)
        for b in botones:
            b.update()

        # Dibujado
        pantalla.fill(FONDO)

        # Título
        render_tit = fuente_titulo.render("Demostración de UI: Botones, Barras de Vida y Diálogos", True, BLANCO)
        pantalla.blit(render_tit, (50, 25))

        # Dibujar componentes
        barra_hp.draw(pantalla)
        for b in botones:
            b.draw(pantalla)
        dialogo.draw(pantalla)

        # Instrucción inferior
        render_salida = fuente_retro.render("Presiona ESC para salir", True, GRIS_CLARO)
        pantalla.blit(render_salida, (50, 545))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
