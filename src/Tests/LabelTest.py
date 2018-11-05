import time
import pathlib
import pygame
import sys
import os.path

temporalPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "UI"))
sys.path.append(temporalPath)
from Label import Label,LabelParams
from UIElement import UIElement
sys.path.remove(temporalPath)


def set_parameters_and_create():

    # Crear variables para init de Label
    refX = refY = 100

    dims = (0,0,refX,refY)
    pygame.font.init()
    font = pygame.font.SysFont('Courier New',24)

    params1 = LabelParams(dims, 'Hello', font)
    label1 = Label(params1)
    return label1

standalone = True
if(standalone):
    # Crear screen para los objetos UI
    # pylint: disable=E1101
    pygame.init()
    pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.ACTIVEEVENT])
    size = 800, 600
    screen = pygame.display.set_mode(size)
    UIElement.screen = screen

    label1 = set_parameters_and_create()

    timeStart = time.time()
    endApp = False

    count = 0
    while(not endApp):
        if timeStart + 0.5 < time.time():
            label1.set_text(label1._text + 'X')
            label1.set_color(((count%8)*31 ,(count%8)*31,(count%8)*31))
            count += 1
            timeStart = time.time()

        if count == 2:
            print('asd')

        keyevents = pygame.event.get(pygame.KEYDOWN)
        if(keyevents):
            if keyevents[-1].key == pygame.K_ESCAPE:
                endApp = True

        label1.update()
        events = pygame.event.get(pygame.MOUSEBUTTONDOWN)
        if(events):
            mouseEv = events[-1]
            if label1.has_inside(mouseEv.pos[0],mouseEv.pos[1]):
                label1.update_by_event(mouseEv)

        screen.fill((0,0,0))
        label1.draw()
        pygame.display.flip()
        time.sleep(0.020)
