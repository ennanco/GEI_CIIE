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

        config = Configuracion()
        
        # Calcular los límites de la dead zone
        self.dead_zone_width = self.config.DEAD_ZONE_WIDTH
        self.dead_zone_height = self.config.DEAD_ZONE_HEIGHT
        self.dead_zone_left = (self.viewport_width - self.dead_zone_width) // 2
        self.dead_zone_right = self.dead_zone_left + self.dead_zone_width
        self.dead_zone_top = (self.viewport_height - self.dead_zone_height) // 2
        self.dead_zone_bottom = self.dead_zone_top + self.dead_zone_height

    def obtener_posicion(self):
        return (self.scroll_x, self.scroll_y)

    def inCamera(self, sprite):
        # Comprobar si el rectangulo (posicion en pantalla) del sprite esta dentro de la camara
        return sprite.rect.left > 0 and sprite.rect.right < self.viewport_width and sprite.rect.bottom > 0 and sprite.rect.top < self.viewport_height

    def update(self, grupo_jugadores):
        """Actualiza la posición de la cámara según los sprites del grupo de jugadores.
        
        Esta función maneja el scroll horizontal de la cámara basándose en las posiciones
        de los jugadores más a la izquierda y derecha del grupo. El comportamiento varía
        dependiendo de la distancia entre los jugadores:
        
        1. Si los jugadores están más separados que el ancho de la zona muerta:
           - Los jugadores son forzados a mantenerse dentro de sus zonas muertas respectivas
           - La cámara no se mueve
        
        2. Si los jugadores están lo suficientemente cerca:
           - La cámara se mueve para mantener a ambos jugadores visibles
           - El movimiento respeta los límites del mundo
        
        Args:
            grupo_jugadores (pygame.sprite.Group): Grupo de sprites que representan a los jugadores.
                                                 Debe contener al menos un sprite.
            
        Returns:
            bool: True si la cámara se ha movido y estaba permitido moverla,
                 False si la cámara no se movió o el movimiento fue bloqueado.
        """
        # Verificación inicial de que hay jugadores para procesar
        if not grupo_jugadores or not grupo_jugadores.sprites():
            return False

        # Encontrar los sprites en los extremos izquierdo y derecho
        # Usamos min/max con una función lambda que compara las posiciones left/right de los rectángulos
        target_izq = min(grupo_jugadores.sprites(), key=lambda t: t.rect.left)
        target_der = max(grupo_jugadores.sprites(), key=lambda t: t.rect.right)
        
        # Guardamos el scroll actual para detectar cambios
        scroll_anterior = self.scroll_x
        # Flag que indica si se permite mover la cámara
        mover_camara = True

        # Calculamos la distancia total entre el extremo izquierdo del jugador más a la izquierda
        # y el extremo derecho del jugador más a la derecha
        distancia_jugadores = target_der.rect.right - target_izq.rect.left

        # CASO 1: Los jugadores están demasiado separados (más que el ancho de la zona muerta)
        if distancia_jugadores > self.dead_zone_width:
            # Si el jugador izquierdo intenta salir de su zona muerta
            if target_izq.rect.left < self.dead_zone_left + self.scroll_x:
                # Lo forzamos a mantenerse en el límite de la zona muerta
                target_izq.establecerPosicion((self.scroll_x + self.dead_zone_left, target_izq.posicion[1]))
                mover_camara = False
            
            # Si el jugador derecho intenta salir de su zona muerta
            if target_der.rect.right > self.dead_zone_right + self.scroll_x:
                # Lo forzamos a mantenerse en el límite de la zona muerta
                target_der.establecerPosicion((self.scroll_x + self.dead_zone_right - target_der.rect.width, 
                                            target_der.posicion[1]))
                mover_camara = False

        # CASO 2: Los jugadores están lo suficientemente cerca para moverse juntos
        else:
            # Si el jugador izquierdo sale de la zona muerta
            if target_izq.rect.left < self.dead_zone_left + self.scroll_x:
                # Calculamos y aplicamos el desplazamiento necesario hacia la izquierda
                desplazamiento = (self.dead_zone_left + self.scroll_x) - target_izq.rect.left
                # Verificamos que el desplazamiento no haga que el jugador derecho salga de la zona muerta
                # El desplazamiento mueve la cámara a la izquierda, por lo que el jugador derecho debe mantenerse
                # dentro del límite derecho de la zona muerta
                if target_der.rect.right - desplazamiento <= self.dead_zone_right + self.scroll_x:
                    self.scroll_x -= desplazamiento
                else:
                    # Si el jugador derecho saldría de la zona muerta, ajustamos la posición del izquierdo
                    target_izq.establecerPosicion((self.scroll_x + self.dead_zone_left, target_izq.posicion[1]))
                    mover_camara = False

            # Si el jugador derecho sale de la zona muerta
            elif target_der.rect.right > self.dead_zone_right + self.scroll_x:
                # Calculamos y aplicamos el desplazamiento necesario hacia la derecha
                desplazamiento = target_der.rect.right - (self.dead_zone_right + self.scroll_x)
                # Verificamos que el desplazamiento no haga que el jugador izquierdo salga de la zona muerta
                if target_izq.rect.left + desplazamiento >= self.dead_zone_left + self.scroll_x:
                    self.scroll_x += desplazamiento
                else:
                    # Si el jugador izquierdo saldría de la zona muerta, ajustamos la posición del derecho
                    target_der.establecerPosicion((self.scroll_x + self.dead_zone_right - target_der.rect.width, 
                                                target_der.posicion[1]))
                    mover_camara = False

        # Verificación final: Aseguramos que el scroll no se salga de los límites del mundo
        if self.scroll_x < 0:  # Límite izquierdo del mundo
            self.scroll_x = 0
            mover_camara = False
        elif self.scroll_x + self.viewport_width > self.world_width:  # Límite derecho del mundo
            self.scroll_x = self.world_width - self.viewport_width
            mover_camara = False

        # Retornamos True solo si:
        # 1. El scroll actual es diferente al anterior (hubo movimiento)
        # 2. Estaba permitido mover la cámara (no se alcanzaron límites)
        return self.scroll_x != scroll_anterior and mover_camara

    def actualizar_sprites(self, grupo_sprites:pygame.sprite.Group):
        """Actualiza la posición en pantalla de todos los sprites según el scroll"""
        for sprite in grupo_sprites:
            sprite.establecerPosicionPantalla((sprite.posicion[0] - self.scroll_x, 
                                             sprite.posicion[1] - self.scroll_y))

    def draw_debug(self, screen):
        # Dibujar la dead zone (para debug)
        pygame.draw.rect(screen, (255, 0, 0), 
                        (self.dead_zone_left, self.dead_zone_top, 
                         self.dead_zone_width, self.dead_zone_height), 
                        1)
