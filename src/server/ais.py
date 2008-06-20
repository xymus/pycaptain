from random import randint, random, choice
from time import time
from math import pi, fabs, cos, sin

from common.utils import * 
from objects import Object, Asteroid, Sun, Nebula
from ships import Ship
from weapons import *
from players import Human
from common import config
from common import ids
# from ships import *

class AiPilot:
    def __init__(self):
        self.stance = 0
        self.goingTo = False
        self.dockingTo = False
        self.dockedTo = False
        self.attacking = False
        self.idle = True
        self.evading = False

    def goTo(self, ship, dest, destOri=0, orbitAltitude=2):
        """main goTo logic. 
Can change self.goingTo. May change self.attacking and self.dockingTo."""
        ship.orbiting = False
        self.goingTo = dest

        if isinstance( dest, Object ):
          if not dest.stats.orbitable:
            dest = (dest.xp, dest.yp)
          else:
      #  elif isinstance( dest, Object ) and dest.stats.orbitable:
            angle = angleBetweenObjects( dest, ship )
     #       print dest.stats.maxRadius*orbitAltitude
            dist = dest.stats.maxRadius*orbitAltitude # +ship.stats.maxRadius
            dest = (dest.xp+cos( angle )*dist, dest.yp+sin( angle )*dist)
        #    if ship.player:
      #      print dist

        dist = distBetween( (ship.xp, ship.yp), dest )
        if not isinstance( ship.player, Human ):
          if dist > 2000:
            if self.attacking:
                self.attacking = False
            if self.dockingTo:
                self.dockingTo = None
            return None

        if dist < max( 8, ship.stats.maxRadius/4 ):
            if ship.xi > 0 or ship.yi > 0:
	        ship.thrust = -1*ship.stats.maxReverseThrust
            else:
	        ship.thrust = 0

            if fabs( ship.ri ) >= 0.0005:
                if ship.ri > 0:
                    ship.rg = -0.3*ship.stats.maxRg
                else:
                    ship.rg = 0.3*ship.stats.maxRg
 
            if isinstance( self.goingTo, Object ) and self.goingTo.stats.orbitable:
                ship.orbiting = self.goingTo

            self.goingTo = False
            self.evading = False
            self.idle = True
            
       #     self.idle( ship )
        else:
            destAngle = angleBetween( (ship.xp, ship.yp), dest )
            angle = angleDiff( destAngle, ship.ori )

            absAngle = fabs( angle )
            if absAngle >  ship.stats.maxRg/5: # 0.08:
                ship.rg = ship.stats.maxRg*8*angle/pi

                if ship.ai and ship.ai.attacking:
                    ship.rg += (2-random())*(0.1*ship.stats.maxRg)

                if ship.rg > ship.stats.maxRg:
                    ship.rg = ship.stats.maxRg
                if ship.rg < -1*ship.stats.maxRg:
                    ship.rg = -1*ship.stats.maxRg
            elif ship.ai and ship.ai.attacking:
                ship.rg += (2-random())*(0.3*ship.stats.maxRg)

                if ship.rg > ship.stats.maxRg:
                    ship.rg = ship.stats.maxRg
                if ship.rg < -1*ship.stats.maxRg:
                    ship.rg = -1*ship.stats.maxRg


            maxThrust = ship.stats.maxThrust+ship.thrustBoost
            if dist > maxThrust*100:
	    	ship.thrust = maxThrust
            else:
	    	ship.thrust = maxThrust*(dist/(maxThrust*100)) - 0.8 * absAngle * maxThrust / pi 
                if ship.thrust < 0 and ship.thrust < -1*ship.stats.maxReverseThrust:
                    ship.thrust = -1*ship.stats.maxReverseThrust

            self.idle = False


    def doTurn( self, ship, game ):
      if ship.pulsedUntil < game.tick:
        removedObjects = []

        if self.goingTo:
            self.goTo( ship, self.goingTo )

        if self.dockingTo and not self.dockingTo.alive:
            print "docking to not alive"
            self.dockingTo = None

        if self.idle:
            if self.dockingTo:
                if ship.zp >= self.dockingTo.zp \
                  and areOver( ship, self.dockingTo ): # somewhere over the mothership
                    self.evade( ship, self.dockingTo, self.dockingTo.stats.maxRadius * 1.5 )
                elif distLowerThanObjects( ship, self.dockingTo, min(20, self.dockingTo.stats.maxRadius/3) ): #distBetweenObjects( ship, self.dockingTo ) < min(20, self.dockingTo.stats.maxRadius / 3): # ready to dock
                    self.dockingTo.addToHangar( ship, game )
                    removedObjects.append( ship )
                    self.dockedTo = self.dockingTo
                    self.dockingTo = False
                    self.idle = True
                else: # away
                    ship.zp = self.dockingTo.zp-2
                    self.goTo( ship, self.dockingTo )

        if self.idle:
            if fabs( ship.ri ) >= 0.0005:
                if ship.ri > 0:
                    ship.rg = -0.1*ship.stats.maxRg
                else:
                    ship.rg = 0.1*ship.stats.maxRg
       #     if fabs( ship.xi ) >= 0.05
            

        return ( [], removedObjects, [] )
      else:
        return ( [], [], [] )
    #    if self.idle:
    #    if self.intercepting:
                	

  #  def atDestination(self, ship):
  #      if self.dockingTo and distBetweenObjects( self.ship, self.dockingTo ) < self.dockingTo.stats.maxRadius / 2:
  #          self.dockedTo = self.dockingTo

    def evade( self, ship, target, dist ):
        self.idle = True
        self.dockedTo = False
        self.evading = True
        angle = random()*2*pi
     #   dist = self.dockingTo.stats.radiusAt( angle ) * 1.5
        dest = ( target.xp+cos(angle)*dist, target.yp+sin(angle)*dist )
        self.goTo( ship, dest )

    def dock( self, ship, motherShip, game ):
        self.idle = True
        self.dockedTo = False
        self.attacking = False
        self.evading = False
        self.dockingTo = motherShip

        if ship.zp >= self.dockingTo.zp: # must go under the ship
     #       for obj in utils.mY # TODO skipped a lot of steps
     #     and not areOver( ship, self.dockingTo ):
            ship.zp = self.dockingTo.zp - 1    #self.evade( ship, self.dockingTo, self.dockingTo.stats.maxRadius * 1.5 )

    def attack( self, ship, target ):
        self.idle = True
        self.goingTo = False
        self.evading = False
        self.attacking = target

    def stop( self, ship ):
        self.idle = True
        self.goingTo = (ship.xp+ship.xi*10,ship.yp+ship.yi*10)
        self.attacking = False
        self.evading = False

  #  def goToOrbit( self, target ):
    def died( self, ship, game ):
        pass


    def getRandomGuardPosition(self, ship, target, closeness ):
   #     print "getting new dest"
        dist = target.stats.maxRadius*closeness
        return (randint(int(target.xp-dist),int(target.xp+dist)), randint(int(target.yp-dist),int(target.yp+dist)) )

    def hitted( self, ship, game, angle, sender, energy, mass, pulse ):
        pass


