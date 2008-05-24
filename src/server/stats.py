from math import pi, atan2, hypot

#from ais import *

from common import ids
from common import config

class ObjectStats:
    def __init__(self,id,radius):
        self.img = id
        self.radius = radius
        self.maxRadius = self.radius
        self.orbitable = False

class OrbitableStats( ObjectStats ):
    def __init__(self,id,radius):
        ObjectStats.__init__(self,id,radius)
        self.orbitable = True

class WeaponStats:
   def __init__(self,id,minRange,maxRange,certainty, energyDamage,massDamage,freqOfFire,speed,weaponType, \
           projectile=None,projectileTtl=5*config.fps, laserWidth=None, \
           soundAtFire=ids.S_EX_FIRE, soundAtHit=ids.S_EX_FIRE, gfxAtFire=ids.G_EXPLOSION, gfxAtHit=ids.G_EXPLOSION \
           ): # id not for img in this only case
        self.img = id
        self.minRange = minRange
        self.maxRange = maxRange
        self.certainty = certainty
        self.energyDamage = energyDamage
        self.massDamage = massDamage
        self.freqOfFire = freqOfFire
        self.speed = speed
        self.weaponType = weaponType
        self.projectile = projectile
        self.projectileTtl = projectileTtl
        self.laserWidth = laserWidth

        self.soundAtFire = soundAtFire
        self.soundAtHit = soundAtHit
        self.gfxAtFire = gfxAtFire
        self.gfxAtHit = gfxAtHit

## ships
class ShipStats( ObjectStats ):
    def __init__(self,id,radius,maxThrust,maxReverseThrust,maxRg,maxHull,maxShield,unavoidableFragments, fragments, engines):
        ObjectStats.__init__(self,id,radius)
        self.maxThrust = maxThrust#*0.3
        self.maxReverseThrust = maxReverseThrust
        self.maxRg = maxRg
        self.maxHull = maxHull
        self.maxShield = maxShield
        self.unavoidableFragments = unavoidableFragments
        self.fragments = fragments
        self.engines = engines
        self.orbitable = False
        self.mass = 0
        self.pointsWorth = 100

class SingleWeaponShipStats( ShipStats ):
    def __init__(self,id,radius,maxThrust,maxReverseThrust,maxRg,maxHull,maxShield,weapon,unavoidableFragments, fragments, engines, weaponPositions=None):
        ShipStats.__init__(self,id,radius,maxThrust,maxReverseThrust,maxRg,maxHull,maxShield,unavoidableFragments, fragments, engines)
        self.weapon = weapon
    #    rx, ry = 10, 0
        if weaponPositions:
            self.weaponPositions = weaponPositions # [RPos( 0, 10 )]# = hypot( rx, ry )
        else:
            self.weaponPositions = [RPos( 0, 10 )]
     #  self.weaponPosAngle = atan2( rx, ry )

class MultipleWeaponsShipStats( ShipStats ):
    def __init__(self,id,radius,maxThrust,maxReverseThrust,maxRg,maxHull,maxShield,turrets,unavoidableFragments, fragments, engines):
        ShipStats.__init__(self,id,radius,maxThrust,maxReverseThrust,maxRg,maxHull,maxShield,unavoidableFragments, fragments, engines)
        self.turrets = turrets

class Flagship( MultipleWeaponsShipStats ):
    def __init__(self,id,radius,maxThrust,maxReverseThrust,maxRg,maxHull,maxShield,turrets, maxEnergy, maxOre, hangarSpace, jumpEnergyCost, launchDelay,radarRange,unavoidableFragments, fragments, engines, hangars=None, civilianBonus=1000, pulseResistant=False, jumpChargeDelay=3*config.fps, jumpRecoverDelay=20*config.fps):
        MultipleWeaponsShipStats.__init__(self,id,radius,maxThrust,maxReverseThrust,maxRg,maxHull,maxShield,turrets,unavoidableFragments, fragments, engines)
        self.maxEnergy = maxEnergy
        self.maxOre = maxOre
        self.hangarSpace = hangarSpace
        self.jumpEnergyCost = jumpEnergyCost
        self.launchDelay = launchDelay
        self.radarRange = radarRange
        self.mass = 0

        self.civilianBonus = civilianBonus
        self.energyAbsorbtion = 1.0
        if hangars:
            self.hangars = hangars
        else:
            self.hangars = [(RPos(0,0), 0)]
        self.pulseResistant = pulseResistant

        self.jumpChargeDelay = jumpChargeDelay # TODO customize to each ship
        self.jumpRecoverDelay = jumpRecoverDelay       
        global bestSpeed
        global bestShield
        global bestHull
        global bestHangar
        global bestCivilian

        bestSpeed = max( bestSpeed, maxThrust )
        bestShield = max( bestShield, maxShield )
        bestHull = max( bestHull, maxHull )
        bestHangar = max( bestHangar, hangarSpace )
        bestCivilian = max( bestCivilian, civilianBonus )

bestSpeed = 0
bestShield = 0
bestHull = 0
bestHangar = 0
bestCivilian = 0

class HarvesterShipStats( MultipleWeaponsShipStats ):
    def __init__(self,id,radius,maxThrust,maxReverseThrust,maxRg,maxHull,maxShield,turrets,maxOre,unavoidableFragments, fragments, engines, turretType, maxRange):
        MultipleWeaponsShipStats.__init__(self,id,radius,maxThrust,maxReverseThrust,maxRg,maxHull,maxShield,turrets,unavoidableFragments, fragments, engines)
        self.maxOre = maxOre
        self.maxRange = maxRange
        self.turretType = turretType

class CivilianShipStats( ShipStats ):
    def __init__(self,id,radius,maxThrust,maxReverseThrust,maxRg,maxHull,maxShield, influenceRadius,unavoidableFragments, fragments, engines ):
        ShipStats.__init__(self,id,radius,maxThrust,maxReverseThrust,maxRg,maxHull,maxShield,unavoidableFragments, fragments, engines)
        self.influenceRadius = influenceRadius

class TurretStats:
    def __init__(self,rx,ry,minAngle=0,maxAngle=0,overShip=True,asAngle=False,civilian=False):
        if asAngle:
            self.dist = rx
            self.distAngle = ry
        else:
            self.dist = hypot( rx, ry )
            self.distAngle = atan2( ry, rx )
        self.minAngle = minAngle
        self.maxAngle = maxAngle
        self.overShip = overShip
        self.civilian = civilian
        if self.maxAngle < self.minAngle:
            self.defaultAngle = (self.minAngle+self.maxAngle+2*pi)/2
        else:
            self.defaultAngle = (self.minAngle+self.maxAngle)/2
        self.civilianEffect = 0 # TODO to replace ids.S_CIVILIAN and nuclear reactor effect

class TurretInstallStats:
    def __init__( self, type,energyCostToBuild,oreCostToBuild,timeToBuild, energyPerFrame,orePerFrame, energyPerUse,orePerUse, freqOfFire,turretSpeed, ai, category=None, weapon=None,weaponPositions=None, special=None, specialValue=None, upgradeFrom=None, civilian=False ):
        self.type = type
        self.energyCostToBuild = energyCostToBuild
        self.oreCostToBuild = oreCostToBuild
        self.timeToBuild = timeToBuild

        self.energyPerFrame = energyPerFrame
        self.orePerFrame = orePerFrame

        self.energyPerUse = energyPerUse
        self.orePerUse = orePerUse

        self.freqOfFire = freqOfFire
        self.turretSpeed = turretSpeed

        self.ai = ai
        self.civilian = civilian
     #   if category:
      #      self.category = category
      #  elif ai == ids.TA_MISSILE_SPECIAL:
      #      self.category = ids.C_MISSILE
      #  elif weapon:
      #      self.category = ids.C_WEAPON
     #   else:
      #      self.category = ids.C_OTHER

        self.weapon = weapon
        self.weaponPositions = weaponPositions
        self.special = special
        self.specialValue = specialValue

        self.upgradeFrom = upgradeFrom
        
        self.overs = []
        over = self.upgradeFrom
        while over:
           self.overs.append( over )
           over = over.upgradeFrom
      #  print self, self.overs

class SunStats( OrbitableStats ):
    def __init__( self, id, radius, damageRadius, maxDamage, energyRadius, maxEnergy ):
        OrbitableStats.__init__( self, id, radius )
        self.damageRadius = damageRadius
        self.maxDamage = maxDamage
        self.energyRadius = energyRadius
        self.maxEnergy = maxEnergy

class BlackHoleStats( OrbitableStats ):
    def __init__( self, id, radius, damageRadius, maxDamage, gravitationalRadius, gravitationalStrength ):
        OrbitableStats.__init__( self, id, radius )
        self.damageRadius = damageRadius
        self.maxDamage = maxDamage
        self.gravitationalRadius = gravitationalRadius
        self.gravitationalStrength = gravitationalStrength

class RPos:
    def __init__( self, angle, dist ):
        self.angle = angle
        self.dist = dist 

