"""
Ejemplo 7: Sprites con Saltos y Física Básica
------------------------------------------

Este ejemplo es parte de una serie de tutoriales incrementales para crear un videojuego.
Construye sobre el Ejemplo 6 (Movimiento Basado en Tiempo) añadiendo la capacidad de saltar
y una física básica de gravedad.

   - Sistema de saltos
   - Física básica de gravedad
   - Postura de salto
   - Control de estado en el aire
   - Movimiento suave basado en tiempo

Nuevos conceptos en este ejemplo:
* Física básica de gravedad
* Estados de movimiento vertical
* Control de saltos
* Posturas adicionales
* Velocidad vertical
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
ARRIBA = 3
ABAJO = 4

# Posturas
SPRITE_QUIETO = 0
SPRITE_ANDANDO = 1
SPRITE_SALTANDO = 2

# Configuración del juego
FPS = 60  # Frames por segundo
RETARDO_ANIMACION = 5  # Updates que durará cada imagen del personaje
VELOCIDAD_JUGADOR = 0.2  # Píxeles por milisegundo
VELOCIDAD_SALTO = 0.3  # Píxeles por milisegundo
GRAVEDAD = 0.004  # Aceleración de la gravedad
ALTURA_MAXIMA = 300  # Altura máxima del salto

# Dimensiones de la pantalla
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600

# Posiciones
POSICION_INICIAL_1 = (100, 300)  # Posición inicial del jugador 1
POSICION_INICIAL_2 = (200, 300)  # Posición inicial del jugador 2

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
    """Clase que representa al jugador con animación, movimiento y saltos."""
    def __init__(self, imagen, coordenadas, posicion):
        super().__init__()
        self.hoja = load_image(imagen, -1)
        self.hoja = self.hoja.convert_alpha()
        
        self.rect = pygame.Rect((7, 25), (30, 40))
        # Esto será la posición en pantalla
        self.rect.x = posicion[0]
        self.rect.y = posicion[1]
        self.movimiento = QUIETO
        self.mirando = IZQUIERDA
        # Está es la posición en el mundo
        self.posicionx = posicion[0]
        self.posiciony = posicion[1]
        self.velocidady = 0  # Velocidad vertical para saltos

        with open(coordenadas, 'r') as pfile:
            datos = pfile.read().split()
        
        self.numPostura = SPRITE_QUIETO  # Comenzamos en postura quieto
        self.numImagenPostura = 0
        cont = 0
        numImagenes = [6, 12, 6]  # [quieto, caminando, saltando]
        
        # Creamos una lista de listas para almacenar las coordenadas de cada postura
        self.coordenadasHoja = []
        
        # Iteramos sobre las tres posturas (0: quieto, 1: caminando, 2: saltando)
        for linea in range(0, 3):
            # Añadimos una lista vacía para cada postura
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            
            # Iteramos sobre cada frame de la postura actual
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

    def mover(self, teclas_pulsadas, arriba, abajo, izquierda, derecha):
        """
        Procesa las teclas pulsadas para determinar el movimiento del jugador.
        No permite saltar si ya está en el aire.
        """
        if teclas_pulsadas[arriba]:
            # Si estamos en el aire, ignoramos el salto
            if self.numPostura == SPRITE_SALTANDO:
                self.movimiento = QUIETO
            else:
                self.movimiento = ARRIBA
        elif teclas_pulsadas[izquierda]:
            self.movimiento = IZQUIERDA
        elif teclas_pulsadas[derecha]:
            self.movimiento = DERECHA
        else:
            self.movimiento = QUIETO

    def update(self, tiempo):
        """
        Actualiza la posición y animación del jugador.
        Maneja el movimiento horizontal, saltos y gravedad.
        """
        # Movimiento horizontal
        if self.movimiento == IZQUIERDA:
            # Si no estamos en el aire, la postura será caminando
            if self.numPostura != SPRITE_SALTANDO:
                self.numPostura = SPRITE_ANDANDO
            self.mirando = IZQUIERDA
            self.posicionx -= VELOCIDAD_JUGADOR * tiempo
            self.rect.left = self.posicionx
        elif self.movimiento == DERECHA:
            # Si no estamos en el aire, la postura será caminando
            if self.numPostura != SPRITE_SALTANDO:
                self.numPostura = SPRITE_ANDANDO
            self.mirando = DERECHA
            self.posicionx += VELOCIDAD_JUGADOR * tiempo
            self.rect.left = self.posicionx
        elif self.movimiento == ARRIBA:
            # Iniciamos el salto
            self.numPostura = SPRITE_SALTANDO
            self.velocidady = VELOCIDAD_SALTO
        elif self.movimiento == QUIETO:
            # Si no estamos saltando, la postura será quieto
            if self.numPostura != SPRITE_SALTANDO:
                self.numPostura = SPRITE_QUIETO

        # Física del salto
        if self.numPostura == SPRITE_SALTANDO:
            # Actualizamos la posición vertical
            self.posiciony -= self.velocidady * tiempo
            # Si llegamos al suelo, terminamos el salto
            if self.posiciony > ALTURA_MAXIMA:
                self.numPostura = SPRITE_QUIETO
                self.posiciony = ALTURA_MAXIMA
                self.velocidady = 0
            else:
                # Aplicamos la gravedad
                self.velocidady -= GRAVEDAD
            # Actualizamos la posición vertical del sprite
            self.rect.bottom = self.posiciony

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
    pygame.display.set_caption('Ejemplo 7: Sprites con Saltos y Física Básica')

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
        jugador1.mover(teclas_pulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT)
            
        # Controles para el jugador 2 (WASD)
        jugador2.mover(teclas_pulsadas, K_w, K_s, K_a, K_d)

        # Actualizamos todos los sprites del grupo
        grupo_jugadores.update(tiempo_pasado)

        # Procedemos a pintar el fondo y los sprites
        pantalla.fill(COLOR_FONDO)
        grupo_jugadores.draw(pantalla)
        pygame.display.update()


if __name__ == "__main__":
    main()
