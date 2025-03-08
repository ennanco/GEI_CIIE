import pygame
import sys
import os
from pygame.locals import *
from personajes import Jugador, Sniper, MiSprite
from configuracion import Configuracion
from recursos import GestorRecursos, Camera


# Obtenemos la configuración (Singleton)
config = Configuracion()

# Constantes
VELOCIDAD_SOL = 0.1 # Pixeles por milisegundo

# Archivos de recursos
ARCHIVO_JUGADOR = 'Jugador.png'
ARCHIVO_COORD_JUGADOR = 'coordJugador.txt'
ARCHIVO_SNIPER = 'Sniper.png'
ARCHIVO_COORD_SNIPER = 'coordSniper.txt'

# -------------------------------------------------
# Clase Fase

class Fase:
    def __init__(self, pantalla):

        # Habria que pasarle como parámetro el número de fase, a partir del cual se cargue
        #  un fichero donde este la configuracion de esa fase en concreto, con cosas como
        #   - Nombre del archivo con el decorado
        #   - Posiciones de las plataformas
        #   - Posiciones de los enemigos
        #   - Posiciones de inicio de los jugadores
        #  etc.
        # Y cargar esa configuracion del archivo en lugar de ponerla a mano, como aqui abajo
        # De esta forma, se podrian tener muchas fases distintas con esta clase

        # Creamos el decorado y el fondo
        self.decorado = Decorado()
        self.fondo = Cielo()

        # Creamos los sprites de los jugadores
        self.jugador1 = Jugador(ARCHIVO_JUGADOR, ARCHIVO_COORD_JUGADOR)
        self.grupoJugadores = pygame.sprite.Group(self.jugador1)

        # Ponemos a los jugadores en sus posiciones iniciales
        self.jugador1.establecerPosicion((200, 551))
        
        # Los enemigos que tendran en este decorado
        enemigo1 = Sniper(ARCHIVO_SNIPER, ARCHIVO_COORD_SNIPER)
        enemigo1.establecerPosicion((1000, 418))
        # Creamos un grupo con los enemigos
        self.grupoEnemigos = pygame.sprite.Group(enemigo1)

        # Creamos las plataformas del decorado
        # La plataforma que conforma todo el suelo
        plataformaSuelo = Plataforma(pygame.Rect(0, 550, 1200, 15))
        # La plataforma del techo del edificio
        plataformaCasa = Plataforma(pygame.Rect(870, 417, 200, 10))
        # y el grupo con las mismas
        self.grupoPlataformas = pygame.sprite.Group(plataformaSuelo, plataformaCasa)
        
        # Creamos un grupo con los Sprites que se mueven
        self.grupoSpritesDinamicos = pygame.sprite.Group(self.jugador1, enemigo1)
        # Creamos otro grupo con todos los Sprites
        self.grupoSprites = pygame.sprite.Group(self.jugador1, enemigo1, plataformaSuelo, plataformaCasa)

        # Creamos la cámara establece la parte del decorado que se va a ver
        self.camara = Camera(config.ANCHO_PANTALLA, config.ALTO_PANTALLA, 
                           self.decorado.rect.width, self.decorado.rect.height)
    
    def update(self, tiempo):
        """
        Actualiza el estado de la fase, incluyendo todos los elementos del juego.
        
        Este método se encarga de:
        1. Actualizar la IA de los enemigos
        2. Actualizar la posición de todos los sprites dinámicos
        3. Comprobar colisiones entre jugadores y enemigos
        4. Actualizar la cámara y el scroll
        5. Actualizar elementos visuales (fondo, decorado)
        
        Args:
            tiempo (int): Milisegundos transcurridos desde la última actualización.
                         Se usa para calcular el movimiento correcto de los elementos.
            
        Returns:
            bool: True si se debe terminar el juego (por ejemplo, por colisión jugador-enemigo),
                 False si el juego debe continuar.
        """
        # Actualización de la IA de los enemigos
        for enemigo in iter(self.grupoEnemigos):
            if self.camara.inCamera(enemigo):
                enemigo.mover_cpu(self.jugador1)  # Si está en cámara, persigue al jugador
            else:
                enemigo.mover_cpu()  # Si está fuera de cámara, es decir no hacer nada QUIETO

        # Actualización de sprites dinámicos (personajes, proyectiles, etc.)
        self.grupoSpritesDinamicos.update(self.grupoPlataformas, tiempo)

        # Comprobación de colisiones entre jugadores y enemigos
        if pygame.sprite.groupcollide(self.grupoJugadores, self.grupoEnemigos, False, False) != {}:
            return True  # Terminar el juego si hay colisión

        # Actualización de la cámara y scroll
        if self.camara.update(self.jugador1):
            # Si la cámara se movió, actualizar posiciones de sprites y decorado
            self.camara.actualizar_sprites(self.grupoSprites)
            self.decorado.update(self.camara.obtener_posicion()[0])

        # Actualización de elementos visuales
        self.fondo.update(tiempo)  # Actualiza posición del sol y color del cielo

        return False  # Continuar el juego

    def draw(self):
        """Dibuja todos los elementos de la fase en la pantalla"""
        # Ponemos primero el fondo
        self.fondo.draw(self.pantalla)
        # Después el decorado
        self.decorado.draw(self.pantalla)
        # Luego los Sprites
        self.grupoSprites.draw(self.pantalla)

    def eventos(self, lista_eventos):
        """
        Procesa los eventos de la fase.
        
        Args:
            lista_eventos: Lista de eventos de Pygame
            
        Returns:
            bool: True si se debe salir del programa, False en caso contrario
        """
        # Miramos a ver si hay algun evento de salir del programa
        for evento in lista_eventos:
            # Si se sale del programa
            if evento.type == pygame.QUIT:
                return True

        # Indicamos la acción a realizar según la tecla pulsada para el jugador
        teclasPulsadas = pygame.key.get_pressed()
        self.jugador1.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT)
        
        return False

