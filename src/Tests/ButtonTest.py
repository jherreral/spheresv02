import time
import pathlib
import pygame
import sys
import os.path

temporalPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "UI"))
sys.path.append(temporalPath)
from Button import Button,ButtonParams,ButtonType,ButtonState
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
    # Setear variables de clase Button
    Button.hoverColor = (0,0,200)
    Button.pressedColor = (200, 0, 0)
    Button.frameWidth = 5
    Button.holdTime = 0.2

    # Crear variables para init de Button
    refX = refY = 100
    path = pathlib.Path.cwd() / "Assets" / "botonA.png"
    imageA = pygame.image.load(wpath(path))

    width = 220
    height = 95
    dims = (width,height,refX,refY)
    frame = Button.frame_creator(dims)

    params = ButtonParams(dims, imageA, frame, ButtonType.PULSE)
    buttonA = Button(params)
    return buttonA

standalone = True
if(standalone):
    # Crear screen para los objetos UI
    # pylint: disable=E1101
    pygame.init()
    pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.ACTIVEEVENT])
    size = 800, 600
    screen = pygame.display.set_mode(size)
    UIElement.screen = screen

    buttonA = set_parameters_and_create()

    while(1):
        buttonA.update()
        events = pygame.event.get(pygame.MOUSEBUTTONDOWN)
        if(events):
            mouseEv = events[-1]
            if buttonA.has_inside(mouseEv.pos[0],mouseEv.pos[1]):
                buttonA.update_by_event(mouseEv)
        
        screen.fill((0,0,0))
        buttonA.draw()
        pygame.display.flip()
        time.sleep(0.020)
