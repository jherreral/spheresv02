import time
import pathlib
import pygame
import sys
import os.path

temporalPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "UI"))
sys.path.append(temporalPath)
from Button import Button
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
    # Setear variables de clase Button, usada por ScrollBar
    Button.hoverColor = (0,0,200)
    Button.pressedColor = (200, 0, 0)
    Button.frameWidth = 5
    Button.holdTime = 0.2

    # Crear variables para init de ScrollBar
    refX = 300
    refY = 200
    buttonPath = pathlib.Path.cwd() / "Assets" / "scrollButton.png"
    barPath = pathlib.Path.cwd() / "Assets" / "scrollBar.png"
    backPath = pathlib.Path.cwd() / "Assets" / "scrollBack.png"

    buttonImage = pygame.image.load(wpath(buttonPath))
    barImage = pygame.image.load(wpath(barPath))
    backImage = pygame.image.load(wpath(backPath))

    width = 20
    height = 150
    barHeight = 10
    dims = (width,height,refX,refY)

    params = ScrollBarParams(dims, backImage, barImage, barHeight, buttonImage)
    scrollBarA = ScrollBar(params)
    return scrollBarA

standalone = True
if(standalone):
    # Crear screen para los objetos UI
    # pylint: disable=E1101
    pygame.init()
    pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.ACTIVEEVENT])
    size = 800, 600
    screen = pygame.display.set_mode(size)
    UIElement.screen = screen

    scrollBarA = set_parameters_and_create()

    maxPosition = 18
    currentPosition = 0

    while(1):
        events = pygame.event.get(pygame.MOUSEBUTTONDOWN)
        if(events):
            mouseEv = events[-1]
            if scrollBarA.has_inside(mouseEv.pos[0],mouseEv.pos[1]):
                scrollBarA.update_by_event(mouseEv)
        
        if scrollBarA.actionDown and currentPosition < maxPosition:
            currentPosition += 1
            scrollBarA.setBarPosition(currentPosition/maxPosition)

        if scrollBarA.actionUp and currentPosition > 0:
            currentPosition -= 1
            scrollBarA.setBarPosition(currentPosition/maxPosition)
 
        scrollBarA.update()
        scrollBarA.actionDown = False
        scrollBarA.actionUp = False
        
        screen.fill((0,0,0))
        scrollBarA.draw()
        pygame.display.flip()
        time.sleep(0.020)