# -------------------------------------------------
# Clase Plataforma

#class Plataforma(pygame.sprite.Sprite):
class Plataforma(MiSprite):
    def __init__(self,rectangulo):
        """Inicializa una plataforma con el rectángulo especificado"""
        super().__init__()
        # Rectangulo con las coordenadas en pantalla que ocupara
        self.rect = rectangulo
        # Y lo situamos de forma global en esas coordenadas
        self.establecerPosicion((self.rect.left, self.rect.bottom))
        # En el caso particular de este juego, las plataformas no se van a ver, asi que no se carga ninguna imagen
        self.image = pygame.Surface((0, 0))


# -------------------------------------------------
# Clase Cielo

class Cielo:
    def __init__(self):
        self.sol = GestorRecursos.CargarImagen('sol.png', -1)
        self.sol = pygame.transform.scale(self.sol, (300, 200))
        self.rect = self.sol.get_rect()
        self.colorCielo = (100, 200, 255) # Color del cielo inicial
        self.posicionx = 0 # El lado izquierdo de la subimagen que se esta visualizando
        self.update(0)

    def update(self, tiempo):
        self.posicionx += VELOCIDAD_SOL * tiempo
        if (self.posicionx - self.rect.width >= config.ANCHO_PANTALLA):
            self.posicionx = 0
        self.rect.right = self.posicionx
        # Calculamos el color del cielo
        if self.posicionx >= ((self.rect.width + config.ANCHO_PANTALLA) / 2):
            ratio = 2 * ((self.rect.width + config.ANCHO_PANTALLA) - self.posicionx) / (self.rect.width + config.ANCHO_PANTALLA)
        else:
            ratio = 2 * self.posicionx / (self.rect.width + config.ANCHO_PANTALLA)
        self.colorCielo = (100*ratio, 200*ratio, 255)
        
    def draw(self,pantalla):
        """Dibuja el cielo en la pantalla"""
        # Dibujamos el color del cielo
        pantalla.fill(self.colorCielo)
        # Y ponemos el sol
        pantalla.blit(self.sol, self.rect)


# -------------------------------------------------
# Clase Decorado

class Decorado:
    def __init__(self):
        # Cargamos la imagen del decorado
        self.imagen = GestorRecursos.CargarImagen('decorado.png', -1)
        self.imagen = pygame.transform.scale(self.imagen, (1200, 300))

        self.rect = self.imagen.get_rect()
        self.rect.bottom = config.ALTO_PANTALLA

        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, config.ANCHO_PANTALLA, config.ALTO_PANTALLA)
        self.rectSubimagen.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto

    def update(self, scrollx):
        self.rectSubimagen.left = scrollx

    def draw(self, pantalla):
        pantalla.blit(self.imagen, self.rect, self.rectSubimagen)
