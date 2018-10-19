import time
import pathlib

import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import ui
sys.path.remove(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


# Crear screen para los objetos UI
# pylint: disable=E1101
ui.pygame.init()
ui.pygame.event.set_blocked([ui.pygame.MOUSEMOTION, ui.pygame.ACTIVEEVENT])
size = 800, 600
screen = ui.pygame.display.set_mode(size)
ui.UIElement._screen = screen

objects = []

import ScrollBarTest
import ButtonTest
objects.append(ScrollBarTest.set_parameters_and_create())
objects.append(ButtonTest.set_parameters_and_create())

while(1):
    for someObject in objects:
        someObject.update()

    events = ui.pygame.event.get(ui.pygame.MOUSEBUTTONDOWN)
    if(events):
        mouseEv = events[-1]

        for someObject in objects:
            if someObject.has_inside(mouseEv.pos[0],mouseEv.pos[1]):
                someObject.update_by_event(mouseEv)
    
    for someObject in objects:
        someObject.draw()
    ui.pygame.display.flip()
    time.sleep(0.020)