class AiPilotFaction( AiPilot ):
    def __init__(self):
        AiPilot.__init__(self)
        self.hittedAt = -1000

    def doTurn( self, ship, game):
        pass

    def hitted( self, ship, game, angle, sender, energy, mass, pulse ):
#        print "hitted"
        AiPilot.hitted( self, ship, game, angle, sender, energy, mass, pulse )
        self.hittedAt = game.tick
        if sender and not self.attacking and game.getRelationBetween( ship.player, sender )<0:
#            print "looking"
            bestDist = 10000
            for obj in game.objects:
                if isinstance( obj, Ship ):
                    dist = utils.distLowerThanObjectsReturn( obj, ship, 1000 )
                    if dist and dist < bestDist:
                        bestDist = dist
                        self.attacking = obj
#                        print "now attacking"
                    

    def needsHelp( self, game ):
        return self.hittedAt > game - config.fps*10

class AiPilotDefense( AiPilotFaction ):
    def __init__(self, defended, radius ):
        AiPilotFaction.__init__(self)
        self.defended = defended
        self.radius = int(radius)
        self.lastDestSetAt = -1000
    #    self.setNewDest()

    def doTurn( self, ship, game):
        if self.attacking and not self.attacking.alive:
            self.attacking = None

        ( ao, ro, ag ) = AiPilot.doTurn( self, ship, game )

        if not self.attacking and self.idle and not self.dockingTo and game.tick%(0.5*config.fps)==2:
            bestDist = 1000
            for obj in game.objects:
                if isinstance( obj, Ship ) and obj.alive and obj.player and game.getRelationBetween( ship.player, obj.player ) < 0:
                  dist = utils.distLowerThanObjectsReturn( ship, obj, bestDist) # obj.ai and obj.ai.attacking == ship:
                  if dist:
                    self.attacking = obj
                    bestDist = dist # utils.distBetweenObjects( ship, obj )
                    break 

        if not self.dockingTo and not self.attacking and (self.idle or self.lastDestSetAt<game.tick-config.fps*5 ):
            self.goTo( ship, self.setNewDest( ship, game) )

        if not self.dockingTo and self.attacking:
            if not self.evading and distLowerThanObjects( ship, self.attacking, ship.weapon.stats.minRange+self.attacking.stats.maxRadius ):
                self.evade( ship, self.attacking, ship.weapon.stats.maxRange*0.9+self.attacking.stats.maxRadius/2 )
            elif self.idle:
                self.goTo( ship, self.attacking )

            if self.attacking and ship.weapon.canFire( ship, game ):
                angle = angleBetweenObjects( ship, self.attacking )
                if ship.ori >= angle - pi/40 \
                  and ship.ori <= angle + pi/40: # TODO
                    if distLowerThanObjects( ship, self.attacking, ship.weapon.stats.maxRange+self.attacking.stats.maxRadius ):
                        ( ao1, ro1, ag1 ) = ship.weapon.fire( ship, game, self.attacking )
                        ( ao, ro, ag ) = ( ao+ao1, ro+ro1, ag+ag1 )

        return ( ao, ro, ag)

    def setNewDest(self,ship, game):
        dist = randint( self.radius/2, self.radius)
        angle = 2*pi*random()
        if isinstance( self.defended, Object ):
            (x,y) = (self.defended.xp, self.defended.yp)
        else:
            (x,y) = self.defended
        self.goingTo = ( x+dist*cos(angle), y+dist*sin(angle) )
        self.lastDestSetAt = game.tick
        return self.goingTo

