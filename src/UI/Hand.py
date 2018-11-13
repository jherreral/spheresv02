from Button import Button,ButtonParams,ButtonType
from Label import Label,LabelParams
from Component import Component

class Hand(Component):
    '''
    Clase Hand que muestra un panel con las cartas del jugador, 
    su nombre, faccion, logo y color.
    '''

    playerDims = (0,0,20,50)
    factionDims = (0,0,50,50)
    logoDims = (60,60,80,10)
    cardDims = (15,20,10,10)
    offset = 5

    def __init__(self,handParams):
        super.__init__(handParams.dims)
        self._font = handParams.font
                
        playerParams = LabelParams(
            (None,None,self._left + self.playerDims[2], self._top + self.playerDims[3]),
            handParams.playerName,
            self._font
        )
        factionParams = LabelParams(
            (None,None,self._left + self.factionDims[2], self._top + self.factionDims[3]),
            handParams.factionName,
            self._font
        )
        self._playerLabel = Label(playerParams)
        self._factionLabel = Label(factionParams)
        self._logoImage = handParams.logoImage
        self._cardList = []
        self._cardBank = handParams.cardBank

    def addCard(self,cardId):
        dims = (self.cardDims[0],
                self.cardDims[1],
                self._left + self.cardDims[2] + self.offset * (len(self._cardList)),
                self.cardDims[3])
        cardParams = ButtonParams(
            dims,
            self._cardBank.getCard(cardId),
            Button.frame_creator(dims)
        )
        self._cardList.append(Button(cardParams))

    def removeCard(self,cardId):
        for card in self._cardList:
            if card.id == cardId:
                self._cardList.remove(card)
                return

    def update(self):
        for card in self._cardList:
            card.update()

    def update_by_event(self,mouseEv):
        if (mouseEv.type == pygame.MOUSEBUTTONDOWN 
            and self.has_inside(mouseEv.pos[0], mouseEv.pos[1])):
            #Comprobación redundante pues este metodo debiera ser 
            #llamado solo cuando le llega un MOUSEBUTTONDOWN al 
            #Component padre en las coordenadas del boton.

            for card in self._cardList:
                if card.has_inside(mouseEv):
                    card.update_by_event(mouseEv)
                    if card.action:
                        self.showCard(card)
                        card.action = False
    
    def showCard(self,card):
        pass

    def draw(self):
        self._playerLabel.draw()
        self._factionLabel.draw()
        self.screen.blit(self._logoImage,
            (self.logoDims[2],self.logoDims[3]))
        for card in self._cardList:
            card.draw()



class HandParams:
    def __init__(self,
        dims,
        playerName,
        factionName,
        logoImage,
        background,
        font,
        cardBank):
        self.dims = dims
        self.playerName = playerName
        self.factionName = factionName
        self.logoImage = logoImage
        self.background = background
        self.font = font
        self.cardBank = cardBank