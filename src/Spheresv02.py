import queue as q
import sys,os

from UI.ui import UI

#Create Queues
GameQueue = q.Queue()
RequestQueue = q.Queue()
UIQueue = q.Queue()

#Create all necesary threads (this is the app thread)

#UI thread - display everything, process user input
uiThread = UI(UIQueue)
uiThread.main()
#Audio thread - Play sound!


exitApp = True
#Main App Loop
while(not exitApp):
    RequestedItem = RequestQueue.get()
    if(RequestedItem == 'GameStart'):
        pass
#Game thread - created when initiating a match, carries the game sequence
#Network thread - create, manage and maintain connections

#App thread - manage app state: main menu, in-game, ... 
