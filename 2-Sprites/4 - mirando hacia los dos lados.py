"""
Ejemplo 4: Sprite Mirando en Ambos Sentidos
-----------------------------------------

Este ejemplo es parte de una serie de tutoriales incrementales para crear un videojuego.
Construye sobre el Ejemplo 3 (Sprite con Animación Controlada) añadiendo la capacidad
de que el personaje mire hacia la dirección del movimiento.

   - Control de la dirección hacia la que mira el personaje
   - Volteo horizontal de la imagen según la dirección
   - Mantenimiento de la dirección al detenerse

Nuevos conceptos en este ejemplo:
* Control de la dirección del personaje
* Volteo horizontal de sprites
* Separación entre movimiento y dirección
* Mejora en la presentación visual
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

# Dimensiones de la pantalla
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

# Posiciones
POSICION_INICIAL = (100, 100)  # Posición inicial del jugador

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
    """Clase que representa al jugador con animación y dirección."""
    def __init__(self, imagen, coordenadas, posicion):
        super().__init__()
        self.hoja = load_image(imagen, -1)
        self.hoja = self.hoja.convert_alpha()
        
        self.rect = pygame.Rect((7, 25), (30, 40))
        self.posicionx = posicion[0]
        self.posiciony = posicion[1]
        self.movimiento = QUIETO
        # Lado hacia el que está mirando
        self.mirando = IZQUIERDA

        with open(coordenadas, 'r') as pfile:
            datos = pfile.read().split()
        
        self.numPostura = 1  # 1 = caminando
        self.numImagenPostura = 0
        cont = 0
        numImagenes = [6, 12]  # [quieto, caminando]
        
        self.coordenadasHoja = []
        for linea in range(0, 2):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for postura in range(1, numImagenes[linea] + 1):
                tmp.append(pygame.Rect(
                    (int(datos[cont]), int(datos[cont + 1])),
                    (int(datos[cont + 2]), int(datos[cont + 3]))
                ))
                cont += 4

        self.retardoMovimiento = 0

    def dibujar(self, pantalla):
        """
        Dibuja el personaje en la pantalla.
        La principal diferencia con ejemplos anteriores es que ahora
        volteamos la imagen horizontalmente según la dirección.
        """
        # Obtenemos el frame actual
        frame = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
        
        if self.mirando == IZQUIERDA:
            # Dibujamos normal si mira a la izquierda
            pantalla.blit(frame, (self.posicionx, self.posiciony))
        else:
            # Volteamos horizontalmente si mira a la derecha
            pantalla.blit(pygame.transform.flip(frame, True, False), 
                         (self.posicionx, self.posiciony))

    def actualizarPostura(self):
        """Actualiza la postura del personaje con un retardo."""
        self.retardoMovimiento -= 1
        if self.retardoMovimiento < 0:
            self.retardoMovimiento = RETARDO_ANIMACION
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
                self.numImagenPostura = 0

    def mover(self, direccion):
        """Cambia el estado de movimiento del jugador."""
        self.movimiento = direccion

    def update(self):
        """Actualiza la posición y animación del jugador."""
        if self.movimiento == IZQUIERDA:
            self.posicionx -= 2
            self.actualizarPostura()
            self.movimiento = QUIETO
            self.mirando = IZQUIERDA
        elif self.movimiento == DERECHA:
            self.posicionx += 2
            self.actualizarPostura()
            self.movimiento = QUIETO
            self.mirando = DERECHA

# -------------------------------------------------
# Funcion principal del juego
# -------------------------------------------------

def main():
    """Función principal del juego."""
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA), 0, 32)
    reloj = pygame.time.Clock()
    pygame.display.set_caption('Ejemplo 4: Sprite Mirando en Ambos Sentidos')

    jugador = Jugador(ARCHIVO_SPRITE, ARCHIVO_COORDENADAS, POSICION_INICIAL)

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