class AiPilotPolice( AiPilotDefense ):
    def __init__( self, defended, radius ):
        AiPilotDefense.__init__(self, defended, radius) 
        self.policingRange = 500

    def doTurn( self, ship, game):
        if not self.attacking and game.tick%(config.fps/2) == 7:
            for obj in game.objects:
                if obj.player and obj.player != ship.player and isinstance( obj.player, Human ) and obj.player.online and obj.ai and obj.ai.attacking and distLowerThanObjects( ship, obj, self.policingRange ) and distLowerThanObjects( ship, obj.ai.attacking, self.policingRange ):
                    self.attack( ship, obj )
                    break

        return AiPilotDefense.doTurn( self, ship, game)

class AiPilotOrbiter( AiPilot ):
    pass

class AiPilotFighter( AiPilot ):
    def __init__(self,flagship):
        AiPilot.__init__(self)
        self.flagship = flagship

    def doTurn( self, ship, game ):
      if self.attacking and not self.attacking.alive:
            self.attacking = None

      if not self.flagship and not self.attacking:
        ( ao, ro, ag ) = ship.die( game )
      else:
        ( ao, ro, ag ) = AiPilot.doTurn( self, ship, game )


        if not self.attacking and self.idle and not self.dockingTo and self.flagship.ai.attacking: #  and game.tick%(0.5*config.fps)==2:
            bestDist = 1000
            for obj in game.objects:
                if isinstance( obj, Ship ) and obj.alive and obj.player and game.getRelationBetween( ship.player, obj.player ) < 0: 
                  dist = utils.distLowerThanObjectsReturn( ship, obj, bestDist) # obj.ai and obj.ai.attacking == ship:
                  if dist:
                    self.attacking = obj
                    bestDist = dist # utils.distBetweenObjects( ship, obj )
                    break 

        if not self.dockingTo and self.idle and not self.attacking:
            self.goTo( ship, self.getRandomGuardPosition(ship, self.flagship, 1.5) )

        if not self.dockingTo and self.attacking:
            if not self.evading and distLowerThanObjects( ship, self.attacking, ship.weapon.stats.minRange+self.attacking.stats.maxRadius ):
                self.evade( ship, self.attacking, ship.weapon.stats.maxRange*0.9+self.attacking.stats.maxRadius/2 )
            elif self.idle:
                self.goTo( ship, self.attacking )

            if self.attacking and ship.weapon.canFire( ship, game ):
                angle = angleBetweenObjects( ship, self.attacking )
                if ship.ori >= angle - pi/40 \
                  and ship.ori <= angle + pi/40: # TODO
                    if distLowerThanObjects( ship, self.attacking, ship.weapon.stats.maxRange+self.attacking.stats.maxRadius ):
                        ( ao1, ro1, ag1 ) = ship.weapon.fire( ship, game, self.attacking )
                        ( ao, ro, ag ) = ( ao+ao1, ro+ro1, ag+ag1 )

      return ( ao, ro, ag)

    #def getRandomGuardPosition(self, ship, target, closeness ):
   #     dist = target.stats.maxRadius*closeness
  #      return (randint(int(target.xp-dist),int(target.xp+dist)), randint(int(target.yp-dist),int(target.yp+dist)) )
