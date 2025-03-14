import pygame
import os
from configuracion import Configuracion

class GestorRecursos:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GestorRecursos, cls).__new__(cls)
            cls._instance.inicializar()
        return cls._instance
    
    def inicializar(self):
        self.config = Configuracion()
        self.imagenes = {}
        self.sonidos = {}
        self.coordenadas = {}
        
    @staticmethod
    def CargarImagen(nombre, colorTransparente=None):
        """Carga una imagen desde el directorio de recursos"""
        if nombre not in GestorRecursos._instance.imagenes:
            # Si no está en el diccionario, la cargamos
            ruta = os.path.join("recursos", "imagenes", nombre)
            imagen = pygame.image.load(ruta)
            if colorTransparente is not None:
                imagen = imagen.convert()
                imagen.set_colorkey(colorTransparente)
            else:
                imagen = imagen.convert_alpha()
            GestorRecursos._instance.imagenes[nombre] = imagen
        return GestorRecursos._instance.imagenes[nombre]
    
    @staticmethod
    def CargarArchivoCoordenadas(nombre):
        """Carga un archivo de coordenadas desde el directorio de recursos"""
        if nombre not in GestorRecursos._instance.coordenadas:
            ruta = os.path.join("recursos", "coordenadas", nombre)
            archivo = open(ruta, "r")
            contenido = archivo.read()
            archivo.close()
            GestorRecursos._instance.coordenadas[nombre] = contenido
        return GestorRecursos._instance.coordenadas[nombre]

class Camera:
    def __init__(self, width, height, world_width, world_height):
        self.width = width
        self.height = height
        self.world_width = world_width
        self.world_height = world_height
        self.scroll = pygame.Vector2(0, 0)
        
    def update(self, target):
        """Actualiza la posición de la cámara basándose en el objetivo"""
        # Calculamos la posición objetivo de la cámara
        target_x = target.rect.centerx - self.width / 2
        target_y = target.rect.centery - self.height / 2
        
        # Limitamos la cámara a los bordes del mundo
        target_x = max(0, min(target_x, self.world_width - self.width))
        target_y = max(0, min(target_y, self.world_height - self.height))
        
        # Si la posición ha cambiado, actualizamos el scroll
        if target_x != self.scroll.x or target_y != self.scroll.y:
            self.scroll.x = target_x
            self.scroll.y = target_y
            return True
        return False
    
    def obtener_posicion(self):
        """Devuelve la posición actual de la cámara"""
        return self.scroll
    
    def inCamera(self, sprite):
        """Comprueba si un sprite está dentro de la vista de la cámara"""
        return (sprite.rect.right > self.scroll.x and 
                sprite.rect.left < self.scroll.x + self.width and
                sprite.rect.bottom > self.scroll.y and 
                sprite.rect.top < self.scroll.y + self.height)
    
    def actualizar_sprites(self, sprites):
        """Actualiza la posición en pantalla de todos los sprites"""
        for sprite in sprites:
            sprite.establecerPosicionPantalla(self.scroll) 