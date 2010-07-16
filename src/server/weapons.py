from math import sin, cos, atan, atan2, pi, fabs
from random import random, randint

import stats
from common import utils
from common import config
from objects import Object
from ships import Ship
from common.gfxs import *

def explode( self, game, explosionRange, energyDamage=0, massDamage=0, pulseLength=0, sender=None, deadlyToSelf=True, sound=ids.S_EX_PULSE ):
    (ao,ro,ag) = ([],[],[])
    for obj in game.objects.getWithinRadius( self, explosionRange ):
        if obj.alive and obj.player:
             (ao0, ro0, ag0) = obj.hit( game, utils.angleBetweenObjects( obj, self ), sender, energyDamage, massDamage, pulse=pulseLength )
             (ao, ro, ag) = (ao+ao0, ro+ro0, ag+ag0)
    
    if deadlyToSelf:
        self.alive = False
        ro.append( self )
        
    ag.append( GfxExplosion( self.pos, explosionRange, sound=sound ) )
    
    return (ao, ro, ag)

class Weapon:
    def __init__( self, stats ):
        self.stats = stats
        self.lastFireAt = 0
	self.weaponSet = 0

    def canFire( self, ship, game ):
        return self.lastFireAt + self.stats.freqOfFire/len( ship.stats.weaponPositions ) < game.tick

    def fire( self, ship, game ):
        self.lastFireAt = game.tick
        return ([],[],[])

    def getPoss( self, ship, game ):
        for pos in ship.stats.weaponPositions[ self.weaponSet ]:
           yield (ship.xp + pos.dist*cos(pos.angle+ship.ori), ship.yp + pos.dist*sin(pos.angle+ship.ori) )
 	self.weaponSet = (self.weaponSet+1)%len( ship.stats.weaponPositions )

class WeaponTurret( Weapon ):
    def canFire( self, ship, turret, game ):
    #    return Weapon.canFire( self, ship, game ) \
        return self.lastFireAt + self.stats.freqOfFire/len( turret.install.stats.weaponPositions ) < game.tick \
           and ship.energy >= turret.install.stats.energyPerUse \
           and ship.ore >= turret.install.stats.orePerUse

    def fire( self, ship, turret, game ):
        (ao,ro,gfxs) = Weapon.fire( self, ship, game )
        ship.energy = ship.energy - turret.install.stats.energyPerUse
        ship.ore = ship.ore - turret.install.stats.orePerUse
        return ([],[],gfxs)

    def getPoss( self, ship, turret, game ):
        turretPos = ship.getTurretPos( turret )
        for pos in turret.install.stats.weaponPositions[ self.weaponSet ]:
            yield (turretPos[0] + pos.dist*cos(pos.angle+turret.rr+ship.ori), turretPos[1] + pos.dist*sin(pos.angle+turret.rr+ship.ori) )
 	    self.weaponSet = (self.weaponSet+1)%len( turret.install.stats.weaponPositions )

class LaserWeapon( Weapon ):
    def fire( self, ship, game, target ):
        (ao,ro,gfxs) = Weapon.fire( self, ship, game )
        for o in self.getPoss( ship, game ):
          (ao0, ro0, gfxs0) = self.hits( o, ship.ori, game, ship, target, ship.weapon )
          (ao, ro, gfxs) = (ao+ao0, ro+ro0, gfxs+gfxs0)
        return (ao,ro,gfxs)

    def hits( self, (xo,yo), ori, game, ship, target, weapon ):
        """Logic: compares the angle to target with the weapon orientation to atan( target.radius / dist between weapon and target )"""
        angle = utils.angleBetween( (xo,yo), (target.xp,target.yp) )
        dist = utils.distBetween( (xo,yo), (target.xp,target.yp) )
        if dist:
            angleSec = atan( float(target.stats.radius)/dist )
        else:
            angleSec = 0
        
        diff = (ori-angle)%(2*pi)

        if diff < angleSec or 2*pi-diff < angleSec: ## hit!
            a = ori+pi
            hullBefore = target.hull
            (ao, ro, gfxs) = target.hit( game, pi+ori, ship.player, weapon.stats.energyDamage, weapon.stats.massDamage )  
            if hullBefore != target.hull: # went throught the shield
                d = ( xo + cos(ori)*dist, yo + sin(ori)*dist )
            else:
                d = ( xo + cos(ori)*(dist-target.stats.maxRadius/2), yo + sin(ori)*(dist-target.stats.maxRadius/2) )
        else:
            (ao, ro, gfxs) = ([],[],[])
            d = ( xo + cos(ori)*weapon.stats.maxRange, yo + sin(ori)*weapon.stats.maxRange )
        
      #  print (xo,yo), max( ship.zp, target.zp)+1, d, weapon.stats.laserWidth, 0
        gfxs.append( weapon.stats.gfxAtFire( (xo,yo), max( ship.zp, target.zp)+1, d, weapon.stats.laserWidth, color=ship.player.race.type ) )
        
        return (ao, ro, gfxs) # (None, None)