#
 #   def getRandomGuardPosition(self, ship, target, closeness ):
 #       dist = target.stats.maxRadius*closeness
#        return (randint(int(target.xp-dist),int(target.xp+dist)), randint(int(target.yp-dist),int(target.yp+dist)) )

    def died( self, ship, game ):
        if self.flagship:
            self.flagship.removeShip( ship )


class AiCaptain( AiPilot ):
    """AI for ships with turrets"""
    def __init__(self,player):
        AiPilot.__init__(self)
        self.launching = {}
        for s in player.race.ships:
            self.launching[ s.img ] = False
   #     self.launchingFighters = False
   #    self.launchingHarvesters = False

    def doTurn( self, ship, game):
        if self.attacking and not self.attacking.alive:
            self.attacking = None

        addedObjects0 = []
        removedObjects0 = []
        addedGfxs0 = []

        for k in self.launching:
            if self.launching[ k ] and len( ship.shipyards[ k ].docked ) > 0 and ship.lastLaunchAt + ship.stats.launchDelay < game.tick:
                for s in ship.shipyards[ k ].docked:
                    if s.dockedAt + ship.stats.launchDelay*3 < game.tick:
                        hangar, hangarAngle = choice(ship.stats.hangars)

                        (s.xp,s.yp) = (ship.xp+hangar.dist*cos( hangar.angle ), ship.yp+hangar.dist*sin( hangar.angle ))
                        angle = ship.ori+hangarAngle
                        (s.xi,s.yi) = (5*cos(angle),5*sin(angle))
                        s.ori = angle

                        s.ai.evade( s, ship, ship.stats.maxRadius*1.5 )
                        addedObjects0.append( s )
                        s.zp = ship.zp-2
                        ship.shipyards[ k ].away.append( s )
                        ship.shipyards[ k ].docked.remove( s )
                        ship.lastLaunchAt = game.tick
                        break
            elif not self.launching[ k ]:
              for s in ship.shipyards[ k ].away:
                s.ai.dock( s, ship, game )

        if self.attacking:
            pass
        elif game.tick%(config.fps/2)==9: # no target
            bestObj = None
            bestDist = ship.stats.radarRange
            for obj in game.objects:
                if isinstance( obj, Ship ) and obj.alive and obj.player and obj.player != ship.player and game.getRelationBetween( ship.player, obj.player ) < 0: #and obj.ai and obj., ai.attacking and obj.ai.attacking.player == ship.player:
                     dist=distLowerThanObjectsReturn( ship, obj, bestDist )
                     if dist: #distLowerThanObjects( ship, obj, bestDist ):#dist < bestDist:
                         bestObj = obj
                         bestDist = dist

            if bestObj:
                self.attack( ship, bestObj )#attacking = bestObj

        # turrets / weapons
        for turret in ship.turrets:
            if turret.ai and turret.activated: # if turret is armed
                (ao, ro, ag) = turret.ai.doTurn( ship, turret, game, self.attacking)
                addedObjects0 = addedObjects0 + ao
                removedObjects0 = removedObjects0 + ro
                addedGfxs0 = addedGfxs0 + ag

        (addedObjects1, removedObjects1, addedGfxs1) = AiPilot.doTurn( self, ship, game )
        return (addedObjects0+addedObjects1, removedObjects0+removedObjects1, addedGfxs0+addedGfxs1)

    def launchShips(self, ship, game, type ): # Fighters(self, ship ):
        self.launching[ type ] = True #Fighters = True
        
    def recallShips(self, ship, game, type ): # Fighters(self, ship ):
        self.launching[ type ] = False
        for s in ship.shipyards[ type ].away: #awayFighters:
            s.ai.dock( s, ship, game )

    def stop(self, ship):
        AiPilot.stop( self, ship )
        for k in ship.shipyards:
          if k != ids.S_HARVESTER:
            for s in ship.shipyards[ k ].away:
              s.ai.stop( s )
        for t in ship.turrets:
          if t.ai:
            t.ai.target = None

    def attack( self, ship, target ):
        self.idle = True
        self.goingTo = False
        self.attacking = target
        for k in ship.shipyards:
            if k != ids.S_HARVESTER:
                for s in ship.shipyards[ k ].away:
                    if s.ai.attacking != self.attacking:
                        s.ai.attack( ship, self.attacking )


