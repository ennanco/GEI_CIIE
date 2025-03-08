class Configuracion:
    """Clase Singleton que maneja la configuración del juego"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Configuracion, cls).__new__(cls)
            cls._instance._inicializar()
        return cls._instance
    
    def _inicializar(self):
        """Inicializa las variables de configuración"""
        # Dimensiones de la pantalla
        self.ANCHO_PANTALLA = 800
        self.ALTO_PANTALLA = 600
        self.FPS = 60
        self.DEAD_ZONE_HEIGHT = 600
        self.DEAD_ZONE_WIDTH = 600