class LaserWeaponTurret( WeaponTurret, LaserWeapon ):
    def fire( self, ship, turret, game, target ):
        (ao,ro,gfxs) = WeaponTurret.fire( self, ship, turret, game )
        for o in self.getPoss( ship, turret, game ):
          (ao0, ro0, gfxs0) = self.hits( o, ship.ori+turret.rr, game, ship, target, turret.weapon )
          (ao, ro, gfxs) = (ao+ao0, ro+ro0, gfxs+gfxs0)
        return (ao,ro,gfxs)

#class LightningWeapon( LaserWeapon ):

class MissileWeapon( Weapon ):
    def fire( self, ship, game, target ):
        (ao,ro,gfxs) = Weapon.fire( self, ship, game )
        for o in self.getPoss( ship, game ):
          ao.append( Missile( o, ship.zp, ship.ori, (ship.xi,ship.yi), target, ship, ship.weapon ) )
          gfxs.append( GfxExplosion( o, 10, sound=ids.S_EX_FIRE ) )
        return (ao,ro,gfxs)

class MissileWeaponTurret( WeaponTurret ):
    def fire( self, ship, turret, game, target, missileId=None, buildType=None ):
        (ao,ro,gfxs) = WeaponTurret.fire( self, ship, turret, game )

        if missileId == None:
            missileReserve = ship.missiles[ turret.weapon.stats.projectile.img ]
        else:
            missileReserve = ship.missiles[ missileId ]

        for o in self.getPoss( ship, turret, game ):
         if missileReserve.amount:
          missileReserve.amount = missileReserve.amount-1
          if turret.install.stats.special == ids.S_NUKE:
              ao.append( NukeMissile( o, ship.zp, ship.ori+turret.rr, (ship.xi,ship.yi), ship.missiles[ turret.weapon.stats.projectile.img].target, ship, turret.weapon, turret.install.stats.specialValue ) )
          elif turret.install.stats.special == ids.S_PULSE:
              ao.append( PulseMissile( o, ship.zp, ship.ori+turret.rr, (ship.xi,ship.yi), ship.missiles[ turret.weapon.stats.projectile.img].target, ship, turret.weapon, turret.install.stats.specialValue ) )
          elif turret.install.stats.special == ids.S_MINER:
              ao.append( MinerMissile( o, ship.zp, ship.ori+turret.rr, (ship.xi,ship.yi), ship.missiles[ turret.weapon.stats.projectile.img].target, ship, turret.weapon, turret.install.stats.specialValue[0], turret.install.stats.specialValue[1], turret.install.stats.specialValue[2] ) )
          elif turret.install.stats.special == ids.S_COUNTER:
              ao.append( CounterMissile( o, ship.zp, ship.ori+turret.rr, (ship.xi,ship.yi), ship.missiles[ turret.weapon.stats.projectile.img].target, ship, turret.weapon, turret.install.stats.specialValue ) )
          elif turret.install.stats.special == ids.S_BUILDER:
              print "to build  ", buildType
              ao.append( BuilderMissile( o, ship.zp, ship.ori+turret.rr, (ship.xi,ship.yi), target, ship, turret.weapon, buildType ) )
          else:
              ao.append( Missile( o, ship.zp, ship.ori+turret.rr, (ship.xi,ship.yi), target, ship, turret.weapon ) )

          gfxs.append( GfxExplosion( o, 10, sound=ids.S_EX_FIRE ) )
        return (ao,ro,gfxs)

    def canFire(self, ship, turret, game ):
        return WeaponTurret.canFire( self, ship, turret, game ) \
          and ship.missiles[ turret.weapon.stats.projectile.img].amount > 0

