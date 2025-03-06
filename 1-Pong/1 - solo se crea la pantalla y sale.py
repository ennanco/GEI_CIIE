# -*- coding: utf-8 -*-
"""
Ejemplo 1: Creación de una ventana básica con PyGame
Este ejemplo muestra los conceptos más básicos de PyGame:
- Inicialización de PyGame
- Creación de una ventana
- Dibujo básico
- Cierre de la aplicación
"""

# Importamos las librerías necesarias
import pygame
import sys
from pygame.locals import *

# Definimos algunos colores básicos como constantes
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Definimos las dimensiones de la pantalla
ANCHO_VENTANA = 800
ALTO_VENTANA = 600

# Inicializamos todos los módulos de PyGame
pygame.init()

# Creamos la ventana con las dimensiones especificadas
# El método set_mode devuelve una superficie (Surface) que representa la ventana
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

# Establecemos el título de la ventana
pygame.display.set_caption("Mi primer ejemplo con PyGame")

# Rellenamos la pantalla de color negro
pantalla.fill(NEGRO)

# Dibujamos un círculo blanco en la posición (50, 50)
# Los parámetros son: superficie, color, posición, radio, grosor (0 = relleno)
pygame.draw.circle(pantalla, BLANCO, (50, 50), 4, 0)

# Actualizamos la pantalla para mostrar los cambios
# Este paso es necesario para que se muestren los cambios en la ventana
pygame.display.update()

# Finalizamos PyGame y salimos del programa
pygame.quit()
sys.exit()
