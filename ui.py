import queue
import pygame
import time
import os
from enum import Enum

def frame_creator(dims):
    return list([(dims[2], dims[3]),
                 (dims[2] + dims[0], dims[3]),
                 (dims[2] + dims[0], dims[3]+dims[1]),
                 (dims[2], dims[3]+dims[1])])


class ButtonType(Enum):
    PULSE = 1
    TOGGLE = 2

class ButtonState(Enum):
    IDLE = 1
    HOVER = 2
    PRESSED = 3

class UIElement:
    """Clase que guarda metodos estaticos y genericos para todos los objetos UI"""
    
    def __init__(self, dims):
        self.__screen = None
        self._width = dims[0]
        self._height = dims[1]
        self._left = dims[2]        
        self._top = dims[3]

    @property
    def _screen(self):
       return self.__screen #Debe ser seteada antes de cualquier llamada a draw()

    @_screen.setter
    def _screen(self,scn):
        self.__screen = scn

    def has_inside(self,x,y):
        if (x > self._left and 
            x < self._left + self._width):
            if (y > self._top and 
                y < self._top + self._height):
                    return True
        return False

class Component(UIElement):
    """Los componentes son secciones de la pantalla de juego"""
    def __init__(self, **kwargs):

        # Un componente inactivo no ejecuta su update()
        self._active = True   
                             
        super().__init__(**kwargs)
    

class Button(UIElement):
    """Boton basico para usar en objetos de UI mayores
    Permite definir sus dimensiones y una imagen para mostrar."""
    
    # Variables de clase que deben ser seteadas 
    # durante inicializacion de UI
    _hoverColor = None
    _pressedColor = None
    _frameWidth = None
    _holdTime = None

    @classmethod
    def frame_creator(cls,dims):
        f2 = cls._frameWidth/2
        return list([(dims[2] + f2, dims[3] + f2),
                 (dims[2] + dims[0] - f2, dims[3] + f2),
                 (dims[2] + dims[0] - f2, dims[3] + dims[1] - f2),
                 (dims[2] + f2, dims[3] + dims[1] - f2)])

    def __init__(self, dims, image, frame, buttonType = ButtonType.PULSE):
        super().__init__(dims)

        # Imagen de fondo del boton.
        self._image = image
        
        # Lista con las 4 esquinas, compensada por _frameWidth.
        self._frame = frame

        # Variable que guarda instante en que se hace click en el boton.          
        self._pressedTime = None    

        self._type = buttonType
        self._state = ButtonState.IDLE
        
        # Prendida por click asincrono, apagada por el padre 
        # sincronamente cuando este procesa el boton con su update
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
        if self.has_inside(x,y):
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
            and self.has_inside(mouseEvent.pos[0], mouseEvent.pos[1])):
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

class ScrollBar(UIElement):
    """Barra de desplazamiento en menus. 
    Contiene 2 Button y la barra arrastrable"""

    #TODO:Dejar _width como variable de clase, no de instancia.
    #     Seteada durante inicialización.
    #TODO:Hacer barra desplazable.

    def __init__(self,
                 dims,
                 backImage,
                 barImage,
                 barHeight,
                 barDisplacement,
                 buttonImage):
        super().__init__(dims)

        self._backImage = pygame.transform.scale(backImage,
                            (self._width, self._height - 2*self._width))
        self._barHeight = barHeight
        self._barImage = pygame.transform.scale(barImage,
                            (self._width, self._barHeight))
        self._barLocalTop = self._width
        self._barDisplacement = barDisplacement
        self._topButton = Button(
            (self._width,self._width,self._left,self._top),
            buttonImage,
            Button.frame_creator((self._width,
                          self._width,
                          self._left,
                          self._top)))
        self._bottomButton = Button(
            (self._width,
            self._width,
            self._left,
            self._top + self._height - self._width),
            pygame.transform.flip(buttonImage,False,True),
            Button.frame_creator((self._width,
                          self._width,
                          self._left,
                          self._top + self._height - self._width)))

    def update_by_event(self,mouseEvent):
        """Método llamado por el contenedor solo cuando 
        hay un evento MOUSEBUTTONDOWN dentro de los bordes de 
        este ScrollBar"""
        if (mouseEvent.type == pygame.MOUSEBUTTONDOWN 
            and self.has_inside(mouseEvent.pos[0], mouseEvent.pos[1])):
            #Comprobación redundante pues este metodo debiera ser 
            #llamado solo cuando le llega un MOUSEBUTTONDOWN al 
            #Component padre en las coordenadas del scrollbar.

            if self._bottomButton.has_inside(mouseEvent.pos[0],
                                            mouseEvent.pos[1]):
                self._bottomButton.update_by_event(mouseEvent)

            if self._topButton.has_inside(mouseEvent.pos[0],
                                         mouseEvent.pos[1]):
                self._topButton.update_by_event(mouseEvent)

    def update(self):
        """Método llamado sincronicamente (cada frame de juego) 
        por el contenedor al cual pertenece este ScrollBar
        para actualizar el estado visual e interno del ScrollBar"""
        self._topButton.update()
        self._bottomButton.update()

        if self._topButton._action:
            self._barLocalTop -= self._barDisplacement
            if self._barLocalTop < self._width:
                self._barLocalTop = self._width
            self._topButton._action = False

        if self._bottomButton._action:
            self._barLocalTop += self._barDisplacement
            if self._barLocalTop > self._height - self._width - self._barHeight:
                self._barLocalTop = self._height - self._width - self._barHeight
            self._bottomButton._action = False

    def draw(self):
        self._topButton.draw()
        self._bottomButton.draw()
        self._screen.blit(self._backImage,
                          (self._left,self._top + self._width))
        self._screen.blit(self._barImage,
                          (self._left,self._top + self._barLocalTop))

