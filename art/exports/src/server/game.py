from players import *
from ships import * # Ship, FlagShip, Turret
from weapons import *
from ais import *
from comms import * # COPlayerStats, COGfxs, COTurret, COShips, COBuildable, CORadar, COPlayer, COPlayers
from random import randint
from utils import distBetweenObjects
import utils
from orders import *
from gfxs import * # temp
# from astres import *
from objects import Object, Asteroid, Planet, Sun, Nebula, BlackHole
import ids
import stats

import config

from time import time

# TODO refactoring: inconsistency in responsability over object -> cobject, with network

class Game:
    def __init__(self):
        self.players = []

        self.objects = []
        self.astres = []
        self.harvestables = []

        self.newGfxs = []
        self.relations = {}

        self.tick = 0

        self.uidsSent = {}

        self.wantedBadGuys = 5

    #    self.badGuysCount = 

    def generateWorld(self):
        for a in range( config.nbrSpots ):
            pass

        # suns
 #       self.astres.append( Sun( -2000, -2000, 500, 1000, 10000, 100 ) )

        # planets
 #       self.astres.append( Planet( 600, 600, 300, 500 ) )

        # nebulas
  #      self.astres.append( Nebula( 1000, -500, 400 ) )

        sol = Sun( stats.S_SOL, 0, 0 )
        mercury = Planet( stats.P_MERCURY, -4100, 1400 )
        venus = Planet( stats.P_VENUS, 5000, 2200 )
        self.earth = Planet( stats.P_EARTH, -3100, 6700 )
        mars = Planet( stats.P_MARS, -7800, -2200 )
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
            self.objects.append( s )

        for i in range( 60 ): # asteroids between saturn and neptune
            dist = 15000
            angle = (1-2*random())*pi/10+pi/7
            asteroid = Asteroid( sol.xp+dist*cos(angle), sol.yp+dist*sin(angle), 300 )
            self.harvestables.append( asteroid )

        for i in range( 30 ): # asteroids outer mars
            dist = 9000
            angle = (1-2*random())*pi/8+pi*9/8
            asteroid = Asteroid( sol.xp+dist*cos(angle), sol.yp+dist*sin(angle), 200 )
            self.harvestables.append( asteroid )


        nebula = Nebula( stats.A_NEBULA, 4800, 500 )
        for i in range( 15 ): # asteroids in nebula
            asteroid = Asteroid( 4800, 800, 800 )
            self.harvestables.append( asteroid )


        self.alphaCentaury = [ Sun( stats.S_SOL, -32000, 16000 ),
                          Planet( stats.P_MARS_2, -28300, 12000 ),
                          Planet( stats.P_SATURN_1, -39000, 8000 ) ]
        for i in range( 40 ): # asteroids around self.alphaCentaury
            dist = 4600
            #angle = 2*pi*i/50
            angle = (1-2*random())*pi/4-pi/8
            asteroid = Asteroid( self.alphaCentaury[0].xp+dist*cos(angle), self.alphaCentaury[0].yp+dist*sin(angle), 200 )
            self.harvestables.append( asteroid )


        self.beta = [ Sun( stats.S_SOL, 8000, -24000 ),
                 Planet( stats.P_MARS_1, 12000, -22000 ),
                 Planet( stats.P_X, 500, -21000 ) ,
                 Planet( stats.P_JUPITER_1, 17000, -24700 )]
        for i in range( 20 ): # asteroids around self.beta[1]
            dist = 600
            angle = 2*pi*random()
            asteroid = Asteroid( self.beta[1].xp+dist*cos(angle), self.beta[1].yp+dist*sin(angle), 80 )
            self.harvestables.append( asteroid )

        self.gamma = [Sun( stats.S_SOL, 40000, 4000 ),
                 Planet( stats.P_MERCURY_1, 39000, -2200 ),
                 Planet( stats.P_X_1, 38000, 11500 ) ]
        for i in range( 20 ): # asteroids around self.gamma[1]
            dist = 750
            angle = 2*pi*random()
            asteroid = Asteroid( self.gamma[1].xp+dist*cos(angle), self.gamma[1].yp+dist*sin(angle), 80 )
            self.harvestables.append( asteroid )
        for i in range( 100 ): # asteroids around self.gamma
            area = choice( [(7000, 300, 5*pi/8, pi/9), (10000, 400, 6*pi/8, pi/8), (12000, 500, 5*pi/8, pi/11) ] ) # , 3000
            dist = area[0] #randint( area[0]-area[1], area[0]+area[1] )
            angle = area[2]+area[3]*(1-2*random())
            asteroid = Asteroid( self.gamma[0].xp+dist*cos(angle), self.gamma[0].yp+dist*sin(angle), area[1] )
            self.harvestables.append( asteroid )

        nebula2 = Nebula( stats.A_NEBULA_2, 8000, -16000 )

        blackHole0 = BlackHole( stats.BH_0, -10000, -10000 )


