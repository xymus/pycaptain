from time import sleep, time
from sys import argv, exit
from threading import Thread
from md5 import md5

from network import Network
from game import Game
from players import Player, Human
from common import comms, config, ids
from common.comms import version

from converters.remote import RemoteConverter
from converters.local import LocalConverter

class Server:
    def __init__( self, Scenario=None, scenarioName="Dragons", addresses=['localhost'], port=config.port, force=False, private=False, adminPassword=None, networkType=Network, game=None ):
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
        
        if not Scenario:
            exec( "from scenarios.%s import %s as Scenario" % (scenarioName.lower(), scenarioName) )
            
        if game:
            self.game = game
        #    if Scenario:
                
        else:
            self.game = Game( Scenario )
            
        self.path = config.defaultSavePath
        
        self.converter = None
        
        global ty, tx, tz
        ty = tx = tz = 0
 
    def run(self):
      optimalFrame = 1.0/config.fps

      self.network = self.networkType( self.game, self.addresses, self.port, version, self.adminPassword )
      self.converter = self.network.converterType() # load according to network type

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
              online = False
              for player in self.game.players:
                  if isinstance(player, Human) and self.network.isConnected(player):
                      online = True
                      break

              if online:
                  self.game.doTurn( inputs )

              tc = time()

             ### update remote players
              for player in self.game.players:
                  if isinstance( player, Human ) and self.network.isConnected( player ) and self.updatingPlayer.has_key( player ) and not self.updatingPlayer[ player ]:
                      thread = Thread( name="update %s"%player.username, target=self.fUpdatePlayer, args=(player,) )
                      thread.start()

             ### sleep and performance calculation
              t1 = time()
              t = (t1-t0)

              if __debug__:
                ts.insert(0, [t,ta-t0, tb-ta, tc-tb, t1-tc, ty-tx, tz-ty])
                if len( ts ) > config.fps*3:
                 ts.pop()
                 if not self.game.tick % config.fps*3:
                     s = [0,]*7
                     for v in ts:
                        for k, va in zip( xrange(len(v)), v):
                            s[k] += va
                     print "%.1ffps" % (float(len( ts ))/s[0])
                   #  print "%.1ffps: ins:%i%% codes:%i%% self.game:%i%% up t:%i%%...ups [ get%i%%, up:%i%% ]"%(float(len( ts ))/s[0], s[1]*100/s[0], s[2]*100/s[0], s[3]*100/s[0],s[4]*100/s[0],s[5]*100/s[0], s[6]*100/s[0])

              tts = optimalFrame - t
              if t < optimalFrame:
                  sleep( tts )
              elif tts < -0.0015:
                  self.network.sendSysmsg( "%.1ffps"%(1.0/t) )

      except KeyboardInterrupt:
          print "KeyboardInterrupt received"
     # except Exception, ex:
    #      self.network.shutdown()
     #     raise ex

      print "shutting down self.network" # shutdown order received, closing connections"
      self.network.shutdown()

    def fUpdatePlayer( self, player ):
            self.updatingPlayer[ player ] = True
  #       try:
            global tx
            tx = time()
            
            cobj, stats, gfxs, players, astres, possibles, msgs = self.converter.convert( self.game, player )
            
           # for msg in player.msgs:
           #     self.network.sendSysmsg( "%s@%s..%s: %s" % (msg.sender.username, msg.sentAt, msg.receivedAt, msg.text) )
           # player.msgs = []
                
           # for msg in self.game.scenario.msgs:
           #     self.network.sendSysmsg( msg )
           # self.game.scenario.msgs = []
            
            global ty
            ty = time()
            self.network.updatePlayer( player, cobj, gfxs, stats, players, astres, possibles, msgs=msgs )
            self.updatingPlayer[ player ] = False
            
            global tz
            tz = time()
   #      except Exception, ex:
    #        self.updatingPlayer[ player ] = False
     #       raise ex


try:
    import psyco
    psyco.full()
except ImportError:
    pass

