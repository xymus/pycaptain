#!/usr/bin/python

import os
import sys
from math import pi

class Tests:
    def __init__( self, server=True, client=True ):
        self.testClient = client
        self.testServer = server
        
        self.scenarioNames = filter( 
            lambda f: len( f )>3 and f[-3:]==".py" and f[0]!="_", 
            os.listdir( os.path.join( sys.path[0], "scenarios" ) ) )
        self.scenarioNames = [ n[:-3] for n in self.scenarioNames]
        
        self.displayNames = filter( 
            lambda f: len( f )>3 and f[-3:]==".py" and f[0]!="_", 
            os.listdir( os.path.join( sys.path[0], "client", "displays" ) ) )
        self.displayNames = [ n[:-3] for n in self.displayNames]
        
        self.testImgPath = os.path.join( sys.path[0], "client", "imgs", "ships", "human-base.png" )

    def verbose( self, text, level=0 ):
        return "%s# %s" % ("  "*level, text)

    def forRun( self ):
        yield self.verbose( "Commons", 0 )
        yield self.verbose( "ids integrity", level=1 )
        from common import ids
        #TODO compare unique ids to detect repetition, not vital but may be useful for debugging

        if self.testClient:
            yield self.verbose( "Client", 0 )

            yield self.verbose( "Client sound mixer", level=1 )
            from client.mixer import Mixer
            mixer = Mixer()
            
            yield self.verbose( "Setting volume to mute", level=2 )
            mixer.setVolume(0)
            
            yield self.verbose( "Client displays", level=1 )
            for name in self.displayNames:
                yield self.verbose( name.capitalize(), level=2 )
                exec( "from client.displays.%s import %s as Display"%( name, name.capitalize() ) )
                #from client.display import Display
                display = Display( resolution=(100,100) )
                
                
                yield self.verbose( "Clearing", level=3 )
                display.beginDraw()
                display.clear( (0,255,0) )
                display.finalizeDraw()
                
                yield self.verbose( "Text", level=3 )
                display.beginDraw()
                display.drawText( "test", (4,4) )
                display.finalizeDraw()
                
                yield self.verbose( "Line", level=3 )
                display.beginDraw()
                display.drawLine( (255,255,255), (0,100), (100,0) )
                display.drawLine( (255,255,255), (0,0), (100,100) )
                display.finalizeDraw()
                
                yield self.verbose( "Circle", level=3 )
                display.beginDraw()
                display.drawCircle( (255,255,255), (50,50), 45 )
                display.finalizeDraw()
                
                yield self.verbose( "Loading image", level=3 )
                img = display.load( self.testImgPath )
                
                yield self.verbose( "Drawing image", level=3 )
                img = display.load( self.testImgPath )
                display.beginDraw()
                display.draw( img, (0,0) )
                display.finalizeDraw()
                
                yield self.verbose( "Drawing image rotated", level=3 )
                img = display.load( self.testImgPath )
                display.beginDraw()
                display.drawRo( img, (0,0), pi/3 )
                display.finalizeDraw()

            yield self.verbose( "Client resources", level=1 )

            yield self.verbose( "Images", level=2 )
            from client.imgs import Imgs, Image, Animation
            imgs = Imgs( display )
            yield self.verbose( "Loading images", level=3 )
            for p in imgs.loadAll( display ):
                pass
                
            yield self.verbose( "Drawing images", level=3 )
            import pygame # To be removed for other implementation
            for k, v in imgs.__dict__.items():
                if isinstance( v, Image ) or isinstance( v, pygame.Surface ):
                    display.beginDraw()
                    if isinstance( v, Image ):
                        display.draw( imgs[k], (0,0) )
                    if  isinstance( v, pygame.Surface ):
                        display.draw( v, (0,0) )
                    display.finalizeDraw()
                    
            yield self.verbose( "Drawing animations", level=3 )
            for k, v in imgs.__dict__.items():
                if isinstance( v, Animation ):
                    for j in xrange( 0, 500 ):
                        imgs.updateAnimations()
                        display.beginDraw()
                        display.draw( v, (0,0) )
                        display.finalizeDraw()

            yield self.verbose( "Sounds", level=2 )
            from client.snds import Snds
            
            yield self.verbose( "Loading sounds", level=3 )
            snds = Snds( mixer )
            for p in snds.loadAll( mixer ):
                pass
                
            yield self.verbose( "Playing sounds", level=3 )
            for k, v in snds.__dict__.items():
                if isinstance( v, pygame.mixer.Sound ):
                    mixer.play( v )

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

            yield self.verbose( "Scenarios", level=1 )
            
            yield self.verbose( "Loading empty scenario", level=2 )
            exec( "from scenarios.__scenario import Scenario as Scenario" )
            games.append( Game( Scenario ) )

            for name in self.scenarioNames:
                yield self.verbose( "Loading scenario %s"%name, level=2 )
                exec( "from scenarios.%s import %s as Scenario"%( name, name.capitalize() ) )
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

         #   yield self.verbose( "Turret instanciation", level=1 )

         #   yield self.verbose( "Turret building", level=1 )

         #   yield self.verbose( "Turret fire", level=1 )

         #   yield self.verbose( "AIs", level=1 )

            yield self.verbose( "Server", level=1 )
            from server.server import Server
            server = Server( scenarioName="Sol", force=True, adminPassword="password" )

            yield True

if __name__ == '__main__':
    from sys import argv

    if "server" in argv[1:]:
        print "Testing server"
        testServer = True
    else:
        testServer = False

    if "client" in argv[1:]:
        print "Testing client"
        testClient = True
    else:
        testClient = False
        
    if not testClient and not testServer:
        testServer = True
        testClient = True

    test = Tests( client=testClient, server=testServer )
    for res in test.forRun():
        if res: print res
        
    try:
        import psyco
        psyco.full()
        hasPsyco = True
    except ImportError:
        hasPsyco = False
        
    if hasPsyco:
        print "### retesting with psyco"
        test = Tests( client=testClient, server=testServer )
        for res in test.forRun():
            if res: print res
        
