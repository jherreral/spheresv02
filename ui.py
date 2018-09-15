import queue
import pygame
import time
from enum import Enum

class ButtonType(Enum):
    PULSE = 1
    TOGGLE = 2

class ButtonState(Enum):
    IDLE = 1
    HOVER = 2
    PRESSED = 3


class UIElement:
    """Clase que guarda metodos estaticos y genericos para todos los objetos UI"""
    
    def __init__(self):
        self.__screen = None

    @property
    def _screen(self):
       return self.__screen #Debe ser seteada antes de cualquier llamada a draw()

    @_screen.setter
    def _screen(self,scn):
        self.__screen = scn

    def is_inside(self,x,y):
        if (x > self._left and 
            x < self._left + self._width):
            if (y > self._top and 
                y < self._top + self._height):
                    return True
        return False

class Component(UIElement):
    """Los componentes son secciones de la pantalla de juego"""
    def __init__(self, **kwargs):
        self._active = True  # Un objeto inactivo 
                             # no ejecuta su update()
        return super().__init__(**kwargs)
    

class Button(UIElement):
    """Boton basico para usar en objetos de UI mayores
    Permite definir sus dimensiones y una imagen para mostrar."""
    
    # Variables de clase que deben ser seteadas 
    # durante inicializacion de UI
    _hoverColor = None
    _pressedColor = None
    _frameWidth = None
    _holdTime = None

    def __init__(self, dims, image, frame, buttonType):
        self._width = dims[0]
        self._height = dims[1]
        self._left = dims[2]        
        self._top = dims[3]


        self._image = image         # Imagen de fondo del boton.
        self._frame = frame         # Lista con las 4 esquinas, 
                                    # compensada por _frameWidth. 
        self._pressedTime = None

        self._type = buttonType
        self._state = ButtonState.IDLE
        self._action = False
        return None

    def update(self):
        """Método llamado sincronicamente (cada frame de juego) 
        por el contenedor al cual pertenece este Button
        para actualizar el estado visual del Button"""
        
        if self._state == ButtonState.PRESSED:
            elapsedTime = time.time() - self._pressedTime
            if elapsedTime < self._holdTime:
                return
        (x,y) = pygame.mouse.get_pos()
        if self.is_inside(x,y):
            self._state = ButtonState.HOVER
        else: 
            if self._type == ButtonType.PULSE:
                self._state = ButtonState.IDLE

    def draw(self):
        """Método llamado sincronicamente por el contenedor 
        para dibujar el estado visual en la pantalla"""
        
        self._screen.blit(self._image,(self._left, self._top))
        if self._state == ButtonState.HOVER:
            pygame.draw.polygon(self._screen,self._hoverColor,
                self._frame,self._frameWidth)
        if self._state == ButtonState.PRESSED:
            pygame.draw.polygon(self._screen,self._pressedColor,
                        self._frame,self._frameWidth)

    def update_by_event(self,mouseEvent):
        """Método llamado por el contenedor solo cuando 
        hay un evento MOUSEBUTTONDOWN dentro de los bordes de 
        este Button"""
        if (mouseEvent.type == pygame.MOUSEBUTTONDOWN 
            and self.is_inside(mouseEvent.pos[0], mouseEvent.pos[1])):
            #Comprobación redundante pues este metodo debiera ser 
            #llamado solo cuando le llega un MOUSEBUTTONDOWN al 
            #Component padre en las coordenadas del boton.

            if self._type == ButtonType.PULSE:
                self._state = ButtonState.PRESSED
                self._pressedTime = time.time()
                self._action = True
            else:
                if self._state == ButtonState.PRESSED:
                    self._state = ButtonState.IDLE
                    self._action = False
                if self._state == ButtonState.IDLE:
                    self._state = ButtonState.PRESSED
                    self._action = True

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

