"""
Ejemplo 1: Toda la Imagen como Sprite
-----------------------------------

Este ejemplo es el primero de una serie de tutoriales incrementales para crear un videojuego.
Introduce los conceptos básicos de Pygame y el manejo de sprites.

Conceptos clave en este ejemplo:
* Estructura básica de un juego en Pygame
* Carga y visualización de imágenes
* Creación y uso de sprites
* Manejo de eventos del teclado
* Control de FPS (frames por segundo)
* Transparencias en imágenes (colorkey)
* Bucle principal del juego
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

# Colores
COLOR_FONDO = (133, 133, 133)  # Color gris

# Funciones auxiliares
def load_image(name, colorkey=None):
    """
    Carga una imagen desde el directorio 'imagenes'.
    
    Parámetros:
        name: Nombre del archivo de imagen
        colorkey: Color que se usará como transparencia
                 - Si es None, no hay transparencia
                 - Si es -1, se usa el color del pixel (0,0)
                 - Si es un color específico, ese será transparente
    
    Notas importantes:
    - pygame.image.load(): Carga la imagen en formato original
    - convert(): Convierte la imagen al formato interno de Pygame
    - set_colorkey(): Define qué color será transparente
    - Flags disponibles para set_colorkey:
        * RLEACCEL: Optimiza el rendimiento de las transparencias (recomendado)
        * SRCALPHA: Usa el canal alpha de la imagen para transparencia
        * SRCCOLORKEY: Usa el color especificado como transparencia
    """
    # Construimos la ruta completa del archivo
    fullname = os.path.join('imagenes', name)
    try:
        # Intentamos cargar la imagen
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', fullname)
        raise SystemExit(message)
    
    # Convertimos la imagen al formato interno de Pygame
    # Esto es necesario para un mejor rendimiento
    image = image.convert()
    
    # Si se especificó un colorkey, lo aplicamos
    if colorkey is not None:
        # Si es -1, usamos el color del primer pixel
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        # Aplicamos la transparencia con optimización RLE
        # RLEACCEL es el flag más común y recomendado para transparencias
        image.set_colorkey(colorkey, RLEACCEL)
    
    return image


# Clases de los objetos del juego

class Jugador(pygame.sprite.Sprite):
    """Clase que representa al jugador."""

    def __init__(self, imagen):
        # Primero invocamos al constructor de la clase padre
        super().__init__()
        # Se carga la imagen
        self.imagen = load_image(imagen, -1)
        #self.imagen = self.imagen.convert_alpha()
        # El rectangulo y la posicion que tendra
        self.rect = self.imagen.get_rect()
        self.rect.topleft = (100, 100)

    def dibujar(self, pantalla):
        """Dibuja el jugador en la pantalla."""
        pantalla.blit(self.imagen, self.rect)



# Funcion principal del juego

def main():
    # Inicializar pygame
    pygame.init()

    # Crear la pantalla
    pantalla = pygame.display.set_mode((800, 600), 0, 32)

    # Creamos el objeto reloj para sincronizar el juego
    reloj = pygame.time.Clock()

    # Poner el título de la ventana
    pygame.display.set_caption('Ejemplo 1: Uso de Sprite')

    # Cargar la imagen del hombre
    jugador = Jugador(ARCHIVO_SPRITE)

    # Variable que controla la posición del Sprite (horizontal)
    pos = 100

    # El bucle de eventos
    while True:
        # Hacemos que el reloj espere a un determinado fps
        reloj.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Modificar posición en función de la tecla pulsada
        teclas_pulsadas = pygame.key.get_pressed()
        if teclas_pulsadas[K_LEFT]:
            jugador.rect.centerx -= 1
        if teclas_pulsadas[K_RIGHT]:
            jugador.rect.centerx += 1
        # Si la tecla es Escape
        if teclas_pulsadas[K_ESCAPE]:
            # Se sale del programa
            pygame.quit()
            sys.exit()

        # Dibujar el fondo de color
        pantalla.fill(COLOR_FONDO)

        # Dibujar el Sprite
        jugador.dibujar(pantalla)

        # Actualizar la pantalla
        pygame.display.update()


if __name__ == "__main__":
    main()
