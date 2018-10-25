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

    # Setear variables de clase Button, usada por ScrollBar
    ui.Button._hoverColor = (0,0,200)
    ui.Button._pressedColor = (200, 0, 0)
    ui.Button._frameWidth = 5
    ui.Button._holdTime = 0.2

    # Crear variables para init de Log
    refX = 100
    refY = 300
    width = 150
    height = 200
    dims = (width,height,refX,refY)

    filePath = pathlib.Path.cwd() / "Tests" / "textForTestingTextField.txt"
    backPath = pathlib.Path.cwd() / "Assets" / "scrollBack.png"

    someFile = open(filePath,'r+')
    barSize = 20
    #Variables para sub-item TextField
    tfDims = (0,0,0,0) 
    pygame.font.init()
    someFont = pygame.font.SysFont('Courier New',12)
    linesToRender = 9
    backImage = ui.pygame.image.load(wpath(backPath))
    textColor = pygame.Color(255,255,255,255)
    
    textFieldParams = ui.TextFieldParams(tfDims, None, linesToRender,
                                someFont, backImage, textColor)

    #Variables para sub-item ScrollBar
    sbDims = (0,0,0,0)
    buttonPath = pathlib.Path.cwd() / "Assets" / "scrollButton.png"
    barPath = pathlib.Path.cwd() / "Assets" / "scrollBar.png"
    buttonImage = ui.pygame.image.load(wpath(buttonPath))
    barImage = ui.pygame.image.load(wpath(barPath))

    barHeight = 10

    scrollBarParams = ui.ScrollBarParams(sbDims, backImage, barImage, barHeight, buttonImage)

    logParams = ui.LogParams(dims,someFile,barSize,textFieldParams,scrollBarParams)
    log = ui.Log(logParams)
    return log

standalone = True
if(standalone):
    # Crear screen para los objetos UI
    # pylint: disable=E1101
    ui.pygame.init()
    ui.pygame.event.set_blocked([ui.pygame.MOUSEMOTION, ui.pygame.ACTIVEEVENT])
    size = 800, 600
    screen = ui.pygame.display.set_mode(size)
    ui.UIElement._screen = screen

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

        keyevents = ui.pygame.event.get(ui.pygame.KEYDOWN)
        if(keyevents):
            if keyevents[-1].key == ui.pygame.K_ESCAPE:
                endApp = True

        log.update()
        events = ui.pygame.event.get(ui.pygame.MOUSEBUTTONDOWN)
        if(events):
            mouseEv = events[-1]
            if log.has_inside(mouseEv.pos[0],mouseEv.pos[1]):
                log.update_by_event(mouseEv)
        
        screen.fill((0,0,0))
        log.draw()
        ui.pygame.display.flip()
        time.sleep(0.020)
    
    someFile.close()
