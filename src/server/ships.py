from objects import Object, Sun
from math import sqrt, pow, atan, pi, sin, cos, fabs, hypot

from common.comms import COObject
from common.utils import *
from common.gfxs import *
from common import config
import stats


class OreBatch:
    def __init__(self, amount, pos=0):
        self.amount = int(amount)
        self.pos = pos

class Ship( Object ):
    def __init__( self, stats, ai, xp, yp, zp=0, ori=0.0, xi=0, yi=0, zi=0, ri=0, thrust=0 ): #, fradius(ang)=(1)
        Object.__init__( self, stats, xp, yp, zp, ori, xi, yi, zi, ri )

        self.alive = True
        self.maxOri = 2*pi

        self.thrust = thrust
        self.rg = 0

  #      self.dest = (200, 100)
  #      self.weapons = []

        self.ai = ai
        self.dockedTo = False
        self.dockedAt = 0 # tick at docking

        self.hull = stats.maxHull
        self.shield = stats.maxShield
        self.inertiaControl = True

        self.headed = True

        self.pulsedUntil = -1000
        self.inNebula = False
        self.inertiaMod = 1
        self.thrustBoost = 0

        self.shipyards = []

    def getRadiusAt( self, ang ): # absolute angle with another object
        return self.stats.maxRadius

    def doTurn(self, game):
        # ai
        if self.ai:
            ( addedObjects0, removedObjects0, addedGfxs0 ) = self.ai.doTurn( self, game )
        else:
            ( addedObjects0, removedObjects0, addedGfxs0 ) = ([],[],[])

        if not self.orbiting and self.pulsedUntil < game.tick:
            # engine thrust
            self.xi = self.xi + self.thrust * cos( self.ori )
            self.yi = self.yi + self.thrust * sin( self.ori )

            # gouvernailstats
            self.ri = self.ri + self.rg

            # inertia controls
            if self.inertiaControl:
                self.xi = self.xi * (0.9+0.01*self.stats.mass)*self.inertiaMod #0.9
                self.yi = self.yi * (0.9+0.01*self.stats.mass)*self.inertiaMod #0.9
                self.zi = self.zi * (0.9+0.01*self.stats.mass)*self.inertiaMod #0.9
                self.ri = self.ri * 0.9 # *self.inertiaMod
                if fabs(self.xi) < 0.05 and fabs(self.yi) < 0.05:
                    self.xi = self.yi = 0
                if fabs(self.ri) < 0.0005:
                    self.ri = 0

        if (not self.ai or self.ai.dockingTo) and randint( 0, config.fps*10 ) == 0:
        #    zDiff = -2 + 4*randint( 0, 1 )
            nz = randint( -5, 5 )
            can = True
            for obj in game.objects:
            #    print "s ", obj.zp <= max( self.zp, nz ), obj.zp >= min( self.zp, nz ), areOver( self, obj )
                if obj != self and obj.zp <= max( self.zp, nz ) and obj.zp >= min( self.zp, nz ) and areOver( self, obj ):
                    can = False
                    break
         #   print "switch", can, nz, obj.zp <= max( self.zp, nz ), obj.zp >= min( self.zp, nz ), areOver( self, obj )
            if can:
                self.zp = nz
                    
 
        ( addedObjects1, removedObjects1, addedGfxs1 ) = Object.doTurn( self, game )
        if self.thrust > 0 and self.stats.engines:
            if randint( 0, 4 ) == 0:
                engine = choice( self.stats.engines )
                (x,y) = (self.xp+engine[0]*cos(self.ori+engine[1]), self.yp+engine[0]*sin(self.ori+engine[1]) )
                addedGfxs1.append( GfxExhaust( (x,y), self.zp, 0, -0.2*self.xi+(0.5-random())*0.4, -0.2*self.yi+(0.5-random())*0.4, random()*pi ) )

        if game.tick%(config.fps)==4:
            self.inNebula = False
            for obj in game.astres:
                if isinstance( obj, Nebula ) and distLowerThanObjects( self, obj, self.stats.maxRadius+obj.stats.maxRadius):
                    self.inNebula = True
                    break

        return ( addedObjects0+addedObjects1, removedObjects0+removedObjects1, addedGfxs0+addedGfxs1 )

    def enterHangar( self ):
        self.xi = 0
        self.yi = 0
        self.zi = 0
        self.ri = 0

    def hit( self, game, angle, sender, energy=0, mass=0, pulse=False ):
      if self.alive:
        if sender and self.player:
            rel = game.getRelationBetween( self.player, sender )
            if pulse:
                relDamage = 100
            else:
                relDamage = energy+mass
            game.setRelationBetween( self.player, sender, max(-100,rel-relDamage) )

        if self.ai:
            self.ai.hitted( self, game, angle, sender, energy, mass, pulse )
        gfxs = []

        damageToShield = min( self.shield, energy + mass/3)

        if damageToShield > 0:
            gfxs.append( GfxShield( (self.xp, self.yp), self.stats.maxRadius, self.shield/self.stats.maxShield, angle, damageToShield ) )

        rEnergy = max( 0, energy-self.shield)
        rMass = max( 0, mass-max( 0, self.shield-energy)*5)
        self.shield = self.shield - damageToShield # max( 0, self.shield - energy - mass/3) 

        damageToHull = min( self.hull, rEnergy/3 + rMass)
        self.hull = self.hull - damageToHull #- rMass - rEnergy/3

        if self.hull == 0: # dead
            if sender:
                sender.points += self.stats.pointsWorth
            (ao0, ro0, ag0 ) = self.die( game )
            return (ao0,ro0,ag0+gfxs)
        else: # alive
            if pulse:
                self.pulsedUntil = game.tick + pulse
        #        print game.tick + pulse, game.tick, pulse
                if self.shield >1:
                    gfxs.append( GfxShield( (self.xp, self.yp), self.stats.maxRadius, self.shield/self.stats.maxShield, 0, 1000 ) )
                self.shield = self.shield/2

            if damageToHull > 0:
                gfxs.append( GfxExplosion( (self.xp+cos(angle)*self.stats.maxRadius/2,self.yp+sin(angle)*self.stats.maxRadius/2), damageToHull, sound=ids.S_EX_FIRE ) ) # TODO place explosion at hit
            return ([],[],gfxs)
      return ([],[],[])

    def die( self, game ):
        self.alive = False
        if self.ai:
            self.ai.died( self, game )
        gfxs = [ GfxExplosion( (self.xp,self.yp), self.stats.maxRadius, sound=ids.S_EX_SHIP) ]
        if self.stats.unavoidableFragments:
           for f in self.stats.unavoidableFragments:
              gfxs.append( GfxFragment( (self.xp, self.yp), self.zp, self.ori, self.xi+(0.5-random())*0.4, self.yi+(0.5-random())*0.4, self.ri+(0.5-random())*0.02, f, randint( int(1.5*self.stats.maxRadius), 2*self.stats.maxRadius ) ) )

        if self.stats.fragments:
            for i in range( int(self.stats.maxRadius/10) ):#f in self.stats.fragments[1:]:
                f = choice( self.stats.fragments )
                gfxs.append( GfxFragment( (self.xp+randint(-1*self.stats.maxRadius,self.stats.maxRadius), self.yp+randint(-1*self.stats.maxRadius,self.stats.maxRadius)), self.zp, random()*2*pi, self.xi+(0.5-random())*0.4, self.yi+(0.5-random())*0.4, (0.5-random())*0.3, f, randint( int(1.5*self.stats.maxRadius), int(2.5*self.stats.maxRadius) ) ) )

        for i in range( 0, randint(1,3*self.stats.maxRadius) ):
            i = randint( 1, 3*self.stats.maxRadius )
            (xi,yi) = ( self.xi+(0.5-random())*0.4, self.yi+(0.5-random())*0.4 )
            gfxs.append( GfxExplosion( (self.xp+randint(-1*self.stats.maxRadius,self.stats.maxRadius)+xi*i, self.yp+randint(-1*self.stats.maxRadius,self.stats.maxRadius)+yi*i), self.stats.maxRadius/(2+random()*3), delai=i ) )
        return ([],[self],gfxs) 

