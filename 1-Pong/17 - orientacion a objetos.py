"""
Ejemplo 17: Orientación a Objetos
Este ejemplo implementa las raquetas y la pelota como objetos:

1. Clases principales:
   - Clase Raqueta: Representa las raquetas de los jugadores
   - Clase Pelota: Gestiona el comportamiento de la pelota

2. Características:
   - Encapsulamiento de datos y comportamiento
   - Manejo de colisiones entre objetos
   - Gestión de puntuación y movimiento
"""

# -------------------------------------------------
# Importar las librerías
# -------------------------------------------------
import pygame
import sys
import time
from pygame.locals import *
from typing import List, Tuple, Optional

# -------------------------------------------------
# Constantes
# -------------------------------------------------

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Configuración de la ventana
ANCHO_VENTANA = 800
ALTO_VENTANA = 600

# Configuración del juego
FPS = 60
TAMANO_PELOTA = 4
VELOCIDAD_INICIAL_PELOTA = 2

# Configuración de las raquetas
ANCHO_RAQUETA = 10
ALTO_RAQUETA = 50
VELOCIDAD_RAQUETA = 5
MARGEN_RAQUETA = 50

# Configuración de textos
TAMANO_FUENTE = 96

# -------------------------------------------------
# Clases de los objetos del juego
# -------------------------------------------------

class Raqueta:
    """Clase que representa una raqueta del juego"""
    
    def __init__(self, posicion: Tuple[int, int], tamano: Tuple[int, int], posicion_marcador: Tuple[int, int]):
        """
        Inicializa una nueva raqueta.
        
        Args:
            posicion: Posición (x, y) de la raqueta
            tamano: Dimensiones (ancho, alto) de la raqueta
            posicion_marcador: Posición (x, y) del marcador
        """
        self._x, self._y = posicion
        self._ancho, self._alto = tamano
        self._puntos = 0
        self._posicion_marcador = posicion_marcador
        self._tipo_letra = pygame.font.SysFont('arial', TAMANO_FUENTE)
    
    @property
    def puntos(self) -> int:
        return self._puntos
        
    @puntos.setter
    def puntos(self, valor: int):
        self._puntos = valor
    
    def mover(self, direccion: int):
        """Mueve la raqueta en la dirección especificada"""
        self._y += direccion * VELOCIDAD_RAQUETA
        self.controla_y()
    
    def controla_y(self):
        """Controla que la raqueta no se salga de los límites verticales"""
        if self._y < 0:
            self._y = 0
        if self._y > ALTO_VENTANA - self._alto:
            self._y = ALTO_VENTANA - self._alto
    
    def colision(self, pelota: 'Pelota') -> bool:
        """Detecta si hay colisión con la pelota"""
        return (pelota.posicion_x - pelota.radio < self._x + self._ancho and
                pelota.posicion_x + pelota.radio > self._x and
                pelota.posicion_y - pelota.radio < self._y + self._alto and
                pelota.posicion_y + pelota.radio > self._y)
    
    def dibuja(self, pantalla: pygame.Surface):
        """Dibuja la raqueta en la pantalla"""
        pygame.draw.rect(pantalla, BLANCO,
                        (self._x, self._y,
                         self._ancho, self._alto))
    
    def dibuja_marcador(self, pantalla: pygame.Surface):
        """Dibuja el marcador en la pantalla"""
        marcador = self._tipo_letra.render(str(self._puntos), True, BLANCO)
        pantalla.blit(marcador, self._posicion_marcador + (50, 50))

class Pelota:
    """Clase que representa la pelota y su comportamiento"""
    
    def __init__(self, sonido_raqueta: Optional[pygame.mixer.Sound],
                 sonido_punto: Optional[pygame.mixer.Sound]):
        """
        Inicializa una nueva pelota.
        
        Args:
            sonido_raqueta: Sonido al golpear una raqueta
            sonido_punto: Sonido al marcar un punto
        """
        self._x = ANCHO_VENTANA // 2
        self._y = ALTO_VENTANA // 2
        self._radio = TAMANO_PELOTA
        self._velocidad_x = VELOCIDAD_INICIAL_PELOTA
        self._velocidad_y = VELOCIDAD_INICIAL_PELOTA
        self._sonido_raqueta = sonido_raqueta
        self._sonido_punto = sonido_punto
    
    @property
    def posicion_x(self) -> int:
        return self._x
    
    @property
    def posicion_y(self) -> int:
        return self._y
    
    @property
    def radio(self) -> int:
        return self._radio
    
    def _reproducir_sonido(self, sonido: Optional[pygame.mixer.Sound]):
        """Reproduce un sonido si está disponible"""
        if sonido is not None:
            sonido.play()
    
    def update(self, jugador1: Raqueta, jugador2: Raqueta) -> Optional[Tuple[int, int]]:
        """
        Actualiza el estado de la pelota.
        
        Returns:
            Optional[Tuple[int, int]]: Puntos a añadir (jugador1, jugador2) o None
        """
        # Colisiones con raquetas
        if jugador1.colision(self) or jugador2.colision(self):
            self._velocidad_x = -self._velocidad_x
            self._reproducir_sonido(self._sonido_raqueta)
        
        # Puntuación
        if self._x <= self._radio:  # La pelota sale por la izquierda
            self._reproducir_sonido(self._sonido_punto)
            return (0, 1)  # Punto para el jugador 2 (derecha)
        elif self._x >= ANCHO_VENTANA - self._radio:  # La pelota sale por la derecha
            self._reproducir_sonido(self._sonido_punto)
            return (1, 0)  # Punto para el jugador 1 (izquierda)
        
        # Rebotes verticales
        if (self._y <= self._radio or
            self._y >= ALTO_VENTANA - self._radio):
            self._velocidad_y = -self._velocidad_y
        
        # Actualizar posición
        self._x += self._velocidad_x
        self._y += self._velocidad_y
        
        return None
    
    def reiniciar(self, direccion: int):
        """Reinicia la pelota en el centro con la dirección especificada"""
        self._x = ANCHO_VENTANA // 2
        self._y = ALTO_VENTANA // 2
        self._velocidad_x = VELOCIDAD_INICIAL_PELOTA * direccion
        self._velocidad_y = VELOCIDAD_INICIAL_PELOTA
    
    def dibuja(self, pantalla: pygame.Surface):
        """Dibuja la pelota en la pantalla"""
        pygame.draw.circle(pantalla, BLANCO,
                         (int(self._x), int(self._y)),
                         self._radio, 0)

