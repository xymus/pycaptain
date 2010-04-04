from threading import Thread
from socket import SocketType, gethostname, gethostbyname, SHUT_RDWR
import socket
import errno
from time import sleep

import players
from common.comms import * # COInput, COObject, LoadCOInput, COObjects

from common import config

from converters.remote import RemoteConverter

class PlayerConnection:
    def __init__( self, player, connection ):
        self.player = player
        self.connection = connection
        self.errors = 0
        self.authentified = False
        self.loseConnection = False

    def auth( self, password ):
        if self.player.password == password:
            self.authentified = True
        return self.authentified

    def close( self ):
        self.loseConnection = True
        try:
        #    self.connection[0].shutdown( SHUT_RDWR )
            self.connection[0].close()
        except Exception, ex:
            print "Exception when closing connection with %s:"%self.player.name, ex

class Network:
    def __init__( self, game, addresses, port, versionString, adminPassword ):
        self.game = game
        self.versionString = versionString
        self.shutdownOrder = False
        self.adminPassword = adminPassword

        self.rawConnections = []
        self.playerCons = []

        self.sockets = []
        self.updating = {}

        self.socketsOpened = [] 
        self.listening = False

        ### open listener sockets
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
            self.listening = True

            tSocket = Thread( name="socket on %s:%i"%(address,port), target=self.threadListener, args=(socket,) )
            tSocket.start()
          except Exception, ex:
            print "failed to open socket on %s:"%address, ex[1]

        self.inputs = []
        self.codes = []
        self.newPlayers = []
        self.shipChoices = []
        
        
        self.converterType = RemoteConverter

      #  self.tWork = Thread( name="network", target=self.fWork )
     #   self.tWork.start()

    ### Listens to initail connection sockets
    def threadListener( self, socket ):
        while not self.shutdownOrder:
            try:
                nCon = socket.accept()

                print "connected with %s:%i" % nCon[1]
                nCon[ 0 ].setblocking(1)
                self.rawConnections.append( nCon )
                nCon[0].send( "%s\n"%self.versionString )

                tConnection = Thread( name="connection with %s:%i"%nCon[1],
                                      target=self.threadManageRawConnection,
                                      args=(nCon,) )
                tConnection.start()
            except Exception, ex:
               pass
            sleep( 0.1 )

        try:
            socket.close()
        except Exception, ex:
            print "failed closing socket", ex

    def threadManageRawConnection( self, con ):
        closing = False
        msgs = ""
        while not self.shutdownOrder and not closing:
            tmpMsg = "a"
            while len(tmpMsg)==0 or tmpMsg[-1] != "\n":
                try:
                    tmpMsg = con[ 0 ].recv( 1024 )
                    msgs = msgs + tmpMsg
                except IOError, ex:
                    if ex.errno == errno.EPIPE:
                        closing = True
                     
                    tmpMsg = ""
                except:
                    tmpMsg = ""
            
            if len(msgs) > 0:
               for msg in msgs.splitlines():
                 words = msg.split()
                 if len( words ) > 0:
                    word = words[0]
                 else:
                    continue


             ### login
                 if word == "user":
                     username = msg[ 5: ] 
                     player = self.game.getPlayer( username )
                     pCon = PlayerConnection( player, con )

                     if not pCon.player: # preparing to create player
                         pCon.tempUsername = username

                     self.playerCons.append( pCon )
                    # print "user %s" % username

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

                         if not pCon.auth( password ):
                             print "auth failed for %s" % pCon.player.username
                             self.playerCons.remove( pCon )
                             pCon.connection[0].send( "auth fail\n" )  
                         else:     
                             self.newPlayers.append( pCon.player )
                             pCon.connection[0].send( "auth succ\n" )
                             print "%s logged in!" % pCon.player.username
                             self.sendSysmsg( "%s logged in!" % pCon.player.username )
                             pCon.player.justLoggedIn = True
                                        
                             ### relay to managePlayerConnection
                             print "launching managePlayerConnection" 
                             self.managePlayerConnection( pCon )
                             print "managePlayerConnection done"
                             
                             ### high level ended, kill low level
                             closing = True

             ### admin functions
                # elif self.adminPassword and self.adminPassword == word[-1]:
                 elif word == "shutdown":
                     self.shutdownOrder = (not self.adminPassword or self.adminPassword == words[-1])
                 elif word == "sysmsg":
                     self.sendSysmsg( msg[ len(word)+1:-1 ] )
                 elif word == "adminmsg":
                     self.sendMsgall( msg[ len(word)+1:-1 ], "admin" )
                 elif word == "code":
                     code = msg[ len(word)+1:0 ]
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


    ### takes the relay of manage raw connection
    ### receives input from clients when connected
    ###   up -> gameplay input
    ###   disconnection notify
    ###   choise -> shipSelection
    def managePlayerConnection( self, playerCon ):
        closing = False
        msgs = ""
        while not self.shutdownOrder and not closing \
         and not playerCon.loseConnection:
        #    print "a"
            tmpMsg = "a"
            while len(tmpMsg)==0 or tmpMsg[-1] != "\n":
            #    print "b"
                try:
                    tmpMsg = playerCon.connection[ 0 ].recv( 1024 )
                    msgs = msgs + tmpMsg

                except IOError, ex:
                    if ex.errno == errno.EPIPE:
                        self.playerCons.remove( playerCon )
                        playerCon.close()
                        self.sendSysmsg( "%s timedout" % playerCon.player.username )
                    else:
                    #    playerCon.errors += 1
                        tmpMsg = ""
                except:
                    tmpMsg = ""
            
            if len(msgs) > 0:
               for msg in msgs.splitlines():
                 words = msg.split()
                 if len( words ) > 0:
                    word = words[0]
                 else:
                    continue

                ### debugging code displaying all inputs
                # print "xxxx", words


             ### input uploads
                 if word == "up":
                     coInput = LoadCOInput( msg[3:] )
                     self.inputs.append( (playerCon.player,coInput) )
                     playerCon.errors = 0
                 elif word == "disconnecting":
                     playerCon.connection[0].close()
                     self.playerCons.remove( playerCon )
                     self.sendSysmsg( "%s disconnected" % playerCon.player.username )
                     closing = True
                 elif word == "choice":
                     print "server: choice=", msg[len(word)+1:]
                     s = int(msg[len(word)+1:])
                     self.shipChoices.append( (playerCon.player, s) )

               msgs = ""
            sleep( 0.005 )


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

   # def sendMsg( self, sendAt, receivedAt, senderName, text, player ):
   #  #   print( "msgall %s" % text )
   #     pCon = getPlayerConFromPlayer( player )
   #     self.sendMsgPcon( text, senderName, pCon )
        
    def sendMsg( self, senderName, sendAt, receivedAt, text, pCon ):
        print( "sendMsg msg %s %i %i %s\n" % (senderName,sendAt,receivedAt,text) )
        if pCon: # for pCon in self.playerCons:
          try:
            pCon.connection[0].send( "msg %s %i %i %s\n" % (senderName,sendAt,receivedAt,text) )
          except Exception, ex:
            print "failed sendMsg", ex


   # def updatePlayer( self, player, objects, gfxs, stats, players ):
   #     if not self.updating[ player ]:
   #         self.updating[ player ] = True
   #         thread = Thread( name="update %s"%player.username, target=self.updatePlayerFThread, args=(player, objects, gfxs, stats, players) )
   #         thread.start()
    def updatePlayer( self, player, objects, gfxs, stats, players, astres=[], possibles=[], msgs=[], sysMsgs=[] ):
        pCon = self.getPlayerConFromPlayer( player )

        if pCon and pCon.loseConnection:
            print "WARNING pCon.loseConnection" 

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
                
            for msg in msgs:
                self.sendMsg( msg[0], msg[1], msg[2], msg[3], pCon )

            string += "downdone\n"

          ### debugging code displaying all outputs
          #  print "vvv", string

            pCon.connection[0].send( string )

          except IOError, ex:
            if ex.errno == errno.EPIPE:
         # except socket.error, ex:
            # broken pipe
          #  if ex[1] == 32 \
          #  or pCon.errors > config.fps*2:
                self.playerCons.remove( pCon )
                pCon.close()
                self.sendSysmsg( "%s timedout" % pCon.player.username )
                print "error in updatePlayer identified", ex
            else:
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

