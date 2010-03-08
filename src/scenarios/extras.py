#
# Author: Alexis Laferriere
# Description: First scenario with 4 solar systems, sol at the center.
# 

from scenarios import Scenario, Step
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

class Extras ( Scenario ):
    title = "Extras"
    description = "Fight Extras!"
    year = 2523
    name = "Extras"
    
    def __init__( self, game ):
        self.player = None

        self.harvestersAtSpawn = 4
        self.wantedBadGuys = 9

        steps = [
            Step( 
                goal=lambda self, game: not filter( lambda ship: ship.alive, self.ennemyShips ),
                onBegin=lambda self, game: self.addExtrasInFields( game, count=self.wantedBadGuys ),
                failure=lambda self, game: False,
                texts = [ (config.fps*10,"You are at the Human outpost over Gamma 1."),
                          (config.fps*20,"There is hostile life forms in the system."),
                          (config.fps*30,"Clear the asteroids fields above the star Gamma.") ] ),
            Step( 
                goal=lambda self, game: not filter( lambda ship: ship.alive, self.ennemyShips ),
                onBegin=lambda self, game: self.addAttackingExtras( game, count=self.wantedBadGuys ),
                failure=lambda self, game: False,
                texts = [ (0,"The human outpost above Gamma 1 is under attack!"),
                          (config.fps*10,"Jump to their help in 10s..."),
                          (config.fps*17,"3s"),
                          (config.fps*18,"2s"),
                          (config.fps*19,"1s"),
                          (config.fps*20,"Jump!") ] ),
            Step( 
                goal=lambda self, game: game.tick - 20*config.fps >= self.lastStepAt,
                onBegin=lambda self, game: False,
                failure=lambda self, game: False,
                texts = [ (0,"The alien's attack has been succesfully repelled!"),
                          (config.fps*10,"Congratulations ;)") ] )
                 ]


        
        Scenario.__init__(self, game, steps=steps )

        self.ennemyShips = []

        self.gamma = [Sun( game.stats.S_SOL, 1000, 4000 ),
                 Planet( game.stats.P_MERCURY_1, 0, -2200 ),
                 Planet( game.stats.P_X_1, -1000, 11500 ) ]
        for i in range( 20 ): # asteroids around self.gamma[1]
            dist = 750
            angle = 2*pi*random()
            asteroid = Asteroid( game, self.gamma[1].xp+dist*cos(angle), self.gamma[1].yp+dist*sin(angle), 80 )
            game.harvestables.append( asteroid )
        for i in range( 100 ): # asteroids around self.gamma
            area = choice( [(7000, 300, 5*pi/8, pi/9), (10000, 400, 6*pi/8, pi/8), (12000, 500, 5*pi/8, pi/11) ] ) # , 3000
            dist = area[0] #randint( area[0]-area[1], area[0]+area[1] )
            angle = area[2]+area[3]*(1-2*random())
            asteroid = Asteroid( game, self.gamma[0].xp+dist*cos(angle), self.gamma[0].yp+dist*sin(angle), area[1] )
            game.harvestables.append( asteroid )

        for i in xrange( 10 ): # civilians around self.gamma[1]
            dist = randint( 100, 800 )
            angle = 2*pi*random()

            (x,y) = (self.gamma[1].xp+dist*cos(angle), self.gamma[1].yp+dist*sin(angle))
            s = Ship( game.stats.CIVILIAN_0, AiCivilian(), x, y, -20 )
            game.objects.append( s )



        game.astres = self.gamma




       # for i in range( 5 ):
       #     self.addExtrasInFields( game )

        spots = []
        for o in game.astres:
          if isinstance( o, Planet ) and not isinstance( o, Sun ):
            spots.append( o )

        for i in xrange( 30 ): # random civilians
            spot = choice( spots )
            dist = randint( 100, 800 )
            angle = 2*pi*random()

            (x,y) = (spot.xp+dist*cos(angle), spot.yp+dist*sin(angle))
            s = Ship( game.stats.CIVILIAN_0, AiCivilian(), x, y, -20 )
            game.objects.append( s )


        self.humanDefense = Faction( game.stats.R_HUMAN, "Human Defenses" )
        nbrBases = 3
        for i in xrange( nbrBases ):
          dist =  self.gamma[1].stats.maxRadius*1.8 #(1.8+0.4*random())
          angle = pi*i*2/nbrBases
          obase = OrbitalBase( self.humanDefense, game.stats.HUMAN_BASE, AiGovernor( self.humanDefense ),self.gamma[1].xp+dist*cos(angle),self.gamma[1].yp+dist*sin(angle),0, 0, 0.0,0.0,0.0, 0)
          for t in obase.turrets:
            if i%2==0:    
              t.install = TurretInstall( game.stats.T_MASS_SR_1 )
              t.weapon = MassWeaponTurret( game.stats.W_MASS_SR_1 )
            else:
              t.install = TurretInstall( game.stats.T_MASS_MR_1 )
              t.weapon = MassWeaponTurret( game.stats.W_MASS_MR )
            t.ai = AiWeaponTurret()
          obase.ori = angle+pi/2
          obase.orbiting = self.gamma[1]
          obase.xi = cos( obase.ori)
          obase.yi = sin( obase.ori)
          obase.ore = obase.stats.maxOre
          obase.ri = -0.008
          game.objects.append( obase )
          self.humanDefense.bases.append( obase )

        for i in xrange( 10 ):
            radius = self.gamma[1].stats.maxRadius*(2.5)
            dist = self.gamma[1].stats.maxRadius*(1.5+1*random())
            angle = 2*pi*random() # AiPilotDefense
            fighter = ShipSingleWeapon(self.humanDefense, game.stats.HUMAN_FIGHTER, AiPilotPolice(self.gamma[1],radius),self.gamma[1].xp+dist*cos(angle),self.gamma[1].yp+dist*sin(angle),0, 4, 0.0,0.0,0.0, 0)
            game.objects.append( fighter )
            self.humanDefense.ships.append( fighter )

       # self.humanDefense.bases.append( obase )
        game.addPlayer( self.humanDefense )


      ## Extra
        self.extraRock0 = Faction( game.stats.R_EXTRA, "Rocks" )
        game.addPlayer( self.extraRock0 )

       # self.addExtrasInFields( game, self.wantedBadGuys )
       # for i in xrange( self.wantedBadGuys ):
       #   self.addExtrasInFields( game )



    def addExtrasInFields( self, game, pos=None, count=1 ):

        player = self.extraRock0 # Faction( game.stats.R_EXTRA, "Rocks" )

        for k in xrange( count ):
          t = randint( 0, 4 )

          area = choice( 
		[#	(750, 50, pi, pi, self.gamma[1].xp, self.gamma[1].yp), 
			(7000, 300, 5*pi/8, pi/9, self.gamma[0].xp, self.gamma[0].yp), 
			(10000, 400, 6*pi/8, pi/8, self.gamma[0].xp, self.gamma[0].yp), 
			(12000, 500, 5*pi/8, pi/11, self.gamma[0].xp, self.gamma[0].yp) 
		] )
          dist = randint( area[0]-area[1], area[0]+area[1] )
          angle = area[2]+area[3]*(1-2*random())

         # angle = 2*pi*random()
         # dist = 750
          (x,y) = area[4]+dist*cos(angle),area[5]+dist*sin(angle)

          if t%4<2: # rock throwing asteroid # mixed
              flagship = FlagShip( player, game.stats.EXTRA_BASE, AiCaptain( player ),x,y,0, 0, 0.0,0.0,0.0, 0)
              for k,t in enumerate(flagship.turrets[:-1]):
                  t.install = TurretInstall( game.stats.T_ROCK_THROWER_1 )
                  t.weapon = MassWeaponTurret( game.stats.W_ROCK_THROWER_1 )
                  t.ai = AiWeaponTurret()
              for k,t in enumerate(flagship.turrets[-1:]):
                  t.install = TurretInstall( game.stats.T_LARVA_0 )
                  t.weapon = MissileWeaponTurret( game.stats.W_LARVA_0 )
                  t.ai = AiWeaponTurret()
          elif t%4==1: # 3 headed dragon
              flagship = FlagShip( player, game.stats.EXTRA_FS_1, AiCaptain( player ),x,y,0, 0, 0.0,0.0,0.0, 0)
              for k,t in enumerate(flagship.turrets):
                  t.install = TurretInstall( game.stats.T_DRAGON_0 )
                  t.weapon = MassWeaponTurret( game.stats.W_DRAGON_0 )
                  t.ai = AiWeaponTurret()
       #   elif i%4==2: # larva launching asteroid
       #       flagship = FlagShip( player, game.stats.EXTRA_BASE, AiCaptain( self.extraRock0 ),x,y,0, 0, 0.0,0.0,0.0, 0)
       #       for k,t in enumerate(flagship.turrets):
       #           t.install = TurretInstall( game.stats.T_LARVA_0 )
       #           t.weapon = MissileWeaponTurret( game.stats.W_LARVA_0 )
       #           t.ai = AiWeaponTurret()
          else: # abandoned flagship
              flagship = FlagShip( player, game.stats.EXTRA_FS_2, AiCaptain( player ),x,y,0, 0, 0.0,0.0,0.0, 0)
              for i in xrange( 8 ):
                  fighter = ShipSingleWeapon(player, game.stats.EXTRA_FIGHTER, AiPilotFighter(flagship),0,0,0, 4, 0.0,0.0,0.0, 0)
                  flagship.shipyards[ fighter.stats.img ].docked.append( fighter )

          for i in range(2):
             harvester = HarvesterShip(player, player.race.defaultHarvester, AiPilotHarvester(flagship), 0,0,0, 4, 0.0,0.0,0.0, 0)
             flagship.shipyards[ harvester.stats.img ].docked.append( harvester )

          flagship.ore = flagship.stats.maxOre
          flagship.missiles[ ids.M_LARVA ].amount = 100
            
          self.ennemyShips.append( flagship )

          game.objects.append( flagship )
          player.flagships.append( flagship )
          print "ennemy at %s %s" % (flagship.xp, flagship.yp)
       # game.addPlayer( player )
        

    def addAttackingExtras( self, game, pos=None, count=1 ):

        player = self.extraRock0

        for k in xrange( count ):

            dist = randint( 2000, 2500 )
            angle = ( 5*pi/8 + pi/4*random())
            (x,y) = self.gamma[1].xp+dist*cos(angle), self.gamma[1].yp+dist*sin(angle)

            t = randint( 0, 2 )

            if t%2==1: # 3 headed dragon
                flagship = FlagShip( player, game.stats.EXTRA_FS_1, AiCaptain( player ),x,y,0, 0, 0.0,0.0,0.0, 0)
                for k,t in enumerate(flagship.turrets):
                  t.install = TurretInstall( game.stats.T_DRAGON_0 )
                  t.weapon = MassWeaponTurret( game.stats.W_DRAGON_0 )
                  t.ai = AiWeaponTurret()
            else: # abandoned flagship
                flagship = FlagShip( player, game.stats.EXTRA_FS_2, AiCaptain( player ),x,y,0, 0, 0.0,0.0,0.0, 0)
                for i in xrange( 8 ):
                  fighter = ShipSingleWeapon(player, game.stats.EXTRA_FIGHTER, AiPilotFighter(flagship),0,0,0, 4, 0.0,0.0,0.0, 0)
                  flagship.shipyards[ fighter.stats.img ].docked.append( fighter )


            flagship.ore = flagship.stats.maxOre
            flagship.missiles[ ids.M_LARVA ].amount = 100
            
            self.ennemyShips.append( flagship )

            game.objects.append( flagship )

            player.flagships.append( flagship )

            aliveTarget = filter( lambda ship: ship.alive, self.humanDefense.bases )
            if aliveTarget:
                flagship.ai.attack( flagship, choice( aliveTarget ) )
            else:
                dist = randint( 10, 500 )
                angle = 2*pi*random()
                (x,y) = self.gamma[1].xp+dist*cos(angle), self.gamma[1].yp+dist*sin(angle)

                flagship.ai.goTo( flagship, (x.y) )


   # def doTurn( self, game ):
   #     if not game.tick%(config.fps*5):
   #        ## manage npcs numbers
   #         npcCount = 0
   #         for o0 in game.objects.objects:
   #             if o0.player and isinstance( o0, FlagShip ) and isinstance( o0.player, Computer ):
   #                 npcCount = npcCount + 1

           # for i in range( npcCount, self.wantedBadGuys ):
           #         self.addExtrasInFields( game )


    def spawn( self, game, player, shipId ):
    #  if not player.flagship and player.points >= game.stats.PlayableShips[ shipId ].points:
        player.race = game.stats.PlayableShips[ shipId ].race
        shipStats = game.stats.PlayableShips[ shipId ].stats

        dist = randint( 10, self.gamma[1].stats.maxRadius )
        angle = 2*pi*random()
        (x,y) = ( self.gamma[1].xp+dist*cos(angle), self.gamma[1].yp+dist*sin(angle) )

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
            frigate = Frigate( player, player.race.defaultFrigate, 
                               AiEscortFrigate( player ), x+100, y+100 )
            game.objects.append( frigate )

        #player.needToUpdateRelations = True

        #if not self.player:
       #self.player = player