class RaceStats:
    def __init__( self, type, flagships, missiles, ships, turrets, defaultHarvester, immuneToPulse=False ):
        self.type = type
        self.flagships = flagships
        self.missiles = missiles
        self.ships = ships
        self.turrets = turrets
        self.defaultHarvester = defaultHarvester
        self.immuneToPulse = immuneToPulse

class Cost:
    def __init__( self, energyCostToBuild,oreCostToBuild,timeToBuild, hangarSpace ):
        self.energyCostToBuild = energyCostToBuild
        self.oreCostToBuild = oreCostToBuild
        self.timeToBuild = timeToBuild
        self.hangarSpace = hangarSpace

class ShipChoice:
    def __init__( self, stats, race, points ):
        self.stats = stats
        self.points = points
        self.race = race # .type

        self.speed = 100*stats.maxThrust/bestSpeed
        self.shield = 100*stats.maxShield/bestShield
        self.hull = 100*stats.maxHull/bestHull
        self.hangar = 100*stats.hangarSpace/bestHangar
        self.turrets = len(stats.turrets)
        self.canJump = (stats.jumpEnergyCost < 10000)
        self.civilians = 100*stats.civilianBonus/bestCivilian


# id,radius,maxThrust,maxReverseThrust,maxRg,maxHull,maxShield
MISSILE_NORMAL = ShipStats( ids.M_NORMAL, 3, 0.6, 0, 0.008, 5, 0, None, None, [(2,pi)] ) 
MISSILE_NUKE = 	ShipStats( ids.M_NUKE, 3, 0.4, 0, 0.004, 5, 0, None, None, [(2,pi)] ) 
MISSILE_PULSE = ShipStats( ids.M_PULSE, 3, 0.6, 0, 0.007, 5, 0, None, None, [(2,pi)] ) 
MISSILE_MINER = ShipStats( ids.M_MINER, 3, 0.5, 0, 0.006, 5, 0, None, None, [(2,pi)] ) 
MISSILE_COUNTER = ShipStats( ids.M_COUNTER, 3, 0.8, 0, 0.005, 5, 0, None, None, [(2,pi)] ) 
MISSILE_AI = ShipStats( ids.M_AI, 3, 0.6, 0, 0.008, 5, 0, None, None, [(2,pi)] ) 
MISSILE_LARVA = ShipStats( ids.M_LARVA, 3, 0.6, 0, 0.008, 5, 0, None, None, [(2,pi)] ) 

BULLET_0 =  	ObjectStats( ids.B_BULLET_0, 3 )
BOMB_0 =  	ObjectStats( ids.B_BOMB_0, 3 )
B_ROCK_0 =  	ObjectStats( ids.B_ROCK_0, 4 )
B_ROCK_1 =  	ObjectStats( ids.B_ROCK_1, 7 )
B_AI_0 =  	ObjectStats( ids.B_AI_0, 4 )
B_FIRE_0 =  	ObjectStats( ids.B_FIRE_0, 5 )
B_ESPHERE =     ObjectStats( ids.B_ESPHERE, 7 )
B_WAVE_0 =      ObjectStats( ids.B_WAVE_0, 7 )
B_WAVE_1 =      ObjectStats( ids.B_WAVE_1, 7 )

# id,minRange,maxRange,certainty, energyDamage,massDamage,freqOfFire,speed,weaponType,projectile=None
W_LASER_SR = 	WeaponStats( ids.W_LASER_SR, 30,250,20, 1,0, 1,0, ids.WT_LASER, laserWidth=1) #, laserColor=ids.RED)
# W_LASER_SR_FIGHTER = 	WeaponStats( ids.W_LASER_SR, 30,250,20, 1,0, 1,0, ids.WT_LASER)
W_LASER_MR_0 = 	WeaponStats( ids.W_LASER_MR_0, 50,400,50, 3,0, 1,0, ids.WT_LASER, laserWidth=2 ) # , laserColor=ids.RED) # 0.5*config.fps
W_LASER_MR_1 = 	WeaponStats( ids.W_LASER_MR_1, 50,500,50, 5,0, 1,0, ids.WT_LASER, laserWidth=3 ) # , laserColor=ids.RED) # 0.5*config.fps

W_MASS_SR_0 = 	WeaponStats( ids.W_MASS_SR, 50, 300, 20, 0,3, 0.3*config.fps,15, ids.WT_MASS, projectile=BULLET_0)
W_MASS_SR_1 = 	WeaponStats( ids.W_MASS_SR, 50, 300, 20, 0,3, 0.2*config.fps,15, ids.WT_MASS, projectile=BULLET_0)
W_MASS_SR_2 = 	WeaponStats( ids.W_MASS_SR, 50, 300, 20, 0,3, 0.1*config.fps,15, ids.WT_MASS, projectile=BULLET_0)
W_MASS_SR_FIGHTER = 	WeaponStats( ids.W_MASS_SR, 50, 300, 20, 0,3, 0.15*config.fps,15, ids.WT_MASS, projectile=BULLET_0)
W_MASS_MR = 	WeaponStats( ids.W_MASS_MR, 50, 500, 50, 0,20, 1*config.fps,10, ids.WT_MASS, projectile=BULLET_0)
W_MASS_LR = 	WeaponStats( ids.W_MASS_LR, 50, 1500, 150, 0,50, 3*config.fps,30, ids.WT_MASS, projectile=BULLET_0)

W_MISSILE = 		WeaponStats( ids.W_MISSILE, 70, 600, 0, 10,5, 1*config.fps,10, ids.WT_MISSILE, projectile=MISSILE_NORMAL, projectileTtl=10*config.fps)
W_MISSILE_NUKE = 	WeaponStats( ids.W_NUKE, 70, 600, 100, 0,800, 2*config.fps,10, ids.WT_MISSILE, projectile=MISSILE_NUKE, projectileTtl=15*config.fps)
W_MISSILE_PULSE = 	WeaponStats( ids.W_PULSE, 70, 600, 0, 1,0, 2*config.fps,10, ids.WT_MISSILE, projectile=MISSILE_PULSE, projectileTtl=15*config.fps)
W_MISSILE_MINER = 	WeaponStats( ids.W_MINER, 70, 600, 0, 10, 5, 4*config.fps,10, ids.WT_MISSILE, projectile=MISSILE_MINER, projectileTtl=15*config.fps)
W_MISSILE_COUNTER = 	WeaponStats( ids.W_COUNTER, 70, 600, 1, 0, 5, 1*config.fps,10, ids.WT_MISSILE, projectile=MISSILE_COUNTER, projectileTtl=10*config.fps)
# W_MISSILE_1 = 	WeaponStats( ids.W_MISSILES_1, 70, 600, 2*config.fps, 5, 5, 50, 0, 0, [RPos(0,7),RPos(0.7,9.2),RPos(-0.7,9.2)], 10,5,10, MISSILE_0)

W_BOMB_0 = 	WeaponStats( ids.W_BOMB_0, 50, 300, 90, 0,20, 0.5*config.fps,0.2, ids.WT_BOMB, projectile=BOMB_0 )

# extras'
W_ROCK_THROWER_0 = 	WeaponStats( ids.W_ROCK_THROWER_0, 50, 300, 20, 0,2, 0.6*config.fps,15, ids.WT_MASS, projectile=B_ROCK_0)
W_ROCK_THROWER_1 = 	WeaponStats( ids.W_ROCK_THROWER_1, 50, 300, 20, 0,2, 0.6*config.fps,15, ids.WT_MASS, projectile=B_ROCK_1)
W_DRAGON_0 = 		WeaponStats( ids.W_DRAGON_0, 50, 300, 20, 5,0, 0.6*config.fps,15, ids.WT_MASS, projectile=B_FIRE_0)
W_LARVA_0 = 		WeaponStats( ids.W_LARVA_0, 70, 600, 0, 10,5, 1*config.fps,10, ids.WT_MISSILE, projectile=MISSILE_LARVA, projectileTtl=10*config.fps)
W_EXTRA_FIGHTER = 	WeaponStats( ids.W_EXTRA_FIGHTER, 50, 300, 20, 3,0, 0.6*config.fps,15, ids.WT_MASS, projectile=B_FIRE_0)
W_EXTRA_BOMBER = 	WeaponStats( ids.W_EXTRA_BOMBER, 50, 300, 90, 0,20, 0.5*config.fps,0.2, ids.WT_BOMB, projectile=BOMB_0 )

# ais'
W_AI_MISSILE = 		WeaponStats( ids.W_AI_MISSILE, 70, 600, 0, 10,5, 1*config.fps,10, ids.WT_MISSILE, projectile=MISSILE_AI, projectileTtl=10*config.fps)

