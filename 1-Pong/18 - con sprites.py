"""
Ejemplo 18: Sprites en PyGame
Este ejemplo demuestra el uso de sprites en PyGame para el manejo de objetos en juegos:

1. Características principales:
   - Uso de pygame.sprite.Sprite como clase base
   - Manejo de colisiones usando rect
   - Carga y renderizado de imágenes para sprites
   - Grupos de sprites para mejor organización
"""

# -------------------------------------------------
# Importar las librerías
# -------------------------------------------------
import pygame
import sys
import time
from pygame.locals import *
from typing import Optional, Tuple, List

# -------------------------------------------------
# Constantes
# -------------------------------------------------

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Configuración del juego
FPS = 60
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
VELOCIDAD_RAQUETA = 5

# Rutas de recursos
RUTA_RAQUETA = 'recursos/raqueta.png'
RUTA_PELOTA = 'recursos/pelota.png'
RUTA_FONDO = 'recursos/pistaTenis.jpg'
RUTA_SONIDO_RAQUETA = 'recursos/Ping_Pong.wav'
RUTA_SONIDO_PUNTO = 'recursos/Aplausos.wav'

# -------------------------------------------------
# Clases de los objetos del juego
# -------------------------------------------------

# -------------------------------------------------
# Raqueta

class Raqueta(pygame.sprite.Sprite):
    """Las raquetas de ambos jugadores implementadas como sprites"""

    def __init__(self, posicion: Tuple[int, int], posicion_marcador: Tuple[int, int]):
        # Inicializar la clase padre Sprite
        super().__init__()
        
        try:
            # Cargar y configurar la imagen
            self.image = pygame.image.load(RUTA_RAQUETA)
            self.rect = self.image.get_rect()
            self.rect.centerx = posicion[0]
            self.rect.centery = posicion[1]
        except pygame.error as e:
            print(f"Error al cargar la imagen de la raqueta: {e}")
            # Crear un rectángulo blanco como fallback
            self.image = pygame.Surface((10, 50))
            self.image.fill(BLANCO)
            self.rect = self.image.get_rect()
            self.rect.centerx = posicion[0]
            self.rect.centery = posicion[1]
        
        # Configuración del marcador
        self.puntos = 0
        self.posicion_marcador = posicion_marcador
        self.tipo_letra = pygame.font.SysFont('arial', 96)

    def controla_y(self):
        """Controla que la raqueta no se salga de los límites verticales"""
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= ALTO_VENTANA:
            self.rect.bottom = ALTO_VENTANA

    def colision(self, pelota: 'Pelota') -> bool:
        """Detecta colisión con la pelota usando los rectángulos de los sprites"""
        return self.rect.colliderect(pelota.rect)

    def update(self, direccion: int = 0):
        """Actualiza la posición de la raqueta según la dirección"""
        if direccion:
            self.rect.centery += direccion * VELOCIDAD_RAQUETA
            self.controla_y()

    def dibuja_marcador(self, pantalla: pygame.Surface):
        """Dibuja el marcador en la pantalla"""
        marcador = self.tipo_letra.render(str(self.puntos), True, BLANCO)
        pantalla.blit(marcador, self.posicion_marcador)

# -------------------------------------------------
# Pelota
    
class Pelota(pygame.sprite.Sprite):
    """La pelota y su comportamiento implementada como sprite"""

    def __init__(self, sonido_raqueta: Optional[pygame.mixer.Sound], sonido_punto: Optional[pygame.mixer.Sound]):
        # Inicializar la clase padre Sprite
        super().__init__()
        
        try:
            # Cargar y configurar la imagen
            self.image = pygame.image.load(RUTA_PELOTA)
            self.rect = self.image.get_rect()
        except pygame.error as e:
            print(f"Error al cargar la imagen de la pelota: {e}")
            # Crear un círculo blanco como fallback
            self.image = pygame.Surface((8, 8))
            pygame.draw.circle(self.image, BLANCO, (4, 4), 4)
            self.rect = self.image.get_rect()
        
        # Posición inicial
        self.rect.centerx = ANCHO_VENTANA // 2
        self.rect.centery = ALTO_VENTANA // 2
        
        # Velocidad inicial
        self.velocidad = [2, 2]
        
        # Sonidos
        self.sonido_raqueta = sonido_raqueta
        self.sonido_punto = sonido_punto

    def update(self, jugador1: Raqueta, jugador2: Raqueta) -> Optional[Tuple[int, int]]:
        """
        Actualiza la posición de la pelota y maneja colisiones
        
        Returns:
            Optional[Tuple[int, int]]: Puntos a añadir (jugador1, jugador2) o None
        """
        # Colisiones con raquetas
        if jugador1.colision(self) or jugador2.colision(self):
            self.velocidad[0] = -self.velocidad[0]
            if self.sonido_raqueta:
                self.sonido_raqueta.play()

        # Control de puntuación
        if self.rect.left <= 0 or self.rect.right >= ANCHO_VENTANA:
            if self.sonido_punto:
                self.sonido_punto.play()
            
            # Determinar quién marcó el punto
            marcador = (0, 1) if self.rect.left <= 0 else (1, 0)  # (jugador1, jugador2)
            
            # Reiniciar posición
            self.rect.centerx = ANCHO_VENTANA // 2
            self.rect.centery = ALTO_VENTANA // 2
            self.velocidad[0] = -self.velocidad[0]
            
            return marcador

        # Rebotes verticales
        if self.rect.top <= 0 or self.rect.bottom >= ALTO_VENTANA:
            self.velocidad[1] = -self.velocidad[1]

        # Actualizar posición
        self.rect.move_ip(tuple(self.velocidad))  # Convertir a tupla para move_ip
        return None

    # Dibuja la pelota
    def dibuja(self, pantalla):
        pantalla.blit(self.image, self.rect);


    
