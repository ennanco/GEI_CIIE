from pyganim import PygAnimation

# Extendemos la clase animacion de PygAnimation para darle posicion
class Animacion(PygAnimation):
    def __init__(self, *args):
        super().__init__(args)
        # Posicion que tendra esta animacion
        self.posicion = (0, 0)
        
    def establecerPosicion(self, posicion):
        # La posicion es una tupla (x, y)
        self.posicion = posicion

    def mover(self, distancia):
        # La distancia es una tupla (x, y)
        self.posicion = (self.posicion[0] + distancia[0], self.posicion[1] + distancia[1])

    def draw(self, pantalla):
        # Dibuja la animacion en la pantalla
        self.blit(pantalla, self.posicion)

# Las distintas animaciones que tendremos

# La animacion del fuego
class AnimacionFuego(Animacion):
    def __init__(self):
        super().__init__([
                        ('imagenes/flame_a_0001.png', 0.1),
                        ('imagenes/flame_a_0002.png', 0.1),
                        ('imagenes/flame_a_0003.png', 0.1),
                        ('imagenes/flame_a_0004.png', 0.1),
                        ('imagenes/flame_a_0005.png', 0.1),
                        ('imagenes/flame_a_0006.png', 0.1)])

# La animacion del rayo
class AnimacionRayo(Animacion):
    def __init__(self):
        super().__init__([
                        ('imagenes/bolt_strike_0001.png', 0.1),
                        ('imagenes/bolt_strike_0002.png', 0.1),
                        ('imagenes/bolt_strike_0003.png', 0.1),
                        ('imagenes/bolt_strike_0004.png', 0.1),
                        ('imagenes/bolt_strike_0005.png', 0.1),
                        ('imagenes/bolt_strike_0006.png', 0.1),
                        ('imagenes/bolt_strike_0007.png', 0.1),
                        ('imagenes/bolt_strike_0008.png', 0.1),
                        ('imagenes/bolt_strike_0009.png', 0.1),
                        ('imagenes/bolt_strike_0010.png', 0.1)])

# La animacion del humo
class AnimacionHumo(Animacion):
    def __init__(self):
        super().__init__([
                        ('imagenes/smoke_puff_0001.png', 0.1),
                        ('imagenes/smoke_puff_0002.png', 0.1),
                        ('imagenes/smoke_puff_0003.png', 0.1),
                        ('imagenes/smoke_puff_0004.png', 0.1),
                        ('imagenes/smoke_puff_0005.png', 0.1),
                        ('imagenes/smoke_puff_0006.png', 0.1),
                        ('imagenes/smoke_puff_0007.png', 0.1),
                        ('imagenes/smoke_puff_0008.png', 0.2),
                        ('imagenes/smoke_puff_0009.png', 0.2),
                        ('imagenes/smoke_puff_0010.png', 0.2)])