# evolved's
W_ESPHERE_0 = 	WeaponStats( ids.W_ESPHERE_0, 50, 500, 50, 10,5, 1*config.fps,10, ids.WT_MASS, projectile=B_ESPHERE)
#W_ESPHERE_1 = 	WeaponStats( ids.W_ESPHERE_1, 50, 500, 50, 10,0, 1*config.fps,10, ids.WT_MASS, projectile=B_ESPHERE)
#W_ESPHERE_2 = 	WeaponStats( ids.W_ESPHERE_2, 50, 500, 50, 10,0, 1*config.fps,10, ids.WT_MASS, projectile=B_ESPHERE)
W_BURST_LASER_0 = 	WeaponStats( ids.W_BURST_LASER_0, 50, 500, 50, 10,0, 1*config.fps,10, ids.WT_LASER, laserWidth=2 )
W_OMNI_LASER_0 = 	WeaponStats( ids.W_OMNI_LASER_0, 50, 500, 50, 2,0, 1,10, ids.WT_LASER, laserWidth=4 )
W_OMNI_LASER_1 = 	WeaponStats( ids.W_OMNI_LASER_1, 50, 500, 50, 3,0, 1,10, ids.WT_LASER, laserWidth=5 )
W_OMNI_LASER_2 = 	WeaponStats( ids.W_OMNI_LASER_2, 50, 500, 50, 4,0, 1,10, ids.WT_LASER, laserWidth=6 )
W_SUBSPACE_WAVE_0 = 	WeaponStats( ids.W_SUBSPACE_WAVE_0, 50, 500, 50, 0,10, 1*config.fps,5, ids.WT_MASS, projectile=B_WAVE_0, projectileTtl=5*config.fps)
W_SUBSPACE_WAVE_1 = 	WeaponStats( ids.W_SUBSPACE_WAVE_1, 50, 500, 50, 0,20, 1*config.fps,5, ids.WT_MASS, projectile=B_WAVE_1, projectileTtl=5*config.fps)

ASTEROIDS =	[ OrbitableStats( ids.A_0, 46 ), OrbitableStats( ids.A_1, 41 ), OrbitableStats( ids.A_2, 26 ), OrbitableStats( ids.A_3, 37 ), OrbitableStats( ids.A_4, 24 ) ] #[ OrbitableStats( 0, 10 ), OrbitableStats( 1, 20 ), OrbitableStats( 2, 30 ) ], \
                  #[ OrbitableStats( 3, 10 ), OrbitableStats( 4, 20 ), OrbitableStats( 5, 30 ) ], \
                  #[ OrbitableStats( 6, 10 ), OrbitableStats( 7, 20 ), OrbitableStats( 8, 30 ) ] ]

P_MERCURY =	OrbitableStats( ids.P_MERCURY, 190 )
P_MARS =	OrbitableStats( ids.P_MARS, 281 )
P_EARTH =	OrbitableStats( ids.P_EARTH, 325 )
P_VENUS =	OrbitableStats( ids.P_VENUS, 250 )
P_JUPITER =	OrbitableStats( ids.P_JUPITER, 700 )
P_SATURN =	OrbitableStats( ids.P_SATURN, 551 )
P_NEPTUNE =	OrbitableStats( ids.P_NEPTUNE, 350 )

P_MOON =	OrbitableStats( ids.P_MOON, 110 )
P_MARS_1 =	OrbitableStats( ids.P_MARS_1, 290 )
P_MARS_2 =	OrbitableStats( ids.P_MARS_2, 320 )
P_JUPITER_1 =	OrbitableStats( ids.P_JUPITER_1, 600 )
P_MERCURY_1 =	OrbitableStats( ids.P_MERCURY_1, 240 )
P_X =		OrbitableStats( ids.P_X, 250 )
P_X_1 =		OrbitableStats( ids.P_X_1, 240 )
P_SATURN_1 =	OrbitableStats( ids.P_SATURN_1, 551 )

P_GAIA =	OrbitableStats( ids.P_GAIA, 300 )

S_SOL = 	SunStats( ids.S_SOL, 1750, 3500, 7, 15000, 0.2 )
BH_0 = 		BlackHoleStats( ids.A_BLACK_HOLE, 240, 400, 10, 1200, 20. )

A_NEBULA =	ObjectStats( ids.A_NEBULA, 800 )
A_NEBULA_1 =	ObjectStats( ids.A_NEBULA, 1000 )
A_NEBULA_2 =	ObjectStats( ids.A_NEBULA, 1000 )

### ships

 ## human
#SHIP = 		SingleWeaponShipStats( 9, 20, 0.3, 0.2, 0.008, 50, 100, W_MASS_SR, None, None, [(20,pi)] )
FIGHTER =	SingleWeaponShipStats( ids.S_FIGHTER, 15, 0.6, 0, 0.012, 20, 20, W_MASS_SR_FIGHTER, [ids.F_FIGHTER_0,ids.F_FIGHTER_1,ids.F_FIGHTER_2], None, [(15,pi)] )
BOMBER =	SingleWeaponShipStats( ids.S_BOMBER, 15, 0.5, 0, 0.010, 30, 25, W_BOMB_0, [ids.S_BOMBER], None, [(15,pi)] )
# FIGHTER =	SingleWeaponShipStats( ids.S_FIGHTER, 10, 0.6, 0, 0.012, 15, 10, W_LASER_SR )

FLAGSHIP_0 =	Flagship( ids.S_FLAGSHIP_0, 80, 0.1, 0.05, 0.002, 350, 500,
                [TurretStats(53, 8, 5*pi/3,2*pi/3, True),
                 TurretStats(53,-8, 4*pi/3,1*pi/3, True),
                 TurretStats(13,16, 0,pi, True),
                 TurretStats(13,-16, pi,2*pi, True),
                 TurretStats(-20.5,41.5, 0,4*pi/3, True),
                 TurretStats(-20.5,-41.5, 2*pi/3,2*pi, True),
                 ],
                 1000, 1000, 500, 500, 0.4*config.fps, 2500, [ids.F_FLAGSHIP_0], [ids.F_LARGE_0, ids.F_LARGE_1], [(80,pi)] ) 
FLAGSHIP_1 =	Flagship( ids.S_FLAGSHIP_1, 100, 0.1, 0.05, 0.002, 300, 500, 
                 [TurretStats(40.5,11.5,pi/4,3*pi/4, True), # up
                 TurretStats(19,11.5,pi/4,3*pi/4, True),
                 TurretStats(0.5,11.5,pi/4,3*pi/4, True),
                 TurretStats(-22.5,11.5,pi/4,3*pi/4, True),
                 TurretStats(40.5,-11.5,5*pi/4,7*pi/4, True), # down
                 TurretStats(19,-11.5,5*pi/4,7*pi/4, True),
                 TurretStats(0.5,-11.5,5*pi/4,7*pi/4, True),
                 TurretStats(-22.5,-11.5,5*pi/4,7*pi/4, True),
                 TurretStats(-45.5,41.5, 0,4*pi/3, True), # wings
                 TurretStats(-45.5,-41.5, 2*pi/3,2*pi, True) ],
                3000, 3000, 300, 500, 0.7*config.fps, 2500, [ids.F_FLAGSHIP_1], [ids.F_LARGE_0, ids.F_LARGE_1], [(80,pi)],
                hangars=[(RPos(0, 0 ), pi/2), (RPos(0, 0 ), 3*pi/2)] )
FLAGSHIP_2 =	Flagship( ids.S_FLAGSHIP_2, 70, 0.1, 0.05, 0.002, 400, 500, 
                [TurretStats(8,21,0,pi, True),
                 TurretStats(8,-21,pi,2*pi, True),
                 TurretStats(-43,22,pi/3,4*pi/3, True),
                 TurretStats(-43,-22,2*pi/3,5*pi/3, True)], 
                3000, 3000, 1000, 500, 0.2*config.fps, 2500, [ids.F_FLAGSHIP_2], [ids.F_LARGE_0, ids.F_LARGE_1], [(70,pi)] )


ORBITALBASE =	Flagship( ids.S_ORBITALBASE, 45, 0, 0, 0.002, 800, 1000,
                [ TurretStats(25,i*pi*2/6, i*pi*2/6-pi/3,i*pi*2/6+pi/3, True, asAngle=True) for i in xrange( 6 ) ],
                1000, 1000, 1000, 100000, 0.2*config.fps, 1000, None, [ids.F_LARGE_0, ids.F_LARGE_1], [] )

 ## Nomad
NOMAD_FIGHTER =	SingleWeaponShipStats( ids.S_NOMAD_FIGHTER, 15, 0.6, 0, 0.012, 20, 20, W_MASS_SR_FIGHTER, [ids.S_NOMAD_FIGHTER], None, [(15,pi)] )

NOMAD_FS_0 =	Flagship( ids.S_NOMAD_FS_0, 80, 0.1, 0.05, 0.001, 350, 500,
                [TurretStats(53, 8, 0,2*pi/3, True),
                 TurretStats(53,-8, 4*pi/3,2*pi, True),
                 TurretStats(13,16, 0,pi, True),
                 TurretStats(13,-16, pi,2*pi, True),
                 TurretStats(-20.5,41.5, 0,4*pi/3, True),
                 TurretStats(-20.5,-41.5, 2*pi/3,2*pi, True),
                 ],
                 1000, 1000, 500, 500, 0.4*config.fps, 2500, [ids.S_NOMAD_FS_0], [ids.F_LARGE_0, ids.F_LARGE_1], [(80,pi)] ) 