# -------------------------------------------------
# Funciones del juego
# -------------------------------------------------

def mostrar_pantalla_inicio(pantalla: pygame.Surface, tipo_letra: pygame.font.Font, imagen_fondo: Optional[pygame.Surface]):
    """Muestra la pantalla de inicio del juego"""
    if imagen_fondo is not None:
        pantalla.blit(imagen_fondo, (0, 0))
    else:
        pantalla.fill(NEGRO)
    
    texto_titulo = tipo_letra.render('PONG', True, BLANCO)
    texto_mensaje = tipo_letra.render('Pulse cualquier tecla', True, BLANCO)
    
    pantalla.blit(texto_titulo, (50, ALTO_VENTANA // 4, 200, 100))
    pantalla.blit(texto_mensaje, (20, ALTO_VENTANA // 2, 200, 100))
    pygame.display.update()
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == KEYDOWN:
                esperando = False

def main():
    """Función principal del juego"""
    # Inicializar pygame
    pygame.init()
    pygame.mixer.init()

    # Cargar recursos
    try:
        sonido_raqueta = pygame.mixer.Sound('recursos/Ping_Pong.wav')
        sonido_aplausos = pygame.mixer.Sound('recursos/Aplausos.wav')
    except pygame.error as e:
        print(f"Error al cargar el sonido de la raqueta: {e}")
        sonido_raqueta = None
        sonido_aplausos = None
        

    try:
        imagen_fondo = pygame.image.load('recursos/pistaTenis.jpg').convert()
        imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO_VENTANA, ALTO_VENTANA))
    except pygame.error as e:
        print(f"Error al cargar la imagen de fondo: {e}")
        imagen_fondo = None

    # Crear la pantalla
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Ejemplo 17: Orientación a Objetos")

    # Configuración adicional
    reloj = pygame.time.Clock()
    tipo_letra = pygame.font.SysFont('arial', TAMANO_FUENTE)
    pygame.key.set_repeat(1, 25)
    pygame.mouse.set_visible(False)

    # Crear objetos del juego
    jugador1 = Raqueta(
        (MARGEN_RAQUETA, ALTO_VENTANA // 2),          # Posición inicial: (x=50px desde la izquierda, y=centro de la pantalla)
        (ANCHO_RAQUETA, ALTO_RAQUETA),                # Dimensiones: (ancho=10px, alto=50px)
        (ANCHO_VENTANA // 4, ALTO_VENTANA // 8)       # Posición del marcador: (x=1/4 del ancho, y=1/8 del alto)
    )
    
    jugador2 = Raqueta(
        (ANCHO_VENTANA - MARGEN_RAQUETA - ANCHO_RAQUETA, ALTO_VENTANA // 2),  # Posición inicial: (x=740px desde la izquierda, y=centro)
        (ANCHO_RAQUETA, ALTO_RAQUETA),                                         # Dimensiones: (ancho=10px, alto=50px)
        (ANCHO_VENTANA * 3 // 4, ALTO_VENTANA // 8)                           # Posición del marcador: (x=3/4 del ancho, y=1/8 del alto)
    )
    
    pelota = Pelota(sonido_raqueta, sonido_aplausos)

    # Mostrar pantalla de inicio
    mostrar_pantalla_inicio(pantalla, tipo_letra, imagen_fondo)

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
                if evento.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif evento.key == K_q:
                    jugador1.mover(-1)
                elif evento.key == K_a:
                    jugador1.mover(1)
                elif evento.key == K_o:
                    jugador2.mover(-1)
                elif evento.key == K_l:
                    jugador2.mover(1)

        # Actualizar estado del juego
        resultado = pelota.update(jugador1, jugador2)
        if resultado is not None:
            puntos_j1, puntos_j2 = resultado
            jugador1.puntos += puntos_j1
            jugador2.puntos += puntos_j2
            time.sleep(1)
            pelota.reiniciar(-1 if puntos_j1 > 0 else 1)

        # Dibujar elementos
        if imagen_fondo is not None:
            pantalla.blit(imagen_fondo, (0, 0))
        else:
            pantalla.fill(NEGRO)
        
        jugador1.dibuja(pantalla)
        jugador2.dibuja(pantalla)
        pelota.dibuja(pantalla)
        
        jugador1.dibuja_marcador(pantalla)
        jugador2.dibuja_marcador(pantalla)
        
        pygame.display.update()

if __name__ == "__main__":
    main()
