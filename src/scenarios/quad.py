#
# Author: Alexis Laferriere
# Description: First scenario with 4 solar systems, sol at the center.
# 

from scenario import Scenario
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
from server import stats

class Quad ( Scenario ):
    def __init__( self, game ):

        self.harvestersAtSpawn = 4
        self.wantedBadGuys = 5

        sol = Sun( stats.S_SOL, 0, 0 )
        mercury = Planet( stats.P_MERCURY, -4100, 1400 )
        venus = Planet( stats.P_VENUS, 5000, 2200 )
        self.earth = Planet( stats.P_EARTH, -3100, 6700 )
        self.mars = Planet( stats.P_MARS, -7800, -2200 )
        moon = Planet( stats.P_MOON, -3900, 6400 )
        jupiter = Planet( stats.P_JUPITER, -12000, -4800 )
        saturn = Planet( stats.P_SATURN, 13000, 2500 )
        neptune = Planet( stats.P_NEPTUNE, 15000, 7000 )

        moon.zp = -50
        moon.yi = 0.1
        moon.orbiting = self.earth

        for i in xrange( 20 ): # civilians around self.earth
            dist = randint( 100, 800 )
            angle = 2*pi*random()

            (x,y) = (self.earth.xp+dist*cos(angle), self.earth.yp+dist*sin(angle))
            s = Ship( stats.CIVILIAN_0, AiCivilian(), x, y, -20 )
            game.objects.append( s )

        for i in range( 60 ): # asteroids between saturn and neptune
            dist = 15000
            angle = (1-2*random())*pi/10+pi/7
            asteroid = Asteroid( sol.xp+dist*cos(angle), sol.yp+dist*sin(angle), 300 )
            game.harvestables.append( asteroid )

        for i in range( 30 ): # asteroids outer self.mars
            dist = 9000
            angle = (1-2*random())*pi/8+pi*9/8
            asteroid = Asteroid( sol.xp+dist*cos(angle), sol.yp+dist*sin(angle), 200 )
            game.harvestables.append( asteroid )


        nebula = Nebula( stats.A_NEBULA, 4800, 500 )
        for i in range( 15 ): # asteroids in nebula
            asteroid = Asteroid( 4800, 800, 800 )
            game.harvestables.append( asteroid )


        self.alphaCentaury = [ Sun( stats.S_SOL, -32000, 16000 ),
                          Planet( stats.P_MARS_2, -28300, 12000 ),
                          Planet( stats.P_SATURN_1, -39000, 8000 ) ]
        for i in range( 40 ): # asteroids around self.alphaCentaury
            dist = 4600
            #angle = 2*pi*i/50
            angle = (1-2*random())*pi/4-pi/8
            asteroid = Asteroid( self.alphaCentaury[0].xp+dist*cos(angle), self.alphaCentaury[0].yp+dist*sin(angle), 200 )
            game.harvestables.append( asteroid )


        self.beta = [ Sun( stats.S_SOL, 8000, -24000 ),
                 Planet( stats.P_MARS_1, 12000, -22000 ),
                 Planet( stats.P_X, 500, -21000 ) ,
                 Planet( stats.P_JUPITER_1, 17000, -24700 )]
        for i in range( 20 ): # asteroids around self.beta[1]
            dist = 600
            angle = 2*pi*random()
            asteroid = Asteroid( self.beta[1].xp+dist*cos(angle), self.beta[1].yp+dist*sin(angle), 80 )
            game.harvestables.append( asteroid )

        self.gamma = [Sun( stats.S_SOL, 40000, 4000 ),
                 Planet( stats.P_MERCURY_1, 39000, -2200 ),
                 Planet( stats.P_X_1, 38000, 11500 ) ]
        for i in range( 20 ): # asteroids around self.gamma[1]
            dist = 750
            angle = 2*pi*random()
            asteroid = Asteroid( self.gamma[1].xp+dist*cos(angle), self.gamma[1].yp+dist*sin(angle), 80 )
            game.harvestables.append( asteroid )
        for i in range( 100 ): # asteroids around self.gamma
            area = choice( [(7000, 300, 5*pi/8, pi/9), (10000, 400, 6*pi/8, pi/8), (12000, 500, 5*pi/8, pi/11) ] ) # , 3000
            dist = area[0] #randint( area[0]-area[1], area[0]+area[1] )
            angle = area[2]+area[3]*(1-2*random())
            asteroid = Asteroid( self.gamma[0].xp+dist*cos(angle), self.gamma[0].yp+dist*sin(angle), area[1] )
            game.harvestables.append( asteroid )

        nebula2 = Nebula( stats.A_NEBULA_2, 8000, -16000 )

        blackHole0 = BlackHole( stats.BH_0, -30000, -20000 )