class AiGovernor( AiCaptain ):
    def goTo(self, ship, dest, destOri=0, orbitAltitude=2):
        pass

class AiTurret:
    def __init__( self ):
        self.target = None
        self.attacking = False
        self.rTarget = 0
        self.foundNothingAt = -1000

    def doTurn( self, ship, turret, game, attack):

        pos = ship.getTurretPos( turret )
        
        ## test if main target is in range
        if ship.ai.attacking and ship.ai.attacking.alive and ship.ai.attacking != self.target and self.objectInRange( ship, turret, pos, ship.ai.attacking ): 
            att = self.getAngleToTarget( ship, turret, pos, ship.ai.attacking )
            if self.angleInRange( ship, turret, att ):
                self.target = ship.ai.attacking

        ## already have a target, previous or super
        if self.target and self.objectInRange( ship, turret, pos, self.target ): 
            att = self.getAngleToTarget( ship, turret, pos, self.target )
            if self.angleInRange( ship, turret, att ):
                self.angleToTarget = self.rTarget = att
            else:
                self.target = None

      #  if turret.stats.minAngle != 0 and turret.stats.maxAngle != 0 \
     #     and self.rTarget > turret.stats.maxAngle or self.rTarget < turret.stats.minAngle:
       #     halfUncovered = (2*pi-(turret.stats.maxAngle-turret.stats.minAngle))/2
       #     if self.rTarget > turret.stats.maxAngle:
       #       if self.rTarget < turret.stats.maxAngle+halfUncovered:
       #         self.rTarget = turret.stats.maxAngle
      #        else:
      #          self.rTarget = turret.stats.minAngle
      #      else:
      #        if self.rTarget > turret.stats.minAngle-halfUncovered:
      #          self.rTarget = turret.stats.minAngle
      #        else:
      #          self.rTarget = turret.stats.maxAngle

        ## return to default position
        if not self.target:
            self.angleToTarget = self.rTarget = turret.stats.defaultAngle
        
        ## turn turret
        angleD = angleDiff(self.rTarget, turret.rr)
        if fabs( angleD ) > turret.install.stats.turretSpeed:
            if angleD < 0:
                turret.rr = turret.rr - turret.install.stats.turretSpeed
            else:
                turret.rr = turret.rr + turret.install.stats.turretSpeed
        else:
            turret.rr = self.rTarget

        return ( [], [], [] )

    def getAngleToTarget( self, ship, turret, pos, target ):
        if turret.weapon.stats.speed == 0: 
            targetPos = (target.xp, target.yp)
        else:
            dist = distBetweenObjects( ship, target )
            targetPos = (target.xp+target.xi*dist/turret.weapon.stats.speed, target.yp+target.yi*dist/turret.weapon.stats.speed)
        angle = angleBetween( pos, targetPos )
            
        return (angle-ship.ori)%(2*pi)

    def angleInRange( self, ship, turret, angle ):
         if turret.stats.minAngle == 0 and turret.stats.maxAngle == 0:
             return True
         elif isinstance( turret.weapon, MissileWeaponTurret ):
             return True

         angle = angle % (2*pi)
         if turret.stats.maxAngle < turret.stats.minAngle:
            return not (angle >= turret.stats.maxAngle and angle <= turret.stats.minAngle)
         else:
            return angle <= turret.stats.maxAngle and angle >= turret.stats.minAngle

    def distInRange( self, ship, turret, dist ):
        return dist <= turret.weapon.stats.maxRange and dist >= turret.weapon.stats.minRange

    def objectInRange( self, ship, turret, pos, target ):
        dist = distLowerThanReturn( pos, (target.xp, target.yp), turret.weapon.stats.maxRange+target.stats.maxRadius)
        if dist:
            return dist >= turret.weapon.stats.minRange
        else:
            return False #dist <= turret.weapon.stats.maxRange and dist >= turret.weapon.stats.minRange

