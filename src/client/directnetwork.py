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
        self.updated = False
        
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

    def updatePlayer( self, objects, gfxs, stats, players, astres, possibles, msgusers, sysmsgs ):
        self.objects =  objects
        self.gfxs += gfxs.gfxs
        self.stats = stats
        self.players = players
        self.msgusers += msgusers
        self.sysmsgs += sysmsgs
        if astres:
            self.astres = astres
        if possibles:
            self.possibles = possibles
        self.updated = True
        
    def getUpdates(self): 
        shutdown = self.shutdown
        bump = self.bump
        msgusers = self.msgusers
        sysmsgs = self.sysmsgs
        objects =  self.objects
        astres = self.astres
        gfxs = self.gfxs
        players = self.players
        stats = self.stats
        possibles = self.possibles
        self.msgusers = []
        self.sysmsgs = []
        self.objects =  []
        self.gfxs =  []
        self.players =  None
        
        self.updated = False
        
        return ( shutdown, bump, msgusers, sysmsgs, objects, astres, gfxs, stats, players, possibles )
    
    def pubQuit(self):
        self.server.disconnect( self )

    def sendMsguser( self, text, destName ):
        pass

    def close(self):
        pass

def join(lists):
    return "".join(lists)




