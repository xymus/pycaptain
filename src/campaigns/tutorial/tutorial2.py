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

class Tutorial2( Scenario ):
    title = _("Tutorial 2 - ore and basic combat")
    description = _("Your mission is to collect 300 material from the asteroid close to the moon.")
    year = 2275.2
    name = "Tutorial2"
        
    def __init__(self, game, steps=None, name=None, description=None, year=0):
        
        stats = Stats()
        stats.R_HUMAN.turrets = [ stats.T_LASER_SR_1, stats.T_LASER_SR_0,
stats.T_MASS_SR_1, stats.T_MASS_SR_0, stats.T_MASS_MR_0 ]
        stats.R_HUMAN.missiles = []
        stats.R_HUMAN.ships = [ stats.HARVESTER ]
        stats.PlayableShips = {}
        
        steps = [
            Step( 
                goal=lambda self, game: utils.distLowerThanObjects( self.player.flagship, self.asteroid, 300 ),
                failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
             #   onBegin=lambda self, game: self.player.flagship.ore = 500,
                texts = [ (0, "We need some materials."),
                            (4*config.fps, "There is an asteroid close to the Moon."),
                            (8*config.fps, "Get close to it.") ] ),
            Step( 
                goal=lambda self, game: self.player.flagship.ai.launching[ self.player.race.defaultHarvester.img ],
                failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
                texts = [ (0, "Begin collecting raw ore."),
     (4*config.fps, "To do so, launch your harvester by pressing the blue arrow button at the bottom of the screen.") ] ),
            Step(
                goal=lambda self, game: self.player.flagship.oreProcess,
                failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
                texts = [ (0, "Now wait for them to bring back the ore."),
                (6*config.fps, "Don't worry about the ships following you around."),
                (10*config.fps, "They are civilian and while they are under your protection they speed up building processes.") ] ),
            Step( 
                goal=lambda self, game: self.player.flagship.ore >= 100,
                failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
                texts = [ (0, "They have now added the raw ore to the processing queue."),
                (4*config.fps, "Wait a little while and it will be transformed into usable materials."),
                (8*config.fps, "Keep harvesting and processing the ore until you reach 100 material."),
                (12*config.fps, "Notice the moving bars at the bottom right corner of the screen..."),
                (14*config.fps, "they represents the ore being processed."),
                (18*config.fps, "once they reach the right, they are usable!"),
                (22*config.fps, "They will then be added to the ore stock indicated by the blue gage in the bottom right corner."), ] ),
            Step( 
                goal=lambda self, game: self.player.flagship.shipyards[ self.player.race.defaultHarvester.img ].getCount() >= 4,
                failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
                texts = [ (0, "You now have enough material to build a new harvester and speed it up!"),
    (2*config.fps, "To do so, click on the icon of the harvester at the bottom of the screen, under the launch button.") ] ),
            Step( 
                goal=lambda self, game: self.player.flagship.ore >= 300,
                failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
                texts = [ (0, "Keep harvesting and processing ore util you reach 300 material."),
                (4*config.fps, "It will follow the orders the others already received."),
                (8*config.fps, "Notice the blue bar in the upper right corner and the green one in the bottm right..."),
                (12*config.fps, "the blue one represents your shield and the green one your hull.") ] ),
            Step( 
                goal=lambda self, game: len( filter( lambda turret: turret.install, self.player.flagship.turrets ) ) >= 3,
                failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
                texts = [ (0, "There are rumors of pirates in the area."),
                (4*config.fps, "Build one more mass cannon turret on your ship."),
                (8*config.fps, "To do so, click on an empty slot on the right of the screen and select an affordable turret."), ] ),
            Step( 
                goal=lambda self, game: not self.ennemyShip.alive,
                failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
                onBegin=lambda self, game: (self.addAttackingEnnemy( game, (self.moon.xp-1500,self.moon.yp-800), self.player.flagship, "Pirate lambda" ), game.setRelationBetween( self.player, self.ennemy, 1 )),
                texts = [ (0, "Defend yourself from the incoming pirate ship."),
                (4*config.fps, "To attack it, simply left-click on it once."),
                (8*config.fps, "Your crew will aim and fire the turrets."),
                (12*config.fps, "You can still help them by manoeuvering the ship so that the ennemy is in range of the turrets.") ] ),
            Step( 
                goal=lambda self, game: utils.distLowerThanObjects( self.player.flagship, self.orbitalbase, 100 ),
                failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
                texts = [ (0, "Well done!"),
                (2*config.fps, "Recall your harvester and return to the orbital base.") ] ),
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
        
        # asteroids over the moon, vital to scenario
        for i in xrange( 1 ):
            self.asteroid = Asteroid( game, self.moon.xp-200, self.moon.yp+150, 10 )
            game.harvestables.append( self.asteroid )
        
        for i in xrange( 3 ): # civilians around self.earth
            dist = randint( 100, 800 )
            angle = 2*pi*random()

            (x,y) = (self.earth.xp+dist*cos(angle), self.earth.yp+dist*sin(angle))
            s = Ship( game.stats.CIVILIAN_0, AiCivilian(), x, y, -20 )
            game.objects.append( s )

        for i in range( 50 ): # asteroids outer self.mars
            dist = 9000
            angle = (1-2*random())*pi/8+pi*9/8
            asteroid = Asteroid( game, self.sol.xp+dist*cos(angle), self.sol.yp+dist*sin(angle), 300 )
            game.harvestables.append( asteroid )

        game.astres = [self.sol, self.mercury, self.venus, self.earth, self.moon, self.mars, self.jupiter, self.saturn, self.neptune, self.moon ]
        
        dist = self.earth.stats.maxRadius*1.5
        angle = 5*pi/8
        self.orbitalbase = OrbitalBase( None, game.stats.HUMAN_BASE_MINING, None, self.earth.xp+dist*cos(angle),self.earth.yp+dist*sin(angle))
        self.orbitalbase.ri = -0.013
        game.objects.append( self.orbitalbase )
        
        self.player = None
        
    def addAttackingEnnemy( self, game, (x,y), attackedShip, attackerName ):
        player = Computer( game.stats.R_HUMAN, attackerName )
        flagship = FlagShip( player, game.stats.HUMAN_PIRATE, AiCaptain( player ),x,y )
        flagship.ore = flagship.stats.maxOre
        for t in flagship.turrets:
            t.buildInstall( game.stats.T_MASS_SR_1 )
        flagship.ai.attack( flagship, attackedShip )
      #  flagship.shield = 0
      #  flagship.hull = flagship.stats.maxHull/3  
        
        player.flagship = flagship
        self.ennemyShip = flagship
        self.ennemy = player
        game.addPlayer( self.ennemy )
        game.objects.append( self.ennemyShip )
        
    def addRandomNpc( self, game, race=None, loc=None ):
        pass

    def doTurn( self, game ):
        Scenario.doTurn( self, game )

    def spawn( self, game, player, shipId=None ):
        Scenario.spawn( self, game, player, shipId )
        
        player.race = game.stats.R_HUMAN
        shipStats = game.stats.HUMAN_CARGO

        (x,y) = ( self.orbitalbase.xp+50, self.orbitalbase.yp+60 )

        flagship = FlagShip( player, shipStats, AiCaptain( player ),x,y,0, 0, 0.0,0.0,0.0, 0)
        flagship.ore = 0
        flagship.energy = 0
        flagship.ori = 7/8*pi+pi/2

        flagship.turrets[1].buildInstall( game.stats.T_MASS_SR_0 )
        flagship.turrets[0].buildInstall( game.stats.T_MASS_MR_0 )

        player.flagship = flagship        
        game.objects.append( flagship )

        for i in xrange( 3 ):
           harvester = HarvesterShip(player, player.race.defaultHarvester, AiPilotHarvester(flagship), 0,0,0, 4, 0.0,0.0,0.0, 0)
           flagship.shipyards[ harvester.stats.img ].docked.append( harvester )

        player.needToUpdateRelations = True
        
