from Component import Component
from TextField import TextField,TextFieldParams
from ScrollBar import ScrollBar,ScrollBarParams
import pygame


class Log(Component):
    def __init__(self, logParams):
        """
        Cada instancia de Log requiere objeto logParams con:
          dims, logFile, barSize,
          TextFieldParams con: dims, linesToRender,font,backImage,textColor
          ScrollBarParams con: dims, backImage, barImage, barHeight, buttonImage
        """
        super().__init__(logParams.dims)
        self._logFile = logParams.logFile
        self._barSize = logParams.barSize #En pixeles de ancho
        
        # Modificar ciertos parametros para el TextField, 
        # el resto debe venir de afuera.
        self._textFieldParams = logParams.textFieldParams
        self._textFieldParams.dims = (self._width - self._barSize,
                                     self._height,
                                     self._left,
                                     self._top)
        self._textFieldParams.someFile = self._logFile

        # Modificar ciertos parametros para el ScrollBar
        self._barParams = logParams.barParams
        self._barParams.dims = (self._barSize,
                               self._height,
                               self._left + self._width - self._barSize,
                               self._top)

        # Crear objetos de Log
        self._textField = TextField(self._textFieldParams)
        self._scrollBar = ScrollBar(self._barParams)

    def update(self):
        """Método llamado sincronicamente (cada frame de juego) 
        por el contenedor al cual pertenece este Log
        para actualizar el estado visual e interno del Log"""
        
        self._textField.update()
        self._scrollBar.setBarPosition(self._textField.textPercent())
        self._scrollBar.update()
        self._scrollBar.actionUp = False
        self._scrollBar.actionDown = False  

    def update_by_event(self,mouseEv):
        """Método llamado por el contenedor solo cuando 
        hay un evento MOUSEBUTTONDOWN dentro de los bordes de 
        este Log"""
        if (mouseEv.type == pygame.MOUSEBUTTONDOWN 
            and self.has_inside(mouseEv.pos[0], mouseEv.pos[1])):
            #Comprobación redundante pues este metodo debiera ser 
            #llamado solo cuando le llega un MOUSEBUTTONDOWN al 
            #Component padre.

            if self._textField.has_inside(mouseEv.pos[0],
                                            mouseEv.pos[1]):
                self._textField.update_by_event(mouseEv)

            if self._scrollBar.has_inside(mouseEv.pos[0],
                                         mouseEv.pos[1]):
                self._scrollBar.update_by_event(mouseEv)

            if self._scrollBar.actionUp:
                self._textField.moveUp()
                self._scrollBar.actionUp = False

            if self._scrollBar.actionDown:
                self._textField.moveDown()
                self._scrollBar.actionDown = False

    def draw(self):
        self._textField.draw()
        self._scrollBar.draw()

class LogParams:
    def __init__(self,dims, logFile, barSize, textFieldParams, barParams):
        self.dims = dims
        self.logFile = logFile
        self.barSize = barSize
        self.textFieldParams = textFieldParams
        self.barParams = barParams
