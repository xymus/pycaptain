#!/usr/bin/python

# TODO

def verbose( text, level=0 ):
    print "%s# %s" % ("  "*level, text)

verbose( "ids integrity" )
from common import ids
# compare unique ids to detect repetition, not vital but may be useful for debugging

verbose( "Server stats" )
from server import stats

verbose( "Client display" )
from client.display import Display
display = Display()

verbose( "Client sound mixer" )
from client.mixer import Mixer
mixer = Mixer()

verbose( "Client resources" )

verbose( "Images", level=1 )
from client.imgs import Imgs
imgs = Imgs( display )
imgs.loadAll( display )

verbose( "Sounds", level=1 )
from client.snds import Snds
snds = Snds( mixer )
snds.loadAll( mixer )

verbose( "Texts", level=1 )
from client.texts import Texts
texts = Texts()
texts.loadAll()

verbose( "Game from Scenarios" )
from server.game import Game
games = []

verbose( "Loading empty scenario" )
exec( "from scenarios.scenario import Scenario as Scenario" )
games.append( Game( Scenario ) )

verbose( "Loading scenario Quad", level=1 )
exec( "from scenarios.quad import Quad as Scenario" )
games.append( Game( Scenario ) )

verbose( "Loading scenario Sol", level=1 )
exec( "from scenarios.sol import Sol as Scenario" )
games.append( Game( Scenario ) )

# verbose( "Game from Sol" )
# from server.game import Game
# game = Game( Scenario )

    
verbose( "Players" )
from server.players import Player

verbose( "Computer", level=1 )
from server.players import Computer
playerComputer0 = Computer( stats.R_HUMAN, "computer human" )

verbose( "Faction", level=1 )
from server.players import Faction
playerFaction0 = Faction( stats.R_AI, "faction ai" )

verbose( "Human players", level=1 )
from server.players import Human
playerHuman0 = Human( stats.R_NOMAD, "human nomad" )



verbose( "Objects" )
from server.objects import Object

verbose( "Asteroid", level=1 )
from server.objects import Asteroid
asteroids = []
while len( asteroids ) < 100:
    asteroids.append( Asteroid( 0, 0, 100 ) )

verbose( "Planet", level=1 )
from server.objects import Planet
planet0 = Planet( stats.P_EARTH, 100, 0 )

verbose( "Sun", level=1 )
from server.objects import Sun
sun0 = Sun( stats.S_SOL, 5000, 0 )

verbose( "Nebula", level=1 )
from server.objects import Nebula
nebula0 = Nebula( stats.A_NEBULA, -1000, 0 )

verbose( "Blackhole", level=1 )
from server.objects import BlackHole 
blackhole0 = BlackHole( stats.BH_0, 0, 10000 )


verbose( "Ships", level=1 )

verbose( "Simple ship", level=2 )
from server.ships import Ship
ship0 = Ship( stats.FIGHTER, None, 0, 0 )

verbose( "ShipWithTurrets", level=2 )
from server.ships import ShipWithTurrets
ship0 = ShipWithTurrets( None, stats.HARVESTER, None, 0, 0 )

verbose( "Turret instanciation" )

verbose( "Turret building" )

verbose( "Turret fire" )

verbose( "AIs" )

verbose( "Server" )
from server.server import Server
server = Server( scenarioName="Scenario", force=True )


