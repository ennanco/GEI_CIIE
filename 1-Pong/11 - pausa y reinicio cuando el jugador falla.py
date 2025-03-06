# -*- coding: utf-8 -*-
"""
Ejemplo 11: Sistema de pausa y reinicio al fallar
Este ejemplo introduce dos conceptos importantes:

1. Sistema de puntuación:
   - Detección cuando la pelota sale por los laterales
   - Identificación del jugador que ha fallado
   - Reinicio de la pelota al centro

2. Mecánica de pausa:
   - Uso de time.sleep() para crear una pausa
   - Dar tiempo a los jugadores para prepararse
   - Reinicio desde el centro hacia el último ganador

Mejoras en la jugabilidad:
- Pausa de 1 segundo cuando un jugador falla
- Reinicio de la pelota al centro
- La pelota sale en dirección al jugador que ganó el punto

Se mantienen las mejoras anteriores:
- Sistema de colisiones con las raquetas
- Control de límites de las raquetas
- Control mediante key.set_repeat
"""

# Importamos las librerías necesarias
import pygame
import sys
import time
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
TIEMPO_PAUSA = 1       # Segundos de pausa al fallar

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
    x=ANCHO_VENTANA // 2,  # Centrada en X
    y=ALTO_VENTANA // 2    # Centrada en Y
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
pygame.display.set_caption("Ejemplo 11: Pausa y reinicio")

# Configuración avanzada de PyGame
pygame.key.set_repeat(1, 25)
pygame.mouse.set_visible(False)

# Creamos el objeto reloj para sincronizar el juego
reloj = pygame.time.Clock()

def reiniciar_pelota(direccion_x):
    """
    Reinicia la pelota al centro de la pantalla y realiza una pausa.
    
    Args:
        direccion_x: Dirección en X (-1 hacia la izquierda, 1 hacia la derecha)
    
    Returns:
        tuple: Nueva posición y velocidad de la pelota después de la pausa
    """
    time.sleep(TIEMPO_PAUSA)  # Pausa dramática
    return (
        Posicion(x=ANCHO_VENTANA // 2, y=ALTO_VENTANA // 2),  # Nueva posición
        Velocidad(x=2 * direccion_x, y=2)                      # Nueva velocidad
    )

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
                nueva_y = raqueta1.y - VELOCIDAD_RAQUETA
                if nueva_y < 0:
                    nueva_y = 0
                raqueta1 = Raqueta(
                    x=raqueta1.x,
                    y=nueva_y,
                    ancho=raqueta1.ancho,
                    alto=raqueta1.alto
                )
            elif evento.key == K_a:
                nueva_y = raqueta1.y + VELOCIDAD_RAQUETA
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
                nueva_y = raqueta2.y - VELOCIDAD_RAQUETA
                if nueva_y < 0:
                    nueva_y = 0
                raqueta2 = Raqueta(
                    x=raqueta2.x,
                    y=nueva_y,
                    ancho=raqueta2.ancho,
                    alto=raqueta2.alto
                )
            elif evento.key == K_l:
                nueva_y = raqueta2.y + VELOCIDAD_RAQUETA
                if nueva_y > ALTO_VENTANA - ALTO_RAQUETA:
                    nueva_y = ALTO_VENTANA - ALTO_RAQUETA
                raqueta2 = Raqueta(
                    x=raqueta2.x,
                    y=nueva_y,
                    ancho=raqueta2.ancho,
                    alto=raqueta2.alto
                )

    # Comprobación de colisiones
    nueva_velocidad = velocidad_pelota

    # Colisión con la raqueta del jugador 1
    if (posicion_pelota.x - TAMANO_PELOTA < raqueta1.x + raqueta1.ancho and  # Lado derecho de la raqueta
        posicion_pelota.x + TAMANO_PELOTA > raqueta1.x and                    # Lado izquierdo de la raqueta
        posicion_pelota.y - TAMANO_PELOTA < raqueta1.y + raqueta1.alto and   # Parte inferior de la raqueta
        posicion_pelota.y + TAMANO_PELOTA > raqueta1.y):                      # Parte superior de la raqueta
        nueva_velocidad = Velocidad(
            x=-velocidad_pelota.x,  # Invertimos la dirección horizontal
            y=velocidad_pelota.y    # Mantenemos la dirección vertical
        )

    # Colisión con la raqueta del jugador 2
    if (posicion_pelota.x - TAMANO_PELOTA < raqueta2.x + raqueta2.ancho and  # Lado derecho de la raqueta
        posicion_pelota.x + TAMANO_PELOTA > raqueta2.x and                    # Lado izquierdo de la raqueta
        posicion_pelota.y - TAMANO_PELOTA < raqueta2.y + raqueta2.alto and   # Parte inferior de la raqueta
        posicion_pelota.y + TAMANO_PELOTA > raqueta2.y):                      # Parte superior de la raqueta
        nueva_velocidad = Velocidad(
            x=-velocidad_pelota.x,  # Invertimos la dirección horizontal
            y=velocidad_pelota.y    # Mantenemos la dirección vertical
        )

    # Comprobación de límites y puntuación
    if posicion_pelota.x <= TAMANO_PELOTA:  # Punto para el jugador 2
        posicion_pelota, velocidad_pelota = reiniciar_pelota(1)  # Pelota hacia jugador 2
        continue  # Saltamos el resto del ciclo

    if posicion_pelota.x >= ANCHO_VENTANA - TAMANO_PELOTA:  # Punto para el jugador 1
        posicion_pelota, velocidad_pelota = reiniciar_pelota(-1)  # Pelota hacia jugador 1
        continue  # Saltamos el resto del ciclo

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

