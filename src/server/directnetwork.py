from threading import Thread
from socket import SocketType, gethostname, gethostbyname
import socket
from time import sleep

import players
from common.comms import *
from common import config

from network import Network, PlayerConnection

from converters.local import LocalConverter

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
        
        self.msgusers = []
        self.msgalls = []
        self.sysmsgs = []

        self.listening = True
      #  self.tWork = Thread( name="network", target=self.fWork )
     #   self.tWork.start()
        self.converterType = LocalConverter
     
    def connect( self, client ):
        self.clients.append( client )
        
    def up( self, client, inputs ):
        self.inputs.append( (self.players[ client ],inputs) )

    def login( self, client, username ):
        player = self.game.getPlayer( username )
        
        if not player:
            print "player not found"
            player = self.game.addRemotePlayer( username, "")
            
        self.players[ client ] = player
        self.newPlayers.append( player )
        print "logged in %s for %s" % ( username, client )
    
    def disconnect( self, client ):
        print self.clients, client, self.clients.count( client )
        
        if self.clients.count( client ):
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
        self.sysmsgs.append( text )

    def sendMsgall( self, text, senderName ):
        self.msgalls.append( "%s: %s"%(senderName, text) )

    def sendMsg( self, text, senderName, playerCon ):
        self.msgalls.append( "%s: %s"%(senderName, text) ) # TODO reimplement if multiple players can connect to directnetwork
        
        
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
        if self.sysmsgs:
            print self.sysmsgs
        client.updatePlayer( objects, gfxs, stats, players, astres, possibles, self.msgalls, self.msgusers, self.sysmsgs )
        self.msgalls = []
        self.msgusers = []
        self.sysmsgs = []
        
         
  #  def briefPlayer( self, pCon, astres ):
 #       client = self.getClientFromPlayer( player )  
  #      client.briefPlayer( objects, gfxs, stats, players, astres, possibles )

    def isConnected( self, player ):
        return self.getClientFromPlayer( player )