NOMAD_FS_1 =	Flagship( ids.S_NOMAD_FS_1, 100, 0.1, 0.05, 0.002, 300, 500, 
                 [TurretStats(40.5,11.5,pi/4,3*pi/4, True), # up
                 TurretStats(19,11.5,pi/4,3*pi/4, True),
                 TurretStats(0.5,11.5,pi/4,3*pi/4, True),
                 TurretStats(-22.5,11.5,pi/4,3*pi/4, True),
                 TurretStats(40.5,-11.5,5*pi/4,7*pi/4, True), # down
                 TurretStats(19,-11.5,5*pi/4,7*pi/4, True),
                 TurretStats(0.5,-11.5,5*pi/4,7*pi/4, True),
                 TurretStats(-22.5,-11.5,5*pi/4,7*pi/4, True),
                 TurretStats(-45.5,41.5, 0,4*pi/3, True), # wings
                 TurretStats(-45.5,-41.5, 2*pi/3,2*pi, True) ],
                3000, 3000, 300, 500, 0.7*config.fps, 2500, [ids.S_NOMAD_FS_1], [ids.F_LARGE_0, ids.F_LARGE_1], [(80,pi)],
                hangars=[(RPos(0, 0 ), pi/2), (RPos(0, 0 ), 3*pi/2)] )
NOMAD_FS_2 =	Flagship( ids.S_NOMAD_FS_2, 70, 0.1, 0.05, 0.002, 400, 500, 
                [TurretStats(8,21,0,pi, True),
                 TurretStats(8,-21,pi,2*pi, True),
                 TurretStats(-43,22,pi/3,4*pi/3, True),
                 TurretStats(-43,-22,2*pi/3,5*pi/3, True)], 
                3000, 3000, 1000, 500, 0.2*config.fps, 2500, [ids.S_NOMAD_FS_2], [ids.F_LARGE_0, ids.F_LARGE_1], [(70,pi)] )
NOMAD_BASE =	Flagship( ids.S_NOMAD_BASE, 45, 0, 0, 0.002, 800, 1000,
                [ TurretStats(25,i*pi*2/6, i*pi*2/6-pi/3,i*pi*2/6+pi/3, True, asAngle=True) for i in xrange( 6 ) ],
                1000, 1000, 1000, 100000, 0.2*config.fps, 1000, None, [ids.F_LARGE_0, ids.F_LARGE_1], [] )


 ## AIs
AI_FIGHTER =	SingleWeaponShipStats( ids.S_AI_FIGHTER, 8, 0.6, 0, 0.012, 20, 20, W_LASER_SR, [ids.S_AI_FIGHTER], None, [(8,pi)] )
AI_BOMBER =	SingleWeaponShipStats( ids.S_AI_BOMBER, 8, 0.6, 0, 0.012, 20, 20, W_AI_MISSILE, [ids.S_AI_BOMBER], None, [(8,pi)] )

AI_BASE =	Flagship( ids.S_AI_BASE, 100, 0, 0, 0.002, 400, 1500,
                [ TurretStats(75,(i*pi*2/3)%(2*pi), (i*pi*2/3-pi*3/4)%(2*pi), (i*pi*2/3+pi*3/4)%(2*pi), False, asAngle=True) for i in xrange( 3 ) ] + \
                [ TurretStats(15,(i*pi*2/3+pi/3)%(2*pi), (i*pi*2/3)%(2*pi), (i*pi*2/3+2*pi/3)%(2*pi), False, asAngle=True) for i in xrange( 3 ) ],
                1000, 1000, 1000, 100000, 0.5*config.fps, 1000, None, [ids.F_AI_0], [],
                [ (RPos(0, 0 ), i*2*pi/3+pi/3) for i in xrange( 3 ) ] )
AI_FS_0 =	Flagship( ids.S_AI_FS_0, 100, 0.1, 0.05, 0.002, 300, 800,
                [ TurretStats(75, (i*pi*2/3)%(2*pi), (i*pi*2/3-pi*3/4)%(2*pi), (i*pi*2/3+pi*3/4)%(2*pi), False, asAngle=True) for i in xrange( 3 ) ] + \
                [ TurretStats(15, (i*pi*2/3+pi/3)%(2*pi), (i*pi*2/3)%(2*pi), (i*pi*2/3+2*pi/3)%(2*pi), False, asAngle=True) for i in xrange( 3 ) ],
                1000, 1000, 300, 500, 0.5*config.fps, 1000, None, [ids.F_AI_0], [],
                [ (RPos(0, 0 ), i*2*pi/3+pi/3) for i in xrange( 3 ) ] )
AI_FS_1 =	Flagship( ids.S_AI_FS_1, 100, 0.1, 0.05, 0.002, 400, 800,
                [ TurretStats(75, (i*pi*2/3)%(2*pi), (i*pi*2/3-pi*3/4)%(2*pi), (i*pi*2/3+pi*3/4)%(2*pi), False, asAngle=True) for i in xrange( 3 ) ] + \
                [ TurretStats(15, (i*pi*2/3+pi/3)%(2*pi), (i*pi*2/3)%(2*pi), (i*pi*2/3+2*pi/3)%(2*pi), False, asAngle=True) for i in xrange( 3 ) ],
                1000, 1000, 400, 500, 0.5*config.fps, 1000, None, [ids.F_AI_0], [],
                [ (RPos(0, 0 ), i*2*pi/3+pi/3) for i in xrange( 3 ) ] )
AI_FS_2 =	Flagship( ids.S_AI_FS_2, 100, 0.1, 0.05, 0.002, 500, 800,
                [ TurretStats(75, (i*pi*2/3)%(2*pi), (i*pi*2/3-pi*3/4)%(2*pi), (i*pi*2/3+pi*3/4)%(2*pi), False, asAngle=True) for i in xrange( 3 ) ] + \
                [ TurretStats(15, (i*pi*2/3+pi/3)%(2*pi), (i*pi*2/3)%(2*pi), (i*pi*2/3+2*pi/3)%(2*pi), False, asAngle=True) for i in xrange( 3 ) ],
                1000, 1000, 800, 500, 0.5*config.fps, 1000, None, [ids.F_AI_0], [],
                [ (RPos(0, 0 ), i*2*pi/3+pi/3) for i in xrange( 3 ) ] )

 ## evolved
EVOLVED_FIGHTER =	SingleWeaponShipStats( ids.S_EVOLVED_FIGHTER, 8, 0.6, 0, 0.012, 20, 20, W_LASER_SR, [ids.S_EVOLVED_FIGHTER], None, [(8,pi)], weaponPositions=[RPos(0.3,12), RPos(-0.3,12)] )
EVOLVED_BOMBER =	SingleWeaponShipStats( ids.S_EVOLVED_BOMBER, 8, 0.6, 0, 0.012, 20, 20, W_ESPHERE_0, [ids.S_EVOLVED_BOMBER], None, [(8,pi)], weaponPositions=[RPos(0,15)] ) # [RPos(0.3,12), RPos(0,15), RPos(-0.3,12)]

  # id,radius,maxThrust,maxReverseThrust,maxRg,maxHull,maxShield,turrets, maxEnergy, maxOre, hangarSpace, jumpEnergyCost, launchDelay,radarRange,unavoidableFragments, fragments, engines
EVOLVED_FS_0 =  Flagship( ids.S_EVOLVED_FS_0, 70, 0.1, 0.05, 0.001, 300, 800, 
                [TurretStats(92, 35, 19*pi/12,11*pi/12, True),
                 TurretStats(92,-35, 13*pi/12,5*pi/12, True),
                 TurretStats(-82,47, pi/12,5*pi/4, True),
                 TurretStats(-82,-47,3*pi/4,23*pi/12, True)], 
                3000, 3000, 400, 500, 0.3*config.fps, 2500, None, [ids.F_LARGE_0, ids.F_LARGE_1], [(70,pi)] )
EVOLVED_FS_1 =  Flagship( ids.S_EVOLVED_FS_1, 140, 0.1, 0.04, 0.001, 200, 1000, 
                [TurretStats(63,-53, pi*6/5,2*pi, True),
                 TurretStats(23,-53, pi*7/5,pi*9/5, True),
                 TurretStats(94,47, 0,pi*4/5, True),
                 TurretStats(53,47, pi*1/5,pi*4/5, True),
                 TurretStats(114,-6, -pi/2,pi/2, True)], 
                3000, 3000, 900, 500, 0.3*config.fps, 2500, None, [ids.F_LARGE_0, ids.F_LARGE_1], [(70,pi)],
                hangars=[(RPos(-0.14, 44 ), pi/2), (RPos(-0.14, 44 ), pi/-2), (RPos(-0.07, 85 ), pi/2), (RPos(-0.07, 85 ), pi/-2), ] )
