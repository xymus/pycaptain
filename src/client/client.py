#!/usr/bin/python

from sys import exit, argv
import sys
import os
from time import time, sleep
from threading import Thread
from md5 import md5

from screens.gui import Gui
from screens.join import JoinMenu
from screens.ship import MenuShips 
from screens.loading import LoadingScreen
from screens.main import MainMenu
from screens.scenario import ScenarioMenu
from screens.waiting import WaitingScreen
from screens.load import LoadMenu

from network import Network
from directnetwork import DirectNetwork
from common.comms import COObject, COInput, CopyCOInput, version
from universe import Universe

from common import config
from sys import argv

if "--help" in argv or "-h" in argv:
    print """Usage: %s [OPTIONS]
-f\tTry to launch in fullscreen mode, depends on system 
\tavailability and pygame.
-s\tSafe mode, exceptiona handled on main loop. Prevents 
\tcomplete freeze when in fullscreen mode.""" % argv[0]
    exit()

class Client:
    def __init__( self, displayName="Sdl" ):
        self.displayName = displayName
        self.network = None
        self.prefs = None

        self.gui = None
        self.joinMenu = None
        self.menuShips = None

        self.optimalFrame = 1.0/30
        self.useServer = False

        self.universe = Universe()

        self.at = "mainmenu"
        self.runningServer = False

    def run(self):

        if "-f" in argv:
            fullscreen = True
            resolution = None
        else:
            fullscreen = False
            resolution = (960,680)

        exec( "from displays.%s import %s as Display"%( self.displayName.lower(), self.displayName.capitalize() ) )
        self.display = Display( resolution, fullscreen )
        
        splash = LoadingScreen( self.display )
        mixer, imgs, snds, texts, self.prefs = splash.loadAll()
        
        from server.stats import Stats # TODO REMOVE, for testing purpose only
        
        self.stats = Stats().statsDict #stats.statsDict
        self.gui = Gui( self.display, mixer, imgs, snds, texts, self.prefs, self.stats, 
            eQuit=self.eQuitGame, eSave=self.eSave, eScreenshot=self.eScreenshot  )

        self.mainmenu = MainMenu( self.gui.display, self.gui.imgs, 
            eQuit=self.eQuit, eQuickPlay=self.eQuickPlay, eJoin=self.eJoin, eScenario=self.eScenario, eLoad=self.eLoad
            )
        self.joinMenu = JoinMenu( self.gui.display, self.gui.imgs, self.prefs.user, self.prefs.password, self.prefs.server, config.port, 
            eOk=self.eJoinConnect, eBack=self.eJoinBack 
            )
        self.menuShips = MenuShips( self.gui.display, self.gui.imgs, self.gui.texts, eQuit=self.eQuitGame, eOk=self.eShipOk )
        self.scenarioMenu = ScenarioMenu( self.gui.display, self.gui.imgs, eBack=self.eJoinBack, ePlay=self.ePlay )
        self.waitingScreen = WaitingScreen( self.gui.display, self.gui.imgs, eCancel=self.eQuitGame )
        self.loadMenu = LoadMenu( self.gui.display, self.gui.imgs, eBack=self.eJoinBack, eLoad=self.eLoadGame )
       
        self.inputs = COInput()
        self.lastInputs = None

        self.objects = []

        self.run = True
        self.useServer = True            

       #### main loop ###
        while self.run:
            t0 = time()

            if self.at == "mainmenu":
                self.mainmenuLoop()
            elif self.at == "join":
                self.joinLoop()
            elif self.at == "game":
                self.gameLoop()
            elif self.at == "ship":
                self.shipLoop()
            elif self.at == "scenario":
                self.scenarioLoop()
            elif self.at == "waiting":
                self.waitingLoop()
            elif self.at == "load":
                self.loadLoop()

            t1 = time()
            tts = self.optimalFrame - (t1-t0)
            if tts > 0:
                sleep( tts )

        ## close network
        if self.network:
            self.network.shutdown = True
            self.network.pubQuit()
            self.network.close()

        ## if server run locally, kill it
        if self.runningServer:
            self.server.shutdown = True

        ## close gui
        self.gui.close()

    def gameLoop( self ):
           ## get inputs
        #    self.inputs.orders = []
            self.gui.objects = self.objects
            (quit, inputs, msgalls, msgusers, goToShipSelection) = self.gui.manageInputs( self.display )

            for msguser in msgusers:
                self.network.sendMsguser( msguser[0], msguser[1] )

            for msgall in msgalls:
                self.network.sendMsguser( msgall )

            if goToShipSelection:
                self.at = "ship"

           ## get update from server
            if self.network:
                while isinstance( self.network, DirectNetwork ) and not self.network.updated:  # TODO remove when gameplays implemented
                    sleep( 0.001 )
                    
                ( shutdown, bump, msgalls, msgusers, sysmsgs, objects, astres, gfxs, playerStats, players, possibles ) = self.network.getUpdates()
                if objects:
                    self.objects = objects

                for msg in msgalls:
                    self.gui.addMsg( "%s says to all: %s" % msg )

                for msg in msgusers:
                    self.gui.addMsg( "%s says to you: %s" % msg )

                for msg in sysmsgs:
                    self.gui.addMsg( "system: %s" % msg )
               #     print "system: %s" % msg

                if shutdown:
                    self.useServer = False

                if bump:
                    self.useServer = False

                if players:
                    self.universe.players = players
                if astres:
                    self.universe.astres = astres # self.universe.astres + astres
                if gfxs:
                    self.universe.gfxs =  self.universe.gfxs + gfxs

                if playerStats.dead:
                    self.at = "ship"

               ## draw view
                self.gui.objects = self.objects
                self.gui.astres = self.universe.astres
                self.gui.gfxs = self.universe.gfxs
                self.gui.playerStats = playerStats
                self.gui.stats = self.stats
                self.gui.players = self.universe.players
                self.gui.lag = self.network.lag
                self.gui.draw( self.display )

               ## update animations frame
                self.gui.imgs.updateAnimations()

               ## send inputs to server
                if self.useServer:
                    if not self.lastInputs or len(inputs.orders) \
                      or inputs.xc != self.lastInputs.xc or inputs.yc != self.lastInputs.yc \
                      or inputs.wc != self.lastInputs.wc or inputs.hc != self.lastInputs.hc:
                        self.lastInputs = CopyCOInput( inputs )
                        self.network.sendInputs( inputs )

                if quit:
                    self.run = False
                    self.useServer = False

                self.universe.doTurn()
                
                
    def eScreenshot( self, sender, (x,y) ):
        self.display.takeScreenshot()        


