from threading import Thread
from socket import SocketType, gethostname, gethostbyname
import socket
from time import sleep

import players
from common.comms import *
from common import config

from network import Network, PlayerConnection

class DirectNetwork( Network ):
    def __init__( self, game, addresses, port, versionString, adminPassword ):
        self.game = game
        self.versionString = versionString
        self.shutdownOrder = False
        self.adminPassword = adminPassword

        self.clients = [] 
        self.players = {} 

        self.inputs = []
        self.codes = []
        self.newPlayers = []
        self.shipChoices = []

        self.listening = True
      #  self.tWork = Thread( name="network", target=self.fWork )
     #   self.tWork.start()
     
    def connect( self, client ):
        self.clients.append( client )
        
    def up( self, client, inputs ):
        self.inputs.append( (self.players[ client ],inputs) )

    def login( self, client, username ):
        player = self.game.getPlayer( username )
        
        if not player:
           player = self.game.addRemotePlayer( username, "")
            
        self.players[ client ] = player
        self.newPlayers.append( player )
        print "logged in %s for %s" % ( username, client )
    
    def disconnect( self, client ):
        self.clients.remove( client )
        if not len( self.clients ):
            self.shutdown()
    
    def choice( self, client, choice ):
        print "choice", choice
        self.shipChoices.append( (self.players[ client ], choice) )
    
    def shutdown( self ):
        self.shutdownOrder = True


    def getInputs( self ):
        inputs =  self.inputs
        codes = self.codes
        newPlayers = self.newPlayers
        shipChoices = self.shipChoices

        self.lastInputs = []
        self.codes = []
        self.newPlayers = []
        self.shipChoices = []

        return inputs, codes, newPlayers, shipChoices

    def getShutdownOrder( self ):
        return self.shutdownOrder

    def sendSysmsg( self, text ):
        pass

    def sendMsgall( self, text, senderName ):
        pass

    def sendMsg( self, text, senderName, playerCon ):
        pass
        
        
    def getClientFromPlayer( self, player ):
        client = None
        for k, v in self.players.items():
            if v == player:
                client = k
                break
                
        if not client:
           pass # print "client not found", self.players
           # raise Exception()
            
        return client

    def updatePlayer( self, player, objects, gfxs, stats, players, astres=[], possibles=[] ):
        client = self.getClientFromPlayer( player )  
        client.updatePlayer( objects, gfxs, stats, players, astres, possibles )
         
  #  def briefPlayer( self, pCon, astres ):
 #       client = self.getClientFromPlayer( player )  
  #      client.briefPlayer( objects, gfxs, stats, players, astres, possibles )

    def isConnected( self, player ):
        return self.getClientFromPlayer( player )