EVOLVED_FS_2 =  Flagship( ids.S_EVOLVED_FS_2, 140, 0.1, 0.04, 0.001, 200, 1200, 
                [TurretStats(63,-53, pi*6/5,2*pi, True),
                 TurretStats(23,-53, pi*7/5,pi*9/5, True),
                 TurretStats(94,47, 0,pi*4/5, True),
                 TurretStats(53,47, pi*1/5,pi*4/5, True),
                 TurretStats(114,-6, -pi/2,pi/2, True)], 
                3000, 3000, 250, 500, 0.3*config.fps, 2500, None, [ids.F_LARGE_0, ids.F_LARGE_1], [(70,pi)],
                hangars=[(RPos(-0.14, 44 ), pi/2), (RPos(-0.14, 44 ), pi/-2), (RPos(-0.07, 85 ), pi/2), (RPos(-0.07, 85 ), pi/-2), ] )

 ## extras
EXTRA_FS_0 =  Flagship( ids.S_EXTRA_FS_0, 70, 0.08, 0.02, 0.002, 1000, 0,  # Asteroid
                [TurretStats(12,i*pi*2/3, i*pi*2/3-pi*3/4,i*pi*2/3+pi*3/4, True, asAngle=True) for i in xrange( 3 )], 
                3000, 3000, 400, 500, 0.2*config.fps, 500, [ ids.S_EXTRA_FS_0 ], None, [(70,pi)] ) # TODO
EXTRA_FS_1 =  Flagship( ids.S_EXTRA_FS_1, 70, 0.1, 0.02, 0.004, 2000, 0, # dragon
                [TurretStats(52,i*pi/12-pi/12, i*pi/12-pi/12-pi/3,i*pi/12-pi/12+pi/3, True, asAngle=True) for i in xrange( 3 )], 
                3000, 3000, 500, 500, 0.2*config.fps, 750, [ ids.S_EXTRA_FS_1 ], None, [(70,pi)] ) # TODO
EXTRA_FS_2 =  Flagship( ids.S_EXTRA_FS_2, 70, 0.1, 0.02, 0.003, 2000, 0, # dead flagship
                [TurretStats(30,i*pi*2/4, i*pi*2/4-pi*3/4,i*pi*2/4+pi*3/4, True, asAngle=True) for i in xrange( 4 )], 
                3000, 3000, 200, 500, 0.2*config.fps, 750, [ ids.S_EXTRA_FS_2 ], None, [(70,pi)] ) # TODO

EXTRA_FIGHTER =	SingleWeaponShipStats( ids.S_EXTRA_FIGHTER, 8, 0.6, 0, 0.012, 20, 20, W_EXTRA_FIGHTER, [ids.S_EXTRA_FIGHTER], None, [(8,pi)], weaponPositions=[RPos(0,12)] ) # TODO
EXTRA_BOMBER =	SingleWeaponShipStats( ids.S_EXTRA_BOMBER, 8, 0.6, 0, 0.012, 20, 20, W_EXTRA_BOMBER, [ids.S_EXTRA_BOMBER], None, [(8,pi)], weaponPositions=[RPos(0,0)] ) # TODO

 ## neutrals
CIVILIAN_0 = 	CivilianShipStats( ids.S_CIVILIAN_0, 32, 0.1, 0.05, 0.002, 50, 100, 500, None, [ids.F_LARGE_0], [(32,pi)] )
MINE = ObjectStats( ids.S_MINE, 2 ) 


### turrets
# type,energyCostToBuild,oreCostToBuild,timeToBuild, energyPerFrame,orePerFrame, energyPerUse,orePerUse, freqOfFire,turretSpeed, ai, weapon=None,weaponPositions=None, special=None
T_LASER_SR_0 = 	TurretInstallStats( ids.T_LASER_SR_0, 0,75,5*config.fps, 0,0, 1,0, 0.3*config.fps,0.05, ids.TA_COMBAT_ROTATING, weapon=W_LASER_SR,weaponPositions=[RPos(0,11)] )
T_LASER_SR_1 = 	TurretInstallStats( ids.T_LASER_SR_1, 0,75,5*config.fps, 0,0, 1,0, 0.3*config.fps,0.05, ids.TA_COMBAT_ROTATING, weapon=W_LASER_SR,weaponPositions=[RPos(0.5,11),RPos(-0.5,11)], upgradeFrom=T_LASER_SR_0 )
T_LASER_MR_0 = 	TurretInstallStats( ids.T_LASER_MR_0, 0,250,10*config.fps, 0,0, 0.5,0, 1*config.fps,0.004, ids.TA_COMBAT_ROTATING, weapon=W_LASER_MR_0,weaponPositions=[RPos(0,10)] )
T_LASER_MR_1 = 	TurretInstallStats( ids.T_LASER_MR_1, 0,750,10*config.fps, 0,0, 0.5,0, 1*config.fps,0.004, ids.TA_COMBAT_ROTATING, weapon=W_LASER_MR_1,weaponPositions=[RPos(0,10)], upgradeFrom=T_LASER_MR_0 )

T_MASS_SR_0 = 	TurretInstallStats( ids.T_MASS_SR_0, 0,100,5*config.fps, 0,0, 0,1, 0.2*config.fps,0.05, ids.TA_COMBAT_ROTATING, weapon=W_MASS_SR_0,weaponPositions=[RPos(0,15)] )
T_MASS_SR_1 = 	TurretInstallStats( ids.T_MASS_SR_1, 0,100,15*config.fps, 0,0, 0,1, 0.2*config.fps,0.05, ids.TA_COMBAT_ROTATING, weapon=W_MASS_SR_1,weaponPositions=[RPos(0,15)], upgradeFrom=T_MASS_SR_0 ) # [RPos(0.2,15), RPos(-0.2,15)]
T_MASS_SR_2 = 	TurretInstallStats( ids.T_MASS_SR_2, 0,100,45*config.fps, 0,0, 0,1, 0.2*config.fps,0.05, ids.TA_COMBAT_ROTATING, weapon=W_MASS_SR_2,weaponPositions=[RPos(0,15)], upgradeFrom=T_MASS_SR_1 ) # [RPos(0.2,15), RPos(0,15), RPos(-0.2,15)]
T_MASS_MR_0 = 	TurretInstallStats( ids.T_MASS_MR_0, 0,200,10*config.fps, 0,0, 0,1, 0.8*config.fps,0.02, ids.TA_COMBAT_ROTATING, weapon=W_MASS_MR,weaponPositions=[RPos(0,22)] )
T_MASS_MR_1 = 	TurretInstallStats( ids.T_MASS_MR_1, 0,200,10*config.fps, 0,0, 0,1, 0.8*config.fps,0.02, ids.TA_COMBAT_ROTATING, weapon=W_MASS_MR,weaponPositions=[RPos(0.3,22),RPos(-0.3,22)], upgradeFrom=T_MASS_MR_0 )
T_MASS_LR = 	TurretInstallStats( ids.T_MASS_LR, 0,700,30*config.fps, 0,0, 0,1, 2*config.fps,0.01, ids.TA_COMBAT_ROTATING, weapon=W_MASS_LR,weaponPositions=[RPos(0,11)], upgradeFrom=T_MASS_MR_0 )

T_MISSILE_0 = 	TurretInstallStats( ids.T_MISSILES_0, 0,100,15*config.fps, 0,0, 0,0, 0.5*config.fps,0, ids.TA_COMBAT_STABLE, weapon=W_MISSILE,weaponPositions=[RPos(0,10)] )
T_MISSILE_1 = 	TurretInstallStats( ids.T_MISSILES_1, 0,350,60*config.fps, 0,0, 0,0, 0.5*config.fps,0, ids.TA_COMBAT_STABLE, weapon=W_MISSILE,weaponPositions=[RPos(0.5,10),RPos(-0.5,10)], upgradeFrom=T_MISSILE_0 )
T_MISSILE_2 = 	TurretInstallStats( ids.T_MISSILES_2, 0,1200,180*config.fps, 0,0, 0,0, 0.5*config.fps,0, ids.TA_COMBAT_STABLE, weapon=W_MISSILE,weaponPositions=[RPos(0.5,10),RPos(0,10),RPos(-0.5,10)], upgradeFrom=T_MISSILE_1 )