class MassWeapon( Weapon ):
    def fire( self, ship, game, target ):
        (ao,ro,gfxs) = Weapon.fire( self, ship, game )
        angle = ship.ori
        speed = ship.weapon.stats.speed
        for o in self.getPoss( ship, game ):
            i = ( ship.xi + speed*cos(angle), ship.yi + speed*sin(angle) )

            if ship.weapon.stats.projectile.explosionRange:
                bullet = ExplodingBullet( o, ship.zp, angle, i, target, ship, ship.weapon )
            else:
                bullet = Bullet( o, ship.zp, angle, i, target, ship, ship.weapon )
                
            ao.append( bullet )
            gfxs.append( GfxExplosion( o, 3, sound=ids.S_EX_FIRE ) )
        return (ao,ro,gfxs)

class MassWeaponTurret( WeaponTurret ):
    def fire( self, ship, turret, game, target ):
        (ao,ro,gfxs) = WeaponTurret.fire( self, ship, turret, game )
        angle = (ship.ori+turret.rr)%(2*pi)
        speed = turret.weapon.stats.speed
        for o in self.getPoss( ship, turret, game ):
            i = ( ship.xi+speed*cos(angle), ship.yi+speed*sin(angle) )

            if turret.weapon.stats.projectile.explosionRange:
                bullet = ExplodingBullet( o, ship.zp, angle, i, target, ship, turret.weapon )
            else:
                bullet = Bullet( o, ship.zp, angle, i, target, ship, turret.weapon )
                
            ao.append( bullet )
            gfxs.append( GfxExplosion( o, 3, sound=ids.S_EX_FIRE ) )
        return (ao,ro,gfxs)

#class OmniLaserWeapon( Weapon ):
#    pass
    
class OmniLaserWeaponTurret( LaserWeaponTurret ):

    def hits( self, (xo,yo), ori, game, ship, target, weapon ):
        """Logic: compares the angle to target with the weapon orientation to atan( target.radius / dist between weapon and target )"""
        angle = utils.angleBetween( (target.xp,target.yp), (xo,yo) )

        hullBefore = target.hull
        (ao, ro, gfxs) = target.hit( game, angle, ship.player, weapon.stats.energyDamage, weapon.stats.massDamage )  
        if hullBefore != target.hull: # went throught the shield
            d = ( target.xp+target.stats.maxRadius/4*cos(angle), target.yp+target.stats.maxRadius/4*sin(angle))
        else:
            d = ( target.xp+target.stats.maxRadius*cos(angle), target.yp+target.stats.maxRadius*sin(angle))
            
        gfxs.append( weapon.stats.gfxAtFire( (xo,yo), max( ship.zp, target.zp)+1, d, weapon.stats.laserWidth, color=ship.player.race.type ) )
        
        return (ao, ro, gfxs) 

class BombWeapon( Weapon ):
    def fire( self, ship, game, target ):
        (ao,ro,ag) = ([],[],[])
        for obj in game.objects.objects:
            if obj.alive and obj.player and utils.distLowerThanObjects( self, obj, self.stats.explosionRange + obj.stats.maxRadius ):
                 if ship.ai.player:
                     sender = ship.ai.player
                 else:
                     sender = None
                 (ao0, ro0, ag0) = obj.hit( game, utils.angleBetweenObjects( obj, ship ), sender, self.stats.energyDamage, self.stats.massDamage, pulse=self.stats.pulseLength ) # self.weapon.stats.pulseLength
                 (ao, ro, ag) = (ao+ao0, ro+ro0, ag+ag0)
        ag0 = [ GfxExplosion( (ship.xp,ship.yp), self.stats.explosionRange, sound=ids.S_EX_PULSE ) ]
        return (ao, ro+ro0, ag+ag0)