### main menu loop ###
    def mainmenuLoop( self ):
        self.mainmenu.draw( self.display )
        self.mainmenu.manageInputs( self.display )
            
    def eQuit(self, sender, (x,y)):
        self.run = False
            
    def eQuickPlay(self, sender, (x,y)):
        self.launchLocalServer()
        if self.network:
            self.at = "waiting"
            
    def eJoin(self, sender, (x,y)):
        self.at = "join"
        
    def eScenario( self, sender, (x,y) ):
        self.at = "scenario"
        
### load menu loop ###
    def loadLoop( self ):
        self.loadMenu.draw( self.display )
        self.loadMenu.manageInputs( self.display )
        
    def eLoadGame( self, sender, (x,y) ):
        from server.game import LoadGame
        path = self.loadMenu.selectedPath
        game = LoadGame( path )
        if game:
            self.launchLocalServer( game=game )
            if self.network:
                self.at = "waiting"

### waiting loop ###
    def waitingLoop( self ):
        self.waitingScreen.draw( self.display )
        self.waitingScreen.manageInputs( self.display )
        
        if self.network:
            ( shutdown, bump, msgalls, msgusers, sysmsgs, objects, astres, gfxs, stats, players, possibles ) = self.network.getUpdates( )
            
            for msg in msgalls:
                self.gui.addMsg( "%s says to all: %s" % msg )

            for msg in msgusers:
                self.gui.addMsg( "%s says to you: %s" % msg )

            for msg in sysmsgs:
                self.gui.addMsg( "system: %s" % msg )
                
            if stats and not stats.dead:
                self.gui.reset()
                self.at = "game"
            elif possibles:
                self.menuShips.changeSelected( options=possibles )
                self.at = "ship"
            
### scenario menu loop ###
    def scenarioLoop( self ):
        self.scenarioMenu.draw( self.display )
        self.scenarioMenu.manageInputs( self.display )
        
    def ePlay( self, sender, (x,y) ):
        self.launchLocalServer( self.scenarioMenu.selectedScenario )
        if self.network:
            self.at = "waiting"
            
    def eQuitGame( self, sender, (x,y) ):
        self.at = "mainmenu"
        if self.network:
            self.network.shutdown = True
            self.network.pubQuit()
            self.network.close()
            self.network = None

        ## if server run locally, kill it
        if self.runningServer:
            self.server.shutdown = True
            self.runningServer = False
        
        
### join menu loop ###
    def joinLoop( self ):
        self.joinMenu.draw( self.display )
        self.joinMenu.manageInputs( self.display )
        
        if self.runningServer and self.server.shutdown:
            # server failed
            self.runningServer = False
            self.network = None
            self.joinMenu.setError( "Server failed to open any listening sockets, please wait a few minutes, kill dead processes or reboot." )
            

        if self.network:
            success,msg = self.network.getConnectState()
         #   print success,msg
            if success:
                self.at = "ship"
                
                if not self.runningServer and (self.server != self.prefs.server or self.user != self.prefs.user or self.password != self.prefs.password):
                    self.prefs.save( self.user, self.password, self.server )
            elif success == None: # still trying 
                self.joinMenu.setError( msg )
            else: # failed
                self.joinMenu.ctrlOk.enabled = True
                self.joinMenu.setError( msg )
            
    def eJoinBack(self, sender, (x,y)):
        self.at = "mainmenu"
    
    def eJoinConnect(self, sender, (x,y)):
    
        if self.joinMenu.cPassword.text == self.joinMenu.initialPassword:
            self.password = self.prefs.password #   joinMenu.initialPassword
        else:
            self.password = md5(self.joinMenu.cPassword.text).hexdigest()
            
        self.server, self.port, self.user = self.joinMenu.cServer.text, int(self.joinMenu.cPort.text), self.joinMenu.cUser.text
        
        self.joinMenu.ctrlOk.enabled = False
        self.network = Network( self.server, self.port, self.user, self.password, version )
        self.network.connect()
        
    def eToggleFullscreen(self, sender, (x,y)):
        self.gui.display.toggleFullscreen()

### ship loop ###
    def shipLoop( self ):
        self.menuShips.draw( self.display )

        ( shutdown, bump, msgalls, msgusers, sysmsgs, objects, astres, gfxs, stats, players, possibles ) = self.network.getUpdates( )
        
        for msg in msgalls:
            self.gui.addMsg( "%s says to all: %s" % msg )

        for msg in msgusers:
            self.gui.addMsg( "%s says to you: %s" % msg )

        for msg in sysmsgs:
            self.gui.addMsg( "system: %s" % msg )
            
        if stats and not stats.dead:
            self.gui.reset()
            self.at = "game"

        if possibles:
            self.menuShips.options = possibles
        self.menuShips.manageInputs( self.display )
            
    def eShipOk(self, sender, (x,y)):
        self.network.sendShipChoice( self.menuShips.selectedOption )

    def launchLocalServer( self, scenario=None, game=None ):
        from server.server import Server
        from server.directnetwork import DirectNetwork as DirectNetworkServer
        self.server = Server( addresses=["localhost"], networkType=DirectNetworkServer, force=True, Scenario=scenario, game=game )

        self.serverThread = Thread( name="server", target=self.server.run )
        self.serverThread.start()

        sleep( 0.1 )
        if self.server.network:
            self.runningServer = True
            
            if os.name == "posix":
                user = os.getlogin()
            else:
                user = "echec"
                
            self.network = DirectNetwork( self.server.network )
            self.network.connect( user ) 
            
    def eLoad( self, sender, (x,y) ):
        self.loadMenu.reset( self.display, self.gui.imgs )
        self.at = "load"
        
        
        
    def eSave( self, sender, (x,y) ):
        if self.runningServer:
            saveGameRoot = os.path.join( sys.path[0], "client", "saves" )
            if self.server.game.save( os.path.join( saveGameRoot, "%s-%i.pyfl"%(self.server.game.scenario.name, self.server.game.tick) ) ):
                self.gui.addMsg( "saved as %s-%i.pyfl"%(self.server.game.scenario.name, self.server.game.tick) )
            else:
                self.gui.addMsg( "saving failed" )

try:
    import psyco
    psyco.full()
except ImportError, ex:
    print "Failed to import psyco. Under debian/linux apt-get python-psyco to speed up the game."

#client = Client()
#
#try:
#  if "-s" in argv:
#    try:
#        client.run()
#    except Exception, ex:
#        print ex
#  else:
#    client.run()
#except KeyboardInterrupt:
#  print "KeyboardInterrupt"
#  if client.run:
#      client.run = False

