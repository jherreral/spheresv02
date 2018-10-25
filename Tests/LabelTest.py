import time
import pathlib

import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import ui
sys.path.remove(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


def set_parameters_and_create():

    # Crear variables para init de Label
    refX = refY = 100

    dims = (0,0,refX,refY)
    ui.pygame.font.init()
    font = ui.pygame.font.SysFont('Courier New',24)

    params1 = ui.LabelParams(dims, 'Hello', font)
    label1 = ui.Label(params1)
    return label1

standalone = True
if(standalone):
    # Crear screen para los objetos UI
    # pylint: disable=E1101
    ui.pygame.init()
    ui.pygame.event.set_blocked([ui.pygame.MOUSEMOTION, ui.pygame.ACTIVEEVENT])
    size = 800, 600
    screen = ui.pygame.display.set_mode(size)
    ui.UIElement._screen = screen

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

        keyevents = ui.pygame.event.get(ui.pygame.KEYDOWN)
        if(keyevents):
            if keyevents[-1].key == ui.pygame.K_ESCAPE:
                endApp = True

        label1.update()
        events = ui.pygame.event.get(ui.pygame.MOUSEBUTTONDOWN)
        if(events):
            mouseEv = events[-1]
            if label1.has_inside(mouseEv.pos[0],mouseEv.pos[1]):
                label1.update_by_event(mouseEv)

        screen.fill((0,0,0))
        label1.draw()
        ui.pygame.display.flip()
        time.sleep(0.020)
