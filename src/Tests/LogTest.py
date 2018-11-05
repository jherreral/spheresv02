import time
import pathlib
import pygame
import sys
import os.path

temporalPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "UI"))
sys.path.append(temporalPath)
from Log import Log,LogParams
from Button import Button
from TextField import TextField,TextFieldParams
from ScrollBar import ScrollBar,ScrollBarParams
from UIElement import UIElement
sys.path.remove(temporalPath)


def wpath(path):
    result = ""
    for idx,part in enumerate(path.parts):
        if idx == 0:
            result = part
        else:
            result += "\\" + part
    return result

def set_parameters_and_create():

    # Setear variables de clase TextField
    TextField.xMargin = 5
    TextField.yMargin = 5

    # Setear variables de clase Button, usada por ScrollBar
    Button.hoverColor = (0,0,200)
    Button.pressedColor = (200, 0, 0)
    Button.frameWidth = 5
    Button.holdTime = 0.2

    # Crear variables para init de Log
    refX = 100
    refY = 300
    width = 150
    height = 200
    dims = (width,height,refX,refY)

    filePath = pathlib.Path.cwd() / "src" / "Tests" / "textForTestingTextField.txt"
    backPath = pathlib.Path.cwd() / "Assets" / "scrollBack.png"

    someFile = open(filePath,'r+')
    barSize = 20
    #Variables para sub-item TextField
    pygame.font.init()
    someFont = pygame.font.SysFont('Courier New',12)
    backImage = pygame.image.load(wpath(backPath))
    textColor = pygame.Color(255,255,255,255)
    
    textFieldParams = TextFieldParams(None, None,
                                someFont, backImage, textColor)

    #Variables para sub-item ScrollBar
    buttonPath = pathlib.Path.cwd() / "Assets" / "scrollButton.png"
    barPath = pathlib.Path.cwd() / "Assets" / "scrollBar.png"
    buttonImage = pygame.image.load(wpath(buttonPath))
    barImage = pygame.image.load(wpath(barPath))

    barHeight = 10

    scrollBarParams = ScrollBarParams(None, backImage, barImage, barHeight, buttonImage)

    logParams = LogParams(dims,someFile,barSize,textFieldParams,scrollBarParams)
    log = Log(logParams)
    return log

standalone = True
if(standalone):
    # Crear screen para los objetos UI
    # pylint: disable=E1101
    pygame.init()
    pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.ACTIVEEVENT])
    size = 800, 600
    screen = pygame.display.set_mode(size)
    UIElement.screen = screen

    log = set_parameters_and_create()
    someFile = log._logFile
    timeStart = time.time()
    
    endApp = False

    while(not endApp):
        if timeStart + 5 < time.time():
            currentPosition = someFile.tell()
            someFile.seek(0,os.SEEK_END)
            someFile.write("Appending longerlongerline\n")
            someFile.seek(currentPosition)
            timeStart = time.time()

        keyevents = pygame.event.get(pygame.KEYDOWN)
        if(keyevents):
            if keyevents[-1].key == pygame.K_ESCAPE:
                endApp = True

        log.update()
        events = pygame.event.get(pygame.MOUSEBUTTONDOWN)
        if(events):
            mouseEv = events[-1]
            if log.has_inside(mouseEv.pos[0],mouseEv.pos[1]):
                log.update_by_event(mouseEv)
        
        screen.fill((0,0,0))
        log.draw()
        pygame.display.flip()
        time.sleep(0.020)
    
    someFile.close()
