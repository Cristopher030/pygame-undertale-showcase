# 🎮 Pygame Showcase & Undertale Combat Encounter

[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame--ce-2.5.8%2B-green.svg)](https://pyga.me/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Style](https://img.shields.io/badge/Art%20Style-Undertale%20Retro%208--Bit-red.svg)](https://undertale.com)

Un repositorio pedagógico y completo diseñado para aprender el desarrollo de videojuegos 2D con **Pygame**. Incluye **7 módulos de código independientes** que explican las mecánicas fundamentales del motor gráfico y un **videojuego completo y jugable inspirado en *UNDERTALE*** (la batalla de combate por turnos y esquiva *Bullet Hell* contra **Bob el Espectro**).

> **¡Sin dependencias externas de archivos!**  
> Todos los gráficos, animaciones, fuentes y efectos de sonido chiptune de 8 bits se generan **procedimentalmente en tiempo real mediante código en memoria**. Puedes clonar el repositorio y ejecutar cualquier archivo al instante sin preocuparte por imágenes `.png` faltantes o audios `.wav` rotos.

---

## 📋 Tabla de Contenidos

1. [Estructura del Repositorio](#-estructura-del-repositorio)
2. [Requisitos e Instalación](#-requisitos-e-instalación)
3. [Explicación Detallada de los Ejemplos de Pygame](#-explicación-detallada-de-los-ejemplos-de-pygame)
   - [01 - Creación de Ventana y Formas Geométricas](#01_ventana_y_formaspy)
   - [02 - Manejo de Eventos, Teclado, Ratón y Delta Time](#02_eventos_y_movimientopy)
   - [03 - Arquitectura con Sprites, Grupos y Animación](#03_sprites_y_animacionespy)
   - [04 - Detección y Resolución de Colisiones 2D](#04_colisiones_y_fisicaspy)
   - [05 - Interfaz de Usuario, Texto y Botones](#05_texto_interfaz_usuariopy)
   - [06 - Síntesis de Audio y Efectos Chiptune](#06_sonido_sintetizadopy)
   - [07 - Sistema de Partículas y Mezcla Aditiva](#07_sistema_particulaspy)
4. [Videojuego: Undertale - Batalla Espectral](#-videojuego-undertale---batalla-espectral)
   - [Mecánicas y Sistema de Combate](#mecánicas-del-juego)
   - [Controles](#controles)
   - [Estructura del Código del Juego](#estructura-del-juego)
5. [Guía para Subir este Proyecto a GitHub](#-guía-para-subir-a-github)
6. [Licencia](#-licencia)

---

## 📁 Estructura del Repositorio

```text
pygame-undertale-showcase/
│
├── .gitignore                      # Archivos temporales e ignorados por Git
├── README.md                       # Documentación completa y manual de usuario
├── requirements.txt                # Dependencias del proyecto (pygame / pygame-ce)
│
├── ejemplos/                       # Módulos educativos de funcionalidades Pygame
│   ├── 01_ventana_y_formas.py      # Bucle de juego, primitivas vectoriales y canal alfa
│   ├── 02_eventos_y_movimiento.py  # Entrada de usuario, límites de pantalla y delta time
│   ├── 03_sprites_y_animaciones.py # Clases Sprite, Group y spritesheet procedural
│   ├── 04_colisiones_y_fisicas.py  # AABB, colisión circular y deslizamiento en paredes
│   ├── 05_texto_interfaz_usuario.py# UI: Botones hover, barra con Lerp y máquina de escribir
│   ├── 06_sonido_sintetizado.py    # Sintetizador PCM chiptune y visualizador osciloscopio
│   └── 07_sistema_particulas.py    # Emisores, fuego, explosiones y brillo BLEND_ADD
│
└── juego_undertale/                # Videojuego completo inspirado en Undertale
    ├── main.py                     # Punto de entrada y máquina de estados finitos
    ├── constantes.py               # Paleta de colores, resoluciones y constantes
    ├── audio_retro.py              # Motor de sonido 8-bit procedural y banda sonora
    ├── alma.py                     # El Alma (corazón rojo), hitbox y ruptura Game Over
    ├── caja_combate.py             # Caja de batalla mutante con interpolación (Lerp)
    ├── enemigo.py                  # Bob el Espectro: animación senoidal y bocadillos
    ├── patrones_ataque.py          # Patrones bullet-hell: lágrimas, huesos, orbes y láseres
    └── interfaz_combate.py         # Botones [LUCHAR], [ACTUAR], [OBJETO], [PIEDAD] y retícula
```

---

## 🚀 Requisitos e Instalación

### 1. Requisitos Previos
- **Python 3.10 o superior** (totalmente probado y compatible con Python 3.10, 3.11, 3.12, 3.13 y 3.14).

### 2. Instalación de Dependencias

Abre una terminal en la carpeta del repositorio y ejecuta:

```bash
pip install -r requirements.txt
```

> **Nota sobre versiones recientes de Python:**  
> En entornos modernos como Python 3.13 o 3.14, `pygame-ce` (Pygame Community Edition) proporciona ruedas precompiladas optimizadas con soporte para las últimas versiones del intérprete. El código es 100% compatible tanto con `pygame` estándar como con `pygame-ce`.

---

## 💡 Explicación Detallada de los Ejemplos de Pygame

Cada archivo dentro de la carpeta `ejemplos/` es un script autocontenido que puedes ejecutar de forma individual para estudiar un concepto específico:

### `01_ventana_y_formas.py`
* **Comando para ejecutar:** `python ejemplos/01_ventana_y_formas.py`
* **Conceptos clave explicados:**
  - Inicialización con `pygame.init()`.
  - Creación de ventana con doble búfer (`pygame.display.set_mode()`).
  - Control de velocidad constante con `pygame.time.Clock()` y `tick(60)`.
  - Dibujo de primitivas vectoriales: `rect`, `circle`, `ellipse`, `polygon`, `line`, `lines`.
  - Creación de superficies con canal alfa (`pygame.SRCALPHA`) para manejar transparencias reales RGBA sin ralentizar el renderizado.

### `02_eventos_y_movimiento.py`
* **Comando para ejecutar:** `python ejemplos/02_eventos_y_movimiento.py`
* **Conceptos clave explicados:**
  - Diferencia entre **eventos discretos** (`pygame.KEYDOWN` / `KEYUP`) para disparos o pausas y **sondeo continuo** (`pygame.key.get_pressed()`) para movimiento suave.
  - Implementación de **Delta Time (`dt`)**: cálculo del tiempo transcurrido por fotograma para que la velocidad sea idéntica a 30, 60 o 144 FPS.
  - Confinamiento dentro de la ventana mediante límites matemáticos (*Clamping*).
  - Rebote elástico contra bordes invirtiendo los vectores de velocidad.

### `03_sprites_y_animaciones.py`
* **Comando para ejecutar:** `python ejemplos/03_sprites_y_animaciones.py`
* **Conceptos clave explicados:**
  - Programación Orientada a Objetos aplicada a videojuegos con `pygame.sprite.Sprite`.
  - Agrupación eficiente de entidades mediante `pygame.sprite.Group`.
  - Ciclo de vida de un Sprite: actualización en lote (`group.update()`), dibujado masivo (`group.draw()`) y destrucción (`sprite.kill()`).
  - Generación de secuencias de fotogramas (*spritesheets*) en memoria mediante código procedural.
  - Temporizadores internos de animación e inversión de textura horizontal (`pygame.transform.flip`).

### `04_colisiones_y_fisicas.py`
* **Comando para ejecutar:** `python ejemplos/04_colisiones_y_fisicas.py`
* **Conceptos clave explicados:**
  - Colisión Rectángulo contra Rectángulo (AABB) mediante `rect.colliderect()`.
  - Colisión Círculo contra Círculo mediante distancia euclidiana con `pygame.math.Vector2.distance_to()`.
  - Detección de punto sobre área (`rect.collidepoint()`) para interacción con el cursor del ratón.
  - **Técnica de resolución de colisiones en paredes**: avance y resolución separada en el eje X y luego en el eje Y, permitiendo que el jugador se deslice suavemente por esquinas y muros sin atascarse.

### `05_texto_interfaz_usuario.py`
* **Comando para ejecutar:** `python ejemplos/05_texto_interfaz_usuario.py`
* **Conceptos clave explicados:**
  - Renderizado de fuentes del sistema con `pygame.font.SysFont`.
  - Construcción de una clase `Boton` con estados interactivos: normal, reposo (*hover*), presionado y ejecución de *callbacks*.
  - Cambio dinámico del cursor del sistema a mano interactiva (`pygame.SYSTEM_CURSOR_HAND`).
  - Barra de salud interactiva con interpolación lineal (*Lerp*) y cambio gradual de color (verde -> amarillo -> rojo).
  - Caja de diálogo con efecto progresivo tipo máquina de escribir con salto automático de línea (*word wrap*).

### `06_sonido_sintetizado.py`
* **Comando para ejecutar:** `python ejemplos/06_sonido_sintetizado.py`
* **Conceptos clave explicados:**
  - Configuración del motor de audio de baja latencia con `pygame.mixer.pre_init()` y `pygame.mixer.init()`.
  - Generación de formas de onda en memoria usando `array.array('h')` con enteros con signo de 16 bits a 44.1 kHz.
  - Creación de tonos puros (onda senoidal), timbres retro de 8 bits estilo NES/Game Boy (onda cuadrada), deslizamientos de frecuencia (*pitch slide*) para rayos láser y ruido blanco para golpes o percusiones.
  - Osciloscopio gráfico en tiempo real que traza la forma de onda del sonido reproducido.

### `07_sistema_particulas.py`
* **Comando para ejecutar:** `python ejemplos/07_sistema_particulas.py`
* **Conceptos clave explicados:**
  - Arquitectura modular de partículas: posición, velocidad, aceleración por gravedad, vida útil y desvanecimiento alfa.
  - Mezcla aditiva de colores (`pygame.BLEND_ADD`) para lograr efectos incandescentes de resplandor (*Glow*).
  - Tres emisores interactivos: antorcha de fuego con llamas continuas, explosión radial omnidireccional con gravedad y estela mágica tras el cursor.

---

## 💀 Videojuego: Undertale - Batalla Espectral

Dentro del directorio `juego_undertale/` se encuentra una recreación jugable, detallada y pulida del emblemático sistema de combate de **UNDERTALE**.

```bash
python juego_undertale/main.py
```

### Sinopsis
Mientras exploras las ruinas de Pygame, te encuentras con **Bob el Espectro**, un fantasma melancólico que finge ser una sábana olvidada. Tu destino depende enteramente de tus decisiones: ¿utilizarás la fuerza de tus ataques o te ganarás su amistad mediante palabras amables y tazas de té imaginarias?

---

### Mecánicas del Juego

1. **El Alma (Corazón Rojo)**:
   - Controlas el corazón rojo en 8 direcciones dentro de la caja de batalla.
   - Cuenta con una hitbox precisa de 5 píxeles de radio.
   - Posee cuadros de invulnerabilidad temporales (*i-frames*) con parpadeo tras ser golpeado.
   - Al caer a 0 HP, se activa la cinemática de fractura del alma característica de Undertale.

2. **Caja de Batalla Dinámica (Battle Box)**:
   - La caja no es un marco estático: durante la fase de menú es ancha para acomodar las opciones de texto, y al comenzar el ataque enemigo realiza una transición suave (*Lerp*) reduciéndose al centro de la pantalla.
   - Cuenta con soporte para temblor de pantalla (*Screen Shake*) reactivo a los daños recibidos.

3. **Los 4 Botones del Sistema de Combate**:
   - `[ LUCHAR ]`: Abre un minijuego de puntería con una retícula ovalada y una barra deslizante vertical. Si presionas `[Z]` justo en el centro, ¡asestarás un golpe crítico de 35 de daño con animación de tajo (*slash*)!
   - `[ ACTUAR ]`: Te permite interactuar pacíficamente con Bob:
     * **Comprobar**: Inspecciona las estadísticas (ATK 4, DEF 2) y personalidad de Bob.
     * **Contar Chiste**: Desata un juego de palabras que eleva su medidor de amistad (+40 Piedad).
     * **Halagar**: Elogias la blancura de su sábana espectral (+35 Piedad).
     * **Invitar Té**: Compartes una infusión imaginaria (+50 Piedad).
   - `[ OBJETO ]`: Consume objetos del inventario para recuperar salud (`Tarta de Canela` +20 HP, `Fideo Héroe` +15 HP, `Té Fantasma` +10 HP).
   - `[ PIEDAD ]`:
     * **Perdonar**: Cuando alcanzas el 100% de Piedad interactuando con Bob, su nombre se ilumina en **amarillo dorado**. Al seleccionar Perdonar, ¡terminarás la batalla por la **Ruta Pacifista**!
     * **Huir**: Intentas escapar pacíficamente de la batalla.

4. **Patrones de Proyectiles (Danmaku / Bullet Hell)**:
   - **Lluvia de Lágrimas**: Gotas espectrales que caen verticalmente en oleadas con aberturas seguras para esquivar.
   - **Huesos Deslizantes**: Obstáculos rectangulares horizontales que cruzan a diferentes alturas.
   - **Anillo de Orbes Convergentes**: Esferas mágicas que rodean la caja y se dirigen al unísono hacia la posición del jugador.
   - **Rebote Caótico y Láseres Avisados**: Esferas rebotantes combinadas con líneas de advertencia roja parpadeante que anuncian un disparo láser destructor.

5. **Audio y Banda Sonora Retro Procedural**:
   - El juego incluye una pista musical continua de combate compuesta en 4 compases con sintetizador de bajos, melodía en onda cuadrada y percusión de ruido blanco, además de efectos de sonido para diálogos, selección, impactos y victorias.

---

### Controles

| Tecla / Botón | Acción |
| :--- | :--- |
| **Flechas de Dirección** o **W, A, S, D** | Mover el Alma / Navegar por los menús |
| **Z** / **ENTER** / **ESPACIO** | Confirmar opción / Golpear en minijuego de ataque / Avanzar diálogo |
| **X** / **SHIFT Izquierdo** | Cancelar o retroceder menú / **Modo Precisión** (movimiento lento del Alma para esquivar) |
| **R** | Reintentar la batalla (en pantalla de Victoria o Game Over) |
| **ESC** | Salir del juego |

---

### Estructura del Juego

- `main.py`: Bucle principal y máquina de estados finitos (`MENU_COMBATE`, `SUBMENU_ACCION`, `MINIJUEGO_ATAQUE`, `DIALOGO_ENEMIGO`, `ESQUIVAR_ATAQUE`, `VICTORIA`, `GAME_OVER`).
- `constantes.py`: Dimensiones de ventana (800x600), paleta de colores oficial de Undertale y variables globales.
- `audio_retro.py`: Generador de audio procedural en memoria con buffers PCM de 16 bits y sintetizador musical.
- `alma.py`: Clase `Alma` con matriz de píxeles del corazón rojo, físicas y animación de fragmentación en Game Over.
- `caja_combate.py`: Clase `CajaCombate` con interpolación continua de forma y temblores de pantalla.
- `enemigo.py`: Clase `Enemigo` con animación flotante senoidal, cambio de expresiones faciales y bocadillo de texto tipo cómic.
- `patrones_ataque.py`: Generación matemática de los proyectiles y comprobación de colisiones con el alma.
- `interfaz_combate.py`: Renderizado del HUD, barra de vida amarilla/roja, botones inferiores y minijuego de precisión de combate.

---

## 🌐 Guía para Subir a GitHub

Si deseas publicar este repositorio en tu propia cuenta de GitHub, sigue estos sencillos pasos:

### Opción 1: Mediante la Terminal con Git

1. **Crea un nuevo repositorio vacío en GitHub**:
   - Ve a [github.com/new](https://github.com/new).
   - Asígnale un nombre (por ejemplo: `pygame-undertale-showcase`).
   - Deja **desmarcadas** las casillas de "Add a README file" y ".gitignore" (ya están incluidos en este proyecto).

2. **Conecta tu carpeta local y sube los cambios**:
   Abre una terminal en la carpeta del proyecto y ejecuta:

   ```bash
   # 1. Inicializar Git (si no lo has hecho aún)
   git init

   # 2. Agregar todos los archivos al seguimiento
   git add .

   # 3. Crear el primer commit
   git commit -m "feat: repositorio inicial con ejemplos de Pygame y juego Undertale"

   # 4. Establecer la rama principal
   git branch -M main

   # 5. Vincular con tu repositorio de GitHub (reemplaza TU_USUARIO)
   git remote add origin https://github.com/TU_USUARIO/pygame-undertale-showcase.git

   # 6. Subir el código
   git push -u origin main
   ```

### Opción 2: Mediante GitHub Desktop
1. Abre **GitHub Desktop**.
2. Selecciona **File** > **Add Local Repository...**.
3. Selecciona la carpeta `pygame-undertale-showcase`.
4. Haz clic en **Publish repository** para subirlo directamente a tu cuenta de GitHub.

---

## 📄 Licencia

Este proyecto se distribuye bajo los términos de la **Licencia MIT**. Siéntete libre de utilizar, modificar, ampliar y distribuir este código tanto para fines educativos como personales.

Inspirado en la obra y universo creado por Toby Fox (*UNDERTALE*). Desarrollado con ❤️ y Python.