from ais import * # useless?
from weapons import * # useless?
from turrets import *

class ShipWithTurrets( Ship ):
    def __init__( self, player, stats, ai, xp, yp, zp=0, ori=0.0, xi=0, yi=0, zi=0, ri=0, thrust=0 ):
        Ship.__init__( self, stats, ai, xp, yp, zp, ori, xi, yi, zi, ri, thrust )
        self.turrets = []
        self.turretPoss = {} # [None]*len(stats.turrets)
        for turret in stats.turrets:
            self.turrets.append( Turret( turret ) ) # , None, AiWeaponTurret() ) )

    def getCommObjects(self):
	objects = []
        for turret in self.turrets:
          if not turret.stats.overShip:
            if isinstance( turret, TurretBuildable ) and turret.building:
                t = ids.T_BUILDING
            elif turret.install:
                t = turret.install.stats.type
            else:
                t = None
            if t:
                (x,y) = self.getTurretPos( turret )
                objects.append( COObject( t, x, y, self.zp, self.ori+turret.rr, None, 10 ) )

        objects.append( COObject( self.stats.img, self.xp, self.yp, self.zp, self.ori, None, self.stats.maxRadius  ) )

        for turret in self.turrets:
          if turret.stats.overShip:
            if isinstance( turret, TurretBuildable ) and turret.building:
                t = ids.T_BUILDING
            elif turret.install:
                t = turret.install.stats.type
            else:
                t = None
            if t:
                (x,y) = self.getTurretPos( turret )
                objects.append( COObject( t, x, y, self.zp, self.ori+turret.rr, None, 10 ) )

        return objects

    def doTurn(self,game):
        prevPos = (self.xp, self.yp)
        res = Ship.doTurn( self, game )
        pastPos = (self.xp, self.yp)
        if prevPos != pastPos:
            self.turretPoss = {} # [None]*len(stats.turrets)
        return res

    def getTurretPos(self,turret):
        try:
       # if self.turretPoss.has_key( turret ):
            return self.turretPoss[ turret ]
      #  else:
        except KeyError:
            r = self.ori + turret.stats.distAngle
            x = int(self.xp) + turret.stats.dist*cos( r )
            y = int(self.yp) + turret.stats.dist*sin( r )
            self.turretPoss[ turret ] = (x,y)
            return (x,y)

