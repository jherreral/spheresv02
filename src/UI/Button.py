from UIElement import UIElement
import time
from enum import Enum
import pygame

class ButtonType(Enum):
    PULSE = 1
    TOGGLE = 2

class ButtonState(Enum):
    IDLE = 1
    HOVER = 2
    PRESSED = 3

class Button(UIElement):
    """Boton basico para usar en objetos de UI mayores
    Permite definir sus dimensiones y una imagen para mostrar."""
    
    # Variables de clase que deben ser seteadas 
    # durante inicializacion de UI

    hoverColor = None
    pressedColor = None
    frameWidth = None
    holdTime = None

    @classmethod
    def frame_creator(cls,dims):
        f2 = cls.frameWidth/2
        return list([(dims[2] + f2, dims[3] + f2),
                 (dims[2] + dims[0] - f2, dims[3] + f2),
                 (dims[2] + dims[0] - f2, dims[3] + dims[1] - f2),
                 (dims[2] + f2, dims[3] + dims[1] - f2)])

    def __init__(self, buttonParams):
        super().__init__(buttonParams.dims)

        # Imagen de fondo del boton.
        self._image = buttonParams.image
        
        # Lista con las 4 esquinas, compensada por _frameWidth.
        self._frame = buttonParams.frame

        # Nombre para manejo en listas
        self.id = buttonParams.id

        # Variable que guarda instante en que se hace click en el boton.          
        self._pressedTime = None    

        self._type = buttonParams.buttonType
        self._state = ButtonState.IDLE
        
        # Prendida por click asincrono, apagada por el padre 
        # sincronamente cuando este procesa el boton con su update
        self.action = False        
        return None

    def update(self):
        """Método llamado sincronicamente (cada frame de juego) 
        por el contenedor al cual pertenece este Button
        para actualizar el estado visual del Button"""
        
        if self._state == ButtonState.PRESSED:
            elapsedTime = time.time() - self._pressedTime
            if elapsedTime < self.holdTime:
                return
        (x,y) = pygame.mouse.get_pos()
        if self.has_inside(x,y):
            self._state = ButtonState.HOVER
        else: 
            if self._type == ButtonType.PULSE:
                self._state = ButtonState.IDLE

    def draw(self):
        """Método llamado sincronicamente por el contenedor 
        para dibujar el estado visual en la pantalla"""
        
        self.screen.blit(self._image,(self._left, self._top))
        if self._state == ButtonState.HOVER:
            pygame.draw.polygon(self.screen,self.hoverColor,
                self._frame,self.frameWidth)
        if self._state == ButtonState.PRESSED:
            pygame.draw.polygon(self.screen,self.pressedColor,
                        self._frame,self.frameWidth)

    def update_by_event(self,mouseEvent):
        """Método llamado por el contenedor solo cuando 
        hay un evento MOUSEBUTTONDOWN dentro de los bordes de 
        este Button"""
        if (mouseEvent.type == pygame.MOUSEBUTTONDOWN 
            and self.has_inside(mouseEvent.pos[0], mouseEvent.pos[1])):
            #Comprobación redundante pues este metodo debiera ser 
            #llamado solo cuando le llega un MOUSEBUTTONDOWN al 
            #Component padre en las coordenadas del boton.

            if self._type == ButtonType.PULSE:
                self._state = ButtonState.PRESSED
                self._pressedTime = time.time()
                self.action = True
            else:
                if self._state == ButtonState.PRESSED:
                    self._state = ButtonState.IDLE
                    self.action = False
                if self._state == ButtonState.IDLE:
                    self._state = ButtonState.PRESSED
                    self.action = True

class ButtonParams:
    def __init__(self, dims, image, frame, buttonType = ButtonType.PULSE, id = None):
        self.dims = dims
        self.image = image
        self.frame = frame
        self.buttonType = buttonType
        self.id = id