class Missile( Ship ):
    def __init__( self, (xp,yp), zp, ori, (xi,yi), target, launcher, weapon ):
        Ship.__init__( self, weapon.stats.projectile, None, xp, yp, zp, ori, xi, yi, 0, 0 )
        self.target = target
        self.launcher = launcher
        self.weapon = weapon
        self.maxRi = 0.01
        self.ttl = weapon.stats.projectileTtl #30*5
        self.originalTtl = weapon.stats.projectileTtl
        self.lostTarget = False
        self.thinkFreq = 1 #randint( 2, config.fps/3) # randint( 3, config.fps/2)

        self.xi = launcher.xi
        self.yi = launcher.yi

    def doTurn( self, game ):
        (ao,ro,ag) = Ship.doTurn(self, game)

        if self.inNebula and self.ttl%(config.fps*2)==0:
            self.loseTarget( game )

        if self.lostTarget and (self.originalTtl-self.ttl)>config.fps:
            self.launcher = None

        # detect hit
        for obj in game.objects.getWithinRadius( self, self.stats.maxRadius ):
             if obj.alive and obj.player and (not self.launcher or obj.player != self.launcher.player):
                 if self.launcher:
                     sender = self.launcher.player
                 else:
                     sender = None
                 (ao0, ro0, ag0) = obj.hit( game, utils.angleBetweenObjects( obj, self ), sender, self.weapon.stats.energyDamage, self.weapon.stats.massDamage )
                 (ao1, ro1, ag1) = self.explode( game )
                 (ao, ro, ag) = (ao+ao0+ao1, ro+ro0+ro1, ag+ag0+ag1)
                 break

        if self.alive and not (self.originalTtl-self.ttl)%self.thinkFreq:
            if isinstance( self.target, Object ):
                target = ( self.target.xp, self.target.yp )
                if not self.target.alive:
                    self.target = target
            else:
                target = self.target

        # ori
            destAngle = utils.angleBetween( (self.xp,self.yp), target )
            angle = utils.angleDiff( destAngle, self.ori )

            absAngle = fabs( angle )
            if absAngle > self.stats.maxRg*2: # *(config.fps/10): #*5:
                if angle > 0:
                    self.rg = self.stats.maxRg
                else:
                    self.rg = -1*self.stats.maxRg
            else:
                self.rg = 0

 	    self.thrust = self.stats.maxThrust
        

            if utils.distLowerThan( (self.xp,self.yp), target, self.stats.maxRadius*4 ):
                 (ao1, ro1, ag1) = self.explode( game )
                 (ao, ro, ag) = (ao+ao1, ro+ro1, ag+ag1)
             #    self.alive = False
            #     ro.append( self )
             #    ag.append( GfxExplosion( (self.xp,self.yp), self.stats.maxRadius*3 ) )
                
        if self.alive:
            if self.ttl == 0:
                self.alive = False
                ro.append( self )
            else:
                self.ttl = self.ttl - 1

        return (ao,ro,ag)

    def explode( self, game ):
        self.alive = False
        ro = [ self ]
        ag = [ GfxExplosion( (self.xp,self.yp), self.stats.maxRadius*3, sound=ids.S_EX_FIRE ) ]
        return ([],ro,ag)

    def loseTarget( self, game ):
        dist = randint( 0, 500 )
        angle = 2*pi*random()
        self.lostTarget = True
   #     self.launcher = None
        self.target = (self.xp+dist*cos(angle), self.yp+dist*sin(angle))

class NukeMissile( Missile ):
    def __init__( self, (xp,yp), zp, ori, (xi,yi), target, launcher, weapon, explosionRange ):
        Missile.__init__( self, (xp,yp), zp, ori, (xi,yi), target, launcher, weapon )
        self.explosionRange = explosionRange
        self.thinkFreq = config.fps/10

    def explode( self, game ):
        (ao,ro,ag) = ([],[],[])
        for obj in game.objects.objects:
            if obj.alive and obj.player and utils.distLowerThanObjects( self, obj, self.explosionRange + obj.stats.maxRadius ):
                 if self.launcher:
                     sender = self.launcher.player
                 else:
                     sender = None

                 waveEffect = 5
                 angle = utils.angleBetweenObjects( self, obj )
                 dist = utils.distBetweenObjects( self, obj )
                 modif = max((self.explosionRange-dist-obj.stats.maxRadius)/self.explosionRange, 1)
                 obj.xi += cos(angle)*modif*waveEffect
                 obj.yi += sin(angle)*modif*waveEffect
                 (ao0, ro0, ag0) = obj.hit( game, utils.angleBetweenObjects( obj, self ), sender, modif*self.weapon.stats.energyDamage, self.weapon.stats.massDamage*modif )

                 (ao, ro, ag) = (ao+ao0, ro+ro0, ag+ag0)
        self.alive = False
        ro0 = [ self ]
        ag0 = [ GfxExplosion( (self.xp,self.yp), self.explosionRange, sound=ids.S_EX_NUKE ) ]
        return (ao, ro+ro0, ag+ag0)

