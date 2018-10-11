import ui
import time
import pathlib

def wpath(path):
    result = ""
    for idx,part in enumerate(path.parts):
        if idx == 0:
            result = part
        else:
            result += "\\" + part
    return result

# Crear variables para init de Button
refX = refY = 200
path = pathlib.Path.cwd() / "Assets" / "botonA.png"
imageA = ui.pygame.image.load(wpath(path))

width = 220
height = 95
dims = (width,height,refX,refY)
frame = list([(dims[2], dims[3]),
              (dims[2] + dims[0], dims[3]),
              (dims[2] + dims[0], dims[3]+dims[1]),
              (dims[2], dims[3]+dims[1])])

# Crear screen para los objetos UI
ui.pygame.init()
ui.pygame.event.set_blocked([ui.pygame.MOUSEMOTION, ui.pygame.ACTIVEEVENT])
size = 800, 600
screen = ui.pygame.display.set_mode(size)
ui.Button._screen = screen

# Setear variables de clase Button
ui.Button._hoverColor = (0,0,200)
ui.Button._pressedColor = (200, 0, 0)
ui.Button._frameWidth = 5
ui.Button._holdTime = 0.2


buttonA = ui.Button(dims, imageA, frame, ui.ButtonType.PULSE)

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
