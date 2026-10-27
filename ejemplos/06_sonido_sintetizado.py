"""
=============================================================================
EJEMPLO 06: Generación y Reproducción de Audio Chiptune (pygame.mixer)
=============================================================================
En este archivo aprenderás:
1. Cómo inicializar y configurar el motor de audio pygame.mixer.
2. Cómo sintetizar ondas de sonido retro (8-bit) directamente en memoria
   usando fórmulas matemáticas y el módulo nativo array de Python (sin archivos externos).
3. Creación de efectos sonoros clásicos: Onda Cuadrada (Beep), Salto (Arpegio),
   Láser (Frecuencia descendente), Moneda y Ruido de Impacto/Explosión.
4. Cómo convertir buffers de bytes en objetos pygame.mixer.Sound.
5. Visualización gráfica de la forma de onda en tiempo real en la pantalla.
=============================================================================
"""

import sys
import math
import array
import random
import pygame

# 1. Inicialización del mezclador de audio con frecuencia estándar (44.1 kHz, 16 bits mono)
pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=512)
pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("06 - Pygame: Generación de Audio y Sonidos Chiptune")
reloj = pygame.time.Clock()

fuente_titulo = pygame.font.SysFont("Arial", 20, bold=True)
fuente = pygame.font.SysFont("Consolas", 15)

FONDO   = (18, 20, 26)
BLANCO  = (240, 240, 240)
CYAN    = (0, 230, 255)
VERDE   = (46, 204, 113)
AMARILLO= (241, 196, 15)
ROJO    = (231, 76, 60)

# =============================================================================
# SINTETIZADOR PROCEDURAL DE AUDIO RETRO
# =============================================================================
FRECUENCIA_MUESTREO = 44100

def crear_sonido_desde_muestras(muestras):
    """Convierte una lista de valores numéricos de audio (-32767 a 32767) en un Sound."""
    # Convertimos los valores a enteros con signo de 16 bits ('h')
    datos_pcm = array.array('h', [int(max(-32767, min(32767, v))) for v in muestras])
    return pygame.mixer.Sound(buffer=datos_pcm)

def generar_bip(frecuencia=440.0, duracion=0.15, volumen=0.5):
    """Genera un tono puro de onda senoidal."""
    num_muestras = int(FRECUENCIA_MUESTREO * duracion)
    muestras = []
    for i in range(num_muestras):
        t = i / FRECUENCIA_MUESTREO
        # Envolvente lineal de volumen para evitar chasquidos (clics)
        envolvente = 1.0 - (i / num_muestras)
        valor = math.sin(2.0 * math.pi * frecuencia * t) * 32767 * volumen * envolvente
        muestras.append(valor)
    return crear_sonido_desde_muestras(muestras), muestras

def generar_onda_cuadrada(frecuencia=330.0, duracion=0.18, volumen=0.35):
    """Genera la clásica onda cuadrada 8-bit tipo Game Boy / NES."""
    num_muestras = int(FRECUENCIA_MUESTREO * duracion)
    muestras = []
    periodo = FRECUENCIA_MUESTREO / frecuencia
    for i in range(num_muestras):
        envolvente = 1.0 - (i / num_muestras)
        fase = (i % periodo) / periodo
        valor = (1.0 if fase < 0.5 else -1.0) * 32767 * volumen * envolvente
        muestras.append(valor)
    return crear_sonido_desde_muestras(muestras), muestras

def generar_laser(duracion=0.22, volumen=0.4):
    """Genera un disparo láser retro deslizando la frecuencia de agudo a grave."""
    num_muestras = int(FRECUENCIA_MUESTREO * duracion)
    muestras = []
    fase = 0.0
    for i in range(num_muestras):
        progreso = i / num_muestras
        frec_actual = 900.0 * (1.0 - progreso) + 150.0  # De 900Hz a 150Hz
        fase += 2.0 * math.pi * frec_actual / FRECUENCIA_MUESTREO
        envolvente = 1.0 - progreso
        valor = math.sin(fase) * 32767 * volumen * envolvente
        muestras.append(valor)
    return crear_sonido_desde_muestras(muestras), muestras

def generar_moneda(duracion=0.25, volumen=0.4):
    """Genera un arpegio ascendente clásico de obtención de moneda / ítem."""
    num_muestras = int(FRECUENCIA_MUESTREO * duracion)
    mitad = num_muestras // 2
    muestras = []
    for i in range(num_muestras):
        # Primera mitad a 987 Hz (Si5), segunda mitad a 1318 Hz (Mi6)
        frec = 987.0 if i < mitad else 1318.0
        t = i / FRECUENCIA_MUESTREO
        envolvente = 1.0 - (i / num_muestras)
        # Onda cuadrada suave
        periodo = FRECUENCIA_MUESTREO / frec
        onda = 1.0 if (i % periodo) / periodo < 0.5 else -1.0
        valor = onda * 32767 * volumen * envolvente
        muestras.append(valor)
    return crear_sonido_desde_muestras(muestras), muestras

def generar_ruido_impacto(duracion=0.28, volumen=0.4):
    """Genera ruido blanco modulado para emular golpes o explosiones."""
    num_muestras = int(FRECUENCIA_MUESTREO * duracion)
    muestras = []
    for i in range(num_muestras):
        envolvente = (1.0 - (i / num_muestras)) ** 2
        ruido = random.uniform(-1.0, 1.0)
        valor = ruido * 32767 * volumen * envolvente
        muestras.append(valor)
    return crear_sonido_desde_muestras(muestras), muestras

# =============================================================================
# PROGRAMA PRINCIPAL CON INTERFAZ Y VISUALIZADOR
# =============================================================================
def main():
    # Pre-generamos los efectos de sonido
    snd_bip, m_bip       = generar_bip()
    snd_cuad, m_cuad     = generar_onda_cuadrada()
    snd_laser, m_laser   = generar_laser()
    snd_moneda, m_moneda = generar_moneda()
    snd_golpe, m_golpe   = generar_ruido_impacto()

    muestras_actuales = m_cuad
    nombre_efecto_actual = "Onda Cuadrada 8-Bit"

    botones = [
        {"rect": pygame.Rect(50, 100, 180, 44), "texto": "[1] Tono Bip", "snd": snd_bip, "m": m_bip, "nombre": "Tono Senoidal Bip (440Hz)"},
        {"rect": pygame.Rect(250, 100, 180, 44), "texto": "[2] Onda Cuadrada", "snd": snd_cuad, "m": m_cuad, "nombre": "Onda Cuadrada NES (330Hz)"},
        {"rect": pygame.Rect(450, 100, 180, 44), "texto": "[3] Láser Retro", "snd": snd_laser, "m": m_laser, "nombre": "Disparo Láser con Pitch Slide"},
        {"rect": pygame.Rect(50, 160, 180, 44), "texto": "[4] Moneda / Item", "snd": snd_moneda, "m": m_moneda, "nombre": "Arpegio Doble de Moneda"},
        {"rect": pygame.Rect(250, 160, 180, 44), "texto": "[5] Ruido Impacto", "snd": snd_golpe, "m": m_golpe, "nombre": "Ruido Blanco de Golpe / Daño"},
    ]

    ejecutando = True
    while ejecutando:
        reloj.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_1:
                    snd_bip.play(); muestras_actuales = m_bip; nombre_efecto_actual = "Tono Senoidal Bip"
                elif evento.key == pygame.K_2:
                    snd_cuad.play(); muestras_actuales = m_cuad; nombre_efecto_actual = "Onda Cuadrada NES"
                elif evento.key == pygame.K_3:
                    snd_laser.play(); muestras_actuales = m_laser; nombre_efecto_actual = "Disparo Láser"
                elif evento.key == pygame.K_4:
                    snd_moneda.play(); muestras_actuales = m_moneda; nombre_efecto_actual = "Moneda / Item"
                elif evento.key == pygame.K_5:
                    snd_golpe.play(); muestras_actuales = m_golpe; nombre_efecto_actual = "Ruido Impacto"

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for b in botones:
                    if b["rect"].collidepoint(evento.pos):
                        b["snd"].play()
                        muestras_actuales = b["m"]
                        nombre_efecto_actual = b["nombre"]

        # Renderizado
        pantalla.fill(FONDO)

        # Encabezado
        t_tit = fuente_titulo.render("Sintetizador de Audio Chiptune en Pygame (Sin Archivos Externos)", True, BLANCO)
        pantalla.blit(t_tit, (50, 30))

        t_sub = fuente.render("Haz clic en los botones o presiona los números 1 a 5 en tu teclado:", True, (160, 170, 190))
        pantalla.blit(t_sub, (50, 65))

        # Dibujar botones
        mouse_pos = pygame.mouse.get_pos()
        for b in botones:
            hover = b["rect"].collidepoint(mouse_pos)
            color = (52, 73, 94) if not hover else (41, 128, 185)
            pygame.draw.rect(pantalla, color, b["rect"], border_radius=6)
            pygame.draw.rect(pantalla, CYAN if hover else (100, 110, 130), b["rect"], width=2, border_radius=6)

            txt = fuente.render(b["texto"], True, BLANCO)
            pantalla.blit(txt, txt.get_rect(center=b["rect"].center))

        # VISUALIZADOR DE ONDA DE AUDIO (Osciloscopio)
        rect_visor = pygame.Rect(50, 240, 700, 280)
        pygame.draw.rect(pantalla, (10, 12, 16), rect_visor, border_radius=8)
        pygame.draw.rect(pantalla, (40, 48, 60), rect_visor, width=2, border_radius=8)

        # Línea central del osciloscopio
        centro_y = rect_visor.centery
        pygame.draw.line(pantalla, (30, 40, 50), (rect_visor.left, centro_y), (rect_visor.right, centro_y), 1)

        # Dibujar forma de onda
        if muestras_actuales:
            paso = max(1, len(muestras_actuales) // rect_visor.width)
            puntos_onda = []
            for px in range(rect_visor.width):
                idx = min(len(muestras_actuales) - 1, px * paso)
                muestra_norm = muestras_actuales[idx] / 32767.0
                py = centro_y - int(muestra_norm * (rect_visor.height // 2 - 20))
                puntos_onda.append((rect_visor.left + px, py))

            if len(puntos_onda) > 1:
                pygame.draw.lines(pantalla, CYAN, False, puntos_onda, 2)

        # Información del sonido seleccionado
        txt_visor = fuente.render(f"Forma de Onda: {nombre_efecto_actual}", True, AMARILLO)
        pantalla.blit(txt_visor, (rect_visor.left + 15, rect_visor.top + 15))

        txt_pie = fuente.render("Muestras generadas en tiempo real con PCM 16-Bit | 44100 Hz | Pygame Mixer", True, (130, 140, 160))
        pantalla.blit(txt_pie, (50, 545))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