class PulseMissile( NukeMissile ):

    def explode( self, game ):
        (ao,ro,ag) = ([],[],[])
        for obj in game.objects.objects:
            if obj.alive and obj.player and utils.distLowerThanObjects( self, obj, self.explosionRange + obj.stats.maxRadius ):
                 if self.launcher:
                     sender = self.launcher.player
                 else:
                     sender = None
                 (ao0, ro0, ag0) = obj.hit( game, utils.angleBetweenObjects( obj, self ), sender, self.weapon.stats.energyDamage, self.weapon.stats.massDamage, pulse=10*30 ) # self.weapon.stats.pulseLength
                 (ao, ro, ag) = (ao+ao0, ro+ro0, ag+ag0)
        self.alive = False
        ro0 = [ self ]
        ag0 = [ GfxExplosion( (self.xp,self.yp), self.explosionRange, sound=ids.S_EX_PULSE ) ]
        return (ao, ro+ro0, ag+ag0)

class MinerMissile( NukeMissile ):
    def __init__( self, (xp,yp), zp, ori, (xi,yi), target, launcher, weapon, explosionRange, nbrMines, minesRange ):
        NukeMissile.__init__( self, (xp,yp), zp, ori, (xi,yi), target, launcher, weapon, explosionRange )
        self.nbrMines = nbrMines
        self.minesRange = minesRange

    def explode( self, game ):
        (ao,ro,ag) = ([],[],[])

        for i in range( self.nbrMines ):
            dist = random()*self.explosionRange
            angle = random()*2*pi
            ao.append( Mine( game.stats.MINE, (self.xp+cos(angle)*dist,self.yp+sin(angle)*dist), self.zp, (0,0), self.weapon, self.minesRange, self.minesRange/2 ) )

        self.alive = False
        ro0 = [ self ]
        ag0 = [ GfxExplosion( (self.xp,self.yp), self.explosionRange, sound=ids.S_EX_FIRE ) ]
        return (ao, ro+ro0, ag+ag0)

class CounterMissile( Missile ):
    def __init__( self, (xp,yp), zp, ori, (xi,yi), target, launcher, weapon, effectRange ):
        Missile.__init__( self, (xp,yp), zp, ori, (xi,yi), target, launcher, weapon )
        self.effectRange = effectRange
        self.t = 0

    def doTurn( self, game ):
        (ao,ro,ag) = Missile.doTurn(self, game)
        if self.t%(config.fps)/2 == 0: # fin missiles
            for obj in game.objects.getWithinRadius( self, self.effectRange ):
                if obj != self and isinstance( obj, Missile ):
                     obj.target = self
        self.t += 1
        return (ao,ro,ag)


class BuilderMissile( Missile ):
    def __init__( self, (xp,yp), zp, ori, (xi,yi), target, launcher, weapon, build ):
        Missile.__init__( self, (xp,yp), zp, ori, (xi,yi), target, launcher, weapon )
        self.buildType = build

    def explode( self, game ):
        from ships import Scaffolding
        self.alive = False
    
        print self.launcher.player.race.defaults
        print self.buildType

        if self.launcher.alive and self.launcher.player \
           and self.launcher.player.race.defaults.has_key( self.buildType ):
            ao = [ Scaffolding( self.launcher.player.race.defaultScaffolding, self.xp, self.yp, self.launcher.player, self.launcher.player.race.defaults[ self.buildType ] ) ]
            explosionRange = self.launcher.player.race.defaultScaffolding.maxRadius
        else:
            ao = []
            explosionRange = 100
        ro = [ self ]
        ag = [ GfxExplosion( (self.xp,self.yp), explosionRange, sound=ids.S_EX_FIRE ) ]
        return (ao, ro, ag)


