import time
import pathlib
import pygame
import sys
import os.path


temporalPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "UI"))
sys.path.append(temporalPath)
# from ui import ui
# from Log import Log,LogParams
# from Button import Button
# from TextField import TextField,TextFieldParams
# from ScrollBar import ScrollBar,ScrollBarParams
from UIElement import UIElement
sys.path.remove(temporalPath)

# Crear screen para los objetos UI
# pylint: disable=E1101
pygame.init()
pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.ACTIVEEVENT])
size = 800, 600
screen = pygame.display.set_mode(size)
UIElement._screen = screen

objects = []

import ScrollBarTest
import ButtonTest
import LabelTest
import LogTest
import TextFieldTest
import TrackTest
objects.append(LabelTest.set_parameters_and_create())
objects.append(LogTest.set_parameters_and_create())
objects.append(TextFieldTest.set_parameters_and_create())
objects.append(TrackTest.set_parameters_and_create())
objects.append(ScrollBarTest.set_parameters_and_create())
objects.append(ButtonTest.set_parameters_and_create())


endApp = False

while(not endApp):
    
    keyevents = pygame.event.get(pygame.KEYDOWN)
    if(keyevents):
        if keyevents[-1].key == pygame.K_ESCAPE:
            endApp = True

    for someObject in objects:
        someObject.update()

    events = pygame.event.get(pygame.MOUSEBUTTONDOWN)
    if(events):
        mouseEv = events[-1]
        for someObject in objects:
            if someObject.has_inside(mouseEv.pos[0],mouseEv.pos[1]):
                someObject.update_by_event(mouseEv)
    
    screen.fill((0,0,0))
    for someObject in objects:
        someObject.draw()
    pygame.display.flip()
    time.sleep(0.020)



