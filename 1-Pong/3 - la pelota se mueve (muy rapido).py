# -*- coding: utf-8 -*-
"""
Ejemplo 3: Movimiento básico de una pelota
Este ejemplo introduce conceptos nuevos:
- Movimiento de objetos en la pantalla
- Uso de namedtuple para coordenadas
- Constantes para configuración
- Velocidad de movimiento
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
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Configuración de la ventana
ANCHO_VENTANA = 800
ALTO_VENTANA = 600

# Configuración de la pelota
TAMANO_PELOTA = 4      # Radio de la pelota en píxeles
VELOCIDAD_PELOTA = 5   # Píxeles que se mueve en cada actualización

# Definimos una estructura para la posición usando namedtuple
# Esto nos permite acceder a las coordenadas como posicion.x y posicion.y
# en lugar de usar índices numéricos, haciendo el código más legible
Posicion = namedtuple('Posicion', ['x', 'y'])

# Posición inicial de la pelota la posicion de la pelota es 50, 50
posicion = Posicion(50, 50)

# Creamos la ventana del juego
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Ejemplo 3: Movimiento de pelota")

# Bucle principal del juego
while True:
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
    # En cada iteración, la pelota se mueve diagonalmente
    # sumando VELOCIDAD_PELOTA a ambas coordenadas
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

