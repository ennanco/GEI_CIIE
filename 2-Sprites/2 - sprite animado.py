"""
Ejemplo 2: Sprite Animado
------------------------

Este ejemplo es parte de una serie de tutoriales incrementales para crear un videojuego.
Construye sobre el Ejemplo 1 (toda la imagen como Sprite) añadiendo animación mediante el uso de (spritesheets)

   - Carga de una imagen que contiene múltiples frames de animación
   - Lectura de coordenadas desde un archivo de texto (coordJugador.txt)
   - Recorte de la hoja para obtener cada frame

Nuevos conceptos en este ejemplo:
* Hojas de sprites (spritesheets)
* Animación de personajes
* Lectura de coordenadas desde archivo
* Estados de movimiento (QUIETO, IZQUIERDA, DERECHA)
* Ciclos de animación
"""

import pygame
import sys
import os
from pygame.locals import *

# -------------------------------------------------
# Constantes del juego
# -------------------------------------------------
# Archivos
ARCHIVO_SPRITE = 'images/Jugador.png'  # Archivo del sprite del jugador
ARCHIVO_COORDENADAS = 'images/coordJugador.txt'  # Archivo de coordenadas

# Colores
COLOR_FONDO = (133, 133, 133)  # Color gris

# Estados de movimiento
QUIETO = 0
IZQUIERDA = 1
DERECHA = 2

# Configuración del juego
FPS = 60  # Frames por segundo

# -------------------------------------------------
# Funciones auxiliares
# -------------------------------------------------

def load_image(name, colorkey=None):
    """
    Carga una imagen desde el directorio 'images'.
    Con el colotkey a -1, el color de transparencia sera el del pixel (0,0)
    Ver ejemplo 1 para más detalles sobre el funcionamiento.
    """
    try:
        image = pygame.image.load(name)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

# -------------------------------------------------
# Clases de los objetos del juego
# -------------------------------------------------

class Jugador(pygame.sprite.Sprite):
    """
    Clase que representa al jugador con animación.
    
    Atributos importantes:
    - hoja: La imagen completa que contiene todos los frames
    - rect: Rectángulo que define el área de colisión
    - posicionx/posiciony: Coordenadas del sprite en pantalla
    - movimiento: Estado actual del movimiento
    - numPostura: Índice de la postura actual (0: quieto, 1: caminando)
    - numImagenPostura: Frame actual dentro de la postura
    - coordenadasHoja: Lista de rectángulos que definen cada frame
    """

    def __init__(self, imagen, coordenadas, posicion):
        # Primero invocamos al constructor de la clase padre
        super().__init__()
        # Se carga la hoja de sprites
        self.hoja = load_image(imagen, -1)
        # Convertimos la imagen para usar el canal alpha
        # Esto permite transparencias suaves (no solo colorkey)
        #self.hoja = self.hoja.convert_alpha()
        
        # El rectangulo y la posicion que tendra
        self.rect = pygame.Rect((7, 25), (30, 40))
        self.posicionx = posicion[0]
        self.posiciony = posicion[1]
        
        # El movimiento que esta realizando
        self.movimiento = QUIETO

        # Leemos las coordenadas de un archivo de texto
        # El archivo contiene las coordenadas de cada frame en la hoja
        with open(coordenadas, 'r') as pfile:
            datos = pfile.read().split()
        
        # Inicializamos las variables de animación
        self.numPostura = 1  # 1 = caminando
        self.numImagenPostura = 0
        cont = 0
        # Número de frames en cada postura
        numImagenes = [6, 12]  # [quieto, caminando]
        
        # Creamos la lista de coordenadas para cada frame
        self.coordenadasHoja = []
        for linea in range(0, 2):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for postura in range(1, numImagenes[linea] + 1):
                # Cada frame tiene 4 valores: x, y, ancho, alto
                tmp.append(pygame.Rect(
                    (int(datos[cont]), int(datos[cont + 1])),
                    (int(datos[cont + 2]), int(datos[cont + 3]))
                ))
                cont += 4

    def dibujar(self, pantalla):
        """
        Dibuja el personaje en la pantalla.
        
        Parámetros:
            pantalla: Superficie donde se dibujará el sprite
        """
        # blit: (imagen, posición en pantalla, rectángulo de la imagen a usar)
        pantalla.blit(self.hoja, 
                     (self.posicionx, self.posiciony),
                     self.coordenadasHoja[self.numPostura][self.numImagenPostura])

    def mover(self, direccion):
        """
        Cambia el estado de movimiento del jugador.
        
        Parámetros:
            direccion: Nueva dirección (QUIETO, IZQUIERDA, DERECHA)
        """
        self.movimiento = direccion

    def update(self):
        """
        Actualiza la posición y animación del jugador.
        - Mueve el sprite según la dirección
        - Actualiza el frame de animación
        - Vuelve al estado quieto al terminar el movimiento
        """
        # Si vamos a la izquierda
        if self.movimiento == IZQUIERDA:
            # Actualizamos la posicion
            self.posicionx -= 2
            # Actualizamos la imagen a mostrar
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
                self.numImagenPostura = 0
            # Su siguiente movimiento (si no se pulsa mas) sera estar quieto
            self.movimiento = QUIETO
        # Si vamos a la derecha
        elif self.movimiento == DERECHA:
            # Actualizamos la posicion
            self.posicionx += 2
            # Actualizamos la imagen a mostrar
            self.numImagenPostura -= 1
            if self.numImagenPostura < 0:
                self.numImagenPostura = len(self.coordenadasHoja[self.numPostura]) - 1
            # Su siguiente movimiento (si no se pulsa mas) sera estar quieto
            self.movimiento = QUIETO



# Funcion principal del juego

def main():
    """Función principal del juego."""
    # Inicializar pygame
    pygame.init()

    # Crear la pantalla
    pantalla = pygame.display.set_mode((800, 600), 0, 32)

    # Creamos el objeto reloj para sincronizar el juego
    reloj = pygame.time.Clock()

    # Poner el título de la ventana
    pygame.display.set_caption('Ejemplo 2: Uso de Sprites Animado')

    # Creamos el objeto jugador que va a ser un sprite animado
    # Tiene que tener la imagen, las coordenadas y la posicion
    jugador = Jugador(ARCHIVO_SPRITE,ARCHIVO_COORDENADAS,(100,100))

    # El bucle de eventos
    while True:
        # Hacemos que el reloj espere a un determinado fps
        reloj.tick(FPS)

        for event in pygame.event.get():
            # Si se cierra la ventana o se pulsa Escape
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        # Comprobamos las teclas pulsadas para el movimiento
        teclas_pulsadas = pygame.key.get_pressed()
        if teclas_pulsadas[K_LEFT]:
            jugador.mover(IZQUIERDA)
        elif teclas_pulsadas[K_RIGHT]:
            jugador.mover(DERECHA)

        # Actualizamos el jugador
        jugador.update()

        # Dibujar el fondo de color
        pantalla.fill(COLOR_FONDO)

        # Dibujar el Sprite
        jugador.dibujar(pantalla)

        # Actualizar la pantalla
        pygame.display.update()


if __name__ == "__main__":
    main()
