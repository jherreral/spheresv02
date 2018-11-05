from UIElement import UIElement

class Label(UIElement):
    """Objeto de texto simple, con una sola linea"""

    def __init__(self,labelParams):
        super().__init__(labelParams.dims)
        self._text = labelParams.text
        self._font = labelParams.font
        self._color = labelParams.color
        self._background = labelParams.background
        self._surface = self._font.render(self._text, True, self._color, self._background)

    def draw(self):
        self.screen.blit(self._surface,(self._left,self._top))

    def set_text(self,text):
        self._text = str(text)
        self._surface = self._font.render(self._text, True, self._color, self._background)

    def set_color(self,color):
        self._color = color
        self._surface = self._font.render(self._text, True, self._color, self._background)

    def get_text(self):
        return self._text

    def update(self):
        pass

    def update_by_event(self,mouseEv):
        pass

class LabelParams:

    def __init__(self,
                 dims,
                 text,
                 font,
                 color = (255,255,255),
                 background = None):
        self.dims = dims
        self.text = text
        self.font = font
        self.color = color
        self.background = background
