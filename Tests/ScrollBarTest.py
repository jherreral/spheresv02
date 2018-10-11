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

# Crear screen para los objetos UI
standalone = True
if(standalone):
    ui.pygame.init()
    ui.pygame.event.set_blocked([ui.pygame.MOUSEMOTION, ui.pygame.ACTIVEEVENT])
    size = 800, 600
    screen = ui.pygame.display.set_mode(size)
    ui.UIElement._screen = screen
    
# Setear variables de clase Button
ui.Button._hoverColor = (0,0,200)
ui.Button._pressedColor = (200, 0, 0)
ui.Button._frameWidth = 5
ui.Button._holdTime = 0.2

# Crear variables para init de ScrollBar
refX = 300
refY = 200
buttonPath = pathlib.Path.cwd() / "Assets" / "scrollButton.png"
barPath = pathlib.Path.cwd() / "Assets" / "scrollBar.png"
backPath = pathlib.Path.cwd() / "Assets" / "scrollBack.png"

buttonImage = ui.pygame.image.load(wpath(buttonPath))
barImage = ui.pygame.image.load(wpath(barPath))
backImage = ui.pygame.image.load(wpath(backPath))

width = 20
height = 150
barHeight = 10
barDispl = 3
dims = (width,height,refX,refY)



scrollBarA = ui.ScrollBar(dims, backImage, barImage, barHeight, barDispl, buttonImage)

while(1):
    scrollBarA.update()
    events = ui.pygame.event.get(ui.pygame.MOUSEBUTTONDOWN)
    if(events):
        mouseEv = events[-1]
        if scrollBarA.has_inside(mouseEv.pos[0],mouseEv.pos[1]):
            scrollBarA.update_by_event(mouseEv)
    scrollBarA.draw()
    ui.pygame.display.flip()
    time.sleep(0.020)
