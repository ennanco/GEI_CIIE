import pygame
from pygame.locals import *
from enum import Enum, auto
from escena import *
from recursos import GestorRecursos
from fase import Fase

# -------------------------------------------------
# Clase abstracta ElementoGUI

class ElementoGUI:
    def __init__(self, panel, rectangulo):
        self.panel = panel
        self.rect = rectangulo

    def establecerPosicion(self, posicion):
        self.rect.left = posicion[0]
        self.rect.bottom = posicion[1]

    def posicionEnElemento(self, posicion):
    posicionx, posiciony = posicion
    # alternativamente se podría usar collideoint pero eso no tendría en cuenta los bordes superior y derecho de la forma.
    return (self.rect.left <= posicionx <= self.rect.right) and (self.rect.top <= posiciony <= self.rect.bottom)

    def draw(self):
        raise NotImplemented("Tiene que implementar el metodo dibujar.")
    def accion(self):
        raise NotImplemented("Tiene que implementar el metodo accion.")


# -------------------------------------------------
# Clase Boton y los distintos botones

class Boton(ElementoGUI):
    def __init__(self, panel, nombreImagen, posicion):
        # Se carga la imagen del boton
        self.imagen = GestorRecursos.CargarImagen(nombreImagen,-1)
        self.imagen = pygame.transform.scale(self.imagen, (20, 20))
        # Se llama al método de la clase padre con el rectángulo que ocupa el botón
        super().__init__(panel, self.imagen.get_rect())
        # Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)

    def draw(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

class BotonJugar(Boton):
    def __init__(self, panel):
        super().__init__(panel, 'boton_verde.png', (580,530))
    def accion(self):
        self.panel.menu.ejecutarJuego()

class BotonSalir(Boton):
    def __init__(self, panel):
        super().__init__(panel, 'boton_rojo.png', (580,560))
    def accion(self):
        self.panel.menu.salirPrograma()

# -------------------------------------------------
# Clase TextoGUI y los distintos textos

class TextoGUI(ElementoGUI):
    def __init__(self, panel, fuente, color, texto, posicion):
        # Se crea la imagen del texto
        self.imagen = fuente.render(texto, True, color)
        # Se llama al método de la clase padre con el rectángulo que ocupa el texto
        super().__init__(panel, self.imagen.get_rect())
        # Se coloca el rectangulo en su posicion
        self.establecerPosicion(posicion)
    def draw(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

class TextoJugar(TextoGUI):
    def __init__(self, panel):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.SysFont('arial', 26);
        super().__init__(panel, fuente, (0, 0, 0), 'Jugar', (610, 535))
    def accion(self):
        self.panel.menu.ejecutarJuego()

class TextoSalir(TextoGUI):
    def __init__(self, panel):
        # La fuente la debería cargar el estor de recursos
        fuente = pygame.font.SysFont('arial', 26);
        super().__init__(panel, fuente, (0, 0, 0), 'Salir', (610, 565))
    def accion(self):
        self.panel.menu.salirPrograma()

# -------------------------------------------------
# Clase PanelGUI

class PanelGUI:
    """
        Clase que representa un panel, que es una pantalla que contiene un conjunto de elementos GUI
    """	
    def __init__(self, menu, nombreImagen):
        self.menu = menu
        # Se carga la imagen de fondo
        self.imagen = GestorRecursos.CargarImagen(nombreImagen)
        self.imagen = pygame.transform.scale(self.imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
        # Se tiene una lista de elementos GUI
        self.elementosGUI = []
        self.elementoClic = None

    def eventos(self, lista_eventos):
        
        for evento in lista_eventos:
            if evento.type == MOUSEBUTTONDOWN:
                elementos_raton = [elemento for elemento in self.elementosGUI if elemento.posicionEnElemento(evento.pos)]
                self.elementoClic = elementos_raton[0]
            if evento.type == MOUSEBUTTONUP:
                elementos_raton = [elemento for elemento in self.elementosGUI if elemento.posicionEnElemento(evento.pos)]
                if (elementos_raton[0] == self.elementoClic):
                    elementos_raton[0].accion()
                self.elementoClic = None  

    def draw(self, pantalla):
        # Dibujamos primero la imagen de fondo
        pantalla.blit(self.imagen, self.imagen.get_rect())
        # Después los botones
        for elemento in self.elementosGUI:
            elemento.draw(pantalla)

class PanelInicialGUI(PanelGUI):
    def __init__(self, menu):
        super().__init__(menu, 'portada.jpg')
        # Creamos los botones y los metemos en la lista
        botonJugar = BotonJugar(self)
        botonSalir = BotonSalir(self)
        self.elementosGUI.append(botonJugar)
        self.elementosGUI.append(botonSalir)
        # Creamos el texto y lo metemos en la lista
        textoJugar = TextoJugar(self)
        textoSalir = TextoSalir(self)
        self.elementosGUI.append(textoJugar)
        self.elementosGUI.append(textoSalir)

# -------------------------------------------------
# Clase Menú

class PanelesMenu(Enum):
    PANEL_INICIAL = auto()
    #PANEL_CONFIGURACION = auto()
    #PANEL_CREDITOS = auto()
    #PANEL_OPCIONES = auto()
    #PANEL_CREDITOS = auto()

class Menu(Escena):
    """
        Clase que representa un menu, que es una escena estática que contiene un panel
        o conjunto de paneles como podrían ser los paneles de opciones, etc.
    """
    def __init__(self, director):
        super().__init__(director);
        # Creamos la lista de paneles
        self.listaPaneles = {}
        # Creamos los paneles que vamos a tener
        #   y los metemos en la lista
        self.listaPaneles[PanelesMenu.PANEL_INICIAL] = PanelInicialGUI(self)
        # En que panel estamos actualmente
        self.panelActual = PanelesMenu.PANEL_INICIAL
        # Mostramos el panel inicial
        self.mostrarPanelInicial()

    def update(self, *args):
        """ 
            Se actualiza la pantalla actual, pero en este caso no se 
            hace nada al ser una pantalla estática
        """	
        return

    def eventos(self, lista_eventos):
        # Se mira si se quiere salir de esta escena
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if (evento.type == KEYDOWN and evento.key == K_ESCAPE) or (evento.type == pygame.QUIT):
                self.salirPrograma()

        # Se pasa la lista de eventos a la pantalla actual
        self.listaPaneles[self.panelActual].eventos(lista_eventos)

    def draw(self, pantalla):
        self.listaPaneles[self.panelActual].draw(pantalla)

    #--------------------------------------
    # Metodos propios del menu

    # Implementación del patrón de diseño fachada
    # Los paneles delegarán en el menu las acciones que se requieran
    def salirPrograma(self):
        self.director.salirPrograma()

    def ejecutarJuego(self):
        fase = Fase(self.director)
        self.director.cambiarEscena(fase)

    def mostrarPanelInicial(self):
        self.panelActual = PanelesMenu.PANEL_INICIAL

    # def mostrarPantallaConfiguracion(self):
    #    self.pantallaActual = ...