#        for i in range( 15 ):
 #           asteroid = Asteroid( -7000, -3200, 800 )
 #           self.objects.append( asteroid )

  #      for i in range( 15 ):
   #         asteroid = Asteroid( 8500, 6800, 800 )
     #       self.objects.append( asteroid )
        self.sol = [sol, mercury, venus, self.earth, moon, mars, jupiter, saturn, neptune, nebula, nebula2 ]
        self.astres = [sol, mercury, venus, self.earth, moon, mars, jupiter, saturn, neptune, nebula, nebula2, blackHole0 ] + self.alphaCentaury + self.beta + self.gamma
     #   self.objects = self.objects #  + [sol, mercury, venus, self.earth, moon, mars, jupiter, saturn, neptune, nebula, nebula2 ] + self.alphaCentaury + self.beta

        for i in range( 5 ):
            self.addRandomNpc()

        spots = []
        for o in self.astres:
          if isinstance( o, Planet ) and not isinstance( o, Sun ):
            spots.append( o )

        for i in xrange( 30 ): # random civilians
            spot = choice( spots )
            dist = randint( 100, 800 )
            angle = 2*pi*random()

            (x,y) = (spot.xp+dist*cos(angle), spot.yp+dist*sin(angle))
            s = Ship( stats.CIVILIAN_0, AiCivilian(), x, y, -20 )
            self.objects.append( s )



        self.marsDefense = Faction( stats.R_HUMAN, "Mars Defenses" )
        obase = OrbitalBase( self.marsDefense, stats.ORBITALBASE, AiGovernor( self.marsDefense ),mars.xp+mars.stats.maxRadius*1.5,mars.yp+mars.stats.maxRadius*1.5,0, 0, 0.0,0.0,0.0, 0)
        for t in obase.turrets:
            t.install = TurretInstall( stats.T_MASS_SR_0 )
            t.weapon = MassWeaponTurret( stats.W_MASS_SR_0 )
            t.ai = AiWeaponTurret()
        obase.orbiting = mars
        obase.yi = 1
        obase.ore = obase.stats.maxOre
        obase.ri = -0.008
        self.objects.append( obase )

        for i in xrange( 20 ):
            radius = mars.stats.maxRadius*(2.5)
            dist = mars.stats.maxRadius*(1.5+1*random())
            angle = 2*pi*random() # AiPilotDefense
            fighter = ShipSingleWeapon(self.marsDefense, stats.FIGHTER, AiPilotDefense(mars,radius),mars.xp+dist*cos(angle),mars.yp+dist*sin(angle),0, 4, 0.0,0.0,0.0, 0)
            self.objects.append( fighter )
            self.marsDefense.ships.append( fighter )

        self.marsDefense.bases.append( obase )
        self.addPlayer( self.marsDefense )


        self.earthDefense = Faction( stats.R_HUMAN, "Earth Defenses" )
        nbrBases = 3
        for i in xrange( nbrBases ):
          dist = self.earth.stats.maxRadius*1.8 #(1.8+0.4*random())
          angle = pi*i*2/nbrBases
          obase = OrbitalBase( self.earthDefense, stats.ORBITALBASE, AiGovernor( self.earthDefense ),self.earth.xp+dist*cos(angle),self.earth.yp+dist*sin(angle),0, 0, 0.0,0.0,0.0, 0)
          for t in obase.turrets:
            t.install = TurretInstall( stats.T_MASS_MR )
            t.weapon = MassWeaponTurret( stats.W_MASS_MR )
            t.ai = AiWeaponTurret()
          obase.ori = angle+pi/2
          obase.orbiting = self.earth
          obase.xi = cos( obase.ori)
          obase.yi = sin( obase.ori)
          obase.ore = obase.stats.maxOre
          obase.ri = -0.008
          self.objects.append( obase )
          self.earthDefense.bases.append( obase )

        for i in xrange( 20 ):
            radius = self.earth.stats.maxRadius*(2.5)
            dist = self.earth.stats.maxRadius*(1.5+1*random())
            angle = 2*pi*random() # AiPilotDefense
            fighter = ShipSingleWeapon(self.earthDefense, stats.FIGHTER, AiPilotPolice(self.earth,radius),self.earth.xp+dist*cos(angle),self.earth.yp+dist*sin(angle),0, 4, 0.0,0.0,0.0, 0)
            self.objects.append( fighter )
            self.earthDefense.ships.append( fighter )

        self.earthDefense.bases.append( obase )
        self.addPlayer( self.earthDefense )

       ## ai forces
        self.addAiBase( "Neptune base", neptune )
        self.addAiBase( "Saturn base", saturn )
        self.addAiBase( "Jupiter base", jupiter, 2 )


       ## Evolved
        self.evolvedSwarm0 = Faction( stats.R_EVOLVED, "First Swarm", territories=[Territory((self.alphaCentaury[ 1 ].xp, self.alphaCentaury[ 1 ].yp), 500), Territory((self.alphaCentaury[ 1 ].xp-1000, self.alphaCentaury[ 1 ].yp-500), 500)] )

        (x,y) = self.alphaCentaury[ 1 ].xp-self.alphaCentaury[ 1 ].stats.maxRadius*1.5,self.alphaCentaury[ 1 ].yp+self.alphaCentaury[ 1 ].stats.maxRadius*1.5
        flagship = FlagShip( self.evolvedSwarm0, stats.EVOLVED_FS_1, AiCaptain( self.evolvedSwarm0 ),x,y,0, 0, 0.0,0.0,0.0, 0)
        flagship.ore = flagship.stats.maxOre
        for t in flagship.turrets[:-2]:
            t.install = TurretInstall( stats.T_MASS_MR )
            t.weapon = MassWeaponTurret( stats.W_MASS_MR )
            t.ai = AiWeaponTurret()
        for t in flagship.turrets[-2:]:
            t.install = TurretInstall( stats.T_LASER_SR )
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
            self.objects.append( fighter )
            self.evolvedSwarm0.ships.append( fighter )
        #    flagship.shipyards[ fighter.stats.img ].docked.append( fighter )
        self.objects.append( flagship )
        self.evolvedSwarm0.flagships.append( flagship )
        self.addPlayer( self.evolvedSwarm0 )


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

          self.objects.append( flagship )
          self.extraRock0.flagships.append( flagship )
          flagship.missiles[ ids.M_LARVA ].amount = 100
      #  self.addPlayer( self.extraRock0 )

        for i in xrange( 16 ):
          self.addRandomExtra()


      #  self.harvestables = self.harvestables[:10]


    def doTurn(self,playerInputs):
        addedObjects = []
        removedObjects = []
        addedGfxs = []
        
       ### manage inputs
        for (player,inputs) in playerInputs:
            player.inputs = inputs
                 
       ### players play
        for player in self.players:
            player.doTurn( self )

       ### move objects
        ts = {}
        for o0 in utils.mY( self.objects, self.astres ): # self.objects: , self.harvestables
          if o0.alive:
            t0 = time()
            ( addedObjectsLocal, removedObjectsLocal, addedGfxsLocal ) =  o0.doTurn( self )

            if addedObjectsLocal:
                addedObjects = addedObjects + addedObjectsLocal
            if removedObjectsLocal:
                removedObjects = removedObjects + removedObjectsLocal 
            if addedGfxsLocal:
                addedGfxs = addedGfxs+addedGfxsLocal 
            t1 = time()
            ts[ o0 ] = t1-t0
        ho = None
        bt = 0
        for k in ts:
            if ts[ k ] > bt:
                bt = ts[ k ]
                ho = k
       # print ho
        if __debug__ and not self.tick%(config.fps):
            print utils.i
            utils.i = 0

      ### remove dead objects
        for o1 in removedObjects:
            if isinstance( o1, FlagShip ):
                if isinstance( o1.player, Human ):
                    player.flagship = None
                elif not isinstance( o1.player, Faction ):
                    self.removePlayer( o1.player )

            
            self.objects.remove( o1 ) # WARNING: this assumes harvestable and astres objects won't be removed
        self.objects = self.objects + addedObjects


        if not self.tick%(config.fps*5):

           ## calm tensions between computers and players
            for p0 in self.players:
             if not isinstance( p0, Computer ):
                for p1 in self.players:
                 if isinstance( p1, Computer ):
                    rel = self.getRelationBetween( p1, p0 )
                    if rel < stats.Relations[ p1.race ][ p0.race ]:
                       self.setRelationBetween( p1, p0, rel + 1)
                 #      self.setRelationBetween( p0, p1, rel + 1)

           ## manage npcs numbers
            npcCount = 0
            for o0 in self.objects:
                if o0.player and isinstance( o0, FlagShip ) and isinstance( o0.player, Computer ):
                    npcCount = npcCount + 1

            for i in range( npcCount, self.wantedBadGuys ):
                if randint(0,1):
                    self.addRandomNpc()
                else:
                    self.addRandomExtra()

           ## TODO manage earth defenses / numbers

        self.newGfxs = addedGfxs

        self.tick = self.tick + 1


    def getUpdates(self,player ):
        (x0,y0,x1,y1) = (player.inputs.xc,player.inputs.yc, player.inputs.xc+player.inputs.wc, player.inputs.yc+player.inputs.hc)
        cobjs = []
        cobjs1 = []
    #    print (x0,y0,x1,y1)

        t0 = time()

       ## objects + harvestable (-astres)
        if player.flagship:
          for obj in utils.mY( self.objects ): #, self.harvestables ): # , self.astres ):
            if obj.alive:
             if (obj.xp + obj.stats.maxRadius/2 >= x0 \
              and obj.xp - obj.stats.maxRadius/2 < x1 \
              and obj.yp + obj.stats.maxRadius/2 >= y0 \
              and obj.yp - obj.stats.maxRadius/2 < y1)\
              or obj.zp == -100:
                for cobj in obj.getCommObjects():
                    cobjs.append( (obj, cobj) )
             elif isinstance( obj, FlagShip ) \
              and distBetweenObjects( player.flagship, obj ) <= player.flagship.getRadarRange():
                cs = obj.getCommObjects()
                cobjs.append( (obj, cs[0]) )

        t1 = time()
        self.uidsSent[ player ] = []
        for (k,(obj,cobj)) in enumerate( cobjs ): #zip( xrange(len(cobjs)), cobjs ):
            cobj.uid = k
            if obj == player.flagship:
                cobj.relation = ids.U_FLAGSHIP
            elif obj.player == player:
                cobj.relation = ids.U_OWN
            elif obj.stats.orbitable:
                cobj.relation = ids.U_ORBITABLE
            elif obj.player == None:
        #        print "k=%i, o "%k, obj.player
                cobj.relation = ids.U_NEUTRAL
            elif obj.player != player:
                cobj.relation = ids.U_ENNEMY

            self.uidsSent[ player ].append( obj )
            cobjs1.append( cobj )
            
        t2 = time()
        if player.flagship:
            oreProcess = [0]*20
            for ob in player.flagship.oreProcess:
                p = int(len(oreProcess)*ob.pos / player.flagship.processLength)
                oreProcess[ p ] = oreProcess[ p ] + ob.amount

            t3 = time()
           ## turrets
            turrets = []
            for turret in player.flagship.turrets:
                if turret.building:
                    t = turret.building.type
                    activable = False
                elif turret.install:
                    t = turret.install.stats.type
                    activable = (turret.install.stats.orePerFrame>0 or turret.install.stats.energyPerFrame>0 or turret.install.stats.energyPerUse>0 or turret.install.stats.orePerUse>0 or ( turret.install.stats.weapon!=None and turret.install.stats.weapon.img == ids.W_MISSILE ))
                else:
                    t = 0
                    activable = False

                if turret.install and turret.activated:
                    energyUse = turret.install.stats.energyPerFrame or turret.install.stats.energyPerUse
                    oreUse = turret.install.stats.orePerFrame or turret.install.stats.orePerUse
                else:
                    energyUse = False
                    oreUse = False

                (x,y) = player.flagship.getTurretPos( turret )
                maxRange = 0
                if turret.weapon:
                    maxRange =  turret.weapon.stats.maxRange

                if turret.building:
                    buildPerc = 100*turret.build/turret.buildCost
                    energyRebate = turret.building.energyCostToBuild
                    oreRebate = turret.building.oreCostToBuild
                else:
                    buildPerc = -1
                    energyRebate = 0
                    oreRebate = 0

                buildables = []

             #   print player.race.turrets
                options = [o for o in player.race.turrets]

                if turret.install:
                    for option in turret.install.stats.overs+[turret.install.stats]:
               #         print option.type, turret.install.stats.overs+[turret.install.stats]
                        options.remove( option )
                    #removedOptions = turret.install.stats.overs+[turret.install.stats]
                elif turret.building:
                    for option in turret.building.overs: # +[turret.building]:
                      if option != turret.building.upgradeFrom:
                        options.remove( option )
                    
                    #removedOptions = turret.building.overs+[turret.building]

                for bt in options: #player.race.turrets:
                  
              #-    if bt.upgradeFrom and turret.install and turret.install.stats == bt: # obsolete upgrade, doesn't care about building->allows cancel
              #        removedOptions.append( bt.upgradeFrom )

              #    if not bt in removedOptions or (turret.building and bt == turret.building.upgradeFrom):
                    if turret.install and turret.install.stats == bt.upgradeFrom: # upgradable
                        buildables.append( COBuildable( bt.type, player.flagship.energy >= bt.energyCostToBuild-energyRebate and player.flagship.ore >= bt.oreCostToBuild-oreRebate)) #, bt.energyCostToBuild, bt.oreCostToBuild, bt.category ) )
                   #     removedOptions.append( turret.install.stats )
                    elif (turret.install and turret.install.stats == bt) or (turret.building and turret.building == bt): # already there
                        buildables.append( COBuildable( bt.type, False )) #, bt.energyCostToBuild, bt.oreCostToBuild, bt.category ) )
                    elif not bt.upgradeFrom: # otherwise, not an upgrades
                        buildables.append( COBuildable( bt.type, player.flagship.energy >= bt.energyCostToBuild-energyRebate and player.flagship.ore >= bt.oreCostToBuild-oreRebate )) # , bt.energyCostToBuild, bt.oreCostToBuild, bt.category ) )
                if turret.building or turret.install:
                    buildables.append( COBuildable( 0, True )) # , -1*energyRebate, -1*oreRebate, ids.C_OTHER ) )
               
                turrets.append( COTurret( t, x, y, turret.stats.minAngle+player.flagship.ori, turret.stats.maxAngle+player.flagship.ori, buildPerc, maxRange, turret.activated, activable, energyUse, oreUse, energyRebate, oreRebate, buildables ) )

            t4 = time()
           ## small ships
            ships = []
            shipsSpace = 0
            for k in player.race.ships: 
                k = k.img
                sy = player.flagship.shipyards[ k ]
                if sy.building:
                    buildPerc = sy.build*100/sy.buildCost
                else:
                    buildPerc = -1
                ships.append( COShips( k, len(sy.docked)>0 or len(sy.away)>0, not player.flagship.ai.launching[ k ],  len(sy.docked) + len(sy.away), buildPerc, player.flagship.canBuild( k ), True ) )
                shipsSpace = shipsSpace + (len(sy.docked)+len(sy.away)) * stats.Costs[ k ].hangarSpace

            t5 = time()
           ## missiles
            missiles = []
            missilesSpace = 0
            for missile in player.race.missiles:
                hasTurret = False
                for t in player.flagship.turrets:
                    if t.install and t.install.stats.weapon and t.install.stats.weapon.projectile and t.install.stats.weapon.projectile.img == missile:
                        hasTurret = True
                        break

                if player.flagship.missiles[missile].building:
                    buildPerc = 100*player.flagship.missiles[missile].build/player.flagship.missiles[missile].buildCost
                else:
                    buildPerc = -1

                missiles.append( COShips( missile,  missile != ids.M_NORMAL and hasTurret, player.flagship.missiles[missile].amount>0, player.flagship.missiles[missile].amount, buildPerc, hasTurret and player.flagship.canBuild( missile ), hasTurret ) )
                missilesSpace = missilesSpace + player.flagship.missiles[missile].amount*stats.Costs[ missile ].hangarSpace

            t6 = time()
            radars = [ CORadar( (player.flagship.xp, player.flagship.yp), player.flagship.getRadarRange() ) ]
            
           ## stats if flagship
            pstats = COPlayerStats( self.tick, False, player.flagship.ore, player.flagship.stats.maxOre, player.flagship.energy, player.flagship.stats.maxEnergy, 
player.flagship.shield/player.flagship.stats.maxShield, player.flagship.hull/player.flagship.stats.maxHull,  player.flagship.canJump( self ),
player.flagship.repairing, player.flagship.charging, player.flagship.getHangarSpace(), shipsSpace, missilesSpace, player.flagship.jumpCharge, player.flagship.jumpOverheat, oreProcess, turrets, missiles, ships, radars )
            t7 = time()

            t = t7 - t0
           # print "objects: %.2f uids: %.2f flagship: %.2f turrets: %.2f ships: %.2f missiles: %.2f init: %.2f"%((t1-t0)/t,(t2-t1)/t,(t3-t2)/t,(t4-t3)/t,(t5-t4)/t,(t6-t5)/t,(t7-t5)/t)
        else:
           ## stats if flagship dead
            pstats = COPlayerStats( self.tick, True, 0, 0, 0, 0, 
0, 0,  0,
0, 0, 0, 0, 0, 0, 0,
[], [], [], [], [ CORadar( (self.earth.xp, self.earth.yp), self.earth.stats.maxRadius*2 ) ] )

       ## fxs
        fxs = []
        for fx in self.newGfxs:
            if (fx.xp + fx.maxRadius >= x0 \
              and fx.xp - fx.maxRadius < x1 \
              and fx.yp + fx.maxRadius >= y0 \
              and fx.yp - fx.maxRadius < y1):
                fxs.append( fx )

       ## other players and relations 
        players = []
        if player.needToUpdateRelations:
            player.needToUpdateRelations = False
            for p in self.players:
                if player != p:
                    cop = COPlayer( p.name, p.race.type, (self.getRelationBetween(p, player)+100)/2, (self.getRelationBetween(player, p)+100)/2, isinstance( p, Human ) )
                    players.append( cop )

       ## possible ships to select
        possibles = []
        if player.needToUpdatePossibles:
            player.needToUpdatePossibles = False
            for p in stats.PlayableShips:
               c = stats.PlayableShips[ p ]
               if player.points >= c.points:
                 possibles.append( COPossible( c.stats.img, c.race.type, c.turrets, c.speed, c.shield, c.hull, c.hangar, c.canJump, c.civilians  ) )
            
           # possibles = [ COPossible( ids.S_FLAGSHIP_0, ids.R_HUMAN, 4, 15, 25, 30, 40, 50, 10, 20 ), 
                    #      COPossible( ids.S_FLAGSHIP_1, ids.R_HUMAN, 10, 10, 20, 30, 40, 30, 10, 20 ), 
                    #      COPossible( ids.S_FLAGSHIP_2, ids.R_HUMAN, 4, 15, 30, 30, 40, 100, 10, 20 ), 

                      #    COPossible( ids.S_AI_FS_0, ids.R_AI, 3, 15, 30, 30, 40, 100, 10, 20 ), 
                      #    COPossible( ids.S_AI_FS_1, ids.R_AI, 6, 15, 30, 30, 40, 100, 10, 20 ), 
                      #    COPossible( ids.S_AI_FS_2, ids.R_AI, 8, 15, 30, 30, 40, 100, 10, 20 ), 

                    #      COPossible( ids.S_EVOLVED_FS_0, ids.R_EVOLVED, 4, 15, 30, 30, 40, 100, 10, 20 ), 
                     #     COPossible( ids.S_EVOLVED_FS_1, ids.R_EVOLVED, 5, 15, 30, 30, 40, 100, 10, 20 ) ]

       ## astres
        astres = []
        if player.needToUpdateAstres:
            # sending astres
            player.needToUpdateAstres = False
       #     astres = [ astres ]
            for obj in utils.mY( self.astres, self.harvestables ): # self.astres:
                for cobj in obj.getCommObjects():
                    cobj.relation = ids.U_ORBITABLE # NEUTRAL
                    cobj.uid = 0 #  ids.U_ORBITABLE
                    astres.append( cobj )

        return (cobjs1, pstats, COGfxs( fxs ), players, astres, possibles )

    def getBrief( self, player ):
        cobjs = []
        for obj in self.objects:
            cobjs.append( (obj, cobj) )

    def addRemotePlayer(self, username, password ):
        player = Human( stats.R_HUMAN, username, password )
        self.addPlayer( player )
        self.uidsSent[ player ] = []

        return player

    def giveShip( self, player, shipId ):
    #  print player.points, stats.PlayableShips[ shipId ].points
      if not player.flagship and player.points >= stats.PlayableShips[ shipId ].points:
        player.race = stats.PlayableShips[ shipId ].race
        shipStats = stats.PlayableShips[ shipId ].stats

        dist = randint( 10, self.earth.stats.maxRadius )
        angle = 2*pi*random()
        (x,y) = ( self.earth.xp+dist*cos(angle), self.earth.yp+dist*sin(angle) )

        flagship = FlagShip( player, shipStats, AiCaptain( player ),x,y,0, 0, 0.0,0.0,0.0, 0)
        flagship.ore = flagship.stats.maxOre/2
        flagship.energy = flagship.stats.maxEnergy / 2
        flagship.oir = 2*pi*random()

        for t in flagship.turrets[-2:]:
            t.install = TurretInstall( stats.T_MASS_SR_0 )
            t.weapon = MassWeaponTurret( stats.W_MASS_SR_0 )
            t.ai = AiWeaponTurret()
        player.flagship = flagship
        
        self.objects.append( flagship )

        for i in range(config.harvestersAtSpawn):
           harvester = HarvesterShip(player, player.race.defaultHarvester, AiPilotHarvester(flagship), 0,0,0, 4, 0.0,0.0,0.0, 0)
           flagship.shipyards[ harvester.stats.img ].docked.append( harvester )

        player.needToUpdateRelations = True
    #  else:
     #   raise Warning( "Cheat: player %s, tried to get ship out of reach." % player.name )

     #   print "ship given", player.name, shipId, shipStats
        

    def addPlayer( self, player ):
        self.relations[ player ] = {}
        for other in self.players:
            if isinstance( other, Human ):
                other.needToUpdateRelations = True
            if isinstance( player, Computer ) or isinstance( other, Computer ):
                self.relations[ player ][ other ] = stats.Relations[ player.race ][ other.race ]
                self.relations[ other ][ player ] = stats.Relations[ other.race ][ player.race ]
            else: ## if both are human players
                self.relations[ player ][ other ] = 20
                self.relations[ other ][ player ] = 20

        self.players.append( player )

    def getPlayer( self, name ):
        for p in self.players:
        #    if isinstance( p, Human ) and p.username == username:
            if p.name == name:
                return p

    def removePlayer( self, player ):
     #   self.players.remove( player )
        pass
     #   print "removing player"
    #    for k, r in self.relations:
     #       if k == player: # r.has_key( player ):
     #           del( r[ player ] )
      #  del( self.relations[ player ] )


    def getRelationBetween( self, p0, p1 ):
   #     print p0, p1
        if p0 == p1:
            return 101
        else:
            return self.relations[ p0 ][ p1 ]

    def setRelationBetween( self, p0, p1, rel=20 ): 
        if p0 and p1 and p0 != p1 and (isinstance( p0, Human ) or isinstance( p1, Human )):
            if isinstance( p0, Human ):
                p0.needToUpdateRelations = True
            if isinstance( p1, Human ):
                p1.needToUpdateRelations = True

            self.relations[ p0 ][ p1 ] = rel


    def saveToDisk( self, path ):
        pass

    def loadFromDisk( self, path ):
        pass

    def addShip( self, stat, ai, pos=None ):
        pass

    def addRandomNpc( self, pos=None, i=None ):

      # position
      if pos:
          (x,y) = pos
      else:
        valid = False

        spots = []
        for o in self.sol:
          if isinstance( o, Planet ) and not isinstance( o, Sun ):
              spots.append( o )
        spot = choice( spots )

        while not valid:
          dist = randint( 100, 800 )
          angle = 2*pi*random()

          (x,y) = (spot.xp+dist*cos(angle), spot.yp+dist*sin(angle))

          valid = True
          for o in self.astres:
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
            t.install = TurretInstall( stats.T_LASER_MR_0 )
            t.weapon = LaserWeaponTurret( stats.W_LASER_MR_0 )
            t.ai = AiTurret()
        for t in flagship.turrets[:2]+flagship.turrets[-2:]:
            t.install = TurretInstall( stats.T_LASER_SR )
            t.weapon = LaserWeaponTurret( stats.W_LASER_SR )
            t.ai = AiWeaponTurret()

      elif i < 3:
        flagship = FlagShip( player, stats.FLAGSHIP_2, AiCaptain( player ),x,y,0, 0, 0.0,0.0,0.0, 0)
        flagship.ore = flagship.stats.maxOre
        for t in flagship.turrets:
            t.install = TurretInstall( stats.T_MASS_SR_0 )
            t.weapon = MassWeaponTurret( stats.W_MASS_SR_0 )
            t.ai = AiWeaponTurret()
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
            t.install = TurretInstall( stats.T_MASS_MR )
            t.weapon = MassWeaponTurret( stats.W_MASS_MR )
            t.ai = AiWeaponTurret()
        for t in flagship.turrets[-2:]:
            t.install = TurretInstall( stats.T_LASER_SR )
            t.weapon = LaserWeaponTurret( stats.W_LASER_SR )
            t.ai = AiWeaponTurret()
        for i in range(4):
           harvester = HarvesterShip(player, player.race.defaultHarvester, AiPilotHarvester(flagship), 0,0,0, 4, 0.0,0.0,0.0, 0)
           flagship.shipyards[ harvester.stats.img ].docked.append( harvester )

      flagship.ori = 2*pi*random()
      player.flagship = flagship
      self.objects.append( flagship )
      self.addPlayer( player )
        
    def executeCode( self, code ):
        eval( code )

    def addAiBase( self, name, orbited, count=1 ):

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
        self.objects.append( obase )

        for i in xrange( 8 ):
            if i>=6:
                fighter = ShipSingleWeapon(player, stats.AI_BOMBER, AiPilotFighter(obase),0,0,0, 4, 0.0,0.0,0.0, 0)
            else:
                fighter = ShipSingleWeapon(player, stats.AI_FIGHTER, AiPilotFighter(obase),0,0,0, 4, 0.0,0.0,0.0, 0)
            obase.shipyards[ fighter.stats.img ].docked.append( fighter )

        player.bases.append( obase )
      self.addPlayer( player )

    def addRandomExtra( self, count=1 ):

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

          self.objects.append( flagship )
          player.flagships.append( flagship )
          flagship.missiles[ ids.M_LARVA ].amount = 100
        self.addPlayer( player )