class Label(UIElement):
    """Objeto de texto simple, con una sola linea"""

    def __init__(self,dims,text,font,background=None):
        super().__init__(dims)
        self._text = text
        self._font = font
        self._background = background
        self._surface = font.render(self._text, True, (255,255,255), self._background)

    def draw(self):
        self._screen.blit(self._surface,(self._left,self._top))

    def set_text(self,text):
        self._text = text

class TextField(UIElement):
    """Muestra parte de un archivo de texto, con ajuste de linea. """

    _xMargin = None

    def __init__(self,
                 dims,
                 someFile,
                 linesToRender,
                 font,
                 background,
                 textColor):
        super().__init__(dims)
        
        #Parse arguments
        self._originalFile = someFile
        self._linesToRender = linesToRender
        self._font = font
        self._background = pygame.transform.scale(
            background,
            (self._width,self._height))
        self._textColor = textColor
        
        self._maxCharactersPerLine = self._calculate_max_characters()
        self._lastKnownFileLength = 0

        self._lines = []
        self._translate_file_lines()

        self._linePosition = 0
        self._movedLines = 0
        self._currentSurfaces = []
        for line in self._lines[0:(self._linesToRender-1)]:
            self._currentSurfaces.append(self._font.render(
                line.strip(), True, self._textColor))

    def _calculate_max_characters(self):
        metric = self._font.metrics('W')
        return (self._width - 2 *self._xMargin) // metric[0][4]

    def _translate_file_lines(self):
        '''Lee el archivo original o su diferencia, procesa las 
        lineas nuevas y las guarda en la lista de lineas de la instancia.
        '''
        #Leer nuevas lineas y ajustar contador hasta nuevo final de archivo
        self._originalFile.seek(self._lastKnownFileLength)
        rawNewLines = list(self._originalFile)
        self._lastKnownFileLength = self._originalFile.tell()

        #Cortar lineas y agregarlas a lista previa
        newLines = []
        for rawLine in rawNewLines:
            rawLine = rawLine.strip()
            nOfDivisions = len(rawLine)//self._maxCharactersPerLine
            if nOfDivisions > 0:
                for i in range(nOfDivisions):
                    newLines.append(rawLine[(self._maxCharactersPerLine * i) : (self._maxCharactersPerLine * (i+1) - 1)])
                newLines.append(rawLine[(self._maxCharactersPerLine * (i+1)) :])
            else:
                newLines.append(rawLine)

        #Anexar nuevas lineas a listado general y correr lineas en pantalla
        self._lines.extend(newLines)
        #self._movedLines += len(newLines)


    def update(self):
        if self._movedLines != 0:
            for i in range(abs(self._movedLines)):
                if self._movedLines < 0:
                    self._currentSurfaces.pop(0)
                    self._currentSurfaces.insert(0,
                        self._font.render(self._lines[self._linePosition - (i+1)], 
                                        True, 
                                        self._textColor))
                else:
                    self._currentSurfaces.pop()
                    self._currentSurfaces.append(
                        self._font.render(self._lines[self._linePosition + self._linesToRender + i], 
                                        True, 
                                        self._textColor))
            self._linePosition += self._movedLines
            self._movedLines = 0


    def draw(self):
        self._screen.blit(self._background, (self._left, self._top))
        lineHeight = self._font.get_height()
        for idx,someLine in enumerate(self._currentSurfaces):
            self._screen.blit(someLine, (self._left + self._xMargin,
                             self._top + idx * lineHeight))

    def update_by_event(self,mouseEv):
        pass


class UI:
    """Clase principal de User Interface, 
    encargada de procesar peticiones para el usuario, 
    la entrada del usuario y dibujar en pantalla"""

    def __init__(self, q):
        self._queue = q

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