# -------------------------------------------------
# Funcion principal del juego
# -------------------------------------------------

def mostrar_pantalla_inicio(pantalla: pygame.Surface, imagen_fondo: Optional[pygame.Surface]):
    """Muestra la pantalla de inicio y espera a que se pulse una tecla"""
    # Dibujar fondo
    if imagen_fondo:
        pantalla.blit(imagen_fondo, (0, 0))
    else:
        pantalla.fill(NEGRO)
    
    # Mostrar textos
    tipo_letra = pygame.font.SysFont('arial', 96)
    pantalla.blit(tipo_letra.render('PONG', True, BLANCO), (50, ALTO_VENTANA // 4))
    pantalla.blit(tipo_letra.render('Pulse cualquier tecla', True, BLANCO), (20, ALTO_VENTANA // 2))
    pygame.display.update()
    
    # Esperar tecla
    esperar = True
    while esperar:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == KEYDOWN:
                esperar = False

def main():
    """Función principal del juego"""
    # Inicializar pygame
    pygame.init()
    pygame.mixer.init()

    # Cargar recursos
    try:
        sonido_raqueta = pygame.mixer.Sound(RUTA_SONIDO_RAQUETA)
        sonido_punto = pygame.mixer.Sound(RUTA_SONIDO_PUNTO)
    except pygame.error as e:
        print(f"Error al cargar los sonidos: {e}")
        sonido_raqueta = None
        sonido_punto = None

    try:
        imagen_fondo = pygame.image.load(RUTA_FONDO).convert()
    except pygame.error as e:
        print(f"Error al cargar la imagen de fondo: {e}")
        imagen_fondo = None

    # Configurar pantalla
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Ejemplo 18: Sprites en PyGame")
    reloj = pygame.time.Clock()

    # Configuración adicional
    pygame.key.set_repeat(1, 25)
    pygame.mouse.set_visible(False)

    # Crear sprites
    jugador1 = Raqueta((50, ALTO_VENTANA // 2), (ANCHO_VENTANA // 4, ALTO_VENTANA // 8))
    jugador2 = Raqueta((ANCHO_VENTANA - 50, ALTO_VENTANA // 2), (ANCHO_VENTANA * 3 // 4, ALTO_VENTANA // 8))
    pelota = Pelota(sonido_raqueta, sonido_punto)

    # Crear grupos de sprites
    todos_los_sprites = pygame.sprite.Group()
    todos_los_sprites.add(jugador1, jugador2, pelota)

    # Mostrar pantalla de inicio
    mostrar_pantalla_inicio(pantalla, imagen_fondo)

    # Bucle principal
    while True:
        # Control de FPS
        reloj.tick(FPS)

        # Procesar eventos
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif evento.key == K_q:
                    jugador1.update(-1)
                elif evento.key == K_a:
                    jugador1.update(1)
                elif evento.key == K_o:
                    jugador2.update(-1)
                elif evento.key == K_l:
                    jugador2.update(1)

        # Actualizar estado del juego
        resultado = pelota.update(jugador1, jugador2)
        if resultado:
            puntos_j1, puntos_j2 = resultado
            jugador1.puntos += puntos_j1
            jugador2.puntos += puntos_j2
            time.sleep(1)

        # Dibujar elementos
        if imagen_fondo:
            pantalla.blit(imagen_fondo, (0, 0))
        else:
            pantalla.fill(NEGRO)

        # Dibujar todos los sprites
        todos_los_sprites.draw(pantalla)
        
        # Dibujar marcadores
        jugador1.dibuja_marcador(pantalla)
        jugador2.dibuja_marcador(pantalla)
        
        pygame.display.update()

if __name__ == "__main__":
    main()
