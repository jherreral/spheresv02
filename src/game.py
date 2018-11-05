class game(object):
    """Gameborad, it has all the game logic"""

    def __init__(self, **kwargs):

        self.round = 0
        self.zones_data = []
        self.edges_pairs = []
        self.availableCapitals = []
        self.movilization_order = []
        self.turn_deck = []
        self.special_deck = []
        self.discard_deck = []
        self.players = []
        self.zones_per_sphere = [0]*18
        self.startLocations = []
        self.receiveQueue = receiveQueue
        self.sendQueue = sendQueue
        self.cardQueue = cardQueue
        return super().__init__(**kwargs)

    def 