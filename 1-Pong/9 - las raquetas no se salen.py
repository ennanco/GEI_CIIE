# -*- coding: utf-8 -*-
"""
Ejemplo 9: Control de límites para las raquetas


Mejoras en el control de límites:
- Implementación de límites físicos para las raquetas
- Dos formas diferentes de controlar los límites:
  1. Usando max/min (como en ejemplo 8)
  2. Usando if para ajustar la posición (este ejemplo)
- Prevención de que las raquetas se salgan de la pantalla

Se mantienen las mejoras anteriores:
- Control mediante key.set_repeat para movimiento continuo
- Cursor del ratón oculto

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
pygame.display.set_caption("Ejemplo 9: Control de límites")

# Configuración avanzada de PyGame
# Permitimos que las teclas se mantengan pulsadas
pygame.key.set_repeat(1, 25)

# Ocultamos el cursor del ratón
pygame.mouse.set_visible(False)

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
        
        # Control de raquetas mediante eventos de teclado (KEYDOWN)
        if evento.type == KEYDOWN:
            # Salir del juego
            if evento.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            
            # Control de la raqueta 1 (Q/A)
            elif evento.key == K_q:
                # Movemos la raqueta hacia arriba
                nueva_y = raqueta1.y - VELOCIDAD_RAQUETA
                # Verificamos si se sale por arriba
                if nueva_y < 0:
                    nueva_y = 0
                raqueta1 = Raqueta(
                    x=raqueta1.x,
                    y=nueva_y,
                    ancho=raqueta1.ancho,
                    alto=raqueta1.alto
                )
            elif evento.key == K_a:
                # Movemos la raqueta hacia abajo
                nueva_y = raqueta1.y + VELOCIDAD_RAQUETA
                # Verificamos si se sale por abajo
                if nueva_y > ALTO_VENTANA - ALTO_RAQUETA:
                    nueva_y = ALTO_VENTANA - ALTO_RAQUETA
                raqueta1 = Raqueta(
                    x=raqueta1.x,
                    y=nueva_y,
                    ancho=raqueta1.ancho,
                    alto=raqueta1.alto
                )
            
            # Control de la raqueta 2 (O/L)
            elif evento.key == K_o:
                # Movemos la raqueta hacia arriba
                nueva_y = raqueta2.y - VELOCIDAD_RAQUETA
                # Verificamos si se sale por arriba
                if nueva_y < 0:
                    nueva_y = 0
                raqueta2 = Raqueta(
                    x=raqueta2.x,
                    y=nueva_y,
                    ancho=raqueta2.ancho,
                    alto=raqueta2.alto
                )
            elif evento.key == K_l:
                # Movemos la raqueta hacia abajo
                nueva_y = raqueta2.y + VELOCIDAD_RAQUETA
                # Verificamos si se sale por abajo
                if nueva_y > ALTO_VENTANA - ALTO_RAQUETA:
                    nueva_y = ALTO_VENTANA - ALTO_RAQUETA
                raqueta2 = Raqueta(
                    x=raqueta2.x,
                    y=nueva_y,
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
    # Jugador 1 (Izquierda - Q/A)
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
    
    # Jugador 2 (Derecha - O/L)
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