T_INTERDICTOR = TurretInstallStats( ids.T_INTERDICTOR, 0,500,45*config.fps, 1,0, 0,0, 0.5*config.fps,0, None, special=ids.S_INTERDICTOR, specialValue=750 ) # special value: interdictor range
T_RADAR = TurretInstallStats( ids.T_RADAR, 0,200,30*config.fps, 0.05,0, 0,0, 0.5*config.fps,0.1, ids.TA_ROTATING, special=ids.S_RADAR, specialValue=2000 ) # special value: radar range boost
T_NUKE = TurretInstallStats( ids.T_NUKE, 0,500,30*config.fps, 0,0, 0,0, 0.5*config.fps,0, ids.TA_MISSILE_SPECIAL, weapon=W_MISSILE_NUKE,weaponPositions=[RPos(0,10)], special=ids.S_NUKE, specialValue=400 ) # explosion range
T_PULSE = TurretInstallStats( ids.T_PULSE, 0,250,30*config.fps, 0,0, 0,0, 0.5*config.fps,0, ids.TA_MISSILE_SPECIAL, weapon=W_MISSILE_PULSE,weaponPositions=[RPos(0,10)], special=ids.S_PULSE, specialValue=200 ) # range
T_MINER = TurretInstallStats( ids.T_MINER, 0,200,30*config.fps, 0,0, 0,0, 0.5*config.fps,0, ids.TA_MISSILE_SPECIAL, weapon=W_MISSILE_MINER,weaponPositions=[RPos(0,10)], special=ids.S_MINER, specialValue=(60,10,30) ) # explosion range, nbr mines, mines exp range
T_COUNTER = TurretInstallStats( ids.T_COUNTER, 0,150,30*config.fps, 0,0, 0,0, 0.5*config.fps,0, ids.TA_MISSILE_SPECIAL, weapon=W_MISSILE_COUNTER,weaponPositions=[RPos(0,10)], special=ids.S_COUNTER, specialValue=200 ) # effect range
T_GENERATOR = TurretInstallStats( ids.T_GENERATOR, 0,200,30*config.fps, -0.2,0.2, 0,0, 0.5*config.fps,0.2,  ids.TA_ROTATING, special=ids.S_REACTOR, specialValue=750 ) # specialValue=selfDestructRange
T_SOLAR_0 = TurretInstallStats( ids.T_SOLAR_0, 0,100,20*config.fps, 0.05,0, 0,0, 0.5*config.fps,0.008, ids.TA_SOLAR, special=ids.S_SOLAR, specialValue=3 ) # specialValue=solar boost
T_SOLAR_1 = TurretInstallStats( ids.T_SOLAR_1, 0,500,60*config.fps, 0.05,0, 0,0, 0.5*config.fps,0.008, ids.TA_SOLAR, special=ids.S_SOLAR, specialValue=6, upgradeFrom=T_SOLAR_0 ) # specialValue=solar boost
T_SOLAR_2 = TurretInstallStats( ids.T_SOLAR_2, 0,1200,120*config.fps, 0.05,0, 0,0, 0.5*config.fps,0.008, ids.TA_SOLAR, special=ids.S_SOLAR, specialValue=12, upgradeFrom=T_SOLAR_1 ) # specialValue=solar boost
T_HANGAR = TurretInstallStats( ids.T_HANGAR, 0,300,30*config.fps, 0,0, 0,0, 0.5*config.fps,0, None, special=ids.S_HANGAR, specialValue=150 ) # specialValue=space boost
T_BIOSPHERE = TurretInstallStats( ids.T_BIOSPHERE, 0,250,20*config.fps, 0,0, 0,0, 0.5*config.fps,0, None, special=ids.S_CIVILIAN, specialValue=500 ) # specialValue=civilian boost, / 1000
T_BIOSPHERE_1 = TurretInstallStats( ids.T_BIOSPHERE_1, 0,500,40*config.fps, 0,0, 0,0, 0.5*config.fps,0, None, special=ids.S_CIVILIAN, specialValue=2000, upgradeFrom=T_BIOSPHERE ) # specialValue=civilian boost, / 1000
T_SUCKER = TurretInstallStats( ids.T_SUCKER, 0,150,20*config.fps, 0,0, 0,0, 0.5*config.fps,0, None, special=ids.S_SUCKER, specialValue=2 ) # specialValue=ore/(fps/3) frame when in nebula
T_INERTIA = TurretInstallStats( ids.T_INERTIA, 0,500,40*config.fps, 0.2,0, 0,0, 0.5*config.fps,0.2,  ids.TA_ROTATING, special=ids.S_INERTIA, specialValue=1.05 ) # specialValue=inertia mod, WARNING must not go over 1.1!
T_SAIL_0 = TurretInstallStats( ids.T_SAIL_0, 0,300,20*config.fps, 0,0, 0,0, 0.5*config.fps,0.01,  ids.TA_SOLAR, special=ids.S_SAIL, specialValue=1 ) # specialValue= + thrust boost
T_SAIL_1 = TurretInstallStats( ids.T_SAIL_1, 0,600,20*config.fps, 0,0, 0,0, 0.5*config.fps,0.01,  ids.TA_SOLAR, upgradeFrom=T_SAIL_0, special=ids.S_SAIL, specialValue=2 ) # specialValue= + thrust boost
T_SAIL_2 = TurretInstallStats( ids.T_SAIL_2, 0,1000,20*config.fps, 0,0, 0,0, 0.5*config.fps,0.01,  ids.TA_SOLAR, upgradeFrom=T_SAIL_1, special=ids.S_SAIL, specialValue=3 ) # specialValue= + thrust boost
T_JAMMER = TurretInstallStats( ids.T_JAMMER, 0,300,40*config.fps, 0.3,0, 0,0, 0.5*config.fps,0.2,  None, special=ids.S_JAMMER, specialValue=300 ) # specialValue= range
T_SCANNER = TurretInstallStats( ids.T_SCANNER, 0,300,40*config.fps, 0.3,0, 0,0, 0.5*config.fps,0.2,  ids.TA_TARGET, special=ids.S_SCANNER, specialValue=1000 ) # specialValue= range

T_HARVESTER = 	TurretInstallStats( ids.T_HARVESTER, 0, 70, 3*config.fps, 1,0, 0,0, 0.5*config.fps,0.05, ids.TA_HARVESTER, special=ids.S_MINE )
T_SPOTLIGHT = 	TurretInstallStats( ids.T_SPOTLIGHT, 0, 70, 3*config.fps, 1,0, 0,0, 0.5*config.fps,0.08, ids.TA_HARVESTER, special=ids.S_MINE )
T_RED_SPOTLIGHT = 	TurretInstallStats( ids.T_RED_SPOTLIGHT, 0, 70, 3*config.fps, 1,0, 0,0, 0.5*config.fps,0.2, ids.TA_HARVESTER, special=ids.S_MINE )

HARVESTER =		HarvesterShipStats( ids.S_HARVESTER, 11, 0.2, 0.1, 0.02, 30, 15, [TurretStats(0,0, 0, 0, False)], 50, [ids.S_HARVESTER], None, [(11,pi)], T_HARVESTER, 600 )
NOMAD_HARVESTER =		HarvesterShipStats( ids.S_NOMAD_HARVESTER, 11, 0.15, 0.1, 0.02, 30, 15, [TurretStats(7,0, 0, 0, False), TurretStats(-7,0, 0, 0, False)], 70, [ids.S_HARVESTER], None, [(11,pi)], T_SPOTLIGHT, 600 )
NOMAD_HARVESTER_1 =		HarvesterShipStats( ids.S_NOMAD_HARVESTER_1, 11, 0.15, 0.1, 0.02, 30, 15, [TurretStats(7,0, 0, 0, False), TurretStats(-7,0, 0, 0, False)], 70, [ids.S_HARVESTER], None, [(11,pi)], T_SPOTLIGHT, 900 )
EVOLVED_HARVESTER =	HarvesterShipStats( ids.S_EVOLVED_HARVESTER, 11, 0.3, 0.2, 0.02, 30, 15, [TurretStats(4,0, 0, 0, False)], 35, [ids.S_HARVESTER], None, [(11,pi)], T_SPOTLIGHT, 400 )
AI_HARVESTER =		HarvesterShipStats( ids.S_AI_HARVESTER, 11, 0.15, 0.1, 0.02, 30, 15, [TurretStats(7,0, 0, 0, False), TurretStats(-7,0, 0, 0, False)], 70, [ids.S_HARVESTER], None, [(11,pi)], T_SPOTLIGHT, 950 ) # TODO I fear that over 1000, harvesters the ship could easily get lost due to logic in ai.AiPilot.goTo
EXTRA_HARVESTER =	HarvesterShipStats( ids.S_EXTRA_HARVESTER, 11, 0.35, 0.1, 0.02, 30, 15, [TurretStats(12,0, 0, 0, False)], 30, [ids.S_HARVESTER], None, [(11,pi)], T_RED_SPOTLIGHT, 600 )

# extras'
T_ROCK_THROWER_0 = 	TurretInstallStats( ids.T_ROCK_THROWER_0, 0,100,5*config.fps, 0,0, 0,1, 0.2*config.fps,0.05, ids.TA_COMBAT_ROTATING, weapon=W_ROCK_THROWER_0,weaponPositions=[RPos(0,0)] )
T_ROCK_THROWER_1 = 	TurretInstallStats( ids.T_ROCK_THROWER_1, 0,400,5*config.fps, 0,0, 0,3, 0.2*config.fps,0.05, ids.TA_COMBAT_ROTATING, weapon=W_ROCK_THROWER_1,weaponPositions=[RPos(0,0)] )
T_DRAGON_0 = 	TurretInstallStats( ids.T_DRAGON_0, 0,100,5*config.fps, 0,0, 0,1, 0.2*config.fps,0.05, ids.TA_COMBAT_ROTATING, weapon=W_DRAGON_0,weaponPositions=[RPos(0,30)] )
T_LARVA_0 = 	TurretInstallStats( ids.T_LARVA_0, 0,100,15*config.fps, 0,0, 0,0, 0.5*config.fps,0, ids.TA_COMBAT_STABLE, weapon=W_LARVA_0,weaponPositions=[RPos(0,0)] )

