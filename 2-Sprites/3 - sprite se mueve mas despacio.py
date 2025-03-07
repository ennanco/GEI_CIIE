"""
Ejemplo 3: Sprite con Animación Controlada
----------------------------------------

Este ejemplo es parte de una serie de tutoriales incrementales para crear un videojuego.
Construye sobre el Ejemplo 2 (Sprite Animado) añadiendo control de velocidad en la animación.

   - Control de velocidad de animación mediante retardo
   - Separación de la lógica de actualización de postura
   - Mejora en la fluidez del movimiento

Nuevos conceptos en este ejemplo:
* Control de velocidad de animación
* Retardo entre frames
* Separación de lógica de animación
* Mejora en la experiencia de usuario
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
RETARDO_ANIMACION = 5  # Updates que durará cada imagen del personaje
                      # podría de ser un valor distinto para cada postura

# -------------------------------------------------
# Funciones auxiliares
# -------------------------------------------------

def load_image(name, colorkey=None):
    """Carga una imagen desde el directorio 'images'."""
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
    """Clase que representa al jugador con animación controlada."""
    def __init__(self, imagen, coordenadas, posicion):
        super().__init__()
        self.hoja = load_image(imagen, -1)
        # self.hoja = self.hoja.convert_alpha()
        
        self.rect = pygame.Rect((7, 25), (30, 40))
        self.posicionx = posicion[0]
        self.posiciony = posicion[1]
        self.movimiento = QUIETO

        with open(coordenadas, 'r') as pfile:
            datos = pfile.read().split()
        
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

        self.retardoMovimiento = 0

    def dibujar(self, pantalla):
        """Dibuja el personaje en la pantalla."""
        pantalla.blit(self.hoja, 
                     (self.posicionx, self.posiciony),
                     self.coordenadasHoja[self.numPostura][self.numImagenPostura])

    def actualizarPostura(self, siguientePostura):
        """
        Actualiza la postura del personaje con un retardo.
        Esta función es la principal diferencia con el ejemplo anterior.
        En lugar de actualizar la animación cada frame, espera un número
        determinado de frames (RETARDO_ANIMACION) antes de cambiar la imagen.
        """
        # Decrementamos el contador de retardo
        self.retardoMovimiento -= 1
        # Cuando el retardo llega a 0, actualizamos la postura
        if self.retardoMovimiento < 0:
            # Reiniciamos el contador de retardo
            self.retardoMovimiento = RETARDO_ANIMACION
            # Actualizamos la imagen según la dirección (1: adelante, -1: atrás)
            self.numImagenPostura += siguientePostura
            # Si llegamos al final de la animación, volvemos al principio
            if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
                self.numImagenPostura = 0
            # Si retrocedemos más allá del principio, vamos al final
            if self.numImagenPostura < 0:
                self.numImagenPostura = len(self.coordenadasHoja[self.numPostura]) - 1

    def mover(self, direccion):
        """Cambia el estado de movimiento del jugador."""
        self.movimiento = direccion

    def update(self):
        """Actualiza la posición y animación del jugador."""
        if self.movimiento == IZQUIERDA:
            self.posicionx -= 2
            self.actualizarPostura(1)
            self.movimiento = QUIETO
        elif self.movimiento == DERECHA:
            self.posicionx += 2
            self.actualizarPostura(-1)
            self.movimiento = QUIETO

# -------------------------------------------------
# Funcion principal del juego
# -------------------------------------------------

def main():
    """Función principal del juego."""
    pygame.init()
    pantalla = pygame.display.set_mode((800, 600), 0, 32)
    reloj = pygame.time.Clock()
    pygame.display.set_caption('Ejemplo 3: Sprite con Animación Controlada')

    jugador = Jugador(ARCHIVO_SPRITE, ARCHIVO_COORDENADAS, (100, 100))

    while True:
        reloj.tick(FPS)

        # Comprobamos los eventos
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        # Comprobamos las teclas pulsadas para el movimiento
        teclas_pulsadas = pygame.key.get_pressed()
        if teclas_pulsadas[K_LEFT]:
            jugador.mover(IZQUIERDA)
        elif teclas_pulsadas[K_RIGHT]:
            jugador.mover(DERECHA)

        # Procedemos a pintar el fondo y el jugador
        jugador.update()
        pantalla.fill(COLOR_FONDO)
        jugador.dibujar(pantalla)
        pygame.display.update()


if __name__ == "__main__":
    main()