class Bullet( Object ):
    def __init__( self, (xp,yp), zp, ori, (xi,yi), target, launcher, weapon ):
        Object.__init__( self, weapon.stats.projectile, xp, yp, zp, ori, xi, yi, 0, 0 )
        self.target = target
        self.launcher = launcher
        self.weapon = weapon
        self.ttl = weapon.stats.projectileTtl #*3

    def doTurn( self, game ):
        (ao,ro,ag) = Object.doTurn(self, game)

        # detect hit
        for obj in game.objects.getWithinRadius( self, self.stats.maxRadius ):
             if obj.alive and obj.player != None and obj.player != self.launcher.player: # TODO better
                 (ao0, ro0, ag0) = obj.hit( game, utils.angleBetweenObjects( obj, self), self.launcher.player, energy=self.weapon.stats.energyDamage, mass=self.weapon.stats.massDamage )
                 (ao, ro, ag) = (ao+ao0, ro+ro0, ag+ag0)
                 self.alive = False
                 ro.append( self )
                 break

        if self.alive and self.ttl == 0:
            self.alive = False
            ro.append( self )
        else:
            self.ttl = self.ttl - 1

        return (ao,ro,ag)

class ExplodingBullet( Object ):
    def __init__( self, (xp,yp), zp, ori, (xi,yi), target, launcher, weapon ):
        Object.__init__( self, weapon.stats.projectile, xp, yp, zp, ori, xi, yi, 0, 0 )
        self.target = target
        self.launcher = launcher
        self.weapon = weapon
        self.ttl = weapon.stats.projectileTtl

    def doTurn( self, game ):
        (ao,ro,ag) = Object.doTurn(self, game)

        # detect hit
        for obj in game.objects.getWithinRadius( self, self.weapon.stats.projectile.explosionTriggerRange ):
            if obj.alive and obj.player != None and obj.player != self.launcher.player:
                (ao0, ro0, ag0) = explode( self, game, self.weapon.stats.projectile.explosionRange, energyDamage=self.weapon.stats.energyDamage, massDamage=self.weapon.stats.massDamage, sender=self.launcher.player, sound=ids.S_EX_FIRE )
                (ao, ro, ag) = (ao+ao0, ro+ro0, ag+ag0)

        if self.alive and self.ttl == 0:
            (ao0, ro0, ag0) = explode( self, game, self.weapon.stats.projectile.explosionRange, energyDamage=self.weapon.stats.energyDamage, massDamage=self.weapon.stats.massDamage, sender=self.launcher.player, sound=ids.S_EX_FIRE )
            (ao, ro, ag) = (ao+ao0, ro+ro0, ag+ag0)
        else:
            self.ttl = self.ttl - 1

        return (ao,ro,ag)

class Mine( Object ):
    def __init__( self, stats, (xp,yp), zp, (xi,yi), weapon, explosionRange, detectionRange ):
        Object.__init__( self, stats, xp, yp, zp, random()*2*pi, xi, yi, 0, 0 ) # random()*0.01 )
        self.weapon = weapon
        self.ttl = 30*360 #weapon.stats.projectileTtl
        self.detectionRange = detectionRange
        self.explosionRange = explosionRange

    def doTurn( self, game ):
        (ao,ro,ag) = Object.doTurn(self, game)

        ## detect hit
        if not game.tick%20:
            for obj in game.objects.getWithinRadius( self, self.detectionRange ):
                if obj.alive and obj.player and not isinstance( obj, Mine ):
                    (ao0,ro0,ag0) = self.explode( game )
                    (ao,ro,ag) = (ao+ao0,ro+ro0,ag+ag0)
                    break

        ## detect expiration
        if self.alive and self.ttl == 0:
            (ao0,ro0,ag0) = self.explode( game )
            (ao,ro,ag) = (ao+ao0,ro+ro0,ag+ag0)
        else:
            self.ttl = self.ttl - 1

        return (ao,ro,ag)

    def explode( self, game ):
        (ao, ro, ag) = explode( self, game, self.explosionRange, energyDamage=self.weapon.stats.energyDamage, massDamage=self.weapon.stats.massDamage, sender=None, sound=ids.S_EX_FIRE )
        return (ao,ro,ag)


