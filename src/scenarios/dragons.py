from math import pi, sin, cos, ceil
from random import random

from scenarios import Scenario, Step
from server.objects import Asteroid, Planet, Sun
from server.ships import *
from server.weapons import *
from server.ais import *
from server.players import Faction
from server.stats import Stats

from common import utils

class Dragons( Scenario ):
    title = "Infestation"
    description = "There's an infestation of hostile creatures in the Zeta system. That system is an important source of minerals. Your mission is to clean it and make it safe to civilian miners. "
    year = 2278
    name = "Dragons"
        
    def __init__(self, game, steps=None, name=None, description=None, year=0):
    
        stats = Stats()
    #    stats.R_HUMAN.turrets = [ stats.T_SOLAR_0 ]
    #    stats.R_HUMAN.missiles = []
    #    stats.R_HUMAN.ships = []
        stats.PlayableShips = {}
        
        steps = []
        for i in xrange( 8 ):
            print i
            steps.append( Step( 
                goal=lambda self, game: not filter( lambda ship: ship.alive, self.ennemyShips ),
                onBegin=lambda self, game, stepNbr=i+1: self.stepFunction( game, stepNbr ),
                failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
                texts = [ (1,"Clear the area.")] )
                )
        
        Scenario.__init__(self, game, steps=steps, stats=stats )
        
        self.sol = Sun( game.stats.S_SOL, 4000, 0 )

        for i in range( 75 ): # asteroids
            asteroid = Asteroid( game, -2000, 0, 800 )
            game.harvestables.append( asteroid )
            
        game.astres = [ self.sol ]
        
        self.player = None
        self.startingPoint = ( -1000, 0 )
        
        self.ennemyPosition = ( -2000, 0 )
        self.ennemy = Faction( game.stats.R_EXTRA, "Unknown" )
        game.addPlayer( self.ennemy )
        
        self.infestedAsteroid = Asteroid( game, self.ennemyPosition[0], self.ennemyPosition[1], 0 )
        game.harvestables.append( self.infestedAsteroid )
        
        self.ennemyShips = []
        
    def addRandomNpc( self, game, race=None, loc=None ):
        pass

   # def doTurn( self, game ):
   #     Scenario.doTurn( self, game )
        
        
    def stepFunction( self, game, step ):
        print step
        nbrOfDragons = int(ceil(pow(1.5, step)))
        oreBonus = step*200
        energyBonus = step*100
        
        print nbrOfDragons, oreBonus, energyBonus
        
        self.addDragon( game, count=nbrOfDragons )
        if self.player.flagship:
            self.player.flagship.ore = min( self.player.flagship.stats.maxOre, self.player.flagship.ore + oreBonus )
            self.player.flagship.energy = min( self.player.flagship.stats.maxEnergy, self.player.flagship.energy + energyBonus )
        
    def addDragon( self, game, count=1 ):
        for i in xrange( count ):
            if i%2:
                stat = game.stats.EXTRA_FIGHTER
            else:
                stat = game.stats.EXTRA_BOMBER
            fighter = ShipSingleWeapon(self.ennemy, stat, AiPilotPolice(self.infestedAsteroid,800),self.infestedAsteroid.xp,self.infestedAsteroid.yp,-1, 2*pi*random(), 0.0,0.0,0.0, 0)
            game.objects.append( fighter )
            self.ennemyShips.append( fighter )
        
    def spawn( self, game, player, shipId=None ):
        print "spawning"
        
        player.race = game.stats.R_HUMAN
        shipStats = game.stats.HUMAN_FS_0

        (x,y) = self.startingPoint

        flagship = FlagShip( player, shipStats, AiCaptain( player ),x,y,0, 0, 0.0,0.0,0.0, 0)
        flagship.ore = flagship.stats.maxOre
        flagship.energy = 1000
        flagship.ori = 7/8*pi+pi/2
        
        for turret in flagship.turrets[2:4]:
            turret.buildInstall( game.stats.T_MASS_SR_1 )

        player.flagship = flagship        
        game.objects.append( flagship )

     #   self.player = player
        Scenario.spawn( self, game, player, shipId )
        
