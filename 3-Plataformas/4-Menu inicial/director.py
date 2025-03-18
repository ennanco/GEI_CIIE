# Modulos
import pygame
import sys
from collections import deque
from escena import *
from pygame.locals import *
import configuracion as cfg

class Director:

    def __init__(self):
        # Inicializamos la pantalla y el modo grafico
        self._pantalla = pygame.display.set_mode((cfg.ANCHO_PANTALLA, cfg.ALTO_PANTALLA))
        pygame.display.set_caption("Ejemplo de Juego controlado por el patrón Director")
        # Pila de escenas
        self.pila = deque()
        # Flag que nos indica cuando quieren salir de la escena
        self.salir_escena = False
        # Reloj
        self.reloj = pygame.time.Clock()

    @property
    def pantalla(self):
        """
        Devuelve la pantalla del director
        """
        return self._pantalla

    def bucle(self, escena):

        self.salir_escena = False

        # Eliminamos todos los eventos producidos antes de entrar en el bucle
        pygame.event.clear()
        
        # El bucle del juego, las acciones que se realicen se harán en cada escena
        while not self.salir_escena:

            # Sincronizar el juego a 60 fps
            tiempo_pasado = self.reloj.tick(cfg.FPS)

            # Pasamos los eventos a la escena
            escena.eventos(pygame.event.get())

            # Actualiza la escena
            escena.update(tiempo_pasado)

            # Se dibuja en pantalla
            escena.draw(self.pantalla)
            pygame.display.flip()


    def execute(self):

        # Mientras haya escenas en la pila, ejecutaremos la de arriba
        while (len(self.pila)>0):

            # Se coge la escena a ejecutar como la que este en la cima de la pila
            escena = self.pila[-1]

            # Ejecutamos el bucle de eventos hasta que termine la escena
            self.bucle(escena)


    def salirEscena(self):
        # Indicamos en el flag que se quiere salir de la escena
        self.salir_escena = True
        # Eliminamos la escena actual de la pila (si la hay)
        try:
            self.pila.pop()
        except IndexError:
            pass # Si no hay escenas en la pila, no se hace nada

    def salirPrograma(self):
        # Vaciamos la lista de escenas pendientes
        self.pila.clear() # Liberar la memoria asociada a la pila
        self.salir_escena = True

    def cambiarEscena(self, escena):
        self.salirEscena()
        # Ponemos la escena pasada en la cima de la pila
        self.pila.append(escena)

    def apilarEscena(self, escena):
        self.salir_escena = True
        # Ponemos la escena pasada en la cima de la pila
        #  (por encima de la actual)
        self.pila.append(escena)

