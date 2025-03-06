# -*- coding: utf-8 -*-
"""
Ejemplo 4: Control de velocidad con reloj
Este ejemplo introduce conceptos importantes:
- Uso del reloj de PyGame para controlar la velocidad
- FPS (Frames Per Second) constantes
- Movimiento suave de objetos
- Control del tiempo de ejecución
"""

# Importamos las librerías necesarias
import pygame
import sys
from pygame.locals import *
from collections import namedtuple

# Inicializamos todos los módulos de PyGame
pygame.init()

# Definición de constantes
# Colores en formato RGB (Red, Green, Blue)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Configuración de la ventana
ANCHO_VENTANA = 800
ALTO_VENTANA = 600

# Configuración del juego
FPS = 60                # Frames por segundo objetivo
VELOCIDAD_PELOTA = 2    # Píxeles que se mueve la pelota por frame
TAMANO_PELOTA = 4      # Radio de la pelota en píxeles

# Definimos una estructura para la posición usando namedtuple
# Esto nos permite acceder a las coordenadas como posicion.x y posicion.y
# en lugar de usar índices numéricos, haciendo el código más legible
Posicion = namedtuple('Posicion', ['x', 'y'])

# Posición inicial de la pelota
posicion = Posicion(50, 50)

# Creamos la ventana del juego
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Ejemplo 4: Control de velocidad con reloj")

# Creamos el objeto reloj para sincronizar el juego
# Este objeto nos ayuda a mantener una velocidad constante
reloj = pygame.time.Clock()

# Bucle principal del juego
while True:
    # Control de FPS
    # El método tick() hace que el programa espere lo necesario
    # para mantener los FPS constantes
    reloj.tick(FPS)

    # Procesamiento de eventos
    for evento in pygame.event.get():
        # Si el usuario cierra la ventana
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()
        # Si el usuario presiona la tecla Escape
        elif evento.type == KEYDOWN and evento.key == K_ESCAPE:
            pygame.quit()
            sys.exit()

    # Actualización de la posición de la pelota
    # El movimiento es más suave porque los FPS son constantes
    # Creamos una nueva posición usando namedtuple
    posicion = Posicion(
        x=posicion.x + VELOCIDAD_PELOTA,
        y=posicion.y + VELOCIDAD_PELOTA
    )

    # Limpiamos la pantalla
    pantalla.fill(NEGRO)

    # Dibujamos la pelota en su nueva posición
    # Parámetros: superficie, color, posición, radio, grosor (0 = relleno)
    pygame.draw.circle(
        pantalla,
        BLANCO,
        (int(posicion.x), int(posicion.y)),
        TAMANO_PELOTA,
        0
    )

    # Actualizamos la pantalla para mostrar los cambios
    pygame.display.update()

