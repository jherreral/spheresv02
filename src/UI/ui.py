import queue
import pygame
import time
import sys,os
import pathlib

localPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir,"UI"))
sys.path.append(localPath)

import UIElement
import Log
import TextField
import ScrollBar
import Button
import Track

class CardBank:
    def __init__(self):
        self._cardMap = {}
        cardFolderPath = pathlib.Path.cwd() / "Assets" / "Cards"
        pass

    def getCard(self,cardId):
        pass

class Resources:
    def __init__(self):
        self.cardBank = None
        self.backgrounds = None
        self.strings = None
        self.colors = None
        self.fonts = None

    @staticmethod
    def wpath(path):
        result = ""
        for idx,part in enumerate(path.parts):
            if idx == 0:
                result = part
            else:
                result += "\\" + part
        return result

    def test_load(self):
        backPath = pathlib.Path.cwd() / "Assets" / "scrollBack.png"
        backImage = pygame.image.load(self.wpath(backPath))
        barPath = pathlib.Path.cwd() / "Assets" / "scrollBar.png"
        barImage = pygame.image.load(self.wpath(barPath))
        buttonPath = pathlib.Path.cwd() / "Assets" / "scrollButton.png"
        buttonImage = pygame.image.load(self.wpath(buttonPath))
        self.backgrounds = {'Track':backImage,
                            'Log':backImage,
                            'ScrollBar':barImage,
                            'ScrollButton':buttonImage}
        

        pygame.font.init()
        font1 = pygame.font.SysFont('Courier New',12)
        font2 = pygame.font.SysFont('Courier New',24)
        self.fonts = {'Track':font1,
                      'Log':font1,
                      'Button':font2}

class Config:
    def __init__(self):
        #Color para texto de Track
        self.colorCode = None
        self.trackDims = None
        self.logDims = None
        self.barSize = None
        self.barHeight = None
        self.textColor = None

    def test_load(self):
        self.colorCode = [(255,0,0),
                 (255,255,0),
                 (128,128,0),
                 (0,0,255),
                 (0,255,0),
                 (255,255,200)]
        self.trackDims = (150,70,650,250)
        self.logDims = (150,200,650,50)
        self.barSize = 20
        self.barHeight = 10
        self.textColor = pygame.Color(255,255,255,255)

class GameboardData:
    def __init__(self):
        self.logFile = None
        self.trackData = None
        self.deckData = None
        self.playersData = None
        self.mapData = None

    def test_load(self):

        #Datos para Log
        filePath = pathlib.Path.cwd() / "src" / "Tests" / "textForTestingTextField.txt"
        self.logFile = open(filePath,'r+')

        #Datos para Track
        self.trackData = [[1,2,3,4,2,1],[2,4,6,8,1,3],[9,7,5,3,2,1],[6,5,2,1,2,2]]
    

class UI:
    """Clase principal de User Interface, 
    encargada de procesar peticiones para el usuario, 
    la entrada del usuario y dibujar en pantalla"""

    def __init__(self, q):

        pygame.init()
        pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.ACTIVEEVENT])
        size = 800, 600
        self._screen = pygame.display.set_mode(size)
        UIElement.UIElement.screen = self._screen

        self._exitUI = False
        self._queue = q
        self.resources = Resources()
        self.gameboardData = GameboardData()
        self.configuration = Config()

        self.resources.test_load()
        self.gameboardData.test_load()
        self.configuration.test_load()

        self._set_class_params()

        self.objectTree = []
        self._create_objects()


    def main(self):
        while(not self._exitUI):
            self.get_requests()
            self.get_user_input()
            self.update()
            self.draw()
        self.exit_UI()
        return 0

    def get_requests(self):
        while(not self._queue.empty()):
            Request = self._queue.get()
            return Request

    def _set_class_params(self):
        #Setear variables de clase Track
        Track.Track.xMargin = 0
        Track.Track.yMargin = 0
        Track.Track.xOffset = 16
        Track.Track.yOffset = 0

        # Setear variables de clase TextField
        TextField.TextField.xMargin = 5
        TextField.TextField.yMargin = 5

        # Setear variables de clase Button, usada por ScrollBar
        Button.Button.hoverColor = (0,0,200)
        Button.Button.pressedColor = (200, 0, 0)
        Button.Button.frameWidth = 5
        Button.Button.holdTime = 0.2

    def _create_objects(self):
        #Log
        logParams = Log.LogParams(
                    self.configuration.logDims,
                    self.gameboardData.logFile,
                    self.configuration.barSize,
                    TextField.TextFieldParams(
                        None,
                        None,
                        self.resources.fonts['Log'],
                        self.resources.backgrounds['Log'],
                        self.configuration.textColor),
                    ScrollBar.ScrollBarParams(
                        None,
                        self.resources.backgrounds['Log'],
                        self.resources.backgrounds['ScrollBar'],
                        self.configuration.barHeight,
                        self.resources.backgrounds['ScrollButton'])
                    )
        self.objectTree.append(Log.Log(logParams))

        #Track
        trackParams = Track.TrackParams(
                    self.configuration.trackDims,
                    self.gameboardData.trackData,
                    self.configuration.colorCode,
                    self.resources.backgrounds['Track'],
                    self.resources.fonts['Track']
                    )

        self.objectTree.append(Track.Track(trackParams))

    def get_user_input(self):
        keyevents = pygame.event.get(pygame.KEYDOWN)
        if(keyevents):
            if keyevents[-1].key == pygame.K_ESCAPE:
                self._exitUI = True

        events = pygame.event.get(pygame.MOUSEBUTTONDOWN)
        if(events):
            mouseEv = events[-1]
            for someObject in self.objectTree:
                if someObject.has_inside(mouseEv.pos[0],mouseEv.pos[1]):
                    someObject.update_by_event(mouseEv)

    def update(self):
        for someObject in self.objectTree:
            someObject.update()

    def draw(self):
        self._screen.fill((0,0,0))
        for someObject in self.objectTree:
            someObject.draw()
        pygame.display.flip()
        time.sleep(0.020)

    def exit_UI(self):
        pass


