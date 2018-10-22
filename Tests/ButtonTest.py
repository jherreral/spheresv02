import time
import pathlib

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
    # Setear variables de clase Button
    ui.Button._hoverColor = (0,0,200)
    ui.Button._pressedColor = (200, 0, 0)
    ui.Button._frameWidth = 5
    ui.Button._holdTime = 0.2

    # Crear variables para init de Button
    refX = refY = 100
    path = pathlib.Path.cwd() / "Assets" / "botonA.png"
    imageA = ui.pygame.image.load(wpath(path))

    width = 220
    height = 95
    dims = (width,height,refX,refY)
    frame = ui.Button.frame_creator(dims)

    params = ui.ButtonParams(dims, imageA, frame, ui.ButtonType.PULSE)
    buttonA = ui.Button(params)
    return buttonA

standalone = False
if(standalone):
    # Crear screen para los objetos UI
    # pylint: disable=E1101
    ui.pygame.init()
    ui.pygame.event.set_blocked([ui.pygame.MOUSEMOTION, ui.pygame.ACTIVEEVENT])
    size = 800, 600
    screen = ui.pygame.display.set_mode(size)
    ui.Button._screen = screen

    buttonA = set_parameters_and_create()

    while(1):
        buttonA.update()
        events = ui.pygame.event.get(ui.pygame.MOUSEBUTTONDOWN)
        if(events):
            mouseEv = events[-1]
            if buttonA.has_inside(mouseEv.pos[0],mouseEv.pos[1]):
                buttonA.update_by_event(mouseEv)
        buttonA.draw()
        ui.pygame.display.flip()
        time.sleep(0.020)
