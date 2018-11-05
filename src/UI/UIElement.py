class UIElement:
    """Clase que guarda metodos estaticos y genericos para todos los objetos UI"""
    
    def __init__(self, dims):
        self._screen = None
        self._width = dims[0]
        self._height = dims[1]
        self._left = dims[2]        
        self._top = dims[3]

    @property
    def screen(self):
        return self._screen #Debe ser seteada antes de cualquier llamada a draw()

    @screen.setter
    def screen(self,scn):
        self._screen = scn

    def has_inside(self,x,y):
        if (x > self._left and 
            x < self._left + self._width):
            if (y > self._top and 
                y < self._top + self._height):
                return True
        return False