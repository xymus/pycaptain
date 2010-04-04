#
# Author: Alexis Laferriere
# Description: Randomly generated scenario.
# 

from scenarios import Scenario, Step
from random import randint, choice, random

from server.players import *
from server.ships import *
from server.objects import Object, Asteroid, Planet, Sun, Nebula, BlackHole
from server.weapons import *
from server.ais import *
from common.comms import * 
from common.utils import distBetweenObjects, distBetweenObjects, distLowerThan
from common import utils
from common.orders import *
from common.gfxs import * # temp
from common import ids
from common import config

from common.config import universeWidth, universeHeight

class Randommultiple( Scenario ):
    title = "Random Multiple Systems"
    description = "A randomly generated scenario."
    year = 2544
    name = "RandomMultiple"


    
    def __init__( self, game, nSystems=3, nPlanets=12, nAsteroidFields=9 ):
    
        self.nSystems = nSystems
        self.nPlanets = nPlanets
        self.nAsteroidFields = nAsteroidFields

        self.distBetweenSuns = 30000
        self.distBetweenSunsMod = 4000
        self.planetDistFromSun = 9000 # also asteroids
        self.planetDistFromSunMod = 5000 # also asteroids
        self.minDistBetweenPlanets = 1000

        self.player = None

        self.harvestersAtSpawn = 4
        self.wantedBadGuys = 0

        Scenario.__init__(self, game )
        
        self.suns = []
        self.planets = []
        game.astres = []

        self.ennemyShips = []

        self.generate( game )


    def generate( self, game ):

        ### systems ###
        for s in xrange( self.nSystems ):
            if s == 0:
                ## first sun
                pos = ( randint(-1*universeWidth+self.distBetweenSuns, universeWidth-self.distBetweenSuns), 
                        randint(-1*universeHeight+self.distBetweenSuns, universeHeight-self.distBetweenSuns) )
            else:
                ## others
                ## find another spot
                pos, orbitable = self.getPosition( self.suns, self.distBetweenSuns, self.distBetweenSunsMod, self.suns, self.distBetweenSuns-self.distBetweenSunsMod, self.distBetweenSunsMod/2 )

            sun = Sun( game.stats.S_SOL, pos[0], pos[1] )

            self.suns.append( sun )
            game.astres.append( sun )

        ### planets ###
        for p in xrange( self.nPlanets ):
            pos, sun = self.getPosition( self.suns, self.planetDistFromSun, self.planetDistFromSunMod, self.planets, self.minDistBetweenPlanets, self.minDistBetweenPlanets )

            planet = Planet( choice( game.stats.planets ), pos[0], pos[1] )

            self.planets.append( planet )
            game.astres.append( planet )


        ### asteroids fields ###
        for af in xrange( self.nAsteroidFields ):

            if randint( 0, 4 ) == 0:
                ## around planet
                orbited = choice( self.planets )
                radius = orbited.stats.radius*2.5
                radiusMod = orbited.stats.radius/3
                count = 20
                minAngle = 0
                maxAngle = 2*pi
            else:
                ## around a sun / in a system
                orbited = choice( self.suns )
                radius = randint( self.planetDistFromSun-self.planetDistFromSunMod,
                                  self.planetDistFromSun+self.planetDistFromSunMod ) 
                radiusMod = randint( 100, 300 )

                size = randint( 10, 70 ) # %!
                count = size*3
                minAngle = random()*2*pi
                maxAngle = minAngle + 2*pi*size/100

            self.fillAsteroidField( game, orbited, radius, radiusMod, count, minAngle, maxAngle )

        game.astres = self.planets + self.suns


    def getPosition( self, orbitableTargets, dist, distMod, toAvoid, minDistWithToAvoid, border ):
        valid = False
        while not valid:
            orbitable = choice( orbitableTargets )

            radius = randint( dist-distMod, dist+distMod )
            angle = random()*pi*2

            pos = ( orbitable.xp+radius*cos(angle),
                    orbitable.yp+radius*sin(angle) )

            ## validity test
                ## within universe limits
                ## and not too close to any other sun
            valid = pos[0] < universeWidth-border \
                and pos[0] > -1*universeWidth+border \
                and pos[1] < universeHeight-border \
                and pos[1] > -1*universeHeight+border \
                and not filter( lambda o: distLowerThan( pos, o.pos, minDistWithToAvoid ), toAvoid )

        return pos, orbitable


    def fillAsteroidField( self, game, orbited, dist, distMod, count, minAngle, maxAngle ):
        print "field: ", game, orbited, dist, distMod, count, minAngle, maxAngle
        for i in xrange( count ):
            radius = randint( int(dist-distMod), int(dist+distMod) )
            angle = minAngle+random()*(maxAngle-minAngle)
            asteroid = Asteroid( game, orbited.xp+radius*cos(angle), orbited.yp+radius*sin(angle), 0 )
            game.harvestables.append( asteroid )


    def spawn( self, game, player, shipId ):
        player.race = game.stats.PlayableShips[ shipId ].race
        shipStats = game.stats.PlayableShips[ shipId ].stats

        planet = choice( self.planets )
        dist = randint( 10, planet.stats.maxRadius )
        angle = 2*pi*random()
        (x,y) = ( planet.xp+dist*cos(angle), planet.yp+dist*sin(angle) )

        flagship = FlagShip( player, shipStats, AiCaptain( player ),x,y,0, 0, 0.0,0.0,0.0, 0)
        flagship.ore = flagship.stats.maxOre/2
        flagship.energy = flagship.stats.maxEnergy / 2
        flagship.ori = 2*pi*random()
        
        if player.race == game.stats.R_EVOLVED:
            smallTurret = game.stats.T_ESPHERE_0
            mediumTurret = game.stats.T_SUBSPACE_WAVE_0
        elif player.race == game.stats.R_NOMAD:
            smallTurret = game.stats.T_REPEATER_1
            mediumTurret = game.stats.T_NOMAD_CANNON_0
        elif player.race == game.stats.R_AI:
            smallTurret = game.stats.T_AI_FLAK_1
            mediumTurret = game.stats.T_AI_OMNI_LASER_0
        else:
            smallTurret = game.stats.T_MASS_SR_0
            mediumTurret = game.stats.T_MASS_MR_0

        for t in flagship.turrets[:2]:
            t.buildInstall( mediumTurret )
            
        for t in flagship.turrets[-2:]:
            t.buildInstall( smallTurret )
            
        player.flagship = flagship
        
        game.objects.append( flagship )

        for i in range(self.harvestersAtSpawn):
           harvester = HarvesterShip(player, player.race.defaultHarvester, AiPilotHarvester(flagship), 0,0,0, 4, 0.0,0.0,0.0, 0)
           flagship.shipyards[ harvester.stats.img ].docked.append( harvester )

        Scenario.spawn( self, game, player, shipId=shipId )

        for i in xrange( 0, 3 ):
            frigate = Frigate( player, player.race.defaults[ ids.B_FRIGATE ], 
                               AiEscortFrigate( player ), x+100, y+100 )
            game.objects.append( frigate )