class AiWeaponTurret( AiTurret ):
    def doTurn( self, ship, turret, game, attack):

        ## remove dead target
        if self.target and not self.target.alive:
            self.target = None
            
        ## check if target still in range
        if self.target:
            pos = ship.getTurretPos( turret )
            if not self.objectInRange( ship, turret, pos, self.target ):
                self.target = None
            else:
                att = self.getAngleToTarget( ship, turret, pos, self.target )
                if not self.angleInRange(  ship, turret, att ):
                    self.target = None
                    
        ## find new target
        if not self.target and self.foundNothingAt < game.tick: #  and attack: # attack: #-config.fps/2: # doesn't have a target, non or out of range
         #   posTargets = []
            bestObj = None
            bestAngle = 2*pi
            pos = ship.getTurretPos( turret )
            foundSomethingClose = False
            for obj in game.objects:
                if isinstance( obj, Ship ) and obj.alive and obj.player and obj.player != ship.player and obj.ai and obj.ai.attacking and obj.ai.attacking.player and game.getRelationBetween( obj.ai.attacking.player, ship.player ) < 0 and self.objectInRange( ship, turret, pos, obj ):
                   att = self.getAngleToTarget( ship, turret, pos, obj )
                   foundSomethingClose = True
                   if self.angleInRange(  ship, turret, att ) and fabs( angleDiff( turret.rr, att )) < bestAngle:
                         bestObj = obj

            if bestObj:
                self.target = bestObj
                self.angleToTarget = self.rTarget = bestAngle
            else:
              if foundSomethingClose:
                self.foundNothingAt = game.tick+config.fps/6
              else:
                self.foundNothingAt = game.tick+config.fps/3

        ## return to default position
      #  if not self.target: # still doesn't have a target
      #      self.angleToTarget = self.rTarget = turret.stats.defaultAngle

        ( ao0, ro0, ag0 ) = AiTurret.doTurn( self, ship, turret, game, attack)

        if self.target and turret.weapon.canFire( ship, turret, game ):
            ( ao1, ro1, ag1 ) = self.fireAtWill( ship, turret, game )
            ( ao0, ro0, ag0 ) = ( ao0+ao1, ro0+ro1, ag0+ag1 )

        return ( ao0, ro0, ag0 )

    def fireAtWill( self, ship, turret, game ):
        if isinstance( turret.weapon, LaserWeaponTurret ):
            angleError = pi/8
        else:
            angleError = pi/16
            
        if angleError >= 2*pi or fabs(angleDiff(self.angleToTarget, turret.rr)) < angleError: # * turret.weapon.stats.certainty/100:
            dist = distBetween( ship.getTurretPos( turret ), (self.target.xp, self.target.yp) )
            if dist >= turret.weapon.stats.minRange and dist-self.target.stats.maxRadius <= turret.weapon.stats.maxRange:
                return turret.weapon.fire( ship, turret, game, self.target )
        return ([],[],[])
        
        
class AiWeaponTurretStable( AiWeaponTurret ):
    def fireAtWill( self, ship, turret, game ):
        dist = distBetween( ship.getTurretPos( turret ), (self.target.xp, self.target.yp) )
        if dist >= turret.weapon.stats.minRange and dist-self.target.stats.maxRadius <= turret.weapon.stats.maxRange:
            return turret.weapon.fire( ship, turret, game, self.target )
        else:
            return ([],[],[])
        