#        for i in range( 15 ):
 #           asteroid = Asteroid( -7000, -3200, 800 )
 #           game.objects.append( asteroid )

  #      for i in range( 15 ):
   #         asteroid = Asteroid( 8500, 6800, 800 )
     #       game.objects.append( asteroid )
        self.sol = [sol, mercury, venus, self.earth, moon, self.mars, jupiter, saturn, neptune, nebula, nebula2 ]
        game.astres = [sol, mercury, venus, self.earth, moon, self.mars, jupiter, saturn, neptune, nebula, nebula2, blackHole0 ] + self.alphaCentaury + self.beta + self.gamma
     #   game.objects = game.objects #  + [sol, mercury, venus, self.earth, moon, self.mars, jupiter, saturn, neptune, nebula, nebula2 ] + self.alphaCentaury + self.beta

        for i in range( 5 ):
            self.addRandomNpc( game )

        spots = []
        for o in game.astres:
          if isinstance( o, Planet ) and not isinstance( o, Sun ):
            spots.append( o )

        for i in xrange( 30 ): # random civilians
            spot = choice( spots )
            dist = randint( 100, 800 )
            angle = 2*pi*random()

            (x,y) = (spot.xp+dist*cos(angle), spot.yp+dist*sin(angle))
            s = Ship( stats.CIVILIAN_0, AiCivilian(), x, y, -20 )
            game.objects.append( s )



        self.marsDefense = Faction( stats.R_HUMAN, "Mars Defenses" )
        obase = OrbitalBase( self.marsDefense, stats.ORBITALBASE, AiGovernor( self.marsDefense ),self.mars.xp+self.mars.stats.maxRadius*1.5,self.mars.yp+self.mars.stats.maxRadius*1.5,0, 0, 0.0,0.0,0.0, 0)
        for t in obase.turrets:
            t.install = TurretInstall( stats.T_MASS_SR_0 )
            t.weapon = MassWeaponTurret( stats.W_MASS_SR_0 )
            t.ai = AiWeaponTurret()
        obase.orbiting = self.mars
        obase.yi = 1
        obase.ore = obase.stats.maxOre
        obase.ri = -0.008
        game.objects.append( obase )

        for i in xrange( 20 ):
            radius = self.mars.stats.maxRadius*(2.5)
            dist = self.mars.stats.maxRadius*(1.5+1*random())
            angle = 2*pi*random() # AiPilotDefense
            fighter = ShipSingleWeapon(self.marsDefense, stats.FIGHTER, AiPilotDefense(self.mars,radius),self.mars.xp+dist*cos(angle),self.mars.yp+dist*sin(angle),0, 4, 0.0,0.0,0.0, 0)
            game.objects.append( fighter )
            self.marsDefense.ships.append( fighter )

        self.marsDefense.bases.append( obase )
        game.addPlayer( self.marsDefense )


        self.earthDefense = Faction( stats.R_HUMAN, "Earth Defenses" )
        nbrBases = 3
        for i in xrange( nbrBases ):
          dist = self.earth.stats.maxRadius*1.8 #(1.8+0.4*random())
          angle = pi*i*2/nbrBases
          obase = OrbitalBase( self.earthDefense, stats.ORBITALBASE, AiGovernor( self.earthDefense ),self.earth.xp+dist*cos(angle),self.earth.yp+dist*sin(angle),0, 0, 0.0,0.0,0.0, 0)
          for t in obase.turrets:
            t.install = TurretInstall( stats.T_MASS_MR_0 )
            t.weapon = MassWeaponTurret( stats.W_MASS_MR )
            t.ai = AiWeaponTurret()
          obase.ori = angle+pi/2
          obase.orbiting = self.earth
          obase.xi = cos( obase.ori)
          obase.yi = sin( obase.ori)
          obase.ore = obase.stats.maxOre
          obase.ri = -0.008
          game.objects.append( obase )
          self.earthDefense.bases.append( obase )

        for i in xrange( 20 ):
            radius = self.earth.stats.maxRadius*(2.5)
            dist = self.earth.stats.maxRadius*(1.5+1*random())
            angle = 2*pi*random() # AiPilotDefense
            fighter = ShipSingleWeapon(self.earthDefense, stats.FIGHTER, AiPilotPolice(self.earth,radius),self.earth.xp+dist*cos(angle),self.earth.yp+dist*sin(angle),0, 4, 0.0,0.0,0.0, 0)
            game.objects.append( fighter )
            self.earthDefense.ships.append( fighter )

        self.earthDefense.bases.append( obase )
        game.addPlayer( self.earthDefense )

       ## ai forces
        self.addAiBase( game, "Neptune base", neptune )
        self.addAiBase( game, "Saturn base", saturn )
        self.addAiBase( game, "Jupiter base", jupiter, 2 )


       ## Evolved
        self.evolvedSwarm0 = Faction( stats.R_EVOLVED, "First Swarm", territories=[Territory((self.alphaCentaury[ 1 ].xp, self.alphaCentaury[ 1 ].yp), 500), Territory((self.alphaCentaury[ 1 ].xp-1000, self.alphaCentaury[ 1 ].yp-500), 500)] )

        (x,y) = self.alphaCentaury[ 1 ].xp-self.alphaCentaury[ 1 ].stats.maxRadius*1.5,self.alphaCentaury[ 1 ].yp+self.alphaCentaury[ 1 ].stats.maxRadius*1.5
        flagship = FlagShip( self.evolvedSwarm0, stats.EVOLVED_FS_1, AiCaptain( self.evolvedSwarm0 ),x,y,0, 0, 0.0,0.0,0.0, 0)
        flagship.ore = flagship.stats.maxOre
        for t in flagship.turrets[:-2]:
            t.install = TurretInstall( stats.T_MASS_MR_0 )
            t.weapon = MassWeaponTurret( stats.W_MASS_MR )
            t.ai = AiWeaponTurret()
        for t in flagship.turrets[-2:]:
            t.install = TurretInstall( stats.T_LASER_SR_0 )
            t.weapon = LaserWeaponTurret( stats.W_LASER_SR )
            t.ai = AiWeaponTurret()
        for i in range(4):
           harvester = HarvesterShip(self.evolvedSwarm0, self.evolvedSwarm0.race.defaultHarvester, AiPilotHarvester(flagship), 0,0,0, 4, 0.0,0.0,0.0, 0)
           flagship.shipyards[ harvester.stats.img ].docked.append( harvester )

        for i in xrange( 5 ):
            if i>=3:
                fighter = ShipSingleWeapon(self.evolvedSwarm0, stats.EVOLVED_BOMBER, AiPilotFighter(flagship),0,0,0, 4, 0.0,0.0,0.0, 0)
            else:
                fighter = ShipSingleWeapon(self.evolvedSwarm0, stats.EVOLVED_FIGHTER, AiPilotFighter(flagship),0,0,0, 4, 0.0,0.0,0.0, 0)

        for i in xrange( 10 ):
            fighter = ShipSingleWeapon(self.evolvedSwarm0, stats.EVOLVED_FIGHTER, AiPilotDefense(flagship, 500),0,0,0, 4, 0.0,0.0,0.0, 0)
            (fighter.xp,fighter.yp) = (flagship.xp,flagship.yp)
            game.objects.append( fighter )
            self.evolvedSwarm0.ships.append( fighter )
        #    flagship.shipyards[ fighter.stats.img ].docked.append( fighter )
        game.objects.append( flagship )
        self.evolvedSwarm0.flagships.append( flagship )
        game.addPlayer( self.evolvedSwarm0 )


      ## Extra TODO remove section
        self.extraRock0 = Faction( stats.R_EXTRA, "Rocks" )
        for i in xrange( 0 ): # 4 ):
          angle = 2*pi*random()
          dist = 750 # self.gamma[ 1 ].stats.maxRadius*
          (x,y) = self.gamma[ 1 ].xp-dist*cos(angle),self.gamma[ 1 ].yp+dist*sin(angle)

          if i%4==0:
              flagship = FlagShip( self.extraRock0, stats.EXTRA_FS_0, AiCaptain( self.extraRock0 ),x,y,0, 0, 0.0,0.0,0.0, 0)
              for k,t in enumerate(flagship.turrets):
                  t.install = TurretInstall( stats.T_ROCK_THROWER_1 )
                  t.weapon = MassWeaponTurret( stats.W_ROCK_THROWER_1 )
                  t.ai = AiWeaponTurret()
          elif i%4==1:
              flagship = FlagShip( self.extraRock0, stats.EXTRA_FS_1, AiCaptain( self.extraRock0 ),x,y,0, 0, 0.0,0.0,0.0, 0)
              for k,t in enumerate(flagship.turrets):
                  t.install = TurretInstall( stats.T_DRAGON_0 )
                  t.weapon = MassWeaponTurret( stats.W_DRAGON_0 )
                  t.ai = AiWeaponTurret()
          elif i%4==2:
              flagship = FlagShip( self.extraRock0, stats.EXTRA_FS_0, AiCaptain( self.extraRock0 ),x,y,0, 0, 0.0,0.0,0.0, 0)
              for k,t in enumerate(flagship.turrets):
                  t.install = TurretInstall( stats.T_LARVA_0 )
                  t.weapon = MissileWeaponTurret( stats.W_LARVA_0 )
                  t.ai = AiWeaponTurret()
          else:
              flagship = FlagShip( self.extraRock0, stats.EXTRA_FS_2, AiCaptain( self.extraRock0 ),x,y,0, 0, 0.0,0.0,0.0, 0)
              for i in xrange( 8 ):
                  fighter = ShipSingleWeapon(self.extraRock0, stats.EXTRA_FIGHTER, AiPilotFighter(flagship),0,0,0, 4, 0.0,0.0,0.0, 0)
                  flagship.shipyards[ fighter.stats.img ].docked.append( fighter )

          flagship.ore = flagship.stats.maxOre

          game.objects.append( flagship )
          self.extraRock0.flagships.append( flagship )
          flagship.missiles[ ids.M_LARVA ].amount = 100
      #  game.addPlayer( self.extraRock0 )

        for i in xrange( 16 ):
          self.addRandomExtra( game )


      #  game.harvestables = game.harvestables[:10]


  #  def addRandomNpc( self, game, race=None, loc=None ):
  #      pass


    def addRandomNpc( self, game, pos=None, i=None ):

      # position
      if pos:
          (x,y) = pos
      else:
        valid = False

        spots = []
        for o in self.sol:
          if isinstance( o, Planet ) and not isinstance( o, Sun ) and o != self.earth and o != self.mars:
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
      if not i:
          i = randint( 1, 3 )

      player = GetComputerPlayer()
      if i < 2:
        flagship = FlagShip( player, stats.FLAGSHIP_0, AiCaptain( player ),x,y,0, 0, 0.0,0.0,0.0, 0)
        flagship.ore = flagship.stats.maxOre
        for t in flagship.turrets[2:4]:
            t.buildInstall( stats.T_LASER_MR_0 )
        for t in flagship.turrets[:2]+flagship.turrets[-2:]:
            t.buildInstall( stats.T_LASER_SR_0 )

      elif i < 3:
        flagship = FlagShip( player, stats.FLAGSHIP_2, AiCaptain( player ),x,y,0, 0, 0.0,0.0,0.0, 0)
        flagship.ore = flagship.stats.maxOre
        for t in flagship.turrets:
            t.buildInstall( stats.T_MASS_SR_0 )
        for i in range(10):
           fighter = ShipSingleWeapon(flagship.player, stats.FIGHTER, AiPilotFighter(flagship),0,0,0, 4, 0.0,0.0,0.0, 0)
           flagship.shipyards[ ids.S_FIGHTER ].docked.append( fighter )
        for i in range(4):
           harvester = HarvesterShip(player, player.race.defaultHarvester, AiPilotHarvester(flagship), 0,0,0, 4, 0.0,0.0,0.0, 0)
           flagship.shipyards[ harvester.stats.img ].docked.append( harvester )

      elif i < 4:
        flagship = FlagShip( player, stats.FLAGSHIP_1, AiCaptain( player ),x,y,0, 0, 0.0,0.0,0.0, 0)
        flagship.ore = flagship.stats.maxOre
        for t in flagship.turrets[:-2]:
            t.buildInstall( stats.T_MASS_MR_0 )
        for t in flagship.turrets[-2:]:
            t.buildInstall( stats.T_LASER_SR_0 )
        for i in range(4):
           harvester = HarvesterShip(player, player.race.defaultHarvester, AiPilotHarvester(flagship), 0,0,0, 4, 0.0,0.0,0.0, 0)
           flagship.shipyards[ harvester.stats.img ].docked.append( harvester )

      flagship.ori = 2*pi*random()
      player.flagship = flagship
      game.objects.append( flagship )
      game.addPlayer( player )
        

    def doTurn( self, game ):
        if not game.tick%(config.fps*5):
           ## manage npcs numbers
            npcCount = 0
            for o0 in game.objects:
                if o0.player and isinstance( o0, FlagShip ) and isinstance( o0.player, Computer ):
                    npcCount = npcCount + 1

            for i in range( npcCount, self.wantedBadGuys ):
                if randint(0,1):
                    self.addRandomNpc( game )
                else:
                    self.addRandomExtra( game )

           ## TODO manage earth defenses / numbers


    def addAiBase( self, game, name, orbited, count=1 ):

      player = Faction( stats.R_AI, name )

      for i in xrange(count):
        dist = orbited.stats.maxRadius*1.5
        angle = 2*pi*random()

        obase = OrbitalBase( player, stats.AI_BASE, AiGovernor( player ), orbited.xp+dist*cos(angle),orbited.yp+dist*sin(angle),0, 0, 0.0,0.0,0.0, 0)
        for i,t in enumerate(obase.turrets):
          if i<len(obase.turrets)/2:
            t.install = TurretInstall( stats.T_LASER_MR_1 )
            t.weapon = LaserWeaponTurret( stats.W_LASER_MR_1 )
            t.ai = AiWeaponTurret()
          else:
            t.install = TurretInstall( stats.T_AI_MISSILE_0 )
            t.weapon = MissileWeaponTurret( stats.W_AI_MISSILE )
            t.ai = AiWeaponTurret()
        obase.orbiting = orbited
        obase.yi = 1
        obase.ore = obase.stats.maxOre
        obase.ri = -0.004
        obase.missiles[ ids.M_AI ].amount = 500
        game.objects.append( obase )

        for i in xrange( 8 ):
            if i>=6:
                fighter = ShipSingleWeapon(player, stats.AI_BOMBER, AiPilotFighter(obase),0,0,0, 4, 0.0,0.0,0.0, 0)
            else:
                fighter = ShipSingleWeapon(player, stats.AI_FIGHTER, AiPilotFighter(obase),0,0,0, 4, 0.0,0.0,0.0, 0)
            obase.shipyards[ fighter.stats.img ].docked.append( fighter )

        player.bases.append( obase )
      game.addPlayer( player )

    def addRandomExtra( self, game, count=1 ):

        player = Faction( stats.R_EXTRA, "Rocks" )
        for k in xrange( count ):
          t = randint( 0, 4 )

          area = choice( 
		[	(750, 50, pi, pi, self.gamma[1].xp, self.gamma[1].yp), 
			(7000, 300, 5*pi/8, pi/9, self.gamma[0].xp, self.gamma[0].yp), 
			(10000, 400, 6*pi/8, pi/8, self.gamma[0].xp, self.gamma[0].yp), 
			(12000, 500, 5*pi/8, pi/11, self.gamma[0].xp, self.gamma[0].yp) 
		] )
          dist = randint( area[0]-area[1], area[0]+area[1] )
          angle = area[2]+area[3]*(1-2*random())

         # angle = 2*pi*random()
         # dist = 750
          (x,y) = area[4]-dist*cos(angle),area[5]+dist*sin(angle)

          if t%4<2: # rock throwing asteroid # mixed
              flagship = FlagShip( player, stats.EXTRA_FS_0, AiCaptain( player ),x,y,0, 0, 0.0,0.0,0.0, 0)
              for k,t in enumerate(flagship.turrets[:-1]):
                  t.install = TurretInstall( stats.T_ROCK_THROWER_1 )
                  t.weapon = MassWeaponTurret( stats.W_ROCK_THROWER_1 )
                  t.ai = AiWeaponTurret()
              for k,t in enumerate(flagship.turrets[-1:]):
                  t.install = TurretInstall( stats.T_LARVA_0 )
                  t.weapon = MissileWeaponTurret( stats.W_LARVA_0 )
                  t.ai = AiWeaponTurret()
          elif t%4==1: # 3 headed dragon
              flagship = FlagShip( player, stats.EXTRA_FS_1, AiCaptain( player ),x,y,0, 0, 0.0,0.0,0.0, 0)
              for k,t in enumerate(flagship.turrets):
                  t.install = TurretInstall( stats.T_DRAGON_0 )
                  t.weapon = MassWeaponTurret( stats.W_DRAGON_0 )
                  t.ai = AiWeaponTurret()
       #   elif i%4==2: # larva launching asteroid
       #       flagship = FlagShip( player, stats.EXTRA_FS_0, AiCaptain( self.extraRock0 ),x,y,0, 0, 0.0,0.0,0.0, 0)
       #       for k,t in enumerate(flagship.turrets):
       #           t.install = TurretInstall( stats.T_LARVA_0 )
       #           t.weapon = MissileWeaponTurret( stats.W_LARVA_0 )
       #           t.ai = AiWeaponTurret()
          else: # abandoned flagship
              flagship = FlagShip( player, stats.EXTRA_FS_2, AiCaptain( player ),x,y,0, 0, 0.0,0.0,0.0, 0)
              for i in xrange( 8 ):
                  fighter = ShipSingleWeapon(player, stats.EXTRA_FIGHTER, AiPilotFighter(flagship),0,0,0, 4, 0.0,0.0,0.0, 0)
                  flagship.shipyards[ fighter.stats.img ].docked.append( fighter )

          for i in range(2):
             harvester = HarvesterShip(player, player.race.defaultHarvester, AiPilotHarvester(flagship), 0,0,0, 4, 0.0,0.0,0.0, 0)
             flagship.shipyards[ harvester.stats.img ].docked.append( harvester )

          flagship.ore = flagship.stats.maxOre

          game.objects.append( flagship )
          player.flagships.append( flagship )
          flagship.missiles[ ids.M_LARVA ].amount = 100
        game.addPlayer( player )

    def spawn( self, game, player, shipId ):
    #  if not player.flagship and player.points >= stats.PlayableShips[ shipId ].points:
        player.race = stats.PlayableShips[ shipId ].race
        shipStats = stats.PlayableShips[ shipId ].stats

        dist = randint( 10, self.earth.stats.maxRadius )
        angle = 2*pi*random()
        (x,y) = ( self.earth.xp+dist*cos(angle), self.earth.yp+dist*sin(angle) )

        flagship = FlagShip( player, shipStats, AiCaptain( player ),x,y,0, 0, 0.0,0.0,0.0, 0)
        flagship.ore = flagship.stats.maxOre/2
        flagship.energy = flagship.stats.maxEnergy / 2
        flagship.ori = 2*pi*random()
        
        if player.race == stats.R_EVOLVED:
            smallTurret = stats.T_BURST_LASER_0
            mediumTurret = stats.T_SUBSPACE_WAVE_0
        elif player.race == stats.R_NOMAD:
            smallTurret = stats.T_REPEATER_1
            mediumTurret = stats.T_NOMAD_CANNON_0
        elif player.race == stats.R_AI:
            smallTurret = stats.T_AI_FLAK_1
            mediumTurret = stats.T_AI_OMNI_LASER_0
        else:
            smallTurret = stats.T_MASS_SR_0
            mediumTurret = stats.T_MASS_MR_0

        for t in flagship.turrets[:2]:
            t.buildInstall( mediumTurret )
            
        for t in flagship.turrets[-2:]:
            t.buildInstall( smallTurret )
            
        player.flagship = flagship
        
        game.objects.append( flagship )

        for i in range(self.harvestersAtSpawn):
           harvester = HarvesterShip(player, player.race.defaultHarvester, AiPilotHarvester(flagship), 0,0,0, 4, 0.0,0.0,0.0, 0)
           flagship.shipyards[ harvester.stats.img ].docked.append( harvester )

        player.needToUpdateRelations = True