class ShipSingleWeapon( Ship ):
    def __init__( self, player, stats, ai, xp, yp, zp=0, ori=0.0, xi=0, yi=0, zi=0, ri=0, thrust=0 ):
        Ship.__init__( self, stats, ai, xp, yp, zp, ori, xi, yi, zi, ri, thrust )
        self.player = player
        if stats.weapon.weaponType == ids.WT_MASS or stats.weapon.weaponType == ids.WT_BOMB:
            self.weapon = MassWeapon( stats.weapon )
        elif stats.weapon.weaponType == ids.WT_LASER:
            self.weapon = LaserWeapon( stats.weapon )
        elif stats.weapon.weaponType == ids.WT_MISSILE:
            self.weapon = MissileWeapon( stats.weapon )
        else:
            raise Warning(  "warning: weapon not mass, laser nor missile: %s" % stats.weapon.weaponType )
# TODO add different weapon typee for bombs
  #      self.zp = 1

class Builder:
    def __init__( self ):
        self.building = None
        self.goal = 0
        self.buildAt = 0

class TurretBuildable( Turret ): # unused? TODO if so, remove
    def __init__( self, stats ): # the stats duplicates the stats from ship
        Turret.__init__( self, stats )
        self.building = None
	self.buildCost = 0
	self.build = 0
        self.activated = True

class Shipyard:
    def __init__( self ):
        self.building = None
	self.buildCost = 0
	self.build = 0
	self.away = []
	self.docked = []

    def getCount( self ):
        return len(self.away)+len(self.docked)

class MissileReserve:
    def __init__( self ):
        self.building = None
	self.buildCost = 0
	self.build = 0
	self.amount = 0
	self.target = None

        