class AiSpecialMissileTurret( AiTurret ):
    def doTurn( self, ship, turret, game, attack):
        ( ao0, ro0, ag0 ) = AiTurret.doTurn( self, ship, turret, game, attack)
        if ship.missiles[ turret.weapon.stats.projectile.img ].target \
          and turret.weapon.canFire( ship, turret, game ):
            ( ao1, ro1, ag1 ) = turret.weapon.fire( ship, turret, game, ship.missiles[ turret.weapon.stats.projectile.img ].target )
            ( ao0, ro0, ag0 ) = ( ao0+ao1, ro0+ro1, ag0+ag1 )
            ship.missiles[ turret.weapon.stats.projectile.img ].target = None
        return  ( ao0, ro0, ag0 )

class AiRotatingTurret( AiTurret ):
    def doTurn( self, ship, turret, game, attack):
        turret.rr = turret.rr+turret.install.stats.turretSpeed
        return ([],[],[])

class AiSolarTurret( AiTurret ):
    def doTurn( self, ship, turret, game, attack):
        if not self.target or game.tick%(config.fps*10)==0:
            sunDist = None
            for obj in game.astres:
                if isinstance( obj, Sun ):
                    dist = distLowerThanObjectsReturn( ship, obj, sunDist )
                    if not sunDist or dist: #dist < sunDist:
                        self.target = obj
                        sunDist = dist

        if self.target:
          angle = angleBetweenObjects( ship, self.target )-ship.ori
          angleD = angleDiff(angle, turret.rr)
          if fabs( angleD ) > turret.install.stats.turretSpeed:
            if angleD < 0:
                turret.rr = turret.rr - turret.install.stats.turretSpeed
            else:
                turret.rr = turret.rr + turret.install.stats.turretSpeed
          else:
            turret.rr = angle

        return ([],[],[])

class AiTargeterTurret( AiTurret ):
    def doTurn( self, ship, turret, game, attack):
        #
        #if not self.target and ship.ai.attacking:
        #    self.target = ship.ai.attacking
        self.target = attack
        if game.tick%(config.fps) == 9:
          if self.target:
            self.rTarget = angleBetweenObjects( ship, self.target )-ship.ori
          else:
            self.rTarget = turret.stats.defaultAngle

        
        angleD = angleDiff(self.rTarget, turret.rr)
        if fabs( angleD ) > turret.install.stats.turretSpeed:
            if angleD < 0:
                turret.rr = turret.rr - turret.install.stats.turretSpeed
            else:
                turret.rr = turret.rr + turret.install.stats.turretSpeed
        else:
            turret.rr = self.rTarget

        return ( [], [], [] )
            

#from ships import FlagShip
class AiPilotHarvester( AiPilot ):
    def __init__(self,flagship):
        AiPilot.__init__(self)
        self.flagship = flagship
        self.harvesting = False

    def doTurn( self, ship, game ):
        # idle			
        # harvesting			goTo source
        # idle harvesting		at source
        # orbiting harvesting		atually harvesting
        # idl orbiting harvesting	done harvesting -> docking
	# docking	

        if not self.flagship or not self.flagship.alive: #  or not distLowerThanObjects( self.flagship, ship, :
            self.flagship = None
            bestDist = 5000
            for obj in game.objects:
              if isinstance( obj, Ship ) and obj.shipyards and obj.player and obj.player.race.defaultHarvester == ship.stats:
              #  dist = distBetweenObjects( ship, obj )
                if distLowerThanObjects( ship, obj, bestDist ): #dist < bestDist:
                    dist = bestDist
                    self.flagship = obj

            if self.flagship: 
                self.flagship.shipyards[ ship.stats.img ].away.append( ship )
                ship.player = self.flagship.player
            else:
                ship.die( game )

        if not self.dockingTo and not self.harvesting and self.flagship and self.flagship.noOreCloseAt < game.tick-3*config.fps:
              distFound = ship.stats.maxRange+1
              for obj in game.harvestables:
                    dist = distLowerThanObjectsReturn( ship, obj, distFound )
                    if dist: 
                        distFound = dist
                        self.harvesting = obj

              if not self.harvesting: # found nothing
                  self.flagship.noOreCloseAt = game.tick
                  self.goTo( ship, self.getRandomGuardPosition(ship, self.flagship, 1) )

        if self.harvesting:
            for turret in ship.turrets:
                turret.ai.target = self.harvesting
            if ship.ore >= ship.stats.maxOre:
                self.idle = True
                self.harvesting = False
                for turret in ship.turrets:
                    turret.ai.target = None

                self.dockingTo = self.flagship
                self.orbiting = False
            elif not ship.orbiting: # self.idle and 
                self.goTo( ship, self.harvesting, orbitAltitude=0.8 )
        else:
            for turret in ship.turrets:
                turret.ai.target = None

        # turrets / weapons
        for turret in ship.turrets:
           #if turret.weapon: # if turret is armed
                turret.ai.doTurn( ship, turret, game, self.harvesting)

        return AiPilot.doTurn( self, ship, game )

    def dock( self, ship, target, game ):
        self.harvesting = False
        AiPilot.dock( self, ship, target, game )

    def died( self, ship, game ):
        if self.flagship:
            self.flagship.removeShip( ship )