# ais'
T_AI_MISSILE_0 = 	TurretInstallStats( ids.T_AI_MISSILE_0, 0,100,15*config.fps, 0,0, 0,0, 0.5*config.fps,0, ids.TA_COMBAT_STABLE, weapon=W_AI_MISSILE,weaponPositions=[RPos(0,5)] )

# evolved's
T_ESPHERE_0 =       TurretInstallStats( ids.T_ESPHERE_0, 0,100,10*config.fps, 0,0, 2,0, 0.5*config.fps, 0.05, ids.TA_COMBAT_ROTATING, weapon=W_ESPHERE_0,weaponPositions=[RPos(0,0)] )
T_ESPHERE_1 =       TurretInstallStats( ids.T_ESPHERE_1, 0,100,30*config.fps, 0,0, 2,0, 0.5*config.fps, 0.05, ids.TA_COMBAT_ROTATING, weapon=W_ESPHERE_0,weaponPositions=[RPos(0,0),RPos(0,14)], upgradeFrom=T_ESPHERE_0 )
T_ESPHERE_2 =       TurretInstallStats( ids.T_ESPHERE_2, 0,100,60*config.fps, 0,0, 2,0, 0.5*config.fps, 0.05, ids.TA_COMBAT_ROTATING, weapon=W_ESPHERE_0,weaponPositions=[RPos(0,0),RPos(0,14),RPos(0,25)], upgradeFrom=T_ESPHERE_1 )
T_BURST_LASER_0 =       TurretInstallStats( ids.T_BURST_LASER_0, 0,100,10*config.fps, 0,0, 2,0, 0.5*config.fps, 0.05, ids.TA_COMBAT_ROTATING, weapon=W_BURST_LASER_0,weaponPositions=[RPos(0,5)] )
T_BURST_LASER_1 =       TurretInstallStats( ids.T_BURST_LASER_1, 0,100,10*config.fps, 0,0, 2,0, 0.35*config.fps, 0.05, ids.TA_COMBAT_ROTATING, weapon=W_BURST_LASER_0,weaponPositions=[RPos(0,5)],upgradeFrom=T_BURST_LASER_0 )
T_BURST_LASER_2 =       TurretInstallStats( ids.T_BURST_LASER_2, 0,100,10*config.fps, 0,0, 2,0, 0.20*config.fps, 0.05, ids.TA_COMBAT_ROTATING, weapon=W_BURST_LASER_0,weaponPositions=[RPos(0,5)],upgradeFrom=T_BURST_LASER_1 )
T_OMNI_LASER_0 =       TurretInstallStats( ids.T_OMNI_LASER_0, 0,100,10*config.fps, 0,0, 2,0, 1, 0.05, ids.TA_COMBAT_STABLE, weapon=W_OMNI_LASER_0,weaponPositions=[RPos(0,0)] )
T_OMNI_LASER_1 =       TurretInstallStats( ids.T_OMNI_LASER_1, 0,100,10*config.fps, 0,0, 2,0, 1, 0.05, ids.TA_COMBAT_STABLE, weapon=W_OMNI_LASER_1,weaponPositions=[RPos(0,0)],upgradeFrom=T_OMNI_LASER_0 )
T_OMNI_LASER_2 =       TurretInstallStats( ids.T_OMNI_LASER_2, 0,100,10*config.fps, 0,0, 2,0, 1, 0.05, ids.TA_COMBAT_STABLE, weapon=W_OMNI_LASER_2,weaponPositions=[RPos(0,0)],upgradeFrom=T_OMNI_LASER_1 )
T_SUBSPACE_WAVE_0 =       TurretInstallStats( ids.T_SUBSPACE_WAVE_0, 0,100,10*config.fps, 0,0, 2,0, 0.5*config.fps, 0.05, ids.TA_COMBAT_ROTATING, weapon=W_SUBSPACE_WAVE_0,weaponPositions=[RPos(0,5)] )
T_SUBSPACE_WAVE_1 =       TurretInstallStats( ids.T_SUBSPACE_WAVE_1, 0,100,10*config.fps, 0,0, 2,0, 0.5*config.fps, 0.05, ids.TA_COMBAT_ROTATING, weapon=W_SUBSPACE_WAVE_1,weaponPositions=[RPos(0,5)],upgradeFrom=T_SUBSPACE_WAVE_0 )

R_HUMAN = 	RaceStats( ids.R_HUMAN,
[FLAGSHIP_0, FLAGSHIP_1, FLAGSHIP_2 ], 
[ids.M_NORMAL, ids.M_NUKE, ids.M_PULSE, ids.M_MINER, ids.M_COUNTER ], 
[HARVESTER, FIGHTER, BOMBER ], 
[T_LASER_SR_1, T_LASER_SR_0, T_LASER_MR_1, T_LASER_MR_0,
T_MASS_SR_2, T_MASS_SR_1, T_MASS_SR_0, T_MASS_LR, T_MASS_MR_1, T_MASS_MR_0,
T_MISSILE_2, T_MISSILE_1, T_MISSILE_0, 
T_NUKE, T_PULSE,T_MINER,
T_COUNTER,T_INTERDICTOR, T_RADAR, T_GENERATOR, T_SOLAR_2, T_SOLAR_1, T_SOLAR_0, T_HANGAR, T_BIOSPHERE_1, T_BIOSPHERE, T_INERTIA, T_SUCKER, T_SAIL_2, T_SAIL_1, T_SAIL_0, T_JAMMER ],
HARVESTER ) # WARNING turret upgrades must be before their parent, see game.py:updatePlayer turrets section

R_AI = 		RaceStats( ids.R_AI, 
[], 
[ids.M_NUKE, ids.M_MINER, ids.M_COUNTER, ids.M_AI], 
[AI_HARVESTER, AI_FIGHTER, AI_BOMBER],
[T_LASER_SR_1, T_LASER_SR_0, T_LASER_MR_1, T_LASER_MR_0,
T_MASS_SR_2, T_MASS_SR_1, T_MASS_SR_0, T_MASS_LR, T_MASS_MR_1, T_MASS_MR_0,
T_AI_MISSILE_0,
T_NUKE,T_MINER,
T_COUNTER,T_INTERDICTOR, T_RADAR, T_GENERATOR, T_SOLAR_2, T_SOLAR_1, T_SOLAR_0, T_HANGAR, T_BIOSPHERE_1, T_BIOSPHERE, T_INERTIA, T_SUCKER, T_SAIL_2, T_SAIL_1, T_SAIL_0, T_JAMMER ],
AI_HARVESTER )

R_NOMAD = 	RaceStats( ids.R_NOMAD, 
[FLAGSHIP_0, FLAGSHIP_1, FLAGSHIP_2 ], 
[ids.M_NORMAL, ids.M_NUKE, ids.M_PULSE, ids.M_MINER, ids.M_COUNTER ], 
[HARVESTER, FIGHTER, BOMBER ], 
[T_LASER_SR_1, T_LASER_SR_0, T_LASER_MR_1, T_LASER_MR_0,
T_MASS_SR_2, T_MASS_SR_1, T_MASS_SR_0, T_MASS_LR, T_MASS_MR_1, T_MASS_MR_0,
T_MISSILE_2, T_MISSILE_1, T_MISSILE_0, 
T_NUKE, T_PULSE,T_MINER,
T_COUNTER,T_INTERDICTOR, T_RADAR, T_GENERATOR, T_SOLAR_2, T_SOLAR_1, T_SOLAR_0, T_HANGAR, T_BIOSPHERE_1, T_BIOSPHERE, T_INERTIA, T_SUCKER, T_SAIL_2, T_SAIL_1, T_SAIL_0, T_JAMMER ],
HARVESTER  )

R_EXTRA = 	RaceStats( ids.R_EXTRA, 
[], 
[ids.M_LARVA], 
[EXTRA_HARVESTER, EXTRA_FIGHTER, EXTRA_BOMBER], 
[],
EXTRA_HARVESTER )

R_EVOLVED = 	RaceStats( ids.R_EVOLVED, 
[], 
[ids.M_NORMAL, ids.M_NUKE, ids.M_PULSE, ids.M_MINER, ids.M_COUNTER ], 
[EVOLVED_HARVESTER, EVOLVED_FIGHTER, EVOLVED_BOMBER],
[#T_LASER_SR_1, T_LASER_SR_0, T_LASER_MR_1, T_LASER_MR_0,
#T_MASS_SR_2, T_MASS_SR_1, T_MASS_SR_0, T_MASS_LR, T_MASS_MR_1, T_MASS_MR_0,
T_MISSILE_2, T_MISSILE_1, T_MISSILE_0, 
T_NUKE, T_PULSE,T_MINER,
T_COUNTER,T_INTERDICTOR, T_RADAR, T_GENERATOR, T_SOLAR_2, T_SOLAR_1, T_SOLAR_0, T_HANGAR, T_BIOSPHERE_1, T_BIOSPHERE, T_INERTIA, T_SAIL_2, T_SAIL_1, T_SAIL_0, T_JAMMER,
T_ESPHERE_2, T_ESPHERE_1, T_ESPHERE_0,
T_BURST_LASER_2, T_BURST_LASER_1, T_BURST_LASER_0,
T_OMNI_LASER_2, T_OMNI_LASER_1, T_OMNI_LASER_0,
T_SUBSPACE_WAVE_0, T_SUBSPACE_WAVE_1 ],
EVOLVED_HARVESTER )

