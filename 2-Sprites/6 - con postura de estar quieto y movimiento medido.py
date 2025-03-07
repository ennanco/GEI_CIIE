"""
Ejemplo 6: Movimiento Basado en Tiempo y Postura de Quieto
-----------------------------------------------------

Este ejemplo es parte de una serie de tutoriales incrementales para crear un videojuego.
Construye sobre el Ejemplo 5 (Sprites con Grupos) añadiendo movimiento basado en tiempo
y la capacidad de mostrar una postura cuando el personaje está quieto.

   - Movimiento suave basado en tiempo
   - Postura de quieto cuando no hay movimiento
   - Velocidad constante independiente del FPS
   - Mejor control de la animación

Nuevos conceptos en este ejemplo:
* Movimiento basado en tiempo
* Control de velocidad independiente del FPS
* Postura de quieto
* Mejora en la fluidez del movimiento
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

# Posturas
# También la de QUIETO = 0
ANDANDO = 1

# Configuración del juego
FPS = 60  # Frames por segundo
RETARDO_ANIMACION = 5  # Updates que durará cada imagen del personaje
VELOCIDAD_JUGADOR = 0.2  # Píxeles por milisegundo comparese con la velocidad anterior
                         # que era de 2 píxeles por frame

# Dimensiones de la pantalla
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

# Posiciones
POSICION_INICIAL_1 = (100, 100)  # Posición inicial del jugador 1
POSICION_INICIAL_2 = (200, 100)  # Posición inicial del jugador 2

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
    """Clase que representa al jugador con animación y movimiento basado en tiempo."""
    def __init__(self, imagen, coordenadas, posicion):
        super().__init__()
        self.hoja = load_image(imagen, -1)
        self.hoja = self.hoja.convert_alpha()
        
        self.rect = pygame.Rect((7, 25), (30, 40))
        self.rect.x = posicion[0]
        self.rect.y = posicion[1]
        self.movimiento = QUIETO
        self.mirando = IZQUIERDA
        self.posicionx = posicion[0]

        with open(coordenadas, 'r') as pfile:
            datos = pfile.read().split()
        
        self.numPostura = QUIETO  # Comenzamos en postura quieto
        self.numImagenPostura = 0
        cont = 0
        numImagenes = [6, 12]  # [quieto, caminando]
        
        # Creamos una lista de listas para almacenar las coordenadas de cada postura: quieto y caminando
        self.coordenadasHoja = []
        
        # Iteramos sobre las dos posturas (0: quieto, 1: caminando)
        for linea in range(0, 2):
            # Añadimos una lista vacía para cada postura
            self.coordenadasHoja.append([])
            # Guardamos una referencia a la lista actual para simplificar el código
            tmp = self.coordenadasHoja[linea]
            
            # Iteramos sobre cada frame de la postura actual
            # numImagenes[linea] contiene el número de frames para cada postura
            for postura in range(1, numImagenes[linea] + 1):
                # Cada frame tiene 4 valores en el archivo
                # Creamos un rectángulo con estos valores
                tmp.append(pygame.Rect(
                    (int(datos[cont]), int(datos[cont + 1])),
                    (int(datos[cont + 2]), int(datos[cont + 3]))
                ))
                # Avanzamos 4 posiciones en el array de datos para el siguiente frame
                cont += 4

        self.retardoMovimiento = 0
        # Actualizamos la imagen inicial
        self.actualizarPostura()

    def actualizarPostura(self):
        """Actualiza la postura del personaje con un retardo."""
        self.retardoMovimiento -= 1
        if self.retardoMovimiento < 0:
            self.retardoMovimiento = RETARDO_ANIMACION
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
                self.numImagenPostura = 0
            
            # Actualizamos la imagen según la dirección
            frame = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
            if self.mirando == IZQUIERDA:
                self.image = frame
            else:
                self.image = pygame.transform.flip(frame, True, False)

    def mover(self, direccion):
        """Cambia el estado de movimiento del jugador."""
        self.movimiento = direccion

    def update(self, tiempo):
        """
        Actualiza la posición y animación del jugador.
        El parámetro tiempo es el tiempo transcurrido desde la última actualización
        en milisegundos, lo que permite un movimiento suave independiente del FPS.
        """
        if self.movimiento == IZQUIERDA:
            # La postura actual será estar caminando
            self.numPostura = ANDANDO
            # Está mirando a la izquierda
            self.mirando = IZQUIERDA
            # Actualizamos la posición basada en el tiempo
            self.posicionx -= VELOCIDAD_JUGADOR * tiempo
            #Alineamiento para evitar los sprites flotantes
            self.rect.left = self.posicionx
            # Actualizamos la imagen a mostrar
            self.actualizarPostura()
        elif self.movimiento == DERECHA:
            # La postura actual será estar caminando
            self.numPostura = ANDANDO
            # Está mirando a la derecha
            self.mirando = DERECHA
            # Actualizamos la posición basada en el tiempo
            self.posicionx += VELOCIDAD_JUGADOR * tiempo
            self.rect.left = self.posicionx
            # Actualizamos la imagen a mostrar
            self.actualizarPostura()
        else:
            # La postura actual será estar quieto
            self.numPostura = QUIETO
            # Actualizamos la imagen a mostrar
            self.actualizarPostura()

# -------------------------------------------------
# Funcion principal del juego
# -------------------------------------------------

def main():
    """Función principal del juego."""
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA), 0, 32)
    reloj = pygame.time.Clock()
    pygame.display.set_caption('Ejemplo 6: Movimiento Basado en Tiempo y Postura de Quieto')

    # Creamos los jugadores
    jugador1 = Jugador(ARCHIVO_SPRITE, ARCHIVO_COORDENADAS, POSICION_INICIAL_1)
    jugador2 = Jugador(ARCHIVO_SPRITE, ARCHIVO_COORDENADAS, POSICION_INICIAL_2)

    # Creamos el grupo de Sprites de jugadores
    grupo_jugadores = pygame.sprite.Group(jugador1, jugador2)

    while True:
        # Obtenemos el tiempo transcurrido desde la última actualización
        tiempo_pasado = reloj.tick(FPS)

        # Comprobamos los eventos
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        # Comprobamos las teclas pulsadas para el movimiento
        teclas_pulsadas = pygame.key.get_pressed()
        
        # Controles para el jugador 1 (flechas)
        if teclas_pulsadas[K_LEFT]:
            jugador1.mover(IZQUIERDA)
        elif teclas_pulsadas[K_RIGHT]:
            jugador1.mover(DERECHA)
        else:
            jugador1.mover(QUIETO)
            
        # Controles para el jugador 2 (A y D)
        if teclas_pulsadas[K_a]:
            jugador2.mover(IZQUIERDA)
        elif teclas_pulsadas[K_d]:
            jugador2.mover(DERECHA)
        else:
            jugador2.mover(QUIETO)

        # Actualizamos todos los sprites del grupo
        grupo_jugadores.update(tiempo_pasado)

        # Procedemos a pintar el fondo y los sprites
        pantalla.fill(COLOR_FONDO)
        grupo_jugadores.draw(pantalla)
        pygame.display.update()


if __name__ == "__main__":
    main()
