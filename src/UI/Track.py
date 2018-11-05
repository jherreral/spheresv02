from Component import Component
from Label import Label,LabelParams
from pygame.transform import scale

class Track(Component):
    '''
    Muestra la produccion, petroleo, esferas y capitales de cada
    jugador con su respectivo color.
    Contiene un Label por cada bloque de texto ((nPlayers+1)*4 bloques)

    '''

    xMargin = None
    yMargin = None
    xOffset = None
    yOffset = None

    def __init__(self,trackParams):


        super().__init__(trackParams.dims)
        self._trackData = trackParams.trackData
        self._colorCode = trackParams.colorCode
        self._background = self._background = scale(
                            trackParams.background,
                            (self._width,self._height))
        self._font = trackParams.font

        self._staticLabels = self._create_static_labels()
        self._dynamicLabels = self._create_dynamic_labels()

    def _create_static_labels(self):
        statics = []
        lineSize = self._font.get_linesize()
        for idx,text in enumerate(['Prod','Oils','Sphe','Caps']):
            dims = (None,None,
                    self._left + self.xMargin,
                    self._top + self.yMargin + idx * lineSize)
            params = LabelParams(dims,text,self._font)
            statics.append(Label(params))
        return statics
        
    def _create_dynamic_labels(self):
        dynamics = []
        lineSize = self._font.get_linesize()
        staticOffset = 40
        for idxV,quantityLine in enumerate(self._trackData):
            quantityLabelsList = []
            for idxH,quantity in enumerate(quantityLine):
                dims = (None,None,
                    self._left + self.xMargin + self.xOffset * idxH + staticOffset,
                    self._top + self.yMargin + idxV * lineSize)
                params = LabelParams(dims,str(quantity),self._font,self._colorCode[idxH])
                quantityLabelsList.append(Label(params))
            dynamics.append(quantityLabelsList)
        return dynamics

    def set_new_track_data(self,trackData):
        self._trackData = trackData
        for idxV,line in enumerate(self._dynamicLabels):
            for idxH,label in enumerate(line):
                label.set_text(self._trackData[idxV][idxH])

    def update(self):
        pass

    def update_by_event(self,mouseEv):
        pass

    def draw(self):
        self.screen.blit(self._background,(self._left, self._top))
        for label in self._staticLabels:
            label.draw()
        for line in self._dynamicLabels:
            for label in line:
                label.draw()
        

class TrackParams:
    def __init__(self, dims, trackData, colorCode, background, font):
        '''
        dims: tuple of 4 - (width, height, left, top)
        trackData: list of 4 - [production,oils,spheres,capitals]
            each element is a list of nPlayers
        colorCode: tuple of nPlayers - (color1,color2,color3,...)
            each element is a color tuple
        background: image to use as background
        font: font for all Labels inside Track
        '''
        
        self.dims = dims
        self.trackData = trackData
        self.colorCode = colorCode
        self.background = background
        self.font = font
