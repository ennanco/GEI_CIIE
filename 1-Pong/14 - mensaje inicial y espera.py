"""
Ejemplo 14: Pantalla de inicio y sistema de espera
Este ejemplo introduce una pantalla de bienvenida y un sistema de espera:

1. Pantalla de inicio:
   - Mensaje de bienvenida con el título del juego
   - Instrucciones para comenzar
   - Diseño centrado y legible

2. Sistema de espera:
   - Bucle de espera independiente del juego principal
   - Transición suave entre estados
   - Manejo limpio de eventos
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
# Colores en formato RGB
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

# Configuración del marcador y textos
TAMANO_FUENTE_MARCADOR = 96
TAMANO_FUENTE_TITULO = 96
TAMANO_FUENTE_MENSAJE = 48
ALTURA_MARCADOR = ALTO_VENTANA // 8

# Definimos estructuras usando namedtuple para mejor legibilidad
Posicion = namedtuple('Posicion', ['x', 'y'])
Velocidad = namedtuple('Velocidad', ['x', 'y'])
Raqueta = namedtuple('Raqueta', ['x', 'y', 'ancho', 'alto'])
Marcador = namedtuple('Marcador', ['jugador1', 'jugador2'])

# Estado inicial del juego
marcador = Marcador(jugador1=0, jugador2=0)

# Estado inicial de la pelota
posicion_pelota = Posicion(
    x=ANCHO_VENTANA // 2,
    y=ALTO_VENTANA // 2
)
velocidad_pelota = Velocidad(x=2, y=2)

# Estado inicial de las raquetas
raqueta1 = Raqueta(
    x=MARGEN_RAQUETA,
    y=ALTO_VENTANA // 2 - ALTO_RAQUETA // 2,
    ancho=ANCHO_RAQUETA,
    alto=ALTO_RAQUETA
)

raqueta2 = Raqueta(
    x=ANCHO_VENTANA - MARGEN_RAQUETA - ANCHO_RAQUETA,
    y=ALTO_VENTANA // 2 - ALTO_RAQUETA // 2,
    ancho=ANCHO_RAQUETA,
    alto=ALTO_RAQUETA
)

# Creamos la ventana del juego
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Ejemplo 14: Pantalla de inicio")

# Configuración de las fuentes
fuente_marcador = pygame.font.SysFont('arial', TAMANO_FUENTE_MARCADOR)
fuente_titulo = pygame.font.SysFont('arial', TAMANO_FUENTE_TITULO)
fuente_mensaje = pygame.font.SysFont('arial', TAMANO_FUENTE_MENSAJE)

# Configuración avanzada de PyGame
pygame.key.set_repeat(1, 25)
pygame.mouse.set_visible(False)

# Creamos el objeto reloj para sincronizar el juego
reloj = pygame.time.Clock()

def mostrar_pantalla_inicio():
    """
    Muestra la pantalla de inicio y espera a que el jugador presione una tecla.
    """
    # Limpiamos la pantalla
    pantalla.fill(NEGRO)
    
    # Renderizamos el título
    texto_titulo = fuente_titulo.render('PONG', True, BLANCO)
    rect_titulo = texto_titulo.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 4))
    pantalla.blit(texto_titulo, rect_titulo)
    
    # Renderizamos el mensaje
    texto_mensaje = fuente_mensaje.render('Pulse cualquier tecla', True, BLANCO)
    rect_mensaje = texto_mensaje.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))
    pantalla.blit(texto_mensaje, rect_mensaje)
    
    # Actualizamos la pantalla
    pygame.display.update()
    
    # Esperamos a que se pulse una tecla
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == KEYDOWN:
                esperando = False

def reiniciar_pelota(direccion_x):
    """
    Reinicia la pelota al centro de la pantalla y realiza una pausa.
    
    Args:
        direccion_x: Dirección en X (-1 hacia la izquierda, 1 hacia la derecha)
    
    Returns:
        tuple: Nueva posición y velocidad de la pelota
    """
    time.sleep(TIEMPO_PAUSA)
    return (
        Posicion(x=ANCHO_VENTANA // 2, y=ALTO_VENTANA // 2),
        Velocidad(x=2 * direccion_x, y=2)
    )

def actualizar_puntuacion(marcador_actual, punto_para_jugador1):
    """
    Actualiza y muestra la puntuación.
    
    Args:
        marcador_actual: Marcador actual del juego
        punto_para_jugador1: True si el punto es para el jugador 1
    
    Returns:
        Marcador: Nuevo marcador actualizado
    """
    if punto_para_jugador1:
        nuevo_marcador = Marcador(
            jugador1=marcador_actual.jugador1 + 1,
            jugador2=marcador_actual.jugador2
        )
    else:
        nuevo_marcador = Marcador(
            jugador1=marcador_actual.jugador1,
            jugador2=marcador_actual.jugador2 + 1
        )
    
    print(f'Jugador 1: {nuevo_marcador.jugador1} - Jugador 2: {nuevo_marcador.jugador2}')
    return nuevo_marcador

def dibujar_marcadores(pantalla, marcador, fuente):
    """
    Dibuja los marcadores en la pantalla.
    
    Args:
        pantalla: Superficie de pygame donde dibujar
        marcador: Estado actual del marcador
        fuente: Objeto Font de pygame para renderizar el texto
    """
    # Renderizamos los números
    texto_marcador1 = fuente.render(str(marcador.jugador1), True, BLANCO)
    texto_marcador2 = fuente.render(str(marcador.jugador2), True, BLANCO)
    
    # Calculamos posiciones
    pos_x1 = ANCHO_VENTANA // 4
    pos_x2 = (ANCHO_VENTANA * 3) // 4
    
    # Centramos los textos
    rect1 = texto_marcador1.get_rect(center=(pos_x1, ALTURA_MARCADOR))
    rect2 = texto_marcador2.get_rect(center=(pos_x2, ALTURA_MARCADOR))
    
    # Dibujamos los marcadores
    pantalla.blit(texto_marcador1, rect1)
    pantalla.blit(texto_marcador2, rect2)

# Mostramos la pantalla de inicio
mostrar_pantalla_inicio()

# Bucle principal del juego
while True:
    # Control de FPS
    reloj.tick(FPS)

    # Procesamiento de eventos
    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()
        
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
    if (posicion_pelota.x - TAMANO_PELOTA < raqueta1.x + raqueta1.ancho and
        posicion_pelota.x + TAMANO_PELOTA > raqueta1.x and
        posicion_pelota.y - TAMANO_PELOTA < raqueta1.y + raqueta1.alto and
        posicion_pelota.y + TAMANO_PELOTA > raqueta1.y):
        nueva_velocidad = Velocidad(
            x=-velocidad_pelota.x,
            y=velocidad_pelota.y
        )

    # Colisión con la raqueta del jugador 2
    if (posicion_pelota.x - TAMANO_PELOTA < raqueta2.x + raqueta2.ancho and
        posicion_pelota.x + TAMANO_PELOTA > raqueta2.x and
        posicion_pelota.y - TAMANO_PELOTA < raqueta2.y + raqueta2.alto and
        posicion_pelota.y + TAMANO_PELOTA > raqueta2.y):
        nueva_velocidad = Velocidad(
            x=-velocidad_pelota.x,
            y=velocidad_pelota.y
        )

    # Comprobación de límites y puntuación
    if posicion_pelota.x <= TAMANO_PELOTA:  # Punto para el jugador 2
        marcador = actualizar_puntuacion(marcador, False)
        posicion_pelota, velocidad_pelota = reiniciar_pelota(1)
        continue

    if posicion_pelota.x >= ANCHO_VENTANA - TAMANO_PELOTA:  # Punto para el jugador 1
        marcador = actualizar_puntuacion(marcador, True)
        posicion_pelota, velocidad_pelota = reiniciar_pelota(-1)
        continue

    # Rebote en los límites verticales
    if (posicion_pelota.y <= TAMANO_PELOTA or 
        posicion_pelota.y >= ALTO_VENTANA - TAMANO_PELOTA):
        nueva_velocidad = Velocidad(
            x=velocidad_pelota.x,
            y=-velocidad_pelota.y
        )

    # Actualizamos la velocidad y posición
    velocidad_pelota = nueva_velocidad
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

    # Dibujamos los marcadores
    dibujar_marcadores(pantalla, marcador, fuente_marcador)

    # Actualizamos la pantalla
    pygame.display.update()

