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
from ui import CardBank
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
    Hand.playerDims = (0,0,20,120)
    Hand.factionDims = (0,0,400,120)
    Hand.logoDims = (60,60,400,10)
    Hand.cardDims = (30,40,10,10)
    Hand.offset = 10

    # Crear variables para init de Hand
    refX = 0
    refY = 450
    width = 500
    height = 150
    dims = (width,height,refX,refY)
    
    logoPath = pathlib.Path.cwd() / "Assets" / "logo.png"
    logoImage = pygame.image.load(wpath(logoPath))

    backPath = pathlib.Path.cwd() / "Assets" / "scrollBack.png"
    backImage = pygame.image.load(wpath(backPath))

    pygame.font.init()
    font = pygame.font.SysFont('Courier New',24)

    cardBank = CardBank()
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

    hand1 = set_parameters_and_create()

    timeStart = time.time()
    endApp = False

    count = 0
    while(not endApp):
        if timeStart + 3 < time.time():
            hand1.addCard('00')
            timeStart = time.time()

        keyevents = pygame.event.get(pygame.KEYDOWN)
        if(keyevents):
            if keyevents[-1].key == pygame.K_ESCAPE:
                endApp = True

        hand1.update()
        events = pygame.event.get(pygame.MOUSEBUTTONDOWN)
        if(events):
            mouseEv = events[-1]
            if hand1.has_inside(mouseEv.pos[0],mouseEv.pos[1]):
                hand1.update_by_event(mouseEv)

        screen.fill((0,0,0))
        hand1.draw()
        pygame.display.flip()
        time.sleep(0.020)