# from ais import AiCaptain
#from ships import FlagShip
class AiCivilian( AiPilot ):
    def __init__( self ):
        AiPilot.__init__( self )
        self.follows = None
        self.lastPosAt = 0
        self.patience = config.fps * 2

    def doTurn( self, ship, game ):
        if self.follows and not self.follows.alive:
            self.follows.civilianShips.remove( ship )
            self.follows = None

        if not self.follows and game.tick%20 == 0:
            fs = None
            fsDist = ship.stats.influenceRadius + 1
            for obj in game.objects:
                if isinstance( obj, Ship ) and obj.shipyards:
                   # dist = distBetweenObjects( ship, obj )
                    dist = utils.distLowerThanObjectsReturn( ship, obj, fsDist )
                    if dist : # distLowerThanObjects( ship, obj, fsDist ): # fsDist:
                        fs = obj
                        fsDist = dist
            if fsDist <= ship.stats.influenceRadius:
                self.follows = fs
                self.follows.civilianShips.append( ship )
        
        if self.follows:
            if game.tick%120 == 0:
              valueFollowed = self.evalShip( self.follows )
              for obj in game.objects:
                if isinstance( obj, Ship ) and obj.shipyards and distLowerThanObjects( ship, obj, ship.stats.influenceRadius ):
                    valueOther = self.evalShip( obj )
                    if float(valueOther)/valueFollowed > float(len( obj.civilianShips )+1) / (len( self.follows.civilianShips)+1):
                       self.follows.civilianShips.remove( ship )
                       self.follows = obj
                       self.follows.civilianShips.append( ship )
                
            if self.idle or self.lastPosAt < game.tick - self.patience:
                # get random position
                self.goTo( ship, self.getRandomGuardPosition( ship, self.follows, 2 )  )
                self.lastPosAt = game.tick

        elif not self.goingTo and not ship.orbiting: # found nothing to follow
            oo = None
            ooDist = ship.stats.influenceRadius*10
            for obj in game.astres:
                if obj.stats.orbitable:
                    dist = distLowerThanObjectsReturn( ship, obj, ooDist )
                    if dist: # distLowerThanObjects( ship, obj ): #dist < ooDist:
                        oo = obj
                        ooDist = dist
            if oo: 
                self.goTo( ship, oo )

        ( ao, ro, ag ) = AiPilot.doTurn( self, ship, game )
        return ( ao, ro, ag )

    def evalShip( self, ship ): # TODO
        return ship.civilianValue

    def getRandomGuardPosition(self, ship, target, closeness ):
        dist = target.stats.maxRadius*closeness
     #   (x,y) = (randint(int(target.xp-dist),int(target.xp+dist)), randint(int(target.yp-dist),int(target.yp+dist)) )
        diff = 6 * config.fps * target.stats.maxThrust / ship.stats.maxThrust
    #    (x,y) = ( x+cos(),  )
        return ( randint(int(target.xp-dist),int(target.xp+dist)) + diff*target.xi, 
                 randint(int(target.yp-dist),int(target.yp+dist)) + diff*target.yi )

    def died( self, ship, game ):
        if self.follows:
            self.follows.civilianShips.remove( ship )

class AiPlayer:
    def __init__( self, player ):
        self.player = player

    def doTurn( self, game ):
        pass

# class Player
# class Captain FlagShip Governor
# class fighter
# class harvester
# class ? harvesterDispatcher
# class civilian ship

# AITurretDummy
# AiTurretRotating
# AiTurretCombat



