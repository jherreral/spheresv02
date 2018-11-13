import time
import pathlib
import pygame
import sys
import os.path


temporalPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "UI"))
sys.path.append(temporalPath)
from Button import Button,ButtonParams
from Label import Label,LabelParams
from Hand import Hand,HandParams
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

    #Setear variables de clase Hand
    Hand.playerDims = (0,0,20,50)
    Hand.factionDims = (0,0,50,50)
    Hand.logoDims = (60,60,80,10)
    Hand.cardDims = (15,20,10,10)
    Hand.offset = 5

    # Crear variables para init de Hand
    refX = 100
    refY = 300
    width = 300
    height = 200
    dims = (width,height,refX,refY)
    
    logoPath = pathlib.Path.cwd() / "Assets" / "logo.png"
    logoImage = pygame.image.load(wpath(logoPath))

    backPath = pathlib.Path.cwd() / "Assets" / "scrollBack.png"
    backImage = pygame.image.load(wpath(backPath))

    pygame.font.init()
    font = pygame.font.SysFont('Courier New',24)

    cardBank = None
    params1 = HandParams(dims, 'Jimmy', 'Badgers', logoImage,backImage,font,cardBank)
    hand1 = Hand(params1)
    return hand1

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
