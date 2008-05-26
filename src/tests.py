#!/usr/bin/python

class Tests:
    def __init__( self, server=True, client=True ):
        self.testClient = client
        self.testServer = server

    def verbose( self, text, level=0 ):
        return "%s# %s" % ("  "*level, text)

    def forRun( self ):
        yield self.verbose( "Commons", 0 )
        yield self.verbose( "ids integrity", level=1 )
        from common import ids
        #TODO compare unique ids to detect repetition, not vital but may be useful for debugging

        if self.testClient:
            yield self.verbose( "Client", 0 )
            yield self.verbose( "Client display", level=1 )
            from client.display import Display
            display = Display( resolution=(32,32) )

            yield self.verbose( "Client sound mixer", level=1 )
            from client.mixer import Mixer
            mixer = Mixer()

            yield self.verbose( "Client resources", level=1 )

            yield self.verbose( "Images", level=2 )
            from client.imgs import Imgs
            imgs = Imgs( display )
            for p in imgs.loadAll( display ):
                pass

            yield self.verbose( "Sounds", level=2 )
            from client.snds import Snds
            snds = Snds( mixer )
            for p in snds.loadAll( mixer ):
                pass

            yield self.verbose( "Texts", level=2 )
            from client.texts import Texts
            texts = Texts()
            for p in texts.loadAll():
                pass

        if self.testServer:
            yield self.verbose( "Server", 0 )
            yield self.verbose( "Server stats", level=1 )
            from server import stats

            yield self.verbose( "Game from Scenarios", level=1 )
            from server.game import Game
            games = []

            yield self.verbose( "Loading empty scenario", level=1 )
            exec( "from scenarios.scenario import Scenario as Scenario" )
            games.append( Game( Scenario ) )

            yield self.verbose( "Loading scenario Quad", level=2 )
            exec( "from scenarios.quad import Quad as Scenario" )
            games.append( Game( Scenario ) )

            yield self.verbose( "Loading scenario Sol", level=2 )
            exec( "from scenarios.sol import Sol as Scenario" )
            games.append( Game( Scenario ) )

            # yield self.verbose( "Game from Sol", level=1 )
            # from server.game import Game
            # game = Game( Scenario )

                
            yield self.verbose( "Players", level=1 )
            from server.players import Player

            yield self.verbose( "Computer", level=2 )
            from server.players import Computer
            playerComputer0 = Computer( stats.R_HUMAN, "computer human" )

            yield self.verbose( "Faction", level=2 )
            from server.players import Faction
            playerFaction0 = Faction( stats.R_AI, "faction ai" )

            yield self.verbose( "Human players", level=2 )
            from server.players import Human
            playerHuman0 = Human( stats.R_NOMAD, "human nomad" )



            yield self.verbose( "Objects", level=1 )
            from server.objects import Object

            yield self.verbose( "Asteroid", level=2 )
            from server.objects import Asteroid
            asteroids = []
            while len( asteroids ) < 100:
                asteroids.append( Asteroid( 0, 0, 100 ) )

            yield self.verbose( "Planet", level=2 )
            from server.objects import Planet
            planet0 = Planet( stats.P_EARTH, 100, 0 )

            yield self.verbose( "Sun", level=2 )
            from server.objects import Sun
            sun0 = Sun( stats.S_SOL, 5000, 0 )

            yield self.verbose( "Nebula", level=2 )
            from server.objects import Nebula
            nebula0 = Nebula( stats.A_NEBULA, -1000, 0 )

            yield self.verbose( "Blackhole", level=2 )
            from server.objects import BlackHole 
            blackhole0 = BlackHole( stats.BH_0, 0, 10000 )


            yield self.verbose( "Ships", level=2 )

            yield self.verbose( "Simple ship", level=3 )
            from server.ships import Ship
            ship0 = Ship( stats.FIGHTER, None, 0, 0 )

            yield self.verbose( "ShipWithTurrets", level=3 )
            from server.ships import ShipWithTurrets
            ship0 = ShipWithTurrets( None, stats.HARVESTER, None, 0, 0 )

            yield self.verbose( "Turret instanciation", level=1 )

            yield self.verbose( "Turret building", level=1 )

            yield self.verbose( "Turret fire", level=1 )

            yield self.verbose( "AIs", level=1 )

            yield self.verbose( "Server", level=1 )
            from server.server import Server
            server = Server( scenarioName="Scenario", force=True )

            yield True

if __name__ == '__main__':
    from sys import argv

    if "server" in argv[1:]:
        print "Testing only server"
        testClient = False
    else:
        testClient = True

#    if "client" in argv[1:]:
#        print "Testing only client"
#        testServer = False
#    else:
#        testServer = True

    
    test = Tests( client=testClient )
    for res in test.forRun():
        if res: print res

