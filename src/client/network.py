from threading import Thread
from socket import SocketType
import socket
from time import sleep, time

from common.comms import * # COObject, COInput, LoadCOObject, LoadCOObjects, LoadCOPlayerStatus, LoadCOGfxs

class Network:
    def __init__(self, server, port, username, hashedPassword, version ):
        self.server = server
        self.port = port
        self.username = username
        self.hashedPassword = hashedPassword
        self.version = version
        self.timeout = 0.05
        self.lag = 0


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
        
    def connect(self):
        self.connSocket = Thread( name="connect attempt on %s:%i"%(self.server, self.port), target=self.fConnect )
        self.connSocket.start()
    def fConnect( self ):
        self.connectState = (None,"connecting to server")
        self.socket = SocketType()
        try:
            self.socket.setblocking(2)
            self.socket.connect( (self.server, self.port) )
        except Exception, ex:
            self.connectState = (False,ex[1])
            return None
        
        self.connectState = (None,"waiting for server version")
        sleep( 0.1 )
        msgs = self.socket.recv( 32 )
        if not len( msgs ):
            self.connectState = (False,"unable to get server version")
            return None

        lines = msgs.splitlines()
        serverVersion = lines[0]

        if serverVersion != self.version:
            self.connectState = (False,"Different versions, client: %s, server: %s" % ( self.version, serverVersion ))
            return None
            
        self.connectState = (None,"sending user and password")
        self.socket.send( "user %s\n" % self.username )
        self.socket.send( "pass %s\n" % self.hashedPassword )
        self.connectState = (None,"waiting for server answer to authentification")
        msgs = self.socket.recv( 10 )
        self.socket.setblocking( 1 )

        success =  "auth succ" in msgs.splitlines()

        if not success:
            self.connectState = (False,msgs.splitlines()[0])
            return None

        self.tSocket = Thread( name="socket on %s:%i"%(self.server, self.port), target=self.fManageConnection )
        self.tSocket.start()
        self.connectState = (True,"connection established")
        print "fConnect thread done"
    def getConnectState( self ):
        return self.connectState
      #  if self.tSocket:
      #      return (True,"") # success
      #  else:
      #      return (None,"") # wait
      #  else:
      #      return (False,"") # failed


    def sendInputs(self, inputs):
        try:
          self.socket.send( "up %s\n" % inputs.dump() )
        except Exception, ex:
          print "Failed sendInputs", ex

    def sendShipChoice(self, s):
        try:
          print "choice %i\n" % s
          self.socket.send( "choice %i\n" % s )
        except Exception, ex:
          print "Failed sendShipChoice", ex

    def fManageConnection( self ):

        lastReceptionAt = time()
        msgs = ""
        while not self.shutdown: # and self.lag<self.timeout:
          tmpMsg = "a"
          error = False
          while (len(tmpMsg)==0 or tmpMsg[-1] != "\n") and not self.shutdown:
              try:
                  tmpMsg = self.socket.recv( 1024 )
                  msgs = msgs + tmpMsg
 
                  t = time()
                  self.lag = t-lastReceptionAt
                  lastReceptionAt = t
              except:
                  error = True
                  tmpMsg = ""
                  if len(msgs) > 0 and msgs[-1] != "\n":
                      sleep( 0.005)
    
          if len(msgs) > 0 and not self.shutdown:
            for msg in msgs.splitlines():
              if len(msg):
             #   print "msg", msg
                try:
                    firstSpace = msg.index( " " )
                except:
                    firstSpace = len(msg) #print "network: invalid msg", msg
                  #  continue

                word = msg[ :firstSpace ]

             #   print word
                if word == "shutdown":
                    print "server shutting down"
                    self.shutdown = True
                elif word == "bump":
                    self.bump = True
                elif word == "sysmsg":
                    words = msg.split()
                    self.sysmsgs.append( msg[len(word)+1:] )
                elif word == "msg":
                    words = msg.split()
                    print self, words
                    self.msgusers.append( ( words[1], int(words[2]), int(words[3]), " ".join(words[4:]) ) )
                elif word == "down":
                    try:
                        self.objects = LoadCOObjects( msg[len(word)+1:] ).coobjects
                    except (socket.error,ValueError), ex:
                        print "loading object failed, string:", msg[5:]
                elif word == "stats":
                  #  try:
                        self.stats = LoadCOPlayerStatus( msg[len(word)+1:] )
                 #   except Exception, ex:
                  #     print "loading stats failed, string:", msg[6:], ex
                elif word == "players":
                    try:
                        self.players = LoadCOPlayers( msg[len(word)+1:] ).players
                    except Exception, ex:
                       print "loading players failed, string:", msg[6:], ex
                elif word == "astres":
                    try:
                        self.astres = LoadCOObjects( msg[len(word)+1:] ).coobjects
                    except Exception, ex:
                        print "loading astres failed, string:", msg[6:], ex
                elif word == "gfx":
                    try:
                        self.gfxs = LoadCOGfxs( msg[len(word)+1:] )
                    except Exception, ex:
                        print "loading gfxs failed, string:", msg[4:], ex
                elif word == "possibles":
                    try:
                        self.possibles = LoadCOPossibles( msg[len(word)+1:] ).ships
                    except Exception, ex:
                        print "loading possibles failed, string:", msg[6:], ex
                elif word == "downdone":
                    sleep( 0.01)
          msgs = ''

     #   t = time()-timeStartWaiting
     #   if t>self.timeout*0.9:
     #        self.lag = self.lag + t
     #   else:
     #        self.lag = 0


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

       # self.bump = False
        self.msgusers = []
        self.sysmsgs = []
        self.objects =  []
      #  self.astres =  []
        self.gfxs =  []
        self.players =  None
      #  self.stats = None
      #  self.possibles = []

        return ( shutdown, bump, msgusers, sysmsgs, objects, astres, gfxs, stats, players, possibles )
    
    def pubQuit(self):
        try:
            self.socket.send( "disconnecting\n" )
            sleep( 0.2 )
        except Exception, ex:
            print "failed pubQuit:", ex

    def sendMsguser( self, text, destName ):
        try:
            self.socket.send( "msguser %s %s\n" % (senderName,text) )
        except Exception, ex:
            print "failed sendSysmsg", ex

    def close(self):
        try:
            self.socket.shutdown( socket.SHUT_RDWR )
            self.socket.close()
        except Exception, ex:
            print "failed close:", ex

def join(lists):
    return "".join(lists)




