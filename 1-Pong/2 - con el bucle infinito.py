# -*- coding: utf-8 -*-
"""
Ejemplo 2: Bucle principal del juego (Game Loop)
Este ejemplo introduce conceptos importantes:
- El bucle principal del juego
- Manejo básico de eventos
- Actualización continua de la pantalla
- Cierre controlado del programa
"""

# Importamos las librerías necesarias
import pygame
import sys
from pygame.locals import *

# Definimos colores como constantes
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Definimos las dimensiones de la pantalla
ANCHO_VENTANA = 800
ALTO_VENTANA = 600

# Inicializamos todos los módulos de PyGame
pygame.init()

# Creamos la ventana
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Ejemplo 2: Bucle principal del juego")

# Bucle principal del juego
# Este bucle se ejecuta indefinidamente hasta que se cierre el programa
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

    # Actualización del estado del juego
    # En este ejemplo simple, solo limpiamos la pantalla y dibujamos
    pantalla.fill(NEGRO)
    pygame.draw.circle(pantalla, BLANCO, (50, 50), 4, 0)

    # Dibujamos todo en la pantalla
    # Este paso es necesario para que se muestren los cambios
    pygame.display.update()

