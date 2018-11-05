import time
import pathlib
import pygame
import sys
import os.path

temporalPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "UI"))
sys.path.append(temporalPath)
from TextField import TextField, TextFieldParams
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

    # Crear variables para init de TextField
    refX = 400
    refY = 200
    width = 150
    height = 200
    dims = (width,height,refX,refY)

    pygame.font.init()
    someFont = pygame.font.SysFont('Courier New',12)
    
    filePath = pathlib.Path.cwd() / "src" / "Tests" / "textForTestingTextField.txt"
    backPath = pathlib.Path.cwd() / "Assets" / "scrollBack.png"

    someFile = open(filePath,'r+')
    backImage = pygame.image.load(wpath(backPath))
    textColor = pygame.Color(255,255,255,255)

    
    params = TextFieldParams(dims, someFile,
                                someFont, backImage, textColor)
    textFieldA = TextField(params)
    return textFieldA

standalone = True
if(standalone):
    # Crear screen para los objetos UI
    # pylint: disable=E1101
    pygame.init()
    pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.ACTIVEEVENT])
    size = 800, 600
    screen = pygame.display.set_mode(size)
    UIElement.screen = screen

    textFieldA = set_parameters_and_create()
    someFile = textFieldA._originalFile
    timeStart = time.time()
    
    endApp = False
    while(not endApp):
        if timeStart + 3 < time.time():
            currentPosition = someFile.tell()
            someFile.seek(0,os.SEEK_END)
            someFile.write("Appending  longerlongerline\n")
            someFile.seek(currentPosition)
            timeStart = time.time()

        keyevents = pygame.event.get(pygame.KEYDOWN)
        if(keyevents):
            if keyevents[-1].key == pygame.K_ESCAPE:
                endApp = True

        textFieldA.update()
        events = pygame.event.get(pygame.MOUSEBUTTONDOWN)
        if(events):
            mouseEv = events[-1]
            if textFieldA.has_inside(mouseEv.pos[0],mouseEv.pos[1]):
                textFieldA.update_by_event(mouseEv)
        
        screen.fill((0,0,0))
        textFieldA.draw()
        pygame.display.flip()
        time.sleep(0.020)
    
    someFile.close()
