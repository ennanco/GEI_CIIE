# -*- coding: utf-8 -*-
"""
Ejemplo 5: Rebote en los límites de la pantalla
Este ejemplo introduce conceptos importantes:
- Detección de colisiones con los bordes
- Física básica de rebote
- Vector de velocidad (dirección y sentido)
- Inversión de velocidad al colisionar

Este ejemplo evoluciona del ejemplo 4, manteniendo el control de FPS
y añadiendo el concepto de rebote en los límites.
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
TAMANO_PELOTA = 4      # Radio de la pelota en píxeles

# Definimos estructuras usando namedtuple para mejor legibilidad
Posicion = namedtuple('Posicion', ['x', 'y'])
Velocidad = namedtuple('Velocidad', ['x', 'y'])

# Estado inicial de la pelota
posicion = Posicion(
    x=ANCHO_VENTANA // 2,  # Iniciamos en el centro de la pantalla
    y=ALTO_VENTANA // 2
)
velocidad = Velocidad(x=2, y=2)  # Velocidad inicial en cada eje

# Creamos la ventana del juego
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Ejemplo 5: Rebote en los límites")

# Creamos el objeto reloj para sincronizar el juego
reloj = pygame.time.Clock()

# Bucle principal del juego
while True:
    # Control de FPS
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

    # Comprobación de colisiones con los límites
    nueva_velocidad = velocidad

    # Rebote en los límites horizontales
    if (posicion.x <= TAMANO_PELOTA or 
        posicion.x >= ANCHO_VENTANA - TAMANO_PELOTA):
        nueva_velocidad = Velocidad(
            x=-velocidad.x,  # Invertimos la velocidad en X
            y=velocidad.y    # Mantenemos la velocidad en Y
        )
    
    # Rebote en los límites verticales
    if (posicion.y <= TAMANO_PELOTA or 
        posicion.y >= ALTO_VENTANA - TAMANO_PELOTA):
        nueva_velocidad = Velocidad(
            x=velocidad.x,   # Mantenemos la velocidad en X
            y=-velocidad.y   # Invertimos la velocidad en Y
        )

    # Actualizamos la velocidad
    velocidad = nueva_velocidad
    
    # Actualizamos la posición de la pelota
    posicion = Posicion(
        x=posicion.x + velocidad.x,
        y=posicion.y + velocidad.y
    )

    # Limpiamos la pantalla
    pantalla.fill(NEGRO)

    # Dibujamos la pelota en su nueva posición
    pygame.draw.circle(
        pantalla,
        BLANCO,
        (int(posicion.x), int(posicion.y)),
        TAMANO_PELOTA,
        0
    )

    # Actualizamos la pantalla
    pygame.display.update()

