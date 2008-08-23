from scenarios import Scenario

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


class Sol( Scenario ):
    title = "Sol system"
    description = "Free play in Earth's solar system."
    year = 2523
    name = "Sol"
    
    def __init__(self, game):
        Scenario.__init__(self, game )

        self.harvestersAtSpawn = 4
        self.wantedBadGuys = 10

        self.sol = Sun( game.stats.S_SOL, 0, 0 )
        self.mercury = Planet( game.stats.P_MERCURY, -4100, 1400 ) # 4332
        self.venus = Planet( game.stats.P_VENUS, 5000, 2200 ) # 5462
        self.earth = Planet( game.stats.P_EARTH, -3100, 6700 ) # 7382
        self.mars = Planet( game.stats.P_MARS_1, -7800, -2200 ) # 8104
        self.moon = Planet( game.stats.P_MOON, -3900, 6400 )
        self.jupiter = Planet( game.stats.P_JUPITER, -12000, -4800 ) # 12924
        self.saturn = Planet( game.stats.P_SATURN, 13000, 2500 ) # 13238
        self.neptune = Planet( game.stats.P_NEPTUNE, 15000, 7000 ) # 16552

        self.moon.zp = -50
        self.moon.yi = 0.1
        self.moon.orbiting = self.earth

        self.blackHole = BlackHole( game.stats.BH_0, 10000, -10000 )
        
        for i in xrange( 10 ): # civilians around self.earth
            dist = randint( 100, 800 )
            angle = 2*pi*random()

            (x,y) = (self.earth.xp+dist*cos(angle), self.earth.yp+dist*sin(angle))
            s = Ship( game.stats.CIVILIAN_0, AiCivilian(), x, y, -20 )
            game.objects.append( s )

        for i in range( 60 ): # asteroids between self.saturn and self.neptune
            dist = 15000
            angle = (1-2*random())*pi/10+pi/7
            asteroid = Asteroid( game, self.sol.xp+dist*cos(angle), self.sol.yp+dist*sin(angle), 300 )
            game.harvestables.append( asteroid )

        for i in range( 50 ): # asteroids outer self.mars
            dist = 9000
            angle = (1-2*random())*pi/8+pi*9/8 # 2*random()*pi # 
            asteroid = Asteroid( game, self.sol.xp+dist*cos(angle), self.sol.yp+dist*sin(angle), 200 )
            game.harvestables.append( asteroid )

        game.astres = [self.sol, self.mercury, self.venus, self.earth, self.moon, self.mars, self.jupiter, self.saturn, self.neptune, self.moon, self.blackHole ]

        for i in xrange( self.wantedBadGuys ):
            self.addRandomNpc( game )


    def addRandomNpc( self, game, race=None, loc=None ):
      # position
      if loc:
          (x,y) = loc
      else:
        valid = False

        spots = []
        for o in game.astres:
          if isinstance( o, Planet ) and not isinstance( o, Sun ):
              spots.append( o )
        spot = choice( spots )

        while not valid:
          dist = randint( 100, 800 )
          angle = 2*pi*random()

          (x,y) = (spot.xp+dist*cos(angle), spot.yp+dist*sin(angle))

          valid = True
          for o in game.astres:
              if ( isinstance( o, Sun ) and distLowerThan( (x,y), (o.xp,o.yp), o.stats.damageRadius*1.2 )) \
                or (o.player and not isinstance( o.player, Computer ) and distLowerThan( (x,y), (o.xp,o.yp), 500 )):
                  valid = False
                  break

      # kind of npc
      i = randint( 1, 3 )

      player = GetComputerPlayer( game )
      if i < 2:
        flagship = FlagShip( player, game.stats.HUMAN_FS_0, AiCaptain( player ),x,y,0, 0, 0.0,0.0,0.0, 0)
        flagship.ore = flagship.stats.maxOre
        for t in flagship.turrets[2:4]:
            t.buildInstall( game.stats.T_LASER_MR_0 )
        for t in flagship.turrets[:2]+flagship.turrets[-2:]:
            t.buildInstall( game.stats.T_LASER_SR_0 )
            
      elif i < 3:
        flagship = FlagShip( player, game.stats.HUMAN_FS_2, AiCaptain( player ),x,y,0, 0, 0.0,0.0,0.0, 0)
        flagship.ore = flagship.stats.maxOre
        for t in flagship.turrets:
            t.buildInstall( game.stats.T_MASS_SR_0 )
        for i in range(10):
           fighter = ShipSingleWeapon(flagship.player, game.stats.HUMAN_FIGHTER, AiPilotFighter(flagship),0,0,0, 4, 0.0,0.0,0.0, 0)
           flagship.shipyards[ ids.S_HUMAN_FIGHTER ].docked.append( fighter )
        for i in range(4):
           harvester = HarvesterShip(player, player.race.defaultHarvester, AiPilotHarvester(flagship), 0,0,0, 4, 0.0,0.0,0.0, 0)
           flagship.shipyards[ harvester.stats.img ].docked.append( harvester )

      elif i < 4:
        flagship = FlagShip( player, game.stats.HUMAN_FS_1, AiCaptain( player ),x,y,0, 0, 0.0,0.0,0.0, 0)
        flagship.ore = flagship.stats.maxOre
        for t in flagship.turrets[:-2]:
            t.buildInstall( game.stats.T_MASS_MR_0 )
        for t in flagship.turrets[-2:]:
            t.buildInstall( game.stats.T_LASER_SR_0 )
        for i in range(4):
           harvester = HarvesterShip(player, player.race.defaultHarvester, AiPilotHarvester(flagship), 0,0,0, 4, 0.0,0.0,0.0, 0)
           flagship.shipyards[ harvester.stats.img ].docked.append( harvester )

      flagship.ore = 5000
      flagship.ori = 2*pi*random()
      player.flagship = flagship
      game.objects.append( flagship )
      game.addPlayer( player )


    def doTurn( self, game ):
        if not game.tick%(config.fps*5):
           ## manage npcs numbers
            npcCount = 0
            for o0 in game.objects.objects:
                if o0.player and isinstance( o0, FlagShip ) and isinstance( o0.player, Computer ):
                    npcCount = npcCount + 1

            for i in range( npcCount, self.wantedBadGuys ):
                self.addRandomNpc( game )


    def spawn( self, game, player, shipId ):
        player.race = game.stats.PlayableShips[ shipId ].race
        shipStats = game.stats.PlayableShips[ shipId ].stats

        dist = randint( 10, self.earth.stats.maxRadius )
        angle = 2*pi*random()
        (x,y) = ( self.earth.xp+dist*cos(angle), self.earth.yp+dist*sin(angle) )

        flagship = FlagShip( player, shipStats, AiCaptain( player ),x,y,0, 0, 0.0,0.0,0.0, 0)
        flagship.ore = flagship.stats.maxOre/2
        flagship.energy = flagship.stats.maxEnergy / 2
        flagship.ori = 2*pi*random()

        if player.race == game.stats.R_EVOLVED:
            smallTurret = game.stats.T_BURST_LASER_0
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

        if shipStats == game.stats.AI_FS_0 or shipStats == game.stats.AI_FS_1:
            for t in flagship.turrets[-3:-2] + flagship.turrets[-1:]:
                t.buildInstall( mediumTurret )
            for t in flagship.turrets[:1] + flagship.turrets[-2:-1]:
                t.buildInstall( smallTurret )
        else:
            for t in flagship.turrets[:2]:
                t.buildInstall( mediumTurret )
            for t in flagship.turrets[-2:]:
                t.buildInstall( smallTurret )

        player.flagship = flagship        
        game.objects.append( flagship )

        for i in xrange(self.harvestersAtSpawn):
           harvester = HarvesterShip(player, player.race.defaultHarvester, AiPilotHarvester(flagship), 0,0,0, 4, 0.0,0.0,0.0, 0)
           flagship.shipyards[ harvester.stats.img ].docked.append( harvester )

        player.needToUpdateRelations = True


