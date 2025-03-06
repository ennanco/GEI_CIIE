# -*- coding: utf-8 -*-
"""
Ejemplo 7: Movimiento de las raquetas mediante eventos
Este ejemplo introduce una forma diferente de control respecto al ejemplo 6:

En el ejemplo 6:
- Se usa pygame.key.get_pressed() que detecta teclas mantenidas
- Permite movimiento continuo mientras se mantiene la tecla
- Es ideal para movimiento suave y continuo

En este ejemplo (7):
- Se usan eventos KEYDOWN que detectan cada pulsación individual
- La raqueta se mueve una vez por cada pulsación
- Es útil para movimientos discretos o acciones puntuales
- Demuestra un estilo diferente de control del juego

Otros conceptos que se mantienen:
- Movimiento independiente de cada raqueta
- Restricción de movimiento dentro de los límites
- Uso de namedtuples para estructuras de datos
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
Raqueta = namedtuple('Raqueta', ['x', 'y', 'ancho', 'alto'])  
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
pygame.display.set_caption("Ejemplo 7: Control de raquetas")

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
        # A diferencia del ejemplo 6 que usa get_pressed() para movimiento continuo,
        # aquí cada pulsación (KEYDOWN) mueve la raqueta una sola vez
        if evento.type == KEYDOWN:
            # Salir del juego
            if evento.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            
            # Control de la raqueta 1 (Q/A)
            # La raqueta se mueve una vez por cada pulsación de tecla
            elif evento.key == K_q and raqueta1.y > 0:
                raqueta1 = Raqueta(
                    x=raqueta1.x,
                    y=max(0, raqueta1.y - VELOCIDAD_RAQUETA),
                    ancho=raqueta1.ancho,
                    alto=raqueta1.alto
                )
            elif evento.key == K_a and raqueta1.y < ALTO_VENTANA - ALTO_RAQUETA:
                raqueta1 = Raqueta(
                    x=raqueta1.x,
                    y=min(ALTO_VENTANA - ALTO_RAQUETA, raqueta1.y + VELOCIDAD_RAQUETA),
                    ancho=raqueta1.ancho,
                    alto=raqueta1.alto
                )
            
            # Control de la raqueta 2 (O/L)
            # Mismo comportamiento: una pulsación = un movimiento
            elif evento.key == K_o and raqueta2.y > 0:
                raqueta2 = Raqueta(
                    x=raqueta2.x,
                    y=max(0, raqueta2.y - VELOCIDAD_RAQUETA),
                    ancho=raqueta2.ancho,
                    alto=raqueta2.alto
                )
            elif evento.key == K_l and raqueta2.y < ALTO_VENTANA - ALTO_RAQUETA:
                raqueta2 = Raqueta(
                    x=raqueta2.x,
                    y=min(ALTO_VENTANA - ALTO_RAQUETA, raqueta2.y + VELOCIDAD_RAQUETA),
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

