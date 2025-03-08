import os
import pygame
from pygame.locals import *

# -------------------------------------------------
# Constantes
# -------------------------------------------------

DIR_RECURSOS = 'imagenes'

# -------------------------------------------------
# Clase GestorRecursos
class GestorRecursos:
    """Gestor de recursos del juego"""
    
    recursos = {}
            
    @classmethod
    def CargarImagen(cls, nombre, colorkey=None):
        """
        Carga una imagen desde el disco.
        
        Args:
            nombre: Nombre del archivo de imagen
            colorkey: Color a usar como transparencia (-1 para usar el color del pixel (0,0))
            
        Returns:
            pygame.Surface: La imagen cargada
            
        Raises:
            SystemExit: Si no se puede cargar la imagen
        """
        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
            
        # Si no ha sido cargado anteriormente
        else:
            # Se carga la imagen indicando la carpeta en la que está
            fullname = os.path.join(DIR_RECURSOS, nombre)
            try:
                imagen = pygame.image.load(fullname)
            except pygame.error as message:
                print('Cannot load image:', fullname)
                raise SystemExit(message)
                
            imagen = imagen.convert()
            if colorkey is not None:
                if colorkey == -1:
                    colorkey = imagen.get_at((0, 0))
                imagen.set_colorkey(colorkey, RLEACCEL)
                
            # Se almacena
            cls.recursos[nombre] = imagen
            # Se devuelve
            return imagen

    @classmethod
    def CargarArchivoCoordenadas(cls, nombre):
        """
        Carga un archivo de coordenadas desde el disco.
        
        Args:
            nombre: Nombre del archivo de coordenadas
            
        Returns:
            str: Contenido del archivo
        """
        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
            
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el nombre de su carpeta
            fullname = os.path.join(DIR_RECURSOS, nombre)
            with open(fullname, 'r') as pfile:
                datos = pfile.read()
                
            # Se almacena
            cls.recursos[nombre] = datos
            # Se devuelve
            return datos 

# -------------------------------------------------
# Clase Camara

class Camera:
    
    def __init__(self, width, height, world_width, world_height):
        # Dimensiones de la ventana de visualización
        self.viewport_width = width
        self.viewport_height = height
        # Dimensiones totales del mundo
        self.world_width = world_width
        self.world_height = world_height
        # Posición del scroll
        self.scroll_x = 0
        self.scroll_y = 0

        self.config = Configuracion()
        
        # Calcular los límites de la dead zone
        self.dead_zone_left = (self.viewport_width - self.config.DEAD_ZONE_WIDTH) // 2
        self.dead_zone_right = self.dead_zone_left + self.config.DEAD_ZONE_WIDTH
        self.dead_zone_top = (self.viewport_height - self.config.DEAD_ZONE_HEIGHT) // 2
        self.dead_zone_bottom = self.dead_zone_top + self.config.DEAD_ZONE_HEIGHT

    def obtener_posicion(self):
        return (self.scroll_x, self.scroll_y)

    def inCamera(self, sprite:MiSprite):
        # Comprobar si el rectangulo (posicion en pantalla) del sprite esta dentro de la camara
        return sprite.rect.left>0 and sprite.rect.right<self.width and sprite.rect.bottom>0 and sprite.rect.top<self.height

    def update(self, target):
        # Calcular la posición del jugador en la pantalla
        screen_x = target.posicion[0] - self.scroll_x
        screen_y = target.posicion[1] - self.scroll_y

        # Actualizar scroll_x solo si el jugador está fuera de la dead zone horizontal
        if screen_x < self.dead_zone_left:
            self.scroll_x = target.posicion[0] - self.dead_zone_left
        elif screen_x > self.dead_zone_right:
            self.scroll_x = target.posicion[0] - self.dead_zone_right

        # Actualizar scroll_y solo si el jugador está fuera de la dead zone vertical
        if screen_y < self.dead_zone_top:
            self.scroll_y = target.posicion[1] - self.dead_zone_top
        elif screen_y > self.dead_zone_bottom:
            self.scroll_y = target.posicion[1] - self.dead_zone_bottom

        # Limitar el scroll al tamaño del mundo
        self.scroll_x = max(0, min(self.scroll_x, self.world_width - self.viewport_width))
        self.scroll_y = max(0, min(self.scroll_y, self.world_height - self.viewport_height))

        # Retornar True si la cámara se movió
        return True

    def actualizar_sprites(self, grupo_sprites:pygame.sprite.Group):
        """Actualiza la posición en pantalla de todos los sprites según el scroll"""
        for sprite in grupo_sprites:
            sprite.establecerPosicionPantalla((sprite.posicion[0] - self.scroll_x, 
                                             sprite.posicion[1] - self.scroll_y))

    def draw_debug(self, screen):
        # Dibujar la dead zone (para debug)
        pygame.draw.rect(screen, (255, 0, 0), 
                        (self.dead_zone_left, self.dead_zone_top, 
                         self.config.DEAD_ZONE_WIDTH, self.config.DEAD_ZONE_HEIGHT), 
                        1)
