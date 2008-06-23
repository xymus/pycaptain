#!/usr/bin/python

from sys import exit, argv
import os

from time import time, sleep
from threading import Thread

from gui import Gui
from network import Network
from directnetwork import DirectNetwork
from common.comms import COObject, COInput, CopyCOInput, version
from universe import Universe
from menu import LoginMenu
from menuships import MenuShips 

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
        self.network = None
        self.prefs = None

        self.gui = None
        self.menu = None
        self.menuShips = None

        self.optimalFrame = 1.0/30
        self.useServer = False

        self.universe = Universe()

        self.at = "menu"
        self.runningServer = False

    def run(self):

        if "-f" in argv:
            fullscreen = True
            resolution = None
        else:
            fullscreen = False
            resolution = (960,680)

        self.gui = Gui( fullscreen, resolution )
        self.prefs = self.gui.prefs

        self.menu = LoginMenu( self.gui.display, self.gui.imgs, self.prefs.user, self.prefs.password, self.prefs.server, config.port )
        self.menuShips = MenuShips( self.gui.display, self.gui.imgs, self.gui.texts )
       
        self.inputs = COInput()
        self.lastInputs = None

        self.objects = []

        self.run = True
        self.useServer = True            

       #### main loop ###
        while self.run:
            t0 = time()

            if self.at == "menu":
                self.menuLoop()
            elif self.at == "game":
                self.gameLoop()
            elif self.at == "ship":
                self.shipLoop()

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
            self.inputs.orders = []
            (quit, self.inputs, msgalls, msgusers, goToShipSelection) = self.gui.getInputs( self.inputs, self.objects )

            for msguser in msgusers:
                self.network.sendMsguser( msguser[0], msguser[1] )

            for msgall in msgalls:
                self.network.sendMsguser( msgall )

            if goToShipSelection:
                self.at = "ship"

           ## get update from server
            ( shutdown, bump, msgalls, msgusers, sysmsgs, objects, astres, gfxs, stats, players, possibles ) = self.network.getUpdates()
            if objects:
                self.objects = objects

            for msg in msgalls:
                self.gui.addMsg( "%s says to all: %s" % msg )

            for msg in msgusers:
                self.gui.addMsg( "%s says to you: %s" % msg )

            for msg in sysmsgs:
                self.gui.addMsg( "system: %s" % msg )

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

            if stats.dead:
                self.at = "ship"

           ## draw view
            self.gui.draw( self.objects, self.universe.astres, self.universe.gfxs, stats, self.universe.players, self.network.lag )

           ## update animations frame
            self.gui.imgs.updateAnimations()

           ## send inputs to server
            if self.useServer:
                if not self.lastInputs or len(self.inputs.orders) \
                  or self.inputs.xc != self.lastInputs.xc or self.inputs.yc != self.lastInputs.yc \
                  or self.inputs.wc != self.lastInputs.wc or self.inputs.hc != self.lastInputs.hc:
                    self.lastInputs = CopyCOInput( self.inputs )
                    self.network.sendInputs( self.inputs )

            if quit:
                self.run = False
                self.useServer = False

            self.universe.doTurn()

    def menuLoop( self ):
        self.menu.draw()
        quit,user,password,server,port,local,toggleFullscreen = self.menu.getUpdates()
        if user:
            ( self.server, self.port, self.user, self.password ) = ( server, port, user, password )
            self.menu.cOk.enabled = False
            self.network = Network( server, port, user, password, version )
            self.network.connect() # launchs thread

        if local:
            self.menu.setError( "Launching local server..." )
            self.launchLocalServer()

        if toggleFullscreen:
            self.gui.display.toggleFullscreen()

        if self.runningServer and self.server.shutdown:
            # server failed
            self.runningServer = False
            self.network = None
            self.menu.setError( "Server failed to open any listening sockets, please wait a few minutes, kill dead processes or reboot." )
            

        if self.network:
            success,msg = self.network.getConnectState()
            print success,msg
            if success:
                self.at = "ship"
                
                if not self.runningServer and (self.server != self.prefs.server or self.user != self.prefs.user or self.password != self.prefs.password):
                    self.prefs.save( self.user, self.password, self.server )
            elif success == None: # still trying 
                self.menu.setError( msg )
            else: # failed
                self.menu.cOk.enabled = True
                self.menu.setError( msg )
                
                
        if quit:
            self.run = False

    def shipLoop( self ):
        self.menuShips.draw()

        ( shutdown, bump, msgalls, msgusers, sysmsgs, objects, astres, gfxs, stats, players, possibles ) = self.network.getUpdates()
        if stats and not stats.dead:
            self.at = "game"
            if __debug__: print "not dead, going to game"

        if possibles:
            self.menuShips.options = possibles
        quit, option = self.menuShips.getInputs()

        if option: # upload choice to server
            print "options selected"
            self.network.sendShipChoice( option )

        if quit:
            self.run = False

    def launchLocalServer( self ):
        from server.server import Server
        from server.directnetwork import DirectNetwork as DirectNetworkServer
        self.server = Server( addresses=["localhost"], networkType=DirectNetworkServer, force=True, scenarioName="Sol" )

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

