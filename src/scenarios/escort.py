from scenarios import Scenario
from scenarios.sol import Sol

from random import randint

from server.players import *
from server.ships import *
from server.objects import Object, Asteroid, Planet, Sun, Nebula, BlackHole
from server.weapons import *
from server.ais import *
from common.comms import * 
from common.utils import distBetweenObjects
from common import utils
from common.orders import *
from common.gfxs import * # temp
from common import ids
from common import config


class Escort( Sol ):
    title = "Escort"
    description = "Free play in Earth's solar system, with an escort of frigates!"
    year = 2523
    name = "Escort"
    
    def __init__(self, game):
        Sol.__init__(self, game )

    def spawn( self, game, player, shipId ):
        Sol.spawn( self, game, player, shipId )

        for i in xrange( 0, 5 ):
            frigate = Frigate( player, player.race.defaultFrigate, 
                               AiEscortFrigate( player ), player.flagship.xp+100, player.flagship.yp+100 )
            game.objects.append( frigate )

