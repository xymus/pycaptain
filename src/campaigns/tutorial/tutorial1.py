from math import pi, sin, cos
from random import randint, random

from scenarios import Scenario, Step
from server.objects import Asteroid, Planet, Sun
from server.ships import *
from server.weapons import *
from server.ais import *
from server.players import Computer
from server.stats import Stats

from common import utils

class Tutorial1( Scenario ):
    title = _("Tutorial 1 - manoeuvering and energy")
    description = _("Your mission is to investigate a strange sighting near Mars")
    year = 2275
    name = "Tutorial1"
        
    def __init__(self, game, steps=None, name=None, description=None, year=0):
    
        stats = Stats()
        stats.R_HUMAN.turrets = [ stats.T_SOLAR_0 ]
        stats.R_HUMAN.missiles = []
        stats.R_HUMAN.ships = []
        stats.PlayableShips = {}
        
        steps = [
            Step( 
                goal=lambda self, game: game.tick-9*config.fps>=self.lastStepAt and self.player.inputs.xc and not utils.distLowerThan( (self.player.inputs.xc+self.player.inputs.wc/2, self.player.inputs.yc+self.player.inputs.hc/2 ), self.player.flagship.pos, 200 ),
                failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
                texts = [ (0,_("Look around your ship a bit.")),
    (config.fps*3, _("To move the camera, either use the arrow keys...")),
    (config.fps*6, _("or click on the radar in the upper left corner."))] ),
            Step( 
                goal=lambda self, game: game.tick-6*config.fps>=self.lastStepAt and utils.distLowerThan( (self.player.inputs.xc+self.player.inputs.wc/2, self.player.inputs.yc+self.player.inputs.hc/2 ), self.player.flagship.pos, 2 ),
                failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
                texts = [ (0,_("Good, now stick the camera to your ship.")),
    (config.fps*3, _("To do so, click on the center of the radar.")),] ),
            Step( 
                goal=lambda self, game:  game.tick-9*config.fps>=self.lastStepAt and not utils.distLowerThan( self.startingPoint, self.player.flagship.pos, 100 ),
                failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
                texts = [ (0,_("Now move away from the orbital station.")),
      (3*config.fps, _("To move the ship, left-click on the destination and your crew will manoeuver towards there.") ),
      (6*config.fps, _("To give the order to stop, left-click on the ship.") ) ] ),
            Step( 
                goal=lambda self, game: filter( lambda turret: turret.building==stats.T_SOLAR_0, self.player.flagship.turrets ),
                failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
                texts = [ (0,_("Let's prepare ourselves before going out to explore.")),
          (3*config.fps, _("Jumping uses a lot of energy, so first build 2 solar arrays on your ship.") ),
          (6*config.fps, _("To do so, left-click on one of the black circle at the right of the screen.") ),           
          (9*config.fps, _("Then select the solar array from the list.") ) ] ),
            Step( 
                goal=lambda self, game: filter( lambda turret: turret.install and turret.install.stats==stats.T_SOLAR_0, self.player.flagship.turrets ),
                failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
                texts = [ (0,_("Well done, it will take a little while for it to be completed.")),
                          (3*config.fps, _("Begin building the second one right away.") ),
                          (9*config.fps, _("Notice the green bar in the top right corner...") ),
                          (12*config.fps, _("it indicates the proportion of energy in your battery.") ),
                          (15*config.fps, _("The quantity is indicated in green text next to it..") ) ] ),
            Step( 
                goal=lambda self, game: len(filter( lambda turret: turret.install and turret.install.stats==stats.T_SOLAR_0, self.player.flagship.turrets ) ) >= 2 and game.tick-6*config.fps>=self.lastStepAt,
                failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
                texts = [ (0,_("Every ship benefits from solar energy the closer they are to a sun.") ),
                    (3*config.fps,_("A solar array will capture even more solar energy but will consume a little when in deep space.") ) ] ),
            Step( 
                goal=lambda self, game: self.player.flagship.jumping,
                failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
                texts = [ (0,_("We still need to fill the battery before jumping.")),
                          (3*config.fps, _("Use the long-range sensor in fullscreen mode to see our destination.") ),
                          (6*config.fps, _("Left-click on the Radar button in the upper-left corner.") ),
                          (12*config.fps, _("Notice your poition over Earth. It will be useful to come back.") ),
                          (15*config.fps, _("Mars is the 4th planet from the sun.") ),
                          (18*config.fps, _("You can see it on the right of the asteroid field down left from you.")),
                          (21*config.fps, _("To execute the jump, left-click on the blue button at the top of the screen") ),
                          (24*config.fps, _("the left-click on the destination, the planet Mars.") ), ] ),
            Step( 
                goal=lambda self, game: not self.player.flagship.jumping,
                failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
                onBegin=lambda self, game: self.addEnnemyShip( game, self.ennemyPosition ),
                texts = [ ( 0, _("Know that you can change the destination of the jump while it charges.") ),
                          (3*config.fps, _("Go back to normal view by clicking on the radar button again.") ), ] ),
            Step( 
                goal=lambda self, game: utils.distLowerThan( self.ennemyPosition, self.player.flagship.pos, 500 ),
                failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
                texts = [ ( config.fps, _("Now head for the asteroid field.") ),
                    ( 4*config.fps, _("Reports are that there is a anormal rotating asteroid towards the bottom of the field.") ),
                    ( 7*config.fps, _("Investigate it.") ) ] ),
            Step( 
                goal=lambda self, game: utils.distLowerThan( self.ennemyPosition, self.player.flagship.pos, 200 ),
                failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
                texts = [ ( 0, _("It may be dangerous but get closer to gather data.") ) ] ),
            Step( 
                goal=lambda self, game: self.player.flagship.jumping,
                failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
                texts = [ ( 0, _("What ever it is. It is hostile!") ),
                    ( 1*config.fps, _("Enough data collected.") ),
                    ( 2*config.fps, _("Jump away now!") ) ] ),
            Step( 
                goal=lambda self, game: not self.player.flagship.jumping,
                failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
                texts = [ ( 0, _("Don't worry, your shield and hull should be able to handle the hits for a little longer.") ) ] ),
            Step( 
                goal=lambda self, game: utils.distLowerThanObjects( self.player.flagship, self.orbitalbase, 2000 ),
                failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
                texts = [ ( 1, _("Head back to Earth.") ) ] ),
            Step( 
                goal=lambda self, game: utils.distLowerThanObjects( self.player.flagship, self.orbitalbase, 100 ),
                failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
                texts = [ (0, _("Return to the orbital station.")),
                    ( 3*config.fps, _("Collected data will be useful if they ever try to get closer to Earth.") ) ] ),
                ]
        
        Scenario.__init__(self, game, steps=steps, stats=stats )
        
        ### redefining stats, dangerous
        
        self.sol = Sun( game.stats.S_SOL, 0, 0 )
        self.mercury = Planet( game.stats.P_MERCURY, -4100, 1400 )
        self.venus = Planet( game.stats.P_VENUS, 5000, 2300 )
        self.earth = Planet( game.stats.P_EARTH, -3100, 6700 )
        self.mars = Planet( game.stats.P_MARS_1, -7800, -2300 )
        self.moon = Planet( game.stats.P_MOON, -3900, 6400 )
        self.jupiter = Planet( game.stats.P_JUPITER, -13000, -4800 )
        self.saturn = Planet( game.stats.P_SATURN, 13000, 2500 )
        self.neptune = Planet( game.stats.P_NEPTUNE, 15000, 7000 )
        
        self.moon.zp = -50
        self.moon.yi = 0.1
        self.moon.orbiting = self.earth
        

        for i in range( 50 ): # asteroids outer self.mars
            dist = 9000
            angle = (1-2*random())*pi/8+pi*9/8
            asteroid = Asteroid( game, self.sol.xp+dist*cos(angle), self.sol.yp+dist*sin(angle), 300 )
            game.harvestables.append( asteroid )

        for i in range( 60 ): # asteroids between self.saturn and self.neptune
            dist = 15000
            angle = (1-2*random())*pi/10+pi/7
            asteroid = Asteroid( game, self.sol.xp+dist*cos(angle), self.sol.yp+dist*sin(angle), 300 )
            game.harvestables.append( asteroid )
            
        game.astres = [self.sol, self.mercury, self.venus, self.earth, self.moon, self.mars, self.jupiter, self.saturn, self.neptune, self.moon ]
        
        dist = self.earth.stats.maxRadius*1.5
        angle = 5*pi/8
        self.orbitalbase = OrbitalBase( None, game.stats.HUMAN_BASE_MINING, None, self.earth.xp+dist*cos(angle),self.earth.yp+dist*sin(angle))
        self.orbitalbase.ri = -0.013
        game.objects.append( self.orbitalbase )
        
        self.player = None
        self.startingPoint = ( self.orbitalbase.xp+50, self.orbitalbase.yp+60 )
        
        dist = 9000
        angle = pi*9/8+pi/8*2/3
        self.ennemyPosition = ( self.sol.xp+dist*cos(angle), self.sol.yp+dist*sin(angle) )
        
    def addRandomNpc( self, game, race=None, loc=None ):
        pass

    def doTurn( self, game ):
        Scenario.doTurn( self, game )
        
    def addEnnemyShip( self, game, (x,y), attackedShip=None ):
        player = Computer( game.stats.R_EXTRA, "Unknown" )
        flagship = OrbitalBase( player, game.stats.EXTRA_BASE, AiGovernor( player ),x,y)
        flagship.ore = flagship.stats.maxOre
        flagship.ri = -0.02
        
        for i in xrange( 9 ):
            fighter = ShipSingleWeapon(player, game.stats.EXTRA_FIGHTER, AiPilotFighter(flagship),0,0,0, 4, 0.0,0.0,0.0, 0)
            flagship.shipyards[ fighter.stats.img ].docked.append( fighter )
            
        if attackedShip:
            flagship.ai.attack( flagship, attackedShip )
            
     #   flagship.energy = 0
     #   flagship.shield = 0
     #   flagship.hull = flagship.stats.maxHull/4  
        
        player.flagship = flagship
        self.ennemyShip = flagship
        self.ennemy = player
        game.addPlayer( self.ennemy )
        game.objects.append( self.ennemyShip )
        
    def spawn( self, game, player, shipId=None ):
        Scenario.spawn( self, game, player, shipId )
        
        player.race = game.stats.R_HUMAN
        shipStats = game.stats.HUMAN_SCOUT

        (x,y) = self.startingPoint

        flagship = FlagShip( player, shipStats, AiCaptain( player ),x,y,0, 0, 0.0,0.0,0.0, 0)
        flagship.ore = flagship.stats.maxOre
        flagship.energy = 0
        flagship.ori = 7/8*pi+pi/2

        player.flagship = flagship        
        game.objects.append( flagship )

        player.needToUpdateRelations = True
        
