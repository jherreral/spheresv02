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

    _screen = None  #Debe ser seteada antes de cualquier llamada a draw()


    @_screen.setter
    def set_screen(self,screen):
        type(self)._screen = screen

    def __init__(self, dims, ref, image, buttonType):
        self._width = dims[0]
        self._height = dims[1]
        self._left = dims[2]
        self._top = dims[3]
        self._refX = ref[0]
        self._refY = ref[1]
        self._image = image
        self._type = buttonType
        self._state = ButtonState.IDLE
        self._semipressed = None
        return None

    def is_inside_button(self,x,y):
        if x > (self._left + self._refX) \
            & x < (self._left + self._refX + self._width):
                if y > (self._top + self._refY) \
                & y < (self._top + self_refY + self._height):
                    return True
        return False

    def draw(self):
        pass

    def is_pressed(self,mouseEvent):
        if self._semipressed == False:
            if mouseEvent.type == 'MOUSEBUTTONDOWN' \
            & is_inside_button(mouseEvent.x, mouseEvent.y):
                    self._semipressed = True
        else:
            if mouseEvent.type == 'MOUSEBUTTONUP' \
            & is_inside_button(mouseEvent.x, mouseEvent.y):
                self._state = ButtonState.PRESSED
                self._semipressed = False

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

