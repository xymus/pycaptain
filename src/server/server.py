from time import sleep, time
from sys import argv, exit
from threading import Thread
from md5 import md5

from network import Network
from game import Game
from players import Player
from common import comms

from common import config

class Server:
    def __init__( self, scenarioName="Sol", addresses=['localhost'], port=config.port, force=False, private=False, adminPassword=None, networkType=Network ):
        # TODO implement private, port
        
        self.updatingPlayer = {}
        self.addresses = addresses
        self.private = private        
        self.force = force
        self.port = port
        self.networkType = networkType
        if adminPassword:
            self.adminPassword = md5(adminPassword).hexdigest()
        else:
            self.adminPassword = None
            print "Warning: no admin password set."

        self.shutdown = False
        self.network = None
      #  try:
        exec( "from scenarios.%s import %s as Scenario" % (scenarioName.lower(), scenarioName) )
      #  except ImportError:
      #      print ""
            
        self.game = Game( Scenario )
        self.path = config.defaultSavePath
 
    def run(self):
      optimalFrame = 1.0/config.fps

    #  self.game.generateWorld()

      self.network = self.networkType( self.game, self.addresses, config.port, comms.version, self.adminPassword )

      if not self.network.listening and not self.force:
          print "Failed to open any sockets, shutdown"
          self.shutdown = True
      else:
          print "ready"

      ts = []

      try:
          while not self.network.getShutdownOrder() and not self.shutdown:
              t0 = time()

             ### get inputs from self.network
              inputs, codes, newPlayers, shipChoices = self.network.getInputs()
              ta = time()

              for player in newPlayers:
                  self.updatingPlayer[ player ] = False
                  player.connect()
              #    print "adding", player

              for player, choice in shipChoices:
                  self.game.giveShip( player, choice )

             ### execute admin direct code input
              for code in codes:
                  print "executing %s"%code
                  try:
                      self.game.executeCode( code ) # eval( code )
                  except Exception, ex:
                      print "Failed admin code execution:", ex
              tb = time()

             ### do turn
              self.game.doTurn( inputs )
              tc = time()

             ### update remote players
              ty = tx = tz = 0
              for player in self.game.players:
               #   if isinstance( player, Player ) and self.network.isConnected( player ):
               #       print self.updatingPlayer.has_key( player ), player
                  if isinstance( player, Player ) and self.network.isConnected( player ) and self.updatingPlayer.has_key( player ) and not self.updatingPlayer[ player ]:
                      thread = Thread( name="update %s"%player.username, target=self.fUpdatePlayer, args=(player,) )
                      thread.start()
                      #tx = time()
                      #cobj, stats, gfxs = self.game.getUpdates( player )
                      #ty = time()
                      #self.network.updatePlayer
                      #tz = time()


             ### sleep and performance calculation
              t1 = time()
              t = (t1-t0)

              if __debug__:
                ts.insert(0, [t,ta-t0, tb-ta, tc-tb, ty-tx, tz-ty])
                if len( ts ) > config.fps*3:
                 ts.pop()
                 if not self.game.tick % config.fps*3:
                     s = [0,]*6
                     for v in ts:
                        for k, va in zip( xrange(len(v)), v):
                            s[k] += va
                     print "%.1ffps" % (float(len( ts ))/s[0])
                    # print "%.1ffps: ins:%i%% codes:%i%% self.game:%i%% ...ups [ get%i%%, up:%i%% ]"%(float(len( ts ))/s[0], s[1]*100/s[0], s[2]*100/s[0], s[3]*100/s[0],s[4]*100/s[0],s[5]*100/s[0])

              tts = optimalFrame - t
              if t < optimalFrame:
                  sleep( tts )
             # elif tts < -0.0015:
               #   self.network.sendSysmsg( "%.1ffps"%(1.0/t) )

      except KeyboardInterrupt:
          print "KeyboardInterrupt received"
     # except Exception, ex:
    #      self.network.shutdown()
     #     raise ex

      print "shutting down self.network" # shutdown order received, closing connections"
      self.network.shutdown()

     # print "saving self.game to %s" % path
     # self.game.saveToDisk( path )

    def fUpdatePlayer( self, player ):
            self.updatingPlayer[ player ] = True
  #       try:
            cobj, stats, gfxs, players, astres, possibles = self.game.getUpdates( player )
         #   ty = time()
         #   print len(players)
            self.network.updatePlayer( player, cobj, gfxs, stats, players, astres, possibles )
            self.updatingPlayer[ player ] = False
   #      except Exception, ex:
    #        self.updatingPlayer[ player ] = False
     #       raise ex


try:
    import psyco
    psyco.full()
except ImportError:
    pass

