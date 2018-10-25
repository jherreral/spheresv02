import time
import pathlib
import pygame
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import ui
sys.path.remove(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


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
    ui.TextField._xMargin = 5
    ui.TextField._yMargin = 5

    # Crear variables para init de TextField
    refX = 400
    refY = 200
    width = 150
    height = 200
    dims = (width,height,refX,refY)

    pygame.font.init()
    someFont = pygame.font.SysFont('Courier New',12)
    
    filePath = pathlib.Path.cwd() / "Tests" / "textForTestingTextField.txt"
    backPath = pathlib.Path.cwd() / "Assets" / "scrollBack.png"

    someFile = open(filePath,'r+')
    linesToRender = 11
    backImage = ui.pygame.image.load(wpath(backPath))
    textColor = pygame.Color(255,255,255,255)

    
    params = ui.TextFieldParams(dims, someFile, linesToRender,
                                someFont, backImage, textColor)
    textFieldA = ui.TextField(params)
    return textFieldA

standalone = True
if(standalone):
    # Crear screen para los objetos UI
    # pylint: disable=E1101
    ui.pygame.init()
    ui.pygame.event.set_blocked([ui.pygame.MOUSEMOTION, ui.pygame.ACTIVEEVENT])
    size = 800, 600
    screen = ui.pygame.display.set_mode(size)
    ui.UIElement._screen = screen

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

        keyevents = ui.pygame.event.get(ui.pygame.KEYDOWN)
        if(keyevents):
            if keyevents[-1].key == ui.pygame.K_ESCAPE:
                endApp = True

        textFieldA.update()
        events = ui.pygame.event.get(ui.pygame.MOUSEBUTTONDOWN)
        if(events):
            mouseEv = events[-1]
            if textFieldA.has_inside(mouseEv.pos[0],mouseEv.pos[1]):
                textFieldA.update_by_event(mouseEv)
        
        screen.fill((0,0,0))
        textFieldA.draw()
        ui.pygame.display.flip()
        time.sleep(0.020)
    
    someFile.close()