Buildable = { ids.T_LASER_SR_0:	T_LASER_SR_0, 
              ids.T_LASER_SR_1:	T_LASER_SR_1, 
              ids.T_LASER_MR_0:	T_LASER_MR_0, 
              ids.T_LASER_MR_1:	T_LASER_MR_1, 
              ids.T_MASS_SR_0:	T_MASS_SR_0, 
              ids.T_MASS_SR_1:	T_MASS_SR_1, 
              ids.T_MASS_SR_2:	T_MASS_SR_2, 
              ids.T_MASS_MR_0:	T_MASS_MR_0,  
              ids.T_MASS_MR_1:	T_MASS_MR_1, 
              ids.T_MASS_LR:	T_MASS_LR, 
              ids.T_MISSILES_0:	T_MISSILE_0, 
              ids.T_MISSILES_1:	T_MISSILE_1, 
              ids.T_MISSILES_2:	T_MISSILE_2, 
              ids.T_HARVESTER: 	 T_HARVESTER, 
              ids.T_INTERDICTOR: T_INTERDICTOR, 
              ids.T_RADAR: 	 T_RADAR, 
              ids.T_NUKE: 	 T_NUKE, 
              ids.T_PULSE: 	 T_PULSE, 
              ids.T_HANGAR: 	 T_HANGAR, 
              ids.T_SOLAR_0: 	 T_SOLAR_0, 
              ids.T_SOLAR_1: 	 T_SOLAR_1, 
              ids.T_SOLAR_2: 	 T_SOLAR_2, 
              ids.T_GENERATOR: 	 T_GENERATOR,
              ids.T_MINER: 	 T_MINER,
              ids.T_COUNTER: 	 T_COUNTER,
              ids.T_BIOSPHERE: 	 T_BIOSPHERE,
              ids.T_BIOSPHERE_1: T_BIOSPHERE_1,
              ids.T_INERTIA: 	 T_INERTIA,
              ids.T_SUCKER: 	 T_SUCKER,
              ids.T_SAIL_0: 	 T_SAIL_0,
              ids.T_SAIL_1: 	 T_SAIL_1,
              ids.T_SAIL_2: 	 T_SAIL_2,
              ids.T_JAMMER: 	 T_JAMMER,

              ids.T_AI_MISSILE_0:  T_AI_MISSILE_0,

              ids.T_ESPHERE_0:  T_ESPHERE_0,
              ids.T_ESPHERE_1:  T_ESPHERE_1,
              ids.T_ESPHERE_2:  T_ESPHERE_2,
              ids.T_BURST_LASER_0:  T_BURST_LASER_0,
              ids.T_BURST_LASER_1:  T_BURST_LASER_1,
              ids.T_BURST_LASER_2:  T_BURST_LASER_2,
              ids.T_OMNI_LASER_0:  T_OMNI_LASER_0,
              ids.T_OMNI_LASER_1:  T_OMNI_LASER_1,
              ids.T_OMNI_LASER_2:  T_OMNI_LASER_2,
              ids.T_SUBSPACE_WAVE_0:  T_SUBSPACE_WAVE_0,
              ids.T_SUBSPACE_WAVE_1:  T_SUBSPACE_WAVE_1,

              ids.S_HARVESTER: HARVESTER,
              ids.S_FIGHTER: FIGHTER,
              ids.S_BOMBER: BOMBER,

              ids.S_NOMAD_HARVESTER: NOMAD_HARVESTER,
              ids.S_NOMAD_HARVESTER_1: NOMAD_HARVESTER_1,
              ids.S_NOMAD_FIGHTER: NOMAD_FIGHTER,

              ids.S_AI_HARVESTER: AI_HARVESTER,
              ids.S_AI_FIGHTER: AI_FIGHTER,
              ids.S_AI_BOMBER: AI_BOMBER,

              ids.S_EVOLVED_HARVESTER: EVOLVED_HARVESTER,
              ids.S_EVOLVED_FIGHTER: EVOLVED_FIGHTER,
              ids.S_EVOLVED_BOMBER: EVOLVED_BOMBER,

              ids.S_EXTRA_HARVESTER: EXTRA_HARVESTER,
              ids.S_EXTRA_FIGHTER: EXTRA_FIGHTER,
              ids.S_EXTRA_BOMBER: EXTRA_BOMBER
              }

Costs = { ids.S_HARVESTER: Cost( 0, 100, 10*config.fps, 10 ),
          ids.S_FIGHTER: Cost( 0, 75, 5*config.fps, 10 ),
          ids.S_BOMBER: Cost( 0, 150, 15*config.fps, 15 ),

          ids.S_AI_HARVESTER: Cost( 0, 150, 15*config.fps, 15 ),
          ids.S_AI_FIGHTER: Cost( 0, 70, 10*config.fps, 3 ),
          ids.S_AI_BOMBER: Cost( 0, 200, 20*config.fps, 10 ),

          ids.S_EVOLVED_HARVESTER: Cost( 0, 75, 8*config.fps, 7 ),
          ids.S_EVOLVED_FIGHTER: Cost( 0, 150, 15*config.fps, 15 ),
          ids.S_EVOLVED_BOMBER: Cost( 0, 300, 20*config.fps, 25 ),

          ids.S_EXTRA_HARVESTER: Cost( 0, 75, 8*config.fps, 7 ),
          ids.S_EXTRA_FIGHTER: Cost( 0, 70, 10*config.fps, 3 ),
          ids.S_EXTRA_BOMBER: Cost( 0, 70, 10*config.fps, 3 ),

          ids.M_NORMAL: Cost( 0, 10, 2*config.fps, 1 ),
          ids.M_NUKE:   Cost( 0, 500, 60*config.fps, 40 ),
          ids.M_PULSE: Cost( 0, 150, 30*config.fps, 10 ),
          ids.M_MINER: Cost( 0, 120, 15*config.fps, 10 ),
          ids.M_COUNTER: Cost( 0, 50, 10*config.fps, 5 ),
          ids.M_AI: Cost( 0, 10, 10*config.fps, 5 ),
          ids.M_LARVA: Cost( 0, 10, 10*config.fps, 5 ),
        }

Relations = { R_HUMAN: 	{ R_HUMAN: 100, R_AI: 30, R_NOMAD: 30, R_EXTRA: -50, R_EVOLVED: 10 },
              R_AI: 	{ R_HUMAN: 10, R_AI: 40, R_NOMAD: 10, R_EXTRA: 10, R_EVOLVED: 10 },
              R_NOMAD: 	{ R_HUMAN: 30, R_AI: 10, R_NOMAD: 50, R_EXTRA: 5, R_EVOLVED: 75 },
              R_EXTRA: 	{ R_HUMAN: -50, R_AI: 10, R_NOMAD: -50, R_EXTRA: 20, R_EVOLVED: -50 },
              R_EVOLVED: { R_HUMAN: 25, R_AI: -20, R_NOMAD: 75, R_EXTRA: -50 , R_EVOLVED: 100 } }

PlayableShips = { ids.S_FLAGSHIP_0: ShipChoice( FLAGSHIP_0, R_HUMAN, 0 ), 
                  ids.S_FLAGSHIP_1: ShipChoice( FLAGSHIP_1, R_HUMAN, 200 ), 
                  ids.S_FLAGSHIP_2: ShipChoice( FLAGSHIP_2, R_HUMAN, 500 ),

                  ids.S_EVOLVED_FS_0: ShipChoice( EVOLVED_FS_0, R_EVOLVED, 0 ),
                  ids.S_EVOLVED_FS_1: ShipChoice( EVOLVED_FS_1, R_EVOLVED, 200 ),
                  ids.S_EVOLVED_FS_2: ShipChoice( EVOLVED_FS_2, R_EVOLVED, 500 ),

                  ids.S_AI_FS_0: ShipChoice( AI_FS_0, R_AI, 0 ),
                  ids.S_AI_FS_1: ShipChoice( AI_FS_1, R_AI, 200 ),
                  ids.S_AI_FS_2: ShipChoice( AI_FS_2, R_AI, 500 ),

                  ids.S_NOMAD_FS_0: ShipChoice( NOMAD_FS_0, R_NOMAD, 0 ),
                  ids.S_NOMAD_FS_1: ShipChoice( NOMAD_FS_1, R_NOMAD, 200 ),
                  ids.S_NOMAD_FS_2: ShipChoice( NOMAD_FS_2, R_NOMAD, 500 ),

                #  ids.S_AI_FS_0: ShipChoice( AI_FS_0, 0 ),
               #   ids.S_AI_FS_1: ShipChoice( AI_FS_1, 0 ),
                #  ids.S_AI_FS_2: ShipChoice( AI_FS_2, 0 ) 
}

