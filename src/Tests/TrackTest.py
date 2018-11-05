import time
import pathlib
import pygame
import sys
import os.path


temporalPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "UI"))
sys.path.append(temporalPath)
from Track import Track,TrackParams
from Log import Log,LogParams
from Label import Label,LabelParams
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
    #Setear variables de clase Track
    Track.xMargin = 0
    Track.yMargin = 0
    Track.xOffset = 50
    Track.yOffset = 0

    # Crear variables para init de Track
    refX = 300
    refY = 100
    width = 200
    height = 200
    dims = (width,height,refX,refY)
    trackData = [[1,2,3,4,2,1],[2,4,6,8,1,3],[9,7,5,3,2,1],[6,5,2,1,2,2]]
    colorCode = [(255,0,0),
                 (255,255,0),
                 (128,128,0),
                 (0,0,255),
                 (0,255,0),
                 (255,255,200)]

    backPath = pathlib.Path.cwd() / "Assets" / "scrollBack.png"
    backImage = pygame.image.load(wpath(backPath))

    pygame.font.init()
    font = pygame.font.SysFont('Courier New',24)

    params1 = TrackParams(dims, trackData, colorCode, backImage,font)
    track1 = Track(params1)
    return track1

standalone = True
if(standalone):
    # Crear screen para los objetos UI
    # pylint: disable=E1101
    pygame.init()
    pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.ACTIVEEVENT])
    size = 800, 600
    screen = pygame.display.set_mode(size)
    UIElement.screen = screen

    track1 = set_parameters_and_create()

    timeStart = time.time()
    endApp = False

    count = 0
    while(not endApp):
        if timeStart + 0.1 < time.time():
            new_track = [[count,count,count,count,count,count],[2,4,6,8,1,3],[9,7,5,3,2,1],[6,5,2,1,2,2]]
            track1.set_new_track_data(new_track)
            count += 1
            timeStart = time.time()

        keyevents = pygame.event.get(pygame.KEYDOWN)
        if(keyevents):
            if keyevents[-1].key == pygame.K_ESCAPE:
                endApp = True

        track1.update()
        events = pygame.event.get(pygame.MOUSEBUTTONDOWN)
        if(events):
            mouseEv = events[-1]
            if track1.has_inside(mouseEv.pos[0],mouseEv.pos[1]):
                track1.update_by_event(mouseEv)

        screen.fill((0,0,0))
        track1.draw()
        pygame.display.flip()
        time.sleep(0.020)