class FlagShip( ShipWithTurrets ):
    def __init__( self, player, stats, ai, xp, yp, zp=0, ori=0.0, xi=0, yi=0, zi=0, ri=0, thrust=0 ):
        ShipWithTurrets.__init__( self, player, stats, ai, xp, yp, zp, ori, xi, yi, zi, ri, thrust )
        self.player = player

        # resources
        self.processLength = 60*30
        self.oreProcess = [] # list of OreBatch # (amount,position<chainLength)
        self.ore = 0
        self.energy = self.stats.maxEnergy #0

        self.repairing = True
        self.charging = True
        self.lastRepairsAt = 0
        self.repairDelay = 10
        
        self.civilianShips = []
        self.civilianValue = 1

        self.lastLaunchAt = 0
        self.jumping = None

        self.turrets = []
        for turret in stats.turrets:
            self.turrets.append( TurretBuildable( turret ) ) #, None, AiWeaponTurret() ) )

        self.shipyards = {}
        for s in player.race.ships:
            self.shipyards[ s.img ] = Shipyard()
  #      for b in ['ships', 'missiles']:

        self.missiles = {}
        for m in player.race.missiles:
            self.missiles[ m ] = MissileReserve()


        self.noOreCloseAt = -1000

        self.jumpCharge = 0
        self.jumpOverheat = 0
        
    def doTurn( self, game ):
        self.inertiaMod = 1
        thrustBoost = 0
        nebulaOreSum = 0
       ## build
        # turrets
        for b in self.turrets:
          if b.building:
            b.build = b.build+self.getBuildRate()
            if b.build >= b.buildCost:
                b.buildInstall( b.building )

          if b.install and b.activated:
              if b.install.stats.orePerFrame <= self.ore \
                and b.install.stats.energyPerFrame <= self.energy:
                  self.energy = self.energy-b.install.stats.energyPerFrame
                  self.ore = self.ore-b.install.stats.orePerFrame
              else:
                  b.activated = False
              if b.activated:
                  if b.install.stats.special == ids.S_SUCKER and self.inNebula and game.tick%(config.fps/3)==6: # sucker creates ore when in nebula
                      nebulaOreSum += b.install.stats.specialValue
                  elif b.install.stats.special == ids.S_INERTIA:
                      self.inertiaMod = b.install.stats.specialValue # self.inertiaMod*
                  elif b.install.stats.special == ids.S_SAIL:
                      thrustBoost += b.install.stats.specialValue # self.inertiaMod*
                  elif b.install.stats.special == ids.S_JAMMER and game.tick%(config.fps/2) == 5:
                       for obj in game.objects:
                           if isinstance( obj, Missile ) and distLowerThanObjects( self, obj, b.install.stats.specialValue+obj.stats.maxRadius ):
                               obj.loseTarget( game )
                             
        if nebulaOreSum:
            self.addOreToProcess( nebulaOreSum )  
     #     print self.inertiaMod
                      

        # ships
        hangarSpace = self.getHangarSpace()
        count = self.getHangarUse()
      #  for k1 in self.shipyards:
      #      b1 = self.shipyards[ k1 ]
      #      count = count + len(b1.away) + len(b1.docked)

        for k,b in self.shipyards.iteritems():
     #    print count, hangarSpace
       # b = self.shipyards[ k ]
         if b.building and count+stats.Costs[ k ].hangarSpace<= hangarSpace: #count < self.getMaxShips():
            b.build = b.build+self.getBuildRate()
            if b.build >= b.buildCost:
         #       b.amount = b.amount+1
                if isinstance( stats.Buildable[ k ], stats.HarvesterShipStats ):
                    b.docked.append( HarvesterShip(self.player, stats.Buildable[ k ], AiPilotHarvester(self), 0,0,0, 4, 0.0,0.0,0.0, 0) )
                else:
                    b.docked.append( ShipSingleWeapon(self.player, stats.Buildable[ k ], AiPilotFighter(self),0,0,0, 4, 0.0,0.0,0.0, 0)  )
                count = count + stats.Costs[ k ].hangarSpace
                if self.canBuild( k ):
                   self.buildShip( k )
                else:
                   b.building = False

        # missiles

        for k in self.missiles:
          b = self.missiles[ k ]
          if b.building and count+stats.Costs[ k ].hangarSpace<= hangarSpace: #count < self.getMaxMissiles():
            b.build = b.build+self.getBuildRate()
            if b.build >= b.buildCost:
                b.amount = b.amount+1
                count = count + stats.Costs[ k ].hangarSpace
                if self.canBuild( k ):
                   self.buildMissile( k )
                else:
                   b.building = False

        # resources
        for r in self.oreProcess:
            r.pos = r.pos + self.getBuildRate()
            if r.pos >= self.processLength:
                self.oreProcess.remove( r )
                self.ore = min(self.ore + r.amount,self.stats.maxOre)

        # energy
        basicGain = 0
        absorbtion = 0
    #    energyGain = 0
        if not self.inNebula: # RULE sun blocked out in the nebula
          absorbtion = self.getEnergyAbsorbtion()
        #  basicGain = 0
          for obj in game.astres:
            if isinstance( obj, Sun ):
                dist = distBetweenObjects( self, obj )
                if dist < obj.stats.energyRadius:
                    basicGain = basicGain+(obj.stats.energyRadius-dist)/obj.stats.energyRadius*obj.stats.maxEnergy
        self.energy = min(self.energy + absorbtion * basicGain,self.stats.maxEnergy)

        if thrustBoost: #  and self.thrust == self.stats.maxThrust:
            self.thrustBoost = thrustBoost * basicGain
       #     print basicGain
        else:
            self.thrustBoost = 0

        # repairs
        if self.repairing and self.ore >= self.getHullRepairRate(): #self.lastRepairsAt+self.repairDelay <= game.tick and self.ore > 0:
            if self.hull < self.stats.maxHull:
                self.hull = self.hull + self.getHullRepairRate()
                self.ore = self.ore - self.getHullRepairRate()
                self.repairDelay = game.tick

            for sy in self.shipyards.values():
              for ship in sy.docked: # self.dockedFighters + self.dockedHarvesters:
                if self.ore > 0 and ship.hull < ship.stats.maxHull:
                    ship.hull = ship.hull + self.getHullRepairRate()
                    self.ore = self.ore - self.getHullRepairRate()
                    self.repairDelay = game.tick
 
        if self.inNebula: # RULE nebula drains shield
            self.shield = self.shield*0.99
        else:
          if self.charging:
            if self.shield < self.stats.maxShield and self.energy >= self.getShieldRegenerationRate():
                self.shield = self.shield + self.getShieldRegenerationRate()
                self.energy = self.energy - self.getShieldRegenerationRate()
         # self
         # fighters

        (ao,ro,ag) = ShipWithTurrets.doTurn( self, game )

        ## Jumps
        if self.jumping:
            self.jumpCharge += 1 
            if self.jumpCharge == 100: # TODO set variable max charge, stats?
                (ao0,ro0,ag0) = self.jump( self.jumping, game )
                (ao,ro,ag) = (ao+ao0,ro+ro0,ag+ag0) 
                self.jumping = False
                self.jumpOverheat = config.fps*10 # TODO set variable value in stats?
        elif self.jumpOverheat:
            self.jumpOverheat -= 1

        ## update value tu civilians
        if game.tick%config.fps==3:
          value = 1000
          for turret in self.turrets:
            if turret.install:
                if turret.install.stats.special == ids.S_NUKE:
                    value -= 500
                elif turret.install.stats.special == ids.S_REACTOR:
                    value -= 200
                elif turret.install.stats.special == ids.S_CIVILIAN:
                    value += 500
            if turret.weapon:
                value += (turret.weapon.stats.energyDamage + turret.weapon.stats .massDamage)*turret.weapon.stats.freqOfFire/10
          if value <= 0:
            self.civilianValue = 1
          else:
            self.civilianValue = value
                
        return (ao,ro,ag)
    
    def addOreToProcess( self, amount ):
      #  self.oreProcess[ 0 ] += 
         self.oreProcess.append( OreBatch( amount ) )


    def addToHangar( self, ship, game ): # TODO add space check
        ship.enterHangar()
        ship.dockedAt = game.tick
        if ship in self.shipyards[ ship.stats.img ].away:
          self.shipyards[ ship.stats.img ].away.remove( ship )
        else:
          print "warning: addToHangar: ship not in away"
        self.shipyards[ ship.stats.img ].docked.append( ship )
      #  if isinstance( ship.ai, AiPilotFighter ):
     #      self.awayFighters.remove( ship )
      #      self.dockedFighters.append( ship )
        if isinstance( ship.ai, AiPilotHarvester ):
    #        self.awayHarvesters.remove( ship )
     #       self.dockedHarvesters.append( ship )
            if ship.ore > 0:
                self.addOreToProcess( ship.ore )
                ship.ore = 0

     #   print "docked"

    def canJump( self, game ):
        if self.inNebula:
            return False

        if self.jumping:
            can = True
        else:
            can = not self.jumpOverheat and self.energy >= self.stats.jumpEnergyCost
        if can:
            #for obj in game.astres:
            #    if isinstance( obj, Nebula ) and distLowerThanObjects( self, obj, self.stats.maxRadius+obj.stats.maxRadius):
           #         can = False
           #         break
            for obj in game.objects:
                if isinstance( obj, FlagShip ): # and distLowerThanObjects( self, obj, self.stats.marRadius+obj.stats.maxRadius):
                    for turret in obj.turrets:
                        if turret.install and turret.activated and turret.install.stats.special == ids.S_INTERDICTOR and distLowerThanObjects( self, obj, self.stats.maxRadius+turret.install.stats.specialValue):
                            can = False
                            break
        return can

    def getRadarRange( self ):
        radarRange = self.stats.radarRange
        for turret in self.turrets:
            if turret.install and turret.activated and turret.install.stats.special == ids.S_RADAR:
                radarRange = radarRange+turret.install.stats.specialValue

        if self.inNebula: # RULE nebula reduces radar range 
            radarRange = radarRange/4

        return radarRange

    def getEnergyAbsorbtion( self ):
        absorbtion = 1
        for turret in self.turrets:
            if turret.install and turret.activated and turret.install.stats.special == ids.S_SOLAR:
                absorbtion = absorbtion+turret.install.stats.specialValue
        return absorbtion

    def getShieldRegenerationRate( self ):
        return 0.1

    def getHullRepairRate( self ):
        return 0.05*self.getBuildRate()

    def getHangarSpace( self ):
        space = self.stats.hangarSpace
        for turret in self.turrets:
            if turret.install and turret.activated and turret.install.stats.special == ids.S_HANGAR:
                space = space+turret.install.stats.specialValue
        return space

    def getHangarUse( self ):
        space = 0
        for missile in self.missiles:
            space = space+self.missiles[missile].amount*stats.Costs[ missile ].hangarSpace

        for ship in self.shipyards:
            space = space+self.shipyards[ship].getCount()*stats.Costs[ ship ].hangarSpace

        return space

    def getJumpDelay( self ):
        return config.fps*3

    def getJumpCost( self ):
        return self.stats.jumpEnergyCost

    def die( self, game ):
        (ao,ro,ag) = Ship.die(self, game)
        return (ao,ro,ag)

    def removeShip( self, ship ):
        ship.ai.flagship = None
        for k in self.shipyards:
            if ship in self.shipyards[k].away:
                self.shipyards[k].away.remove( ship )
            if ship in self.shipyards[k].docked:
                self.shipyards[k].docked.remove( ship )

    def jump( self, (xd, yd), game  ):
        if self.canJump( game ):
          gfxs = [GfxExplosion((self.xp,self.yp),self.stats.maxRadius, sound=ids.S_EX_JUMP)]
          if distBetween( (self.xp, self.yp), (xd, yd) ) > self.getRadarRange():
            for k in self.shipyards:
              for s in self.shipyards[k].away: # self.awayFighters + self.awayHarvesters:
                self.removeShip( s )
                s .flaghsip = None
          self.xp, self.yp = xd, yd
          self.ai.goingTo = None
          gfxs.append( GfxExplosion((self.xp,self.yp),self.stats.maxRadius, sound=ids.S_EX_JUMP) )
          self.jumping = False
          self.turretPoss = {}
          return ([],[],gfxs)
        else:
          return ([],[],[])

    def delayedJump( self, (xd,yd) ):
        if self.jumping:
            charge = self.jumpCharge
        else:
            self.energy = self.energy - self.getJumpCost()
            charge = 0
        self.jumping = (xd, yd)
        self.jumpCharge = charge

    def emergencyJump( self ):
        self.energy = self.energy - self.getJumpCost()
        self.jumping = ((1-2*random())*config.universeWidth, (1-2*random())*config.universeHeight)

    def buildTurret( self, turret, toBuild ):
        if turret.building:
            self.ore = self.ore+turret.building.oreCostToBuild
            self.energy = self.energy+turret.building.energyCostToBuild

        turret.ai = None
        turret.weapon = None
        turret.install = None

        turret.building = toBuild
        turret.rr = (turret.stats.maxAngle+turret.stats.minAngle)/2

        if toBuild:
            self.ore = self.ore-toBuild.oreCostToBuild
            self.energy = self.energy-toBuild.energyCostToBuild

            turret.buildCost = toBuild.timeToBuild # oreCostToBuild
            turret.build = 0

    def destroyTurret( self, turret ):
        turret.weapon = None

    def buildShip( self, toBuild, switch=False ):
        if switch and self.shipyards[ toBuild ].building:
            self.shipyards[ toBuild ].building = False
            self.energy = self.energy+stats.Costs[ toBuild ].energyCostToBuild
            self.ore = self.ore+stats.Costs[ toBuild ].oreCostToBuild
        else:
            self.shipyards[ toBuild ].building = True
            self.shipyards[ toBuild ].build = 0
            self.shipyards[ toBuild ].buildCost = stats.Costs[ toBuild ].timeToBuild
            self.energy = self.energy-stats.Costs[ toBuild ].energyCostToBuild
            self.ore = self.ore-stats.Costs[ toBuild ].oreCostToBuild

    def buildMissile( self, toBuild, switch=False ):
        if switch and self.missiles[ toBuild ].building:
            self.missiles[ toBuild ].building = False
            self.energy = self.energy+stats.Costs[ toBuild ].energyCostToBuild
            self.ore = self.ore+stats.Costs[ toBuild ].oreCostToBuild
        else:
            self.missiles[ toBuild ].building = True
            self.missiles[ toBuild ].build = 0
            self.missiles[ toBuild ].buildCost = stats.Costs[ toBuild ].timeToBuild
            self.energy = self.energy-stats.Costs[ toBuild ].energyCostToBuild
            self.ore = self.ore-stats.Costs[ toBuild ].oreCostToBuild

    def canBuild( self, toBuild ):
        return self.energy >= stats.Costs[ toBuild ].energyCostToBuild \
          and self.ore >= stats.Costs[ toBuild ].oreCostToBuild

    def launchMissile( self, type, (x,y) ):
        self.missiles[ type ].target = (x,y)

    def getBuildRate( self ):
        rate = 1.0 + len( self.civilianShips )*0.3
        return rate

    def hit( self, game, angle, sender, energy=0, mass=0, pulse=False ):

        # RULE when pulsed e = e/3
        if pulse:
            self.energy = self.energy/3

        return ShipWithTurrets.hit( self, game, angle, sender, energy, mass, pulse )

    def selfDestruct( self, game ):
      if self.alive:
        # get explosion radius
        radius = self.stats.maxRadius
        for turret in self.turrets:
            if turret.install and turret.insta.stats.special == ids.T_GENERATOR:
                radius += turret.install.stats.specialValue

        # die and explode
        (ao,ro,fxs) = self.die( game)
        fxs.append( GfxExplosion( (self.xp,self.yp), radius, sound=ids.S_EX_NUKE ) )
        
        # hit ships in explosion range
        maxDamage = 1000
        for obj in game.objects:
            if obj.alive:
                dist = distLowerThanObjectsReturn( self, obj, radius+obj.stats.maxRadius )
                if dist:
                    angle = angleBetweenObjects( obj, self )
                    (ao1, ro1, fxs1 ) = obj.hit( game, angle, self.player, mass=maxDamage*dist/radius )

        return (ao,ro,fxs)
      else:
        return ([],[],[])

class OrbitalBase( FlagShip ):
    def __init__( self, player, stats, ai, xp, yp, zp=0, ori=0.0, xi=0, yi=0, zi=0, ri=0, thrust=0 ):
        FlagShip.__init__( self, player, stats, ai, xp, yp, zp, ori, xi, yi, zi, ri, thrust )
        self.headed = False
        self.inertiaControl = False

class HarvesterShip( ShipWithTurrets ):
    def __init__( self, player, sta, ai, xp, yp, zp=0, ori=0.0, xi=0, yi=0, zi=0, ri=0, thrust=0 ):
        self.player = player
        ShipWithTurrets.__init__( self, player, sta, ai, xp, yp, zp, ori, xi, yi, zi, ri, thrust )
        self.ore = 0
        for turret in self.turrets:
            turret.ai = AiTargeterTurret()
            turret.install = TurretInstall( self.stats.turretType )

        self.harvestedInRange = False

    def doTurn( self, game ):
        if self.ai.harvesting and self.orbiting:
            self.ore = min(self.ore + 0.1, self.stats.maxOre )

        return ShipWithTurrets.doTurn( self, game )



