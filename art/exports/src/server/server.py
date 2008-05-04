#!/usr/bin/python

from time import sleep, time
from sys import argv, exit
from threading import Thread

from network import Network
from game import Game
from players import Player
import comms

import config


if "--help" in argv or "-h" in argv:
    print """Usage: %s [addresses]
addresses:\tList of addresses on which to open a listening socket (other of localhost, which is always being opened).""" % argv[0]
    exit()

class Server:
    def __init__( self, addresses=['localhost'] ):
        self.updatingPlayer = {}
        self.addresses = addresses 
        self.shutdown = False
        self.network = None
        self.game = Game()
        self.path = config.defaultPath
 
    def run(self):
      optimalFrame = 1.0/config.fps

      self.game.generateWorld()

      self.network = Network( self.game, self.addresses, config.port, comms.version )

      if not self.network.socketsOpened:
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
         try:
            cobj, stats, gfxs, players, astres, possibles = self.game.getUpdates( player )
         #   ty = time()
         #   print len(players)
            self.network.updatePlayer( player, cobj, gfxs, stats, players, astres, possibles )
            self.updatingPlayer[ player ] = False
         except Exception, ex:
            self.updatingPlayer[ player ] = False
            raise ex


try:
    import psyco
    psyco.full()
except ImportError:
    pass

if __name__ == '__main__':
    server = None
  #  try:
    if len( argv ) > 1:
        server = Server( argv[1:] )
    else:
        server = Server()
    server.run()
  #  except Exception, ex:
  #      if server and server.network:
  #          server.network.shutdown()
  #      raise ex

