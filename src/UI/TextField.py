from pygame.transform import scale
from UIElement import UIElement
import os


class TextField(UIElement):
    """Muestra parte de un archivo de texto, con ajuste de linea. """

    xMargin = None
    yMargin = None


    def __init__(self, textFieldParams):
        
        super().__init__(textFieldParams.dims)
        
        #Parse arguments
        self._originalFile = textFieldParams.someFile
        self._font = textFieldParams.font
        self._background = scale(
            textFieldParams.background,
            (self._width,self._height))
        self._textColor = textFieldParams.textColor
        
        self._maxCharactersPerLine = self._calculate_max_characters()
        self._linesToRender = self._calculate_lines_to_render()
        self._lastKnownFileLength = 0

        self._lines = []
        self._translate_file_lines()

        self._linePosition = 0
        self._movedLines = 0
        self._currentSurfaces = []
        for line in self._lines[0:self._linesToRender]:
            self._currentSurfaces.append(self._font.render(
                line.strip(), True, self._textColor))

    def at_start(self):
        if self._linePosition <= 0:
            return True
        else:
            return False

    def at_end(self):
        if self._linePosition + self._linesToRender >= len(self._lines):
            return True
        else:
            return False

    def _calculate_max_characters(self):
        metric = self._font.metrics('W')
        return (self._width - 2 *self.xMargin) // metric[0][4]

    def _calculate_lines_to_render(self):
        yAdvance = self._font.get_height()
        return (self._height - 2 *self.yMargin) // yAdvance

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
                    newLines.append(rawLine[(self._maxCharactersPerLine * i) : 
                        (self._maxCharactersPerLine * (i+1))])
                newLines.append(rawLine[(self._maxCharactersPerLine * (i+1)) :])
            else:
                newLines.append(rawLine)

        #Anexar nuevas lineas a listado general
        self._lines.extend(newLines)
        return len(newLines)

    def textPercent(self):
        return self._linePosition / (len(self._lines) - self._linesToRender)

    def moveDown(self, move = 1):
        if not self.at_end():
            for i in range(move):
                self._currentSurfaces.pop(0)
                self._currentSurfaces.append(
                    self._font.render(self._lines[self._linePosition + self._linesToRender + i], 
                                    True, 
                                    self._textColor))
            self._linePosition += move
        else:
            return -1

    def moveUp(self, move = 1):
        if not self.at_start():
            for i in range(move):
                self._currentSurfaces.pop()
                self._currentSurfaces.insert(0,
                        self._font.render(self._lines[self._linePosition - (i+1)], 
                                        True, 
                                        self._textColor))
            self._linePosition -= move
        else:
            return -1

    def update(self):
        """
        TextField se actualiza a si mismo 
        si es que hay cambios en la cantidad de lineas.
        """
        oFilePosition = self._originalFile.tell()
        oFileLength = self._originalFile.seek(0,os.SEEK_END)
        self._originalFile.seek(oFilePosition)

        if oFileLength > self._lastKnownFileLength:
            self.moveDown(self._translate_file_lines())

    def draw(self):
        self.screen.blit(self._background, (self._left, self._top))
        lineHeight = self._font.get_height()
        for idx,someLine in enumerate(self._currentSurfaces):
            self.screen.blit(someLine, (self._left + self.xMargin,
                             self._top + idx * lineHeight + self.yMargin))

    def update_by_event(self,mouseEv):
        pass

class TextFieldParams:
    def __init__(self,
                 dims,
                 someFile,
                 font,
                 background,
                 textColor):
        self.dims = dims
        self.someFile = someFile
        self.font = font
        self.background = background
        self.textColor = textColor
