# -*- coding: utf-8 -*-
"""
Ejemplo 6: Añadiendo las raquetas del Pong
Este ejemplo introduce conceptos importantes:
- Múltiples objetos en pantalla
- Control del teclado para movimiento
- Raquetas como rectángulos
- Movimiento restringido (límites de la pantalla)

Este ejemplo evoluciona del ejemplo 5, manteniendo el rebote
y añadiendo las raquetas controladas por el usuario.
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

# Configuración de las raquetas
ANCHO_RAQUETA = 10
ALTO_RAQUETA = 50
VELOCIDAD_RAQUETA = 5
MARGEN_RAQUETA = 50    # Distancia desde el borde de la pantalla

# Definimos estructuras usando namedtuple para mejor legibilidad
Posicion = namedtuple('Posicion', ['x', 'y'])
Velocidad = namedtuple('Velocidad', ['x', 'y'])
Raqueta = namedtuple('Raqueta', ['x', 'y', 'ancho', 'alto'])  # Representa un área rectangular como las utilizadas por PyGame

# Estado inicial de la pelota
posicion_pelota = Posicion(
    x=ANCHO_VENTANA // 2,
    y=ALTO_VENTANA // 2
)
velocidad_pelota = Velocidad(x=2, y=2)

# Estado inicial de las raquetas
# Raqueta izquierda (Jugador 1)
raqueta1 = Raqueta(
    x=MARGEN_RAQUETA,
    y=ALTO_VENTANA // 2 - ALTO_RAQUETA // 2,
    ancho=ANCHO_RAQUETA,
    alto=ALTO_RAQUETA
)

# Raqueta derecha (Jugador 2)
raqueta2 = Raqueta(
    x=ANCHO_VENTANA - MARGEN_RAQUETA - ANCHO_RAQUETA,
    y=ALTO_VENTANA // 2 - ALTO_RAQUETA // 2,
    ancho=ANCHO_RAQUETA,
    alto=ALTO_RAQUETA
)

# Creamos la ventana del juego
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Ejemplo 6: Pong con raquetas")

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
    
    # Obtenemos el estado actual de todas las teclas
    teclas = pygame.key.get_pressed()
    
    # Actualizamos la posición de la raqueta 1 (W/S)
    nueva_y_raqueta1 = raqueta1.y
    if teclas[K_w] and nueva_y_raqueta1 > 0:
        nueva_y_raqueta1 -= VELOCIDAD_RAQUETA
    if teclas[K_s] and nueva_y_raqueta1 < ALTO_VENTANA - ALTO_RAQUETA:
        nueva_y_raqueta1 += VELOCIDAD_RAQUETA
    raqueta1 = Raqueta(
        x=raqueta1.x,
        y=nueva_y_raqueta1,
        ancho=raqueta1.ancho,
        alto=raqueta1.alto
    )
    
    # Actualizamos la posición de la raqueta 2 (Flechas ARRIBA/ABAJO)
    nueva_y_raqueta2 = raqueta2.y
    if teclas[K_UP] and nueva_y_raqueta2 > 0:
        nueva_y_raqueta2 -= VELOCIDAD_RAQUETA
    if teclas[K_DOWN] and nueva_y_raqueta2 < ALTO_VENTANA - ALTO_RAQUETA:
        nueva_y_raqueta2 += VELOCIDAD_RAQUETA
    raqueta2 = Raqueta(
        x=raqueta2.x,
        y=nueva_y_raqueta2,
        ancho=raqueta2.ancho,
        alto=raqueta2.alto
    )

    # Comprobación de colisiones con los límites
    nueva_velocidad = velocidad_pelota

    # Rebote en los límites horizontales
    if (posicion_pelota.x <= TAMANO_PELOTA or 
        posicion_pelota.x >= ANCHO_VENTANA - TAMANO_PELOTA):
        nueva_velocidad = Velocidad(
            x=-velocidad_pelota.x,
            y=velocidad_pelota.y
        )
    
    # Rebote en los límites verticales
    if (posicion_pelota.y <= TAMANO_PELOTA or 
        posicion_pelota.y >= ALTO_VENTANA - TAMANO_PELOTA):
        nueva_velocidad = Velocidad(
            x=velocidad_pelota.x,
            y=-velocidad_pelota.y
        )

    # Actualizamos la velocidad
    velocidad_pelota = nueva_velocidad
    
    # Actualizamos la posición de la pelota
    posicion_pelota = Posicion(
        x=posicion_pelota.x + velocidad_pelota.x,
        y=posicion_pelota.y + velocidad_pelota.y
    )

    # Limpiamos la pantalla
    pantalla.fill(NEGRO)

    # Dibujamos la pelota
    pygame.draw.circle(
        pantalla,
        BLANCO,
        (int(posicion_pelota.x), int(posicion_pelota.y)),
        TAMANO_PELOTA,
        0
    )

    # Dibujamos las raquetas
    #Jugador 1
    pygame.draw.rect(
        pantalla,
        BLANCO,
        (
            raqueta1.x,
            raqueta1.y,
            raqueta1.ancho,
            raqueta1.alto
        )
    )
    #Jugador 2
    pygame.draw.rect(
        pantalla,
        BLANCO,
        (
            raqueta2.x,
            raqueta2.y,
            raqueta2.ancho,
            raqueta2.alto
        )
    )

    # Actualizamos la pantalla
    pygame.display.update()

