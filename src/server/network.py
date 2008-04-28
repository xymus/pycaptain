from threading import Thread
from socket import SocketType, gethostname, gethostbyname
import socket
from time import sleep

import players
from common.comms import * # COInput, COObject, LoadCOInput, COObjects

from common import config

class PlayerConnection:
    def __init__( self, player, connection ):
        self.player = player
        self.connection = connection
        self.errors = 0
        self.authentified = False

    def auth( self, password ):
        if self.player.password == password:
            self.authentified = True
        return self.authentified

class Network:
    def __init__( self, game, addresses, port, versionString ):
        self.game = game
        self.versionString = versionString
        self.shutdownOrder = False

        self.connections = []
        self.playerCons = []

        self.sockets = []
        self.updating = {}

        self.socketsOpened = [] 
        for address in addresses:
          try:
            socket = SocketType()
            socket.setblocking(0)
            socket.bind( ( address, port ) )
            socket.listen( 10 )
            socket.setblocking( 0 )
            print "opened socket on %s:%i" % (address,port)
            self.sockets.append( socket )
            self.socketsOpened.append( address )

            tSocket = Thread( name="socket on %s:%i"%(address,port), target=self.fManageSocket, args=(socket,) )
            tSocket.start()
          except Exception, ex:
            print "failed to open socket on %s:"%address, ex[1]

        self.inputs = []
        self.codes = []
        self.newPlayers = []
        self.shipChoices = []

      #  self.tWork = Thread( name="network", target=self.fWork )
     #   self.tWork.start()

    def fManageSocket( self, socket ):
        while not self.shutdownOrder:
            try:
                nCon = socket.accept()

                print "connected with %s:%i" % nCon[1]
                nCon[ 0 ].setblocking(1)
                self.connections.append( nCon )
                nCon[0].send( "%s\n"%self.versionString )

                tConnection = Thread( name="connection with %s:%i"%nCon[1], target=self.fManageConnection, args=(nCon,) )
                tConnection.start()
            except Exception, ex:
            #    print "Exception in socket.accept()", ex
               pass
            sleep( 0.1 )

        try:
            socket.close()
        except Exception, ex:
            print "failed closing socket", ex

    def fManageConnection( self, con ):
        closing = False
        msgs = ""
        while not self.shutdownOrder and not closing:
           # msgs = ''
            tmpMsg = "a"
            while len(tmpMsg)==0 or tmpMsg[-1] != "\n": #len(tmpMsg) !=  0 and tmpMsg:
                try:
                    tmpMsg = con[ 0 ].recv( 1024 )
                    msgs = msgs + tmpMsg
                except:
                    tmpMsg = ""
             #   print "|"+msgs+"|"
            
            if len(msgs) > 0:
               for msg in msgs.splitlines():
         #        print "\"%s\"" % msg
                 words = msg.split()
                 word = words[0]


             ### login
                 if word == "user":
                     username = msg[ 5: ] 
                     player = self.game.getPlayer( username )
                     pCon = PlayerConnection( player, con )

                     if not pCon.player: # preparing to create player
                         pCon.tempUsername = username

                     self.playerCons.append( pCon )
                     print "user %s" % username

                 elif word == "pass":
                     password = msg[ 5: ] 
                     pCon = self.getPlayerConFromCon( con )

                     if not pCon:
                      #   print "unidentified pass"
                         con[0].send( "auth fail\n" )
                     else:
                     #    self.newPlayers.append( pCon.player )
                         if not pCon.player: # create player
                             pCon.player = self.game.addRemotePlayer( pCon.tempUsername, password)

                         if pCon.auth( password ):
                             self.newPlayers.append( pCon.player )
                             print "%s logged in!" % pCon.player.username
                             pCon.connection[0].send( "auth succ\n" )
                             self.sendSysmsg( "%s logged in!" % pCon.player.username )
                             pCon.player.justLoggedIn = True
                         #    self.briefPlayer( pCon )
                         else:
                             print "auth failed for %s" % pCon.player.username
                             self.playerCons.remove( pCon )
                             pCon.connection[0].send( "auth fail\n" )

             ### input uploads
                 elif word == "up":
              #       print "up %s" % msg[3:]
                     pCon = self.getPlayerConFromCon( con )
                     if pCon:
                         coInput = LoadCOInput( msg[3:] )
                         self.inputs.append( (pCon.player,coInput) )
                         pCon.errors = 0
                 elif word == "disconnecting":
                     pCon = self.getPlayerConFromCon( con )
                     if pCon:
                         pCon.connection[0].close()
                         self.playerCons.remove( pCon )
                         self.sendSysmsg( "%s disconnected" % pCon.player.username )
                         closing = True
                 elif word == "choice":
                     pCon = self.getPlayerConFromCon( con )
                     if pCon:
                         print "server: choice=", msg[len(word)+1:]
                         s = int(msg[len(word)+1:])
                         self.shipChoices.append( (pCon.player, s) )


             ### messaging
                 elif word == "msgall":
                     pCon = self.getPlayerConFromCon( con )
                     if pCon:
                         self.sendMsgall( msg[ len(word)+1: ], pCon.player.username )
               #     for pCon in self.playerCons:
               #         if pCon.connection == connection:
                 elif word == "msguser":
                     senderCon = self.getPlayerConFromCon( con )
                     pCon = self.getPlayerConFromUsername( words[1] )
                     if pCon:
                         self.sendMsgall( " ".join(words[2:]), senderCon.player.username, pCon )
                     

             ### admin functions
                 elif word == "shutdown":
                     self.shutdownOrder = True
                 elif word == "sysmsg":
                     self.sendSysmsg( msg[ len(word)+1: ] )
                 elif word == "adminmsg":
                     self.sendMsgall( msg[ len(word)+1: ], "admin" )
                 elif word == "code":
                     code = msg[ len(word)+1: ]
                     if code:
                         self.codes.append( code )
               msgs = ""
            sleep( 0.005 )

        if not closing:
            try:
                con[0].send( "shutdown\n" )
            except Exception, ex:
                print "failed pub shutdown", ex

            sleep( 0.1 )

        print "closing connection"
        try:
            con[0].close()
        except Exception, ex:
            print "failed closing socket", ex


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

    def getPlayerConFromCon( self, connection ):
        for pCon in self.playerCons:
            if pCon.connection == connection:
                return pCon
        return None

    def getPlayerConFromPlayer( self, player ):
        for pCon in self.playerCons:
            if pCon.player == player:
                return pCon
        return None

    def getPlayerConFromUsername( self, username ): # WARNING: kind of duplicates game.getPlayer( ... )
        for pCon in self.playerCons:
            if pCon.player.username == username:
                return pCon
        return None


    def sendSysmsg( self, text ):
        print( "sysmsg %s" % text )
        for pCon in self.playerCons:
          try:
            pCon.connection[0].send( "sysmsg %s\n" % (text) )
          except Exception, ex:
            print "failed sendSysmsg", ex

    def sendMsgall( self, text, senderName ):
        print( "msgall %s" % text )
        for pCon in self.playerCons:
          try:
            pCon.connection[0].send( "msgall %s %s\n" % (senderName,text) )
          except Exception, ex:
            print "failed sendSysmsg", ex

    def sendMsg( self, text, senderName, playerCon ):
        print( "msgall %s" % text )
        #pCon = getPlayerConFromPlayer( player )
        if playerCon: # for pCon in self.playerCons:
          try:
            playerCon.connection[0].send( "msg %s %s\n" % (senderName,text) )
          except Exception, ex:
            print "failed sendSysmsg", ex


   # def updatePlayer( self, player, objects, gfxs, stats, players ):
   #     if not self.updating[ player ]:
   #         self.updating[ player ] = True
   #         thread = Thread( name="update %s"%player.username, target=self.updatePlayerFThread, args=(player, objects, gfxs, stats, players) )
   #         thread.start()
    def updatePlayer( self, player, objects, gfxs, stats, players, astres=[], possibles=[] ):
        pCon = self.getPlayerConFromPlayer( player )
        if pCon:
          try:
            string = ""

            if objects:
                coobjects = COObjects( objects )
                string += "down %s\n"%coobjects.dump()

            string += "gfx %s\n"%gfxs.dump()
            string += "stats %s\n"%stats.dump()

            if players:
                coplayers = COPlayers( players )
                string += "players %s\n"%coplayers.dump()
            if astres:
                print len( astres )
                coastres = COObjects( astres )
                string += "astres %s\n"%coastres.dump()
            if possibles:
                copossibles = COPossibles( possibles )
                string += "possibles %s\n"%copossibles.dump()

            string += "downdone\n"

            pCon.connection[0].send( string )

          except socket.error, ex:
            if pCon.errors > config.fps*5:
               pCon.connection[0].close()
               self.playerCons.remove( pCon )
               self.sendSysmsg( "%s timedout" % pCon.player.username )
            pCon.errors += 1
            print "error in updatePlayer", ex
     #   self.updating[ player ] = False

    def briefPlayer( self, pCon, astres ):
        pCon = self.getPlayerConFromPlayer( player)
        if pCon:
             pCon.connection[0].send( "sysmsg %s\n" % astre.dump() )
             pCon.connection[0].send( "astres %s\n" % astres.dump() )

    def isConnected( self, player ):
        for pCon in self.playerCons:
            if player == pCon.player and pCon.authentified:
                return True
        return False

