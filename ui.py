import queue
import pygame
from enum import Enum

class ButtonType(Enum):
    PULSE = 1
    TOGGLE = 2

class ButtonState(Enum):
    IDLE = 1
    HOVER = 2
    PRESSED = 3

class Button:
    """Boton basico para usar en objetos de UI mayores
    Permite definir sus dimensiones y una imagen para mostrar."""
    _screen = NULL

    @_screen.setter
    def set_screen(self,screen):
        type(self)._screen = screen

    def __init__(self, dims, image, buttonType):
        self._width = dims[0]
        self._height = dims[1]
        self._left = dims[2]
        self._top = dims[3]
        self._image = image
        self._type = buttonType
        self._state = ButtonState.IDLE
        return None

    def draw(self):
        pass

class UI:
    """Clase principal de User Interface, 
    encargada de procesar peticiones para el usuario, 
    la entrada del usuario y dibujar en pantalla"""

    def __init__(self, q):
        self._queue = q
        return super().__init__(**kwargs)

    def main(self):
        ExitUI = False
        while(not ExitUI):
            self.get_requests()
            self.get_user_input()
            self.draw()
        self.exit_UI()
        return 0

    def get_user_input():
        pass

    def get_requests(self):
        while(not _queue.empty()):
            Request = _queue.get()

    def draw(self):
        pass

    def exit_UI(self):
        pass


    def load_resources(self):
        self.load_images()

    def load_images(self):
        pass

