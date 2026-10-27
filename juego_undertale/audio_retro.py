"""
=============================================================================
MOTOR DE AUDIO RETRO PROCEDURAL (Sintetizador Chiptune sin archivos externos)
=============================================================================
Genera efectos sonoros 8-bit y música ambiental estilo Undertale directamente
en memoria PCM mediante fórmulas matemáticas. No requiere archivos .wav ni .mp3.
=============================================================================
"""

import math
import array
import random
import pygame

FRECUENCIA_AUDIO = 44100

class MotorAudio:
    def __init__(self):
        self.disponible = True
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.pre_init(frequency=FRECUENCIA_AUDIO, size=-16, channels=2, buffer=512)
                pygame.mixer.init()
        except Exception:
            self.disponible = False

        if self.disponible:
            self._generar_efectos()
            self._generar_musica_fondo()
        else:
            self.snd_bip = None
            self.snd_select = None
            self.snd_confirm = None
            self.snd_danio = None
            self.snd_slash = None
            self.snd_curar = None
            self.snd_romper = None
            self.snd_victoria = None
            self.snd_musica = None

    def _crear_sound(self, muestras_mono):
        """Convierte lista mono a un Sound estéreo de 16 bits."""
        muestras_estereo = []
        for val in muestras_mono:
            v_clamped = int(max(-32767, min(32767, val)))
            # Canal izquierdo y canal derecho idénticos
            muestras_estereo.append(v_clamped)
            muestras_estereo.append(v_clamped)
        datos = array.array('h', muestras_estereo)
        return pygame.mixer.Sound(buffer=datos)

    def _generar_efectos(self):
        # 1. Bip de texto (Typewriter blip de Undertale)
        muestras_bip = []
        dur_bip = 0.035
        n_bip = int(FRECUENCIA_AUDIO * dur_bip)
        for i in range(n_bip):
            env = 1.0 - (i / n_bip)
            fase = (i % (FRECUENCIA_AUDIO / 520.0)) / (FRECUENCIA_AUDIO / 520.0)
            onda = 1.0 if fase < 0.5 else -1.0
            muestras_bip.append(onda * 18000 * env)
        self.snd_bip = self._crear_sound(muestras_bip)
        self.snd_bip.set_volume(0.25)

        # 2. Selección en menú (tick)
        muestras_sel = []
        dur_sel = 0.04
        n_sel = int(FRECUENCIA_AUDIO * dur_sel)
        for i in range(n_sel):
            env = 1.0 - (i / n_sel)
            onda = math.sin(2 * math.pi * 750.0 * (i / FRECUENCIA_AUDIO))
            muestras_sel.append(onda * 15000 * env)
        self.snd_select = self._crear_sound(muestras_sel)
        self.snd_select.set_volume(0.3)

        # 3. Confirmación de opción
        muestras_conf = []
        dur_conf = 0.09
        n_conf = int(FRECUENCIA_AUDIO * dur_conf)
        for i in range(n_conf):
            frec = 587.0 if i < n_conf // 2 else 880.0
            env = 1.0 - (i / n_conf)
            fase = (i % (FRECUENCIA_AUDIO / frec)) / (FRECUENCIA_AUDIO / frec)
            onda = 1.0 if fase < 0.5 else -1.0
            muestras_conf.append(onda * 20000 * env)
        self.snd_confirm = self._crear_sound(muestras_conf)
        self.snd_confirm.set_volume(0.35)

        # 4. Sonido de Daño al recibir golpe
        muestras_danio = []
        dur_danio = 0.22
        n_danio = int(FRECUENCIA_AUDIO * dur_danio)
        for i in range(n_danio):
            env = (1.0 - (i / n_danio)) ** 1.5
            ruido = random.uniform(-1.0, 1.0) * 0.7
            fase = (i % (FRECUENCIA_AUDIO / 120.0)) / (FRECUENCIA_AUDIO / 120.0)
            cuadrada = (1.0 if fase < 0.5 else -1.0) * 0.3
            muestras_danio.append((ruido + cuadrada) * 30000 * env)
        self.snd_danio = self._crear_sound(muestras_danio)
        self.snd_danio.set_volume(0.55)

        # 5. Ataque Slash del jugador
        muestras_slash = []
        dur_slash = 0.16
        n_slash = int(FRECUENCIA_AUDIO * dur_slash)
        fase_sl = 0.0
        for i in range(n_slash):
            prog = i / n_slash
            frec = 1200.0 * (1.0 - prog) + 200.0
            fase_sl += 2 * math.pi * frec / FRECUENCIA_AUDIO
            ruido = random.uniform(-0.3, 0.3)
            env = 1.0 - prog
            muestras_slash.append((math.sin(fase_sl) * 0.7 + ruido) * 26000 * env)
        self.snd_slash = self._crear_sound(muestras_slash)
        self.snd_slash.set_volume(0.45)

        # 6. Curación con Ítem
        muestras_curar = []
        dur_curar = 0.35
        n_curar = int(FRECUENCIA_AUDIO * dur_curar)
        notas_curar = [523.25, 659.25, 783.99, 1046.50]  # Do, Mi, Sol, Do agudo
        for i in range(n_curar):
            idx_nota = min(len(notas_curar) - 1, int((i / n_curar) * len(notas_curar)))
            frec = notas_curar[idx_nota]
            env = 1.0 - (i / n_curar)
            t = i / FRECUENCIA_AUDIO
            onda = math.sin(2 * math.pi * frec * t)
            muestras_curar.append(onda * 22000 * env)
        self.snd_curar = self._crear_sound(muestras_curar)
        self.snd_curar.set_volume(0.4)

        # 7. Ruptura del Corazón (Game Over)
        muestras_romper = []
        dur_romper = 0.4
        n_romper = int(FRECUENCIA_AUDIO * dur_romper)
        for i in range(n_romper):
            env = (1.0 - (i / n_romper)) ** 2
            ruido = random.uniform(-1.0, 1.0)
            muestras_romper.append(ruido * 32000 * env)
        self.snd_romper = self._crear_sound(muestras_romper)
        self.snd_romper.set_volume(0.6)

        # 8. Fanfarria de Victoria
        muestras_vic = []
        dur_vic = 0.8
        n_vic = int(FRECUENCIA_AUDIO * dur_vic)
        notas_vic = [440, 554, 659, 880]  # La, Do#, Mi, La
        for i in range(n_vic):
            idx = min(len(notas_vic) - 1, int((i / n_vic) * len(notas_vic)))
            frec = notas_vic[idx]
            env = 1.0 - (i / n_vic)
            fase = (i % (FRECUENCIA_AUDIO / frec)) / (FRECUENCIA_AUDIO / frec)
            onda = 1.0 if fase < 0.5 else -1.0
            muestras_vic.append(onda * 20000 * env)
        self.snd_victoria = self._crear_sound(muestras_vic)
        self.snd_victoria.set_volume(0.45)

    def _generar_musica_fondo(self):
        """Genera un bucle musical chiptune enérgico de 4 compases al estilo Undertale."""
        bpm = 135
        segundos_por_negra = 60.0 / bpm
        duracion_paso = segundos_por_negra / 2  # Corcheas (16 pasos en 2 compases)
        total_pasos = 32
        total_duracion = total_pasos * duracion_paso
        total_muestras = int(FRECUENCIA_AUDIO * total_duracion)

        # Secuencia de melodía (Frecuencias Hz, 0 = silencio)
        melodia = [
            293.66, 293.66, 587.33, 440.00,  # D4, D4, D5, A4
            0,      415.30, 0,      392.00,  # -, G#4, -, G4
            349.23, 293.66, 349.23, 392.00,  # F4, D4, F4, G4
            261.63, 261.63, 587.33, 440.00,  # C4, C4, D5, A4
            0,      415.30, 0,      392.00,
            349.23, 293.66, 349.23, 392.00,
            246.94, 246.94, 587.33, 440.00,  # B3, B3, D5, A4
            0,      415.30, 392.00, 349.23
        ]

        # Secuencia de bajo continuo (Bajo rápido y constante)
        bajo = [
            146.83, 146.83, 146.83, 146.83,
            146.83, 146.83, 146.83, 146.83,
            130.81, 130.81, 130.81, 130.81,
            130.81, 130.81, 130.81, 130.81,
            123.47, 123.47, 123.47, 123.47,
            123.47, 123.47, 123.47, 123.47,
            116.54, 116.54, 116.54, 116.54,
            116.54, 116.54, 116.54, 116.54
        ]

        muestras_musica = []
        for i in range(total_muestras):
            t_total = i / FRECUENCIA_AUDIO
            paso_actual = int(t_total / duracion_paso) % total_pasos
            t_dentro_paso = t_total % duracion_paso

            # Canal Melodía (Onda Cuadrada con envolvente corta)
            frec_m = melodia[paso_actual]
            onda_m = 0.0
            if frec_m > 0:
                periodo_m = FRECUENCIA_AUDIO / frec_m
                fase_m = (i % periodo_m) / periodo_m
                env_m = max(0.0, 1.0 - (t_dentro_paso / duracion_paso) * 1.2)
                onda_m = (1.0 if fase_m < 0.5 else -1.0) * env_m * 0.45

            # Canal Bajo (Onda Triangular / Diente de sierra suave)
            frec_b = bajo[paso_actual]
            periodo_b = FRECUENCIA_AUDIO / frec_b
            fase_b = (i % periodo_b) / periodo_b
            onda_b = (2.0 * abs(2.0 * (fase_b - 0.5)) - 1.0) * 0.35

            # Canal Percusión Hi-Hat retro (ruido en cada contratiempo)
            onda_p = 0.0
            if (paso_actual % 2 == 1) and (t_dentro_paso < 0.03):
                onda_p = random.uniform(-0.15, 0.15) * (1.0 - t_dentro_paso / 0.03)

            mezcla = (onda_m + onda_b + onda_p) * 22000
            muestras_musica.append(mezcla)

        self.snd_musica = self._crear_sound(muestras_musica)
        self.snd_musica.set_volume(0.28)

    def reproducir_musica_combate(self):
        if self.disponible and self.snd_musica:
            self.snd_musica.play(loops=-1)

    def pausar_musica(self):
        if self.disponible and self.snd_musica:
            self.snd_musica.stop()

    def reproducir(self, nombre):
        if not self.disponible:
            return
        snd = getattr(self, f"snd_{nombre}", None)
        if snd:
            snd.play()
