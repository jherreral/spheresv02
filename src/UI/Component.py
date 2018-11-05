from UIElement import UIElement

class Component(UIElement):
    """Los componentes son secciones de la pantalla de juego"""
    def __init__(self, dims):

        # Un componente inactivo no ejecuta su update()
        self._active = True   
                             
        super().__init__(dims)