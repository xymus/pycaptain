#!/usr/bin/python

from threading import Thread
from socket import SocketType
import socket
from time import sleep, time

from network import Network
from common.comms import *

class DirectNetwork( Network ):
    def __init__(self, serverNetwork ):
        self.serverNetwork = serverNetwork

        self.shutdown = False
        self.bump = False
        self.msgalls = []
        self.msgusers = []
        self.sysmsgs = []
        self.objects =  []
        self.astres =  []
        self.gfxs =  []
        self.players = None
        self.stats = None
        self.possibles = []
        self.lag = 0

        self.connectState = (None,"working")
        
        self.server = serverNetwork
        
    def connect(self, username):
    #    try:
            self.server.connect( self )
            self.server.login( self, username )
            self.connectState = (True,"connection established")
    #    except Exception, ex:
    #        self.connectState = (False, ex )
        
    def getConnectState( self ):
        return self.connectState

    def sendInputs(self, inputs):
        self.server.up( self, inputs )

    def sendShipChoice(self, s):
        self.server.choice( self, s )

    def updatePlayer( self, objects, gfxs, stats, players, astres, possibles ):
        self.objects =  objects
        self.gfxs = gfxs.gfxs
        self.stats = stats
        self.players = players
        if astres:
            self.astres = astres
        if possibles:
            self.possibles = possibles
        
    def getUpdates(self): 
        shutdown = self.shutdown
        bump = self.bump
        msgalls = self.msgalls
        msgusers = self.msgusers
        sysmsgs = self.sysmsgs
        objects =  self.objects
        astres = self.astres
        gfxs = self.gfxs
        players = self.players
        stats = self.stats
        possibles = self.possibles

        self.msgalls = []
        self.msgusers = []
        self.sysmsgs = []
        self.objects =  []
        self.gfxs =  []
        self.players =  None
        
        return ( shutdown, bump, msgalls, msgusers, sysmsgs, objects, astres, gfxs, stats, players, possibles )
    
    def pubQuit(self):
        self.server.disconnect( self )


    def sendMsgall( self, text ):
        pass

    def sendMsguser( self, text, destName ):
        pass

    def close(self):
        pass

def join(lists):
    return "".join(lists)




