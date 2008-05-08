#!/usr/bin/python

# TODO

def verbose( level=0, text ):
    print "%s# %s" % (" "*level, text)

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

verbose( level=1, "Images" )
from client.imgs import Imgs
imgs = Imgs( display )
imgs.loadAll( display )

verbose( level=1, "Sounds" )
from client.snds import Snds
snds = Snds( mixer )
snds.loadAll( mixer )

verbose( level=1, "Texts" )
from client.texts import Texts
texts = Texts()
texts.loadAll()

verbose( "Scenarios" )
verbose( level=1, " Loading empty scenario" )
exec( "from scenarios.%s import %s as Scenario" % (scenarioName.lower(), scenarioName) )

verbose( level=1, " Loading scenario Quad" )
exec( "from scenarios.quad import Quad as Scenario" )

verbose( level=1, " Loading scenario Sol" )
exec( "from scenarios.sol import Sol as Scenario" )

verbose( "Game from Sol" )
self.game = Game( Scenario )

verbose( "Object instanciation" )

verbose( "Ship instanciation" )

verbose( "Turret instanciation" )

verbose( "Turret building" )

verbose( "Turret fire" )


verbose( "Server" )
from server.server import Server
server = Server( scenarioName="Scenario", force=True )


