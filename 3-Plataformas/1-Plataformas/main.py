#!/usr/bin/env python

import pygame
import sys
from fase import Fase
from configuracion import Configuracion


def main():
    """Función principal del juego"""
    # Inicializar pygame
    pygame.init()
    
    # Obtenemos la configuración (Singleton)
    config = Configuracion()

    # Crear la pantalla
    pantalla = pygame.display.set_mode((config.ANCHO_PANTALLA, config.ALTO_PANTALLA), 0, 32)

    # Creamos el objeto reloj para sincronizar el juego
    reloj = pygame.time.Clock()

    # Creamos la fase
    fase = Fase(pantalla)

    # El bucle de eventos
    while True:
        # Sincronizar el juego a 60 fps
        tiempo_pasado = reloj.tick(config.FPS)

        # Coge la lista de eventos y se la pasa a la escena
        # Devuelve si se debe parar o no el juego
        if fase.eventos(pygame.event.get()):
            pygame.quit()
            sys.exit()

        # Actualiza la escena
        # Devuelve si se debe parar o no el juego
        if fase.update(tiempo_pasado):
            pygame.quit()
            sys.exit()

        # Se dibuja en pantalla
        fase.draw()
        pygame.display.flip()


if __name__ == '__main__':
    main()

