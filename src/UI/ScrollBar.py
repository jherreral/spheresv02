from UIElement import UIElement
from Button import Button,ButtonParams
import pygame

class ScrollBar(UIElement):
    """Barra de desplazamiento en menus. 
    Contiene 2 Button y la barra arrastrable"""

    #TODO:Dejar _width como variable de clase, no de instancia.
    #     Seteada durante inicialización.
    #TODO:Hacer barra desplazable.

    def __init__(self, scrollBarParams):
        super().__init__(scrollBarParams.dims)

        self._backImage = pygame.transform.scale(scrollBarParams.backImage,
                            (self._width, self._height - 2*self._width))
        self._barHeight = scrollBarParams.barHeight
        self._barImage = pygame.transform.scale(scrollBarParams.barImage,
                            (self._width, self._barHeight))
        self._barLocalTop = self._width

        topButtonParams = ButtonParams(
            (self._width,self._width,self._left,self._top),
            scrollBarParams.buttonImage,
            Button.frame_creator((self._width,
                          self._width,
                          self._left,
                          self._top)))

        bottomButtonParams = ButtonParams(
            (self._width,
            self._width,
            self._left,
            self._top + self._height - self._width),
            pygame.transform.flip(scrollBarParams.buttonImage,False,True),
            Button.frame_creator((self._width,
                          self._width,
                          self._left,
                          self._top + self._height - self._width)))

        self._topButton = Button(topButtonParams)
        self._bottomButton = Button(bottomButtonParams)
            
        self.actionUp = False
        self.actionDown = False

    def setBarPosition(self,percent):
        """Llamado asincronamente por el contenedor para setear 
        la posición de la barra.
        """
        self._barLocalTop = int(percent * 
                            (self._height - 2*self._width - self._barHeight) 
                            + self._width)

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

            # Si hay action, desplazar hacia arriba o hacia abajo
            if self._topButton.action:
                self.actionUp = True
            if self._bottomButton.action:
                self.actionDown = True     

    def update(self):
        """Método llamado sincronicamente (cada frame de juego) 
        por el contenedor al cual pertenece este ScrollBar
        para actualizar el estado visual e interno del ScrollBar"""
        self._topButton.update()
        self._bottomButton.update()
        self._topButton.action = False
        self._bottomButton.action = False

        if self._barLocalTop < self._width:
            self._barLocalTop = self._width

        if self._barLocalTop > self._height - self._width - self._barHeight:
            self._barLocalTop = self._height - self._width - self._barHeight

    def draw(self):
        self._topButton.draw()
        self._bottomButton.draw()
        self.screen.blit(self._backImage,
                          (self._left,self._top + self._width))
        self.screen.blit(self._barImage,
                          (self._left,self._top + self._barLocalTop))

class ScrollBarParams:
    def __init__(self,
                 dims,
                 backImage,
                 barImage,
                 barHeight,
                 buttonImage):
        self.dims = dims
        self.backImage = backImage
        self.barImage = barImage
        self.barHeight = barHeight
        self.buttonImage = buttonImage
