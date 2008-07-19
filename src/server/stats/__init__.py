from math import pi, atan2, hypot

#from self.AIs import *

from common import ids
from common import config
from common import gfxs

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
           projectile=None,projectileTtl=2*config.fps, laserWidth=None, \
           soundAtFire=ids.S_EX_FIRE, soundAtHit=ids.S_EX_FIRE, gfxAtFire=None, gfxAtHit=ids.G_EXPLOSION \
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

#class self.BombWeaponStats( WeaponStats ):
#    self.explosionRange = explosionRange
#    self.pulseLength = pulseLength

## ships
class ShipStats( ObjectStats ):
    def __init__(self,id,radius,maxThrust,maxReverseThrust,maxRg,maxHull,maxShield,unavoidableFragments, fragments, engines,energyCostToBuild=0,oreCostToBuild=0,timeToBuild=0,hangarSpaceNeed=0 ):
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
        self.pointsWorth = radius # /2
        self.energyCostToBuild = energyCostToBuild
        self.oreCostToBuild = oreCostToBuild
        self.timeToBuild = timeToBuild
        self.hangarSpaceNeed = hangarSpaceNeed

class SingleWeaponShipStats( ShipStats ):
    def __init__(self,id,radius,maxThrust,maxReverseThrust,maxRg,maxHull,maxShield,weapon,unavoidableFragments, fragments, engines, weaponPositions=None,energyCostToBuild=0,oreCostToBuild=0,timeToBuild=0,hangarSpaceNeed=0):
        ShipStats.__init__(self,id,radius,maxThrust,maxReverseThrust,maxRg,maxHull,maxShield,unavoidableFragments, fragments, engines, energyCostToBuild=energyCostToBuild, oreCostToBuild=oreCostToBuild, timeToBuild=timeToBuild, hangarSpaceNeed=hangarSpaceNeed )
        """weaponPositions format = [ set1=[pos0,pos1], set2=... ] allows to alternate between different weapon sets"""
        self.weapon = weapon
    #    rx, ry = 10, 0
        if weaponPositions:
            self.weaponPositions = weaponPositions # [RPos( 0, 10 )]# = hypot( rx, ry )
        else:
            self.weaponPositions = [[RPos( 0, 10 )]]
     #  self.weaponPosAngle = atan2( rx, ry )

class MultipleWeaponsShipStats( ShipStats ):
    def __init__(self,id,radius,maxThrust,maxReverseThrust,maxRg,maxHull,maxShield,turrets,unavoidableFragments, fragments, engines,energyCostToBuild=0,oreCostToBuild=0,timeToBuild=0,hangarSpaceNeed=0):
        ShipStats.__init__(self,id,radius,maxThrust,maxReverseThrust,maxRg,maxHull,maxShield,unavoidableFragments, fragments, engines, energyCostToBuild=energyCostToBuild, oreCostToBuild=oreCostToBuild, timeToBuild=timeToBuild, hangarSpaceNeed=hangarSpaceNeed )
        self.turrets = turrets

class Flagship( MultipleWeaponsShipStats ):
    def __init__(self,id,radius,maxThrust,maxReverseThrust,maxRg,maxHull,maxShield,turrets, maxEnergy, maxOre, hangarSpace, jumpEnergyCost, launchDelay,radarRange,unavoidableFragments, fragments, engines, hangars=None, civilianBonus=1000, pulseResistant=False, jumpChargeDelay=3*config.fps, jumpRecoverDelay=20*config.fps, energyCostToBuild=0,oreCostToBuild=0,timeToBuild=0,hangarSpaceNeed=0):
        MultipleWeaponsShipStats.__init__(self,id,radius,maxThrust,maxReverseThrust,maxRg,maxHull,maxShield,turrets,unavoidableFragments, fragments, engines, energyCostToBuild=energyCostToBuild, oreCostToBuild=oreCostToBuild, timeToBuild=timeToBuild, hangarSpaceNeed=hangarSpaceNeed )
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
    def __init__(self,id,radius,maxThrust,maxReverseThrust,maxRg,maxHull,maxShield,turrets,maxOre,unavoidableFragments, fragments, engines, turretType, maxRange, energyCostToBuild=0,oreCostToBuild=0,timeToBuild=0,hangarSpaceNeed=0):
        MultipleWeaponsShipStats.__init__(self,id,radius,maxThrust,maxReverseThrust,maxRg,maxHull,maxShield,turrets,unavoidableFragments, fragments, engines, energyCostToBuild=energyCostToBuild, oreCostToBuild=oreCostToBuild, timeToBuild=timeToBuild, hangarSpaceNeed=hangarSpaceNeed )
        self.maxOre = maxOre
        self.maxRange = maxRange
        self.turretType = turretType

class CivilianShipStats( ShipStats ):
    def __init__(self,id,radius,maxThrust,maxReverseThrust,maxRg,maxHull,maxShield, influenceRadius,unavoidableFragments, fragments, engines, energyCostToBuild=0,oreCostToBuild=0,timeToBuild=0,hangarSpaceNeed=0):
        ShipStats.__init__(self,id,radius,maxThrust,maxReverseThrust,maxRg,maxHull,maxShield,unavoidableFragments, fragments, engines, energyCostToBuild=energyCostToBuild, oreCostToBuild=oreCostToBuild, timeToBuild=timeToBuild, hangarSpaceNeed=hangarSpaceNeed)
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
    def __init__( self, type,energyCostToBuild,oreCostToBuild,timeToBuild, energyPerFrame,orePerFrame, energyPerUse,orePerUse, freqOfFire,turretSpeed, ai, category=None, weapon=None,weaponPositions=None, special=None, specialValue=None, upgradeFrom=None, civilian=False, solar=0, darkExtractor=0, darkEngine=0 ):
        """weaponPositions format = [ set1=[pos0,pos1], set2=... ] allows to alternate between different weapon sets"""
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
      #  elif self.AI == ids.TA_MISSILE_SPECIAL:
      #      self.category = ids.C_MISSILE
      #  elif weapon:
      #      self.category = ids.C_WEAPON
     #   else:
      #      self.category = ids.C_OTHER

        self.weapon = weapon
        self.weaponPositions = weaponPositions
        self.special = special
        self.specialValue = specialValue
        
        ### special
      #  S_NUKE
      #  S_PULSE
     #   S_MINE
      #  S_MINER
      #  S_COUNTER
        
      #  self.interdictor # range
      #  self.generator
      #  self.radar # range d
        self.solar = solar
      #  self.hangar # efficiency
      #  self.civilian # efficiency
      #  self.sucker # eff
      #  self.inertia # eff
      #  self.sail # eff
      #  self.jammer # range, freq
     #   self.scanner  
        self.darkExtractor = darkExtractor
        self.darkEngine = darkEngine

        ### upgrades

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


class Stats:
    def __init__( self ):
        self.ShipChoice = ShipChoice
        self.ObjectStats = ObjectStats
        self.OrbitableStats = OrbitableStats
        self.WeaponStats = WeaponStats
        self.ShipStats = ShipStats
        self.SingleWeaponShipStats = SingleWeaponShipStats
        self.MultipleWeaponsShipStats = MultipleWeaponsShipStats
        self.Flagship = Flagship
        self.HarvesterShipStats = HarvesterShipStats
        self.CivilianShipStats = CivilianShipStats
        self.TurretStats = TurretStats
        self.TurretInstallStats = TurretInstallStats
        self.SunStats = SunStats
        self.BlackHoleStats = BlackHoleStats
        self.RPos = RPos
        self.RaceStats = RaceStats
        self.Cost = Cost
        self.ShipChoice = ShipChoice
        
        # id,radius,maxThrust,maxReverseThrust,maxRg,maxHull,maxShield
        self.MISSILE_NORMAL = ShipStats( ids.M_NORMAL, 3, 0.6, 0, 0.008, 5, 0, None, None, [(2,pi)], energyCostToBuild=0,oreCostToBuild=10,timeToBuild=2*config.fps,hangarSpaceNeed=1 ) 
        self.MISSILE_NUKE = 	ShipStats( ids.M_NUKE, 3, 0.4, 0, 0.004, 5, 0, None, None, [(2,pi)], energyCostToBuild=500,oreCostToBuild=500,timeToBuild=45*config.fps,hangarSpaceNeed=30 ) 
        self.MISSILE_PULSE = ShipStats( ids.M_PULSE, 3, 0.6, 0, 0.007, 5, 0, None, None, [(2,pi)], energyCostToBuild=0,oreCostToBuild=150,timeToBuild=30*config.fps,hangarSpaceNeed=10 ) 
        self.MISSILE_MINER = ShipStats( ids.M_MINER, 3, 0.5, 0, 0.006, 5, 0, None, None, [(2,pi)], energyCostToBuild=0,oreCostToBuild=120,timeToBuild=15*config.fps,hangarSpaceNeed=10 ) 
        self.MISSILE_COUNTER = ShipStats( ids.M_COUNTER, 3, 0.8, 0, 0.005, 5, 0, None, None, [(2,pi)], energyCostToBuild=0,oreCostToBuild=50,timeToBuild=10*config.fps,hangarSpaceNeed=5 ) 
        
        self.MISSILE_AI = ShipStats( ids.M_AI, 3, 0.6, 0, 0.008, 5, 0, None, None, [(2,pi)], energyCostToBuild=0,oreCostToBuild=10,timeToBuild=2*config.fps,hangarSpaceNeed=2 ) 
        
        self.MISSILE_LARVA = ShipStats( ids.M_LARVA, 3, 0.6, 0, 0.008, 5, 0, None, None, [(2,pi)], energyCostToBuild=0,oreCostToBuild=10,timeToBuild=2*config.fps,hangarSpaceNeed=2 ) 
        
        self.MISSILE_EVOLVED = ShipStats( ids.M_EVOLVED, 3, 0.6, 0, 0.008, 5, 0, None, None, [(2,pi)], energyCostToBuild=10,oreCostToBuild=1,timeToBuild=1*config.fps,hangarSpaceNeed=1 ) 
        self.MISSILE_EVOLVED_COUNTER = ShipStats( ids.M_EVOLVED_COUNTER, 3, 0.8, 0, 0.005, 5, 0, None, None, [(2,pi)], energyCostToBuild=40,oreCostToBuild=10,timeToBuild=10*config.fps,hangarSpaceNeed=5 ) 
        self.MISSILE_EVOLVED_PULSE = ShipStats( ids.M_EVOLVED_PULSE, 3, 0.6, 0, 0.007, 5, 0, None, None, [(2,pi)], energyCostToBuild=100,oreCostToBuild=50,timeToBuild=30*config.fps,hangarSpaceNeed=10 ) 

        self.BULLET_0 =  	ObjectStats( ids.B_BULLET_0, 3 )
        self.BOMB_0 =  	ObjectStats( ids.B_BOMB_0, 3 )
        self.B_ROCK_0 =  	ObjectStats( ids.B_ROCK_0, 4 )
        self.B_ROCK_1 =  	ObjectStats( ids.B_ROCK_1, 7 )
        self.B_AI_0 =  	ObjectStats( ids.B_AI_0, 4 )
        self.B_FIRE_0 =  	ObjectStats( ids.B_FIRE_0, 5 )
        self.B_ESPHERE =     ObjectStats( ids.B_ESPHERE, 7 )
        self.B_WAVE_0 =      ObjectStats( ids.B_WAVE_0, 7 )
        self.B_WAVE_1 =      ObjectStats( ids.B_WAVE_1, 10 )
        self.B_EGG_0 =      ObjectStats( ids.B_EGG_0, 6 )

        # id,minRange,maxRange,certainty, energyDamage,massDamage,freqOfFire,speed,weaponType,projectile=None
        self.W_LASER_SR =  	WeaponStats( ids.W_LASER_SR, 30,250,20, 1,0, 1,0, ids.WT_LASER, gfxAtFire = gfxs.GfxLaser, laserWidth=1) #, laserColor=ids.RED)
        # self.W_LASER_SR_FIGHTER = 	WeaponStats( ids.W_LASER_SR, 30,250,20, 1,0, 1,0, ids.WT_LASER)
        self.W_LASER_MR_0 = 	WeaponStats( ids.W_LASER_MR_0, 50,400,50, 3,0, 1,0, ids.WT_LASER, gfxAtFire = gfxs.GfxLaser, laserWidth=2 ) # , laserColor=ids.RED) # 0.5*config.fps
        self.W_LASER_MR_1 = 	WeaponStats( ids.W_LASER_MR_1, 50,500,50, 5,0, 1,0, ids.WT_LASER, gfxAtFire = gfxs.GfxLaser, laserWidth=3 ) # , laserColor=ids.RED) # 0.5*config.fps

        self.W_MASS_SR_0 = 	WeaponStats( ids.W_MASS_SR, 20, 400, 20, 0,4, 0.3*config.fps,15, ids.WT_MASS, projectile=self.BULLET_0)
        self.W_MASS_SR_1 = 	WeaponStats( ids.W_MASS_SR, 20, 400, 20, 0,4, 0.2*config.fps,15, ids.WT_MASS, projectile=self.BULLET_0)
        self.W_MASS_SR_2 = 	WeaponStats( ids.W_MASS_SR, 20, 400, 20, 0,4, 0.1*config.fps,15, ids.WT_MASS, projectile=self.BULLET_0)
        self.W_MASS_SR_FIGHTER = 	WeaponStats( ids.W_MASS_SR, 30, 300, 20, 0,3, 0.15*config.fps,15, ids.WT_MASS, projectile=self.BULLET_0)
        self.W_MASS_MR = 	WeaponStats( ids.W_MASS_MR, 50, 500, 50, 0,20, 1*config.fps,10, ids.WT_MASS, projectile=self.BULLET_0)
        self.W_MASS_LR = 	WeaponStats( ids.W_MASS_LR, 50, 1500, 150, 0,50, 3*config.fps,30, ids.WT_MASS, projectile=self.BULLET_0, projectileTtl=7*config.fps)

        self.W_MISSILE = 		WeaponStats( ids.W_MISSILE, 70, 600, 0, 10,5, 1*config.fps,10, ids.WT_MISSILE, projectile=self.MISSILE_NORMAL, projectileTtl=10*config.fps)
        self.W_MISSILE_NUKE = 	WeaponStats( ids.W_NUKE, 70, 600, 100, 0,800, 2*config.fps,10, ids.WT_MISSILE, projectile=self.MISSILE_NUKE, projectileTtl=15*config.fps)
        self.W_MISSILE_PULSE = 	WeaponStats( ids.W_PULSE, 70, 600, 0, 1,0, 2*config.fps,10, ids.WT_MISSILE, projectile=self.MISSILE_PULSE, projectileTtl=15*config.fps)
        self.W_MISSILE_MINER = 	WeaponStats( ids.W_MINER, 70, 600, 0, 15, 10, 4*config.fps,10, ids.WT_MISSILE, projectile=self.MISSILE_MINER, projectileTtl=15*config.fps)
        self.W_MISSILE_COUNTER = 	WeaponStats( ids.W_COUNTER, 70, 600, 1, 0, 5, 1*config.fps,10, ids.WT_MISSILE, projectile=self.MISSILE_COUNTER, projectileTtl=10*config.fps)
        # self.W_MISSILE_1 = 	WeaponStats( ids.W_MISSILES_1, 70, 600, 2*config.fps, 5, 5, 50, 0, 0, [RPos(0,7),RPos(0.7,9.2),RPos(-0.7,9.2)], 10,5,10, self.MISSILE_0)

        self.W_BOMB_0 = 	WeaponStats( ids.W_BOMB_0, 50, 300, 90, 0,20, 0.5*config.fps,0.2, ids.WT_BOMB, projectile=self.BOMB_0 )

        # self.EXTRAs'
        self.W_ROCK_THROWER_0 = 	WeaponStats( ids.W_ROCK_THROWER_0, 50, 300, 20, 0,2, 0.6*config.fps,15, ids.WT_MASS, projectile=self.B_ROCK_0)
        self.W_ROCK_THROWER_1 = 	WeaponStats( ids.W_ROCK_THROWER_1, 50, 300, 20, 0,2, 0.6*config.fps,15, ids.WT_MASS, projectile=self.B_ROCK_1)
        self.W_DRAGON_0 = 		WeaponStats( ids.W_DRAGON_0, 50, 300, 20, 5,0, 0.6*config.fps,15, ids.WT_MASS, projectile=self.B_FIRE_0)
        self.W_LARVA_0 = 		WeaponStats( ids.W_LARVA_0, 70, 600, 0, 10,5, 1*config.fps,10, ids.WT_MISSILE, projectile=self.MISSILE_LARVA, projectileTtl=10*config.fps)
        self.W_EXTRA_FIGHTER = 	WeaponStats( ids.W_EXTRA_FIGHTER, 50, 300, 20, 3,0, 0.6*config.fps,15, ids.WT_MASS, projectile=self.B_FIRE_0)
        self.W_EXTRA_BOMBER = 	WeaponStats( ids.W_EXTRA_BOMBER, 50, 300, 90, 0,20, 0.5*config.fps,0.2, ids.WT_BOMB, projectile=self.B_EGG_0 )

        # self.AIs'
        self.W_AI_MISSILE = 		WeaponStats( ids.W_AI_MISSILE, 70, 600, 0, 10,5, 1*config.fps,10, ids.WT_MISSILE, projectile=self.MISSILE_AI, projectileTtl=10*config.fps)

        # self.EVOLVED's
        self.W_ESPHERE_0 = 	WeaponStats( ids.W_ESPHERE_0, 50, 500, 50, 10,5, 1*config.fps,10, ids.WT_MASS, projectile=self.B_ESPHERE)
        #W_ESPHERE_1 = 	WeaponStats( ids.W_ESPHERE_1, 50, 500, 50, 10,0, 1*config.fps,10, ids.WT_MASS, projectile=B_ESPHERE)
        #W_ESPHERE_2 = 	WeaponStats( ids.W_ESPHERE_2, 50, 500, 50, 10,0, 1*config.fps,10, ids.WT_MASS, projectile=B_ESPHERE)
        self.W_BURST_LASER_0 = 	WeaponStats( ids.W_BURST_LASER_0, 50, 500, 50, 10,0, 1*config.fps,10, ids.WT_LASER, gfxAtFire = gfxs.GfxLaser, laserWidth=2 )
        self.W_OMNI_LASER_0 = 	WeaponStats( ids.W_OMNI_LASER_0, 50, 500, 50, 2,0, 1,10, ids.WT_OMNI_LASER, gfxAtFire = gfxs.GfxLaser, laserWidth=3 )
        self.W_OMNI_LASER_1 = 	WeaponStats( ids.W_OMNI_LASER_1, 50, 500, 50, 3,0, 1,10, ids.WT_OMNI_LASER, gfxAtFire = gfxs.GfxLaser, laserWidth=4 )
        self.W_OMNI_LASER_2 = 	WeaponStats( ids.W_OMNI_LASER_2, 50, 500, 50, 4,0, 1,10, ids.WT_OMNI_LASER, gfxAtFire = gfxs.GfxLaser, laserWidth=5 )
        self.W_SUBSPACE_WAVE_0 = 	WeaponStats( ids.W_SUBSPACE_WAVE_0, 50, 500, 50, 0,10, 1*config.fps,5, ids.WT_MASS, projectile=self.B_WAVE_0, projectileTtl=4*config.fps)
        self.W_SUBSPACE_WAVE_1 = 	WeaponStats( ids.W_SUBSPACE_WAVE_1, 50, 500, 50, 0,20, 1*config.fps,5, ids.WT_MASS, projectile=self.B_WAVE_1, projectileTtl=4*config.fps)
        
        self.W_EVOLVED_MISSILE = 		WeaponStats( ids.W_EVOLVED_MISSILE, 70, 600, 0, 8,4, 1*config.fps,10, ids.WT_MISSILE, projectile=self.MISSILE_EVOLVED, projectileTtl=10*config.fps)
        self.W_EVOLVED_PULSE = 		WeaponStats( ids.W_EVOLVED_PULSE, 70, 600, 0, 1,0, 2*config.fps,10, ids.WT_MISSILE, projectile=self.MISSILE_EVOLVED_PULSE, projectileTtl=15*config.fps)
        self.W_EVOLVED_COUNTER = 		WeaponStats( ids.W_EVOLVED_COUNTER, 70, 600, 1, 0, 5, 1*config.fps,10, ids.WT_MISSILE, projectile=self.MISSILE_EVOLVED_COUNTER, projectileTtl=10*config.fps)

        # nomad
        self.W_DISCHARGER_0 = 	WeaponStats( ids.W_DISCHARGER_0, 50, 400, 50, 3,0, 1,0, ids.WT_LASER, gfxAtFire = gfxs.GfxLightning, laserWidth=2 )
        self.W_DISCHARGER_1 = 	WeaponStats( ids.W_DISCHARGER_1, 50, 400, 50, 3,0, 1,0, ids.WT_LASER, gfxAtFire = gfxs.GfxLightning, laserWidth=2 )

        self.ASTEROIDS =	[ OrbitableStats( ids.A_0, 46 ), OrbitableStats( ids.A_1, 41 ), OrbitableStats( ids.A_2, 26 ), OrbitableStats( ids.A_3, 37 ), OrbitableStats( ids.A_4, 24 ) ] #[ OrbitableStats( 0, 10 ), OrbitableStats( 1, 20 ), OrbitableStats( 2, 30 ) ], \
                          #[ OrbitableStats( 3, 10 ), OrbitableStats( 4, 20 ), OrbitableStats( 5, 30 ) ], \
                          #[ OrbitableStats( 6, 10 ), OrbitableStats( 7, 20 ), OrbitableStats( 8, 30 ) ] ]

        self.P_MERCURY =	OrbitableStats( ids.P_MERCURY, 190 )
        self.P_MARS =	OrbitableStats( ids.P_MARS, 281 )
        self.P_EARTH =	OrbitableStats( ids.P_EARTH, 325 )
        self.P_VENUS =	OrbitableStats( ids.P_VENUS, 250 )
        self.P_JUPITER =	OrbitableStats( ids.P_JUPITER, 700 )
        self.P_SATURN =	OrbitableStats( ids.P_SATURN, 551 )
        self.P_NEPTUNE =	OrbitableStats( ids.P_NEPTUNE, 350 )

        self.P_MOON =	OrbitableStats( ids.P_MOON, 110 )
        self.P_MARS_1 =	OrbitableStats( ids.P_MARS_1, 290 )
        self.P_MARS_2 =	OrbitableStats( ids.P_MARS_2, 320 )
        self.P_JUPITER_1 =	OrbitableStats( ids.P_JUPITER_1, 600 )
        self.P_MERCURY_1 =	OrbitableStats( ids.P_MERCURY_1, 240 )
        self.P_X =		OrbitableStats( ids.P_X, 250 )
        self.P_X_1 =		OrbitableStats( ids.P_X_1, 240 )
        self.P_SATURN_1 =	OrbitableStats( ids.P_SATURN_1, 551 )

        self.P_GAIA =	OrbitableStats( ids.P_GAIA, 300 )

        self.S_SOL = 	SunStats( ids.S_SOL, 1750, 3500, 7, 15000, 0.2 )
        self.BH_0 = 		BlackHoleStats( ids.A_BLACK_HOLE, 240, 400, 10, 1200, 20. )

        self.A_NEBULA =	ObjectStats( None, 800 )
     #   self.A_NEBULA_1 =	ObjectStats( ids.A_NEBULA, 1000 )
     #   self.A_NEBULA_2 =	ObjectStats( ids.A_NEBULA, 1000 )

        ### ships

         ## self.HUMAN
        #SHIP = 		SingleWeaponShipStats( 9, 20, 0.3, 0.2, 0.008, 50, 100, self.W_MASS_SR, None, None, [(20,pi)] )
        self.HUMAN_FIGHTER =	SingleWeaponShipStats( ids.S_HUMAN_FIGHTER, 15, 0.6, 0, 0.012, 20, 20, self.W_MASS_SR_FIGHTER, [ids.F_FIGHTER_0,ids.F_FIGHTER_1,ids.F_FIGHTER_2], None, [(15,pi)], energyCostToBuild=0,oreCostToBuild=75,timeToBuild=5*config.fps,hangarSpaceNeed=10 )
        self.HUMAN_BOMBER =	SingleWeaponShipStats( ids.S_HUMAN_BOMBER, 15, 0.5, 0, 0.010, 30, 25, self.W_BOMB_0, [ids.S_HUMAN_BOMBER], None, [(15,pi)], energyCostToBuild=0,oreCostToBuild=150,timeToBuild=15*config.fps,hangarSpaceNeed=15 )

        self.HUMAN_PIRATE =	Flagship( ids.S_HUMAN_PIRATE, 50, 0.22, 0.05, 0.0025, 250, 1,
                        [TurretStats(-3, 22, 0,pi, True),
                         TurretStats(-3,-22, pi,2*pi, True)
                         ],
                         500, 200, 100, 500, 1*config.fps, 2500, [], [ids.F_LARGE_0, ids.F_LARGE_1], [(80,pi)] ) 
        self.HUMAN_SCOUT =	Flagship( ids.S_HUMAN_PIRATE, 50, 0.22, 0.05, 0.0025, 250, 100,
                        [TurretStats(-3, 22, 0,pi, True),
                         TurretStats(-3,-22, pi,2*pi, True)
                         ],
                         500, 200, 100, 450, 1*config.fps, 1000, [], [ids.F_LARGE_0, ids.F_LARGE_1], [(80,pi)],
                         jumpChargeDelay=8*config.fps, jumpRecoverDelay=20*config.fps ) 
        self.HUMAN_CARGO =	Flagship( ids.S_HUMAN_CARGO, 70, 0.16, 0.05, 0.0022, 300, 200,
                        [TurretStats(48, 10, 3*pi/2,pi, True),
                         TurretStats(48,-10, pi,pi/2, True),
                         TurretStats(12, 10, 0,pi, True),
                         TurretStats(12,-10, pi,2*pi, True)
                         ],
                         1000, 1000, 600, 2000, 1*config.fps, 750, [], [ids.F_LARGE_0, ids.F_LARGE_1], [(80,pi)] ) 
        self.HUMAN_FS_0 =	Flagship( ids.S_HUMAN_FS_0, 80, 0.13, 0.05, 0.002, 350, 500,
                        [TurretStats(53, 8, 5*pi/3,2*pi/3, True),
                         TurretStats(53,-8, 4*pi/3,1*pi/3, True),
                         TurretStats(13,16, 0,pi, True),
                         TurretStats(13,-16, pi,2*pi, True),
                         TurretStats(-20.5,41.5, 0,4*pi/3, True),
                         TurretStats(-20.5,-41.5, 2*pi/3,2*pi, True),
                         ],
                         1000, 1000, 500, 500, 0.8*config.fps, 2500, [ids.F_HUMAN_FS_0], [ids.F_LARGE_0, ids.F_LARGE_1], [(80,pi)] ) 
        self.HUMAN_FS_1 =	Flagship( ids.S_HUMAN_FS_1, 100, 0.11, 0.05, 0.002, 300, 500, 
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
                        3000, 3000, 300, 500, 0.7*config.fps, 2500, [ids.F_HUMAN_FS_1], [ids.F_LARGE_0, ids.F_LARGE_1], [(80,pi)],
                        hangars=[(RPos(0, 0 ), pi/2), (RPos(0, 0 ), 3*pi/2)], civilianBonus=750 )
        self.HUMAN_FS_2 =	Flagship( ids.S_HUMAN_FS_2, 70, 0.1, 0.05, 0.002, 400, 500, 
                        [TurretStats(8,21,0,pi, True),
                         TurretStats(8,-21,pi,2*pi, True),
                         TurretStats(-43,22,pi/3,4*pi/3, True),
                         TurretStats(-43,-22,2*pi/3,5*pi/3, True)], 
                        3000, 3000, 1000, 500, 0.6*config.fps, 2500, [ids.F_HUMAN_FS_2], [ids.F_LARGE_0, ids.F_LARGE_1], [(70,pi)] )


        self.HUMAN_BASE =	Flagship( ids.S_HUMAN_BASE, 45, 0, 0, 0.002, 800, 1000,
                        [ TurretStats(25,i*pi*2/6, i*pi*2/6-pi/3,i*pi*2/6+pi/3, True, asAngle=True) for i in xrange( 6 ) ],
                        1000, 1000, 500, 100000, 0.2*config.fps, 1000, None, [ids.F_LARGE_0, ids.F_LARGE_1], [] )
        self.HUMAN_BASE_MINING =	Flagship( ids.S_HUMAN_BASE_MINING, 70, 0, 0, 0.002, 800, 1000,
                        [ TurretStats(48,i*pi/2, i*pi/2-2*pi/3,i*pi/2+2*pi/3, True, asAngle=True) for i in xrange( 4 ) ],
                        2000, 5000, 1000, 100000, 0.4*config.fps, 5000, None, [ids.F_LARGE_0, ids.F_LARGE_1], [], 
                        hangars=[ (RPos( i*pi/2, 20 ), i*pi/2 ) for i in xrange( 4 ) ] )

         ## Nomad
        self.NOMAD_FIGHTER =	SingleWeaponShipStats( ids.S_NOMAD_FIGHTER, 15, 0.6, 0, 0.012, 20, 20, self.W_MASS_SR_FIGHTER, [ids.S_NOMAD_FIGHTER], None, [(15,pi)], energyCostToBuild=0,oreCostToBuild=120,timeToBuild=15*config.fps,hangarSpaceNeed=14 )

        self.NOMAD_FS_0 =	Flagship( ids.S_NOMAD_FS_0, 80, 0.09, 0.05, 0.001, 350, 500,
                        [TurretStats(102, 20, 5*pi/3,pi, True),
                         TurretStats(102,-26, 13*pi/13,pi/3, True),
                         TurretStats(-100,20, 0,4*pi/3, True),
                         TurretStats(-100,-20, 2*pi/3,2*pi, True),
                         ],
                         3000, 3000, 800, 500, 1*config.fps, 2500, [ids.S_NOMAD_FS_0], [ids.F_LARGE_0, ids.F_LARGE_1], [(80,pi)], civilianBonus=1500 ) 
        self.NOMAD_FS_1 =	Flagship( ids.S_NOMAD_FS_1, 100, 0.08, 0.05, 0.002, 300, 500, 
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
                        3000, 3000, 300, 500, 0.8*config.fps, 2500, [ids.S_NOMAD_FS_1], [ids.F_LARGE_0, ids.F_LARGE_1], [(80,pi)],
                        hangars=[(RPos(0, 0 ), pi/2), (RPos(0, 0 ), 3*pi/2)], civilianBonus=2000 )
        self.NOMAD_FS_2 =	Flagship( ids.S_NOMAD_FS_2, 70, 0.08, 0.05, 0.002, 400, 500, 
                        [TurretStats(8,21,0,pi, True),
                         TurretStats(8,-21,pi,2*pi, True),
                         TurretStats(-43,22,pi/3,4*pi/3, True),
                         TurretStats(-43,-22,2*pi/3,5*pi/3, True)], 
                        3000, 3000, 1000, 500, 0.6*config.fps, 2500, [ids.S_NOMAD_FS_2], [ids.F_LARGE_0, ids.F_LARGE_1], [(70,pi)], civilianBonus=2000 )
        self.NOMAD_BASE =	Flagship( ids.S_NOMAD_BASE, 45, 0, 0, 0.002, 800, 1000,
                        [ TurretStats(25,i*pi*2/6, i*pi*2/6-pi/3,i*pi*2/6+pi/3, True, asAngle=True) for i in xrange( 6 ) ],
                        1000, 1000, 1000, 100000, 0.2*config.fps, 1000, None, [ids.F_LARGE_0, ids.F_LARGE_1], [] )


         ## self.AIs
        self.AI_FIGHTER =	SingleWeaponShipStats( ids.S_AI_FIGHTER, 8, 0.6, 0, 0.012, 20, 20, self.W_LASER_SR, [ids.S_AI_FIGHTER], None, [(8,pi)], [RPos(8,0)], energyCostToBuild=0,oreCostToBuild=70,timeToBuild=10*config.fps,hangarSpaceNeed=3 )
        self.AI_BOMBER =	SingleWeaponShipStats( ids.S_AI_BOMBER, 8, 0.6, 0, 0.012, 20, 20, self.W_AI_MISSILE, [ids.S_AI_BOMBER], None, [(8,pi)], energyCostToBuild=0,oreCostToBuild=200,timeToBuild=20*config.fps,hangarSpaceNeed=10 )

        self.AI_BASE =	Flagship( ids.S_AI_BASE, 100, 0, 0, 0.002, 400, 1500,
                        [ TurretStats(75,(i*pi*2/3)%(2*pi), (i*pi*2/3-pi*3/4)%(2*pi), (i*pi*2/3+pi*3/4)%(2*pi), True, asAngle=True) for i in xrange( 3 ) ] + \
                        [ TurretStats(15,(i*pi*2/3+pi/3)%(2*pi), (i*pi*2/3)%(2*pi), (i*pi*2/3+2*pi/3)%(2*pi), True, asAngle=True) for i in xrange( 3 ) ],
                        1000, 1000, 1000, 100000, 0.5*config.fps, 1000, None, [ids.F_AI_0], [],
                        [ (RPos(0, 0 ), i*2*pi/3+pi/3) for i in xrange( 3 ) ] )
        self.AI_FS_0 =	Flagship( ids.S_AI_FS_0, 100, 0, 0, 0.002, 300, 800,
                        [ TurretStats(75, (i*pi*2/3)%(2*pi), (i*pi*2/3-pi*3/4)%(2*pi), (i*pi*2/3+pi*3/4)%(2*pi), True, asAngle=True) for i in xrange( 3 ) ] + \
                        [ TurretStats(15, (i*pi*2/3+pi/3)%(2*pi), (i*pi*2/3)%(2*pi), (i*pi*2/3+2*pi/3)%(2*pi), True, asAngle=True) for i in xrange( 3 ) ],
                        1000, 1000, 300, 100, 0.4*config.fps, 1000, None, [ids.F_AI_0], [],
                        [ (RPos(0, 0 ), i*2*pi/3+pi/3) for i in xrange( 3 ) ],
                        jumpChargeDelay=3*config.fps, jumpRecoverDelay=1*config.fps, civilianBonus=500 )
        self.AI_FS_1 =	Flagship( ids.S_AI_FS_1, 100, 0, 0, 0.002, 400, 800,
                        [ TurretStats(75,(i*pi*2/3)%(2*pi), (i*pi*2/3-pi*3/4)%(2*pi), (i*pi*2/3+pi*3/4)%(2*pi), True, asAngle=True) for i in xrange( 3 ) ] + \
                        [ TurretStats(15,(i*pi*2/3+pi/3)%(2*pi), (i*pi*2/3)%(2*pi), (i*pi*2/3+2*pi/3)%(2*pi), True, asAngle=True) for i in xrange( 3 ) ], 
                        1000, 1000, 400, 500, 0.5*config.fps, 1000, None, [ids.F_AI_0], [],
                        [ (RPos(0, 0 ), i*2*pi/3+pi/3) for i in xrange( 3 ) ],
                        jumpChargeDelay=3*config.fps, jumpRecoverDelay=1*config.fps, civilianBonus=500 )
        self.AI_FS_2 =	Flagship( ids.S_AI_FS_2, 100, 0.1, 0.045, 0.002, 500, 800,
                        [ TurretStats(75, (i*pi*2/3)%(2*pi), (i*pi*2/3-pi*3/4)%(2*pi), (i*pi*2/3+pi*3/4)%(2*pi), True, asAngle=True) for i in xrange( 3 ) ] + \
                        [ TurretStats(15, (i*pi*2/3+pi/3)%(2*pi), (i*pi*2/3)%(2*pi), (i*pi*2/3+2*pi/3)%(2*pi), True, asAngle=True) for i in xrange( 3 ) ],
                        1000, 1000, 800, 500, 0.3*config.fps, 1000, None, [ids.F_AI_0], [],
                        [ (RPos(0, 0 ), i*2*pi/3+pi/3) for i in xrange( 3 ) ], civilianBonus=500 )

         ## self.EVOLVED
        self.EVOLVED_FIGHTER =	SingleWeaponShipStats( ids.S_EVOLVED_FIGHTER, 8, 0.6, 0, 0.012, 20, 20, self.W_LASER_SR, [ids.S_EVOLVED_FIGHTER], None, [(8,pi)], weaponPositions=[[RPos(0.3,12), RPos(-0.3,12)]], energyCostToBuild=0,oreCostToBuild=150,timeToBuild=15*config.fps,hangarSpaceNeed=15 )
        self.EVOLVED_BOMBER =	SingleWeaponShipStats( ids.S_EVOLVED_BOMBER, 8, 0.6, 0, 0.012, 20, 20, self.W_ESPHERE_0, [ids.S_EVOLVED_BOMBER], None, [(8,pi)], weaponPositions=[[RPos(0,15)]], energyCostToBuild=0,oreCostToBuild=300,timeToBuild=20*config.fps,hangarSpaceNeed=25 ) 

          # id,radius,maxThrust,maxReverseThrust,maxRg,maxHull,maxShield,turrets, maxEnergy, maxOre, hangarSpace, jumpEnergyCost, launchDelay,radarRange,unavoidableFragments, fragments, engines
        self.EVOLVED_FS_0 =  Flagship( ids.S_EVOLVED_FS_0, 125, 0.1, 0.05, 0.001, 300, 800, 
                        [TurretStats(84, 33, 19*pi/12,11*pi/12, True),
                         TurretStats(84,-33, 13*pi/12,5*pi/12, True),
                         TurretStats(-80,46, pi/12,5*pi/4, True),
                         TurretStats(-80,-46,3*pi/4,23*pi/12, True)], 
                        3000, 3000, 400, 500, 0.8*config.fps, 2500, None, [ids.F_LARGE_0, ids.F_LARGE_1], [(70,pi)], civilianBonus=2000 )
        self.EVOLVED_FS_1 =  Flagship( ids.S_EVOLVED_FS_1, 140, 0.1, 0.04, 0.001, 200, 1000, 
                        [TurretStats(102,-7, pi*3/2,pi/4, True),
                         TurretStats(83,43, pi*20/12,pi*11/12, True),
                         TurretStats(43,43, pi/12,pi*11/12, True),
                         TurretStats(57,-48, 13*pi/12,pi*2/12, True),
                         TurretStats(19,-48, 13*pi/12,pi*23/12, True)], 
                        3000, 3000, 900, 500, 0.6*config.fps, 2500, None, [ids.F_LARGE_0, ids.F_LARGE_1], [(70,pi)],
                        hangars=[(RPos(-0.14, 44 ), pi/2), (RPos(-0.14, 44 ), pi/-2), (RPos(-0.07, 85 ), pi/2), (RPos(-0.07, 85 ), pi/-2), ], civilianBonus=2000 )
        self.EVOLVED_FS_2 =  Flagship( ids.S_EVOLVED_FS_2, 140, 0.11, 0.04, 0.001, 200, 1200, 
                        [TurretStats(89,36, pi*17/12,pi*5/12, True),
                         TurretStats(89,6,  pi*19/12,pi*9/12, True),
                         TurretStats(71,58, pi*13/12,pi*5/12, True),
                         TurretStats(34,58, pi*13/12,pi*4/5, True),
                         TurretStats(57,-33,  pi*21/12,pi*11/12, True),
                         TurretStats(20,-33,  pi/12,pi*11/12, True),
                         TurretStats(-29,77,pi*11/12,pi/12, True),
                         TurretStats(-11,-47, pi/12,pi*11/12, True),
                         TurretStats(-43,-52, pi/12,pi*13/12, True) ], 
                        3000, 3000, 250, 500, 0.5*config.fps, 2500, None, [ids.F_LARGE_0, ids.F_LARGE_1], [(70,pi)],
                        hangars=[(RPos(-0.14, 44 ), pi/2), (RPos(-0.14, 44 ), pi/-2), (RPos(-0.07, 85 ), pi/2), (RPos(-0.07, 85 ), pi/-2), ] )

         ## self.EXTRAs
        self.EXTRA_BASE =  Flagship( ids.S_EXTRA_BASE, 70, 0, 0, 0.002, 1000, 0,  # self.Asteroid
                        [TurretStats(12,i*pi*2/3, i*pi*2/3-pi*3/4,i*pi*2/3+pi*3/4, True, asAngle=True) for i in xrange( 3 )], 
                        3000, 3000, 400, 500, 0.7*config.fps, 500, [ ids.S_EXTRA_BASE ], None, [(70,pi)] ) # TODO
        self.EXTRA_FS_1 =  Flagship( ids.S_EXTRA_FS_1, 70, 0.1, 0.02, 0.004, 2000, 0, # dragon
                        [TurretStats(52,i*pi/12-pi/12, i*pi/12-pi/12-pi/3,i*pi/12-pi/12+pi/3, True, asAngle=True) for i in xrange( 3 )], 
                        3000, 3000, 500, 500, 0.6*config.fps, 750, [ ids.S_EXTRA_FS_1 ], None, [(70,pi)] ) # TODO
        self.EXTRA_FS_2 =  Flagship( ids.S_EXTRA_FS_2, 70, 0.1, 0.02, 0.003, 2000, 0, # dead flagship
                        [TurretStats(30,i*pi*2/4, i*pi*2/4-pi*3/4,i*pi*2/4+pi*3/4, True, asAngle=True) for i in xrange( 4 )], 
                        3000, 3000, 200, 500, 0.5*config.fps, 750, [ ids.S_EXTRA_FS_2 ], None, [(70,pi)] ) # TODO

        self.EXTRA_BASE =  Flagship( ids.S_EXTRA_BASE, 70, 0.08, 0.02, 0.002, 1000, 0,  # self.Asteroid
                        [TurretStats(12,i*pi*2/3, i*pi*2/3-pi*3/4,i*pi*2/3+pi*3/4, True, asAngle=True) for i in xrange( 3 )], 
                        3000, 3000, 400, 500, 0.7*config.fps, 500, [ ids.S_EXTRA_BASE ], None, [(70,pi)] ) # TODO
        self.EXTRA_FIGHTER =	SingleWeaponShipStats( ids.S_EXTRA_FIGHTER, 10, 0.6, 0, 0.012, 20, 20, self.W_EXTRA_FIGHTER, [ids.S_EXTRA_FIGHTER], None, [(8,pi)], weaponPositions=[[RPos(0,12)]], energyCostToBuild=0,oreCostToBuild=70,timeToBuild=10*config.fps,hangarSpaceNeed=3 ) # TODO
        self.EXTRA_BOMBER =	SingleWeaponShipStats( ids.S_EXTRA_BOMBER, 8, 0.6, 0, 0.012, 20, 20, self.W_EXTRA_BOMBER, [ids.S_EXTRA_BOMBER], None, [(8,pi)], weaponPositions=[[RPos(0,0)]], energyCostToBuild=0,oreCostToBuild=200,timeToBuild=20*config.fps,hangarSpaceNeed=12 ) # TODO

         ## neutrals
        self.CIVILIAN_0 = 	CivilianShipStats( ids.S_CIVILIAN_0, 32, 0.1, 0.05, 0.002, 50, 100, 500, None, [ids.F_LARGE_0], [(32,pi)] )
        self.MINE = ObjectStats( ids.S_MINE, 2 ) 


        ### turrets
        # type,energyCostToBuild,oreCostToBuild,timeToBuild, energyPerFrame,orePerFrame, energyPerUse,orePerUse, freqOfFire,turretSpeed, ai, weapon=None,weaponPositions=None, special=None
        self.T_LASER_SR_0 = 	TurretInstallStats( ids.T_LASER_SR_0, 0,75,5*config.fps, 0,0, 1,0, 0.3*config.fps,0.05, ids.TA_COMBAT_ROTATING, weapon=self.W_LASER_SR,weaponPositions=[[RPos(0,11)]] )
        self.T_LASER_SR_1 = 	TurretInstallStats( ids.T_LASER_SR_1, 0,75,5*config.fps, 0,0, 1,0, 0.3*config.fps,0.05, ids.TA_COMBAT_ROTATING, weapon=self.W_LASER_SR,weaponPositions=[[RPos(0.5,11),RPos(-0.5,11)]], upgradeFrom=self.T_LASER_SR_0 )
        self.T_LASER_MR_0 = 	TurretInstallStats( ids.T_LASER_MR_0, 0,250,10*config.fps, 0,0, 0.5,0, 1*config.fps,0.012, ids.TA_COMBAT_ROTATING, weapon=self.W_LASER_MR_0,weaponPositions=[[RPos(0,10)]] )
        self.T_LASER_MR_1 = 	TurretInstallStats( ids.T_LASER_MR_1, 0,750,10*config.fps, 0,0, 0.5,0, 1*config.fps,0.012, ids.TA_COMBAT_ROTATING, weapon=self.W_LASER_MR_1,weaponPositions=[[RPos(0,10)]], upgradeFrom=self.T_LASER_MR_0 )

        self.T_MASS_SR_0 = 	TurretInstallStats( ids.T_MASS_SR_0, 0,100,5*config.fps, 0,0, 0,1, 0.2*config.fps,0.05, ids.TA_COMBAT_ROTATING, weapon=self.W_MASS_SR_0,weaponPositions=[[RPos(0,15)]] )
        self.T_MASS_SR_1 = 	TurretInstallStats( ids.T_MASS_SR_1, 0,100,15*config.fps, 0,0, 0,1, 0.2*config.fps,0.05, ids.TA_COMBAT_ROTATING, weapon=self.W_MASS_SR_0,weaponPositions=[[RPos(0.18,15)],[RPos(-0.18,15)]], upgradeFrom=self.T_MASS_SR_0 ) # [RPos(0.2,15), RPos(-0.2,15)]
        self.T_MASS_SR_2 = 	TurretInstallStats( ids.T_MASS_SR_2, 0,100,45*config.fps, 0,0, 0,1, 0.2*config.fps,0.05, ids.TA_COMBAT_ROTATING, weapon=self.W_MASS_SR_0,weaponPositions=[[RPos(0.25,15)],[RPos(0,15)],[RPos(-0.25,15)]], upgradeFrom=self.T_MASS_SR_1 ) # [RPos(0.2,15), RPos(0,15), RPos(-0.2,15)]
        self.T_MASS_MR_0 = 	TurretInstallStats( ids.T_MASS_MR_0, 0,200,10*config.fps, 0,0, 0,1, 0.8*config.fps,0.02, ids.TA_COMBAT_ROTATING, weapon=self.W_MASS_MR,weaponPositions=[[RPos(0,22)]] )
        self.T_MASS_MR_1 = 	TurretInstallStats( ids.T_MASS_MR_1, 0,200,10*config.fps, 0,0, 0,1, 0.8*config.fps,0.02, ids.TA_COMBAT_ROTATING, weapon=self.W_MASS_MR,weaponPositions=[[RPos(0.3,22)],[RPos(-0.3,22)]], upgradeFrom=self.T_MASS_MR_0 )
        self.T_MASS_LR = 	TurretInstallStats( ids.T_MASS_LR, 0,700,30*config.fps, 0,0, 0,1, 2*config.fps,0.01, ids.TA_COMBAT_ROTATING, weapon=self.W_MASS_LR,weaponPositions=[[RPos(0,11)]], upgradeFrom=self.T_MASS_MR_0 )

        self.T_MISSILE_0 = 	TurretInstallStats( ids.T_MISSILES_0, 0,100,15*config.fps, 0,0, 0,0, 0.5*config.fps,0, ids.TA_COMBAT_STABLE, weapon=self.W_MISSILE,weaponPositions=[[RPos(0,10)]] )
        self.T_MISSILE_1 = 	TurretInstallStats( ids.T_MISSILES_1, 0,350,60*config.fps, 0,0, 0,0, 0.5*config.fps,0, ids.TA_COMBAT_STABLE, weapon=self.W_MISSILE,weaponPositions=[[RPos(0.5,10),RPos(-0.5,10)]], upgradeFrom=self.T_MISSILE_0 )
        self.T_MISSILE_2 = 	TurretInstallStats( ids.T_MISSILES_2, 0,1200,180*config.fps, 0,0, 0,0, 0.5*config.fps,0, ids.TA_COMBAT_STABLE, weapon=self.W_MISSILE,weaponPositions=[[RPos(0.5,10),RPos(0,10),RPos(-0.5,10)]], upgradeFrom=self.T_MISSILE_1 )

        self.T_INTERDICTOR = TurretInstallStats( ids.T_INTERDICTOR, 0,500,45*config.fps, 1,0, 0,0, 0.5*config.fps,0, None, special=ids.S_INTERDICTOR, specialValue=750 ) # special value: interdictor range
        self.T_RADAR = TurretInstallStats( ids.T_RADAR, 0,200,30*config.fps, 0.05,0, 0,0, 0.5*config.fps,0.1, ids.TA_ROTATING, special=ids.S_RADAR, specialValue=2000 ) # special value: radar range self.Boost
        self.T_NUKE = TurretInstallStats( ids.T_NUKE, 0,500,30*config.fps, 0,0, 0,0, 0.5*config.fps,0, ids.TA_MISSILE_SPECIAL, weapon=self.W_MISSILE_NUKE,weaponPositions=[[RPos(0,10)]], special=ids.S_NUKE, specialValue=400 ) # explosion range
        self.T_PULSE = TurretInstallStats( ids.T_PULSE, 0,250,30*config.fps, 0,0, 0,0, 0.5*config.fps,0, ids.TA_MISSILE_SPECIAL, weapon=self.W_MISSILE_PULSE,weaponPositions=[[RPos(0,10)]], special=ids.S_PULSE, specialValue=200 ) # range
        self.T_MINER = TurretInstallStats( ids.T_MINER, 0,200,30*config.fps, 0,0, 0,0, 0.5*config.fps,0, ids.TA_MISSILE_SPECIAL, weapon=self.W_MISSILE_MINER,weaponPositions=[[RPos(0,10)]], special=ids.S_MINER, specialValue=(60,10,30) ) # explosion range, nbr mines, mines exp range
        self.T_COUNTER = TurretInstallStats( ids.T_COUNTER, 0,150,30*config.fps, 0,0, 0,0, 0.5*config.fps,0, ids.TA_MISSILE_SPECIAL, weapon=self.W_MISSILE_COUNTER,weaponPositions=[[RPos(0,10)]], special=ids.S_COUNTER, specialValue=200 ) # effect range
        self.T_GENERATOR = TurretInstallStats( ids.T_GENERATOR, 0,200,30*config.fps, -0.2,0.2, 0,0, 0.5*config.fps,0.2,  ids.TA_ROTATING, special=ids.S_REACTOR, specialValue=750 ) # specialValue=selfDestructRange
        self.T_SOLAR_0 = TurretInstallStats( ids.T_SOLAR_0, 0,100,20*config.fps, 0.05,0, 0,0, 0.5*config.fps,0.008, ids.TA_SOLAR, solar=3 ) # specialValue=solar self.Boost
        self.T_SOLAR_1 = TurretInstallStats( ids.T_SOLAR_1, 0,500,60*config.fps, 0.05,0, 0,0, 0.5*config.fps,0.008, ids.TA_SOLAR, solar=6, upgradeFrom=self.T_SOLAR_0 ) # specialValue=solar self.Boost
        self.T_SOLAR_2 = TurretInstallStats( ids.T_SOLAR_2, 0,1200,120*config.fps, 0.05,0, 0,0, 0.5*config.fps,0.008, ids.TA_SOLAR, solar=12, upgradeFrom=self.T_SOLAR_1 ) # specialValue=solar self.Boost
        self.T_HANGAR = TurretInstallStats( ids.T_HANGAR, 0,300,30*config.fps, 0,0, 0,0, 0.5*config.fps,0, None, special=ids.S_HANGAR, specialValue=150 ) # specialValue=space self.Boost
        self.T_BIOSPHERE = TurretInstallStats( ids.T_BIOSPHERE, 0,250,20*config.fps, 0,0, 0,0, 0.5*config.fps,0, None, special=ids.S_CIVILIAN, specialValue=500 ) # specialValue=civilian self.Boost, / 1000
        self.T_BIOSPHERE_1 = TurretInstallStats( ids.T_BIOSPHERE_1, 0,500,40*config.fps, 0,0, 0,0, 0.5*config.fps,0, None, special=ids.S_CIVILIAN, specialValue=2000, upgradeFrom=self.T_BIOSPHERE ) # specialValue=civilian self.Boost, / 1000
        self.T_SUCKER = TurretInstallStats( ids.T_SUCKER, 0,150,20*config.fps, 0,0, 0,0, 0.5*config.fps,0, None, special=ids.S_SUCKER, specialValue=2 ) # specialValue=ore/(fps/3) frame when in nebula
        self.T_INERTIA = TurretInstallStats( ids.T_INERTIA, 0,500,40*config.fps, 0.2,0, 0,0, 0.5*config.fps,0.2,  ids.TA_ROTATING, special=ids.S_INERTIA, specialValue=1.05 ) # specialValue=inertia mod, WARNING must not go over 1.1!
        self.T_SAIL_0 = TurretInstallStats( ids.T_SAIL_0, 0,300,20*config.fps, 0,0, 0,0, 0.5*config.fps,0.01,  ids.TA_SOLAR, special=ids.S_SAIL, specialValue=1 ) # specialValue= + thrust self.Boost
        self.T_SAIL_1 = TurretInstallStats( ids.T_SAIL_1, 0,600,20*config.fps, 0,0, 0,0, 0.5*config.fps,0.01,  ids.TA_SOLAR, upgradeFrom=self.T_SAIL_0, special=ids.S_SAIL, specialValue=2 ) # specialValue= + thrust self.Boost
        self.T_SAIL_2 = TurretInstallStats( ids.T_SAIL_2, 0,1000,20*config.fps, 0,0, 0,0, 0.5*config.fps,0.01,  ids.TA_SOLAR, upgradeFrom=self.T_SAIL_1, special=ids.S_SAIL, specialValue=3 ) # specialValue= + thrust self.Boost
        self.T_JAMMER = TurretInstallStats( ids.T_JAMMER, 0,300,40*config.fps, 0.3,0, 0,0, 0.5*config.fps,0.2,  None, special=ids.S_JAMMER, specialValue=300 ) # specialValue= range
        self.T_SCANNER = TurretInstallStats( ids.T_SCANNER, 0,300,40*config.fps, 0.3,0, 0,0, 0.5*config.fps,0.2,  ids.TA_TARGET, special=ids.S_SCANNER, specialValue=1000 ) # specialValue= range

        self.T_HARVESTER = 	TurretInstallStats( ids.T_HARVESTER, 0, 70, 3*config.fps, 1,0, 0,0, 0.5*config.fps,0.05, ids.TA_HARVESTER, special=ids.S_MINE )
        self.T_SPOTLIGHT = 	TurretInstallStats( ids.T_SPOTLIGHT, 0, 70, 3*config.fps, 1,0, 0,0, 0.5*config.fps,0.08, ids.TA_HARVESTER, special=ids.S_MINE )
        self.T_RED_SPOTLIGHT = 	TurretInstallStats( ids.T_RED_SPOTLIGHT, 0, 70, 3*config.fps, 1,0, 0,0, 0.5*config.fps,0.2, ids.TA_HARVESTER, special=ids.S_MINE )

        self.HARVESTER =		HarvesterShipStats( ids.S_HARVESTER, 11, 0.2, 0.1, 0.008, 30, 15, [TurretStats(0,0, 0, 0, False)], 50, [ids.S_HARVESTER], None, [(11,pi)], self.T_HARVESTER, 600, energyCostToBuild=0,oreCostToBuild=100,timeToBuild=10*config.fps,hangarSpaceNeed=10 )
        self.NOMAD_HARVESTER =		HarvesterShipStats( ids.S_NOMAD_HARVESTER, 11, 0.15, 0.1, 0.006, 30, 15, [TurretStats(7,0, 0, 0, False), TurretStats(-7,0, 0, 0, False)], 60, [ids.S_HARVESTER], None, [(11,pi)], self.T_SPOTLIGHT, 600, energyCostToBuild=0,oreCostToBuild=75,timeToBuild=8*config.fps,hangarSpaceNeed=6 )
        self.NOMAD_HARVESTER_1 =		HarvesterShipStats( ids.S_NOMAD_HARVESTER_1, 11, 0.15, 0.1, 0.005, 30, 15, [TurretStats(12,0, 0, 0, False), TurretStats(0,0, 0, 0, False), TurretStats(-12,0, 0, 0, False)], 120, [ids.S_HARVESTER], None, [(14,pi)], self.T_SPOTLIGHT, 900, energyCostToBuild=0,oreCostToBuild=150,timeToBuild=16*config.fps,hangarSpaceNeed=10 )
        self.EVOLVED_HARVESTER =	HarvesterShipStats( ids.S_EVOLVED_HARVESTER, 11, 0.3, 0.2, 0.02, 30, 15, [TurretStats(4,0, 0, 0, False)], 35, [ids.S_HARVESTER], None, [(11,pi)], self.T_SPOTLIGHT, 400, energyCostToBuild=0,oreCostToBuild=75,timeToBuild=8*config.fps,hangarSpaceNeed=7 )
        self.AI_HARVESTER =		HarvesterShipStats( ids.S_AI_HARVESTER, 11, 0.15, 0.1, 0.006, 30, 15, [TurretStats(7,0, 0, 0, False), TurretStats(-7,0, 0, 0, False)], 70, [ids.S_HARVESTER], None, [(11,pi)], self.T_SPOTLIGHT, 950, energyCostToBuild=0,oreCostToBuild=150,timeToBuild=15*config.fps,hangarSpaceNeed=15 ) # TODO I fear that over 1000, harvesters the ship could easily get lost due to logic in self.AI.AiPilot.goTo
        self.EXTRA_HARVESTER =	HarvesterShipStats( ids.S_EXTRA_HARVESTER, 11, 0.35, 0.1, 0.009, 30, 15, [TurretStats(12,0, 0, 0, False)], 30, [ids.S_HARVESTER], None, [(11,pi)], self.T_RED_SPOTLIGHT, 600, energyCostToBuild=0,oreCostToBuild=75,timeToBuild=8*config.fps,hangarSpaceNeed=7 )

        # self.EXTRAs'
        self.T_ROCK_THROWER_0 = 	TurretInstallStats( ids.T_ROCK_THROWER_0, 0,100,5*config.fps, 0,0, 0,1, 0.2*config.fps,0.05, ids.TA_COMBAT_ROTATING, weapon=self.W_ROCK_THROWER_0,weaponPositions=[[RPos(0,0)]] )
        self.T_ROCK_THROWER_1 = 	TurretInstallStats( ids.T_ROCK_THROWER_1, 0,400,5*config.fps, 0,0, 0,3, 0.2*config.fps,0.05, ids.TA_COMBAT_ROTATING, weapon=self.W_ROCK_THROWER_1,weaponPositions=[[RPos(0,0)]] )
        self.T_DRAGON_0 = 	TurretInstallStats( ids.T_DRAGON_0, 0,100,5*config.fps, 0,0, 0,1, 0.2*config.fps,0.05, ids.TA_COMBAT_ROTATING, weapon=self.W_DRAGON_0,weaponPositions=[[RPos(0,30)]] )
        self.T_LARVA_0 = 	TurretInstallStats( ids.T_LARVA_0, 0,100,15*config.fps, 0,0, 0,0, 0.5*config.fps,0, ids.TA_COMBAT_STABLE, weapon=self.W_LARVA_0,weaponPositions=[[RPos(0,0)]] )

        # self.AIs'
        self.T_AI_FLAK_0 = 	TurretInstallStats( ids.T_AI_FLAK_0, 0,50,5*config.fps, 0,0, 0,1, 0.2*config.fps,0.05, ids.TA_COMBAT_ROTATING, weapon=self.W_MASS_SR_0, weaponPositions=[[RPos(0.2,18)]] )
        self.T_AI_FLAK_1 = 	TurretInstallStats( ids.T_AI_FLAK_1, 0,150,5*config.fps, 0,0, 0,1, 0.2*config.fps,0.05, ids.TA_COMBAT_ROTATING, weapon=self.W_MASS_SR_0, weaponPositions=[[RPos(-0.2,18),RPos(0.2,18)]], upgradeFrom=self.T_AI_FLAK_0 )
        self.T_AI_FLAK_2 = 	TurretInstallStats( ids.T_AI_FLAK_2, 0,500,5*config.fps, 0,0, 0,1, 0.2*config.fps,0.05, ids.TA_COMBAT_ROTATING, weapon=self.W_MASS_SR_0, weaponPositions=[[RPos(-0.2,18),RPos(0.2,18),RPos(0.52,21)]], upgradeFrom=self.T_AI_FLAK_1 )
        self.T_AI_FLAK_3 = 	TurretInstallStats( ids.T_AI_FLAK_3, 0,1000,5*config.fps, 0,0, 0,1, 0.2*config.fps,0.05, ids.TA_COMBAT_ROTATING, weapon=self.W_MASS_SR_0, weaponPositions=[[RPos(-0.2,18),RPos(0.2,18),RPos(-0.52,21),RPos(0.52,21)]], upgradeFrom=self.T_AI_FLAK_2 )

        self.T_AI_OMNI_LASER_0 =       TurretInstallStats( ids.T_AI_OMNI_LASER_0, 0,200,10*config.fps, 0,0, 2,0, 1, 0, ids.TA_COMBAT_STABLE, weapon=self.W_OMNI_LASER_0,weaponPositions=[[RPos(0,0)]] )
        self.T_AI_OMNI_LASER_1 =       TurretInstallStats( ids.T_AI_OMNI_LASER_1, 0,500,10*config.fps, 0,0, 2,0, 1, 0, ids.TA_COMBAT_STABLE, weapon=self.W_OMNI_LASER_0,weaponPositions=[[RPos(pi/2,7),RPos(3*pi/2,7)]],upgradeFrom=self.T_AI_OMNI_LASER_0 )

        self.T_AI_MISSILE_0 = 	TurretInstallStats( ids.T_AI_MISSILE_0, 0,200,15*config.fps, 0,0, 0,0, 0.5*config.fps,0, ids.TA_COMBAT_STABLE, weapon=self.W_AI_MISSILE, weaponPositions=[[RPos(0.15,30)]] )
        self.T_AI_MISSILE_1 = 	TurretInstallStats( ids.T_AI_MISSILE_1, 0,400,15*config.fps, 0,0, 0,0, 0.5*config.fps,0, ids.TA_COMBAT_STABLE, weapon=self.W_AI_MISSILE, weaponPositions=[[RPos(0.15,30),RPos(-0.3,28)]], upgradeFrom=self.T_AI_MISSILE_0 )
        self.T_AI_MISSILE_2 = 	TurretInstallStats( ids.T_AI_MISSILE_2, 0,750,15*config.fps, 0,0, 0,0, 0.5*config.fps,0, ids.TA_COMBAT_STABLE, weapon=self.W_AI_MISSILE, weaponPositions=[[RPos(0.15,30),RPos(-0.3,28),RPos(-0.15,30)]], upgradeFrom=self.T_AI_MISSILE_1 )
        self.T_AI_MISSILE_3 = 	TurretInstallStats( ids.T_AI_MISSILE_3, 0,1500,15*config.fps, 0,0, 0,0, 0.5*config.fps,0, ids.TA_COMBAT_STABLE, weapon=self.W_AI_MISSILE, weaponPositions=[[RPos(0.15,30),RPos(-0.3,28),RPos(-0.15,30),RPos(0.3,28)]], upgradeFrom=self.T_AI_MISSILE_2 )

        # self.EVOLVED's
        self.T_ESPHERE_0 =       TurretInstallStats( ids.T_ESPHERE_0, 0,100,10*config.fps, 0,0, 2,0, 0.5*config.fps, 0.05, ids.TA_COMBAT_ROTATING, weapon=self.W_ESPHERE_0,weaponPositions=[[RPos(0,0)]] )
        self.T_ESPHERE_1 =       TurretInstallStats( ids.T_ESPHERE_1, 0,100,30*config.fps, 0,0, 2,0, 0.5*config.fps, 0.05, ids.TA_COMBAT_ROTATING, weapon=self.W_ESPHERE_0,weaponPositions=[[RPos(0,0),RPos(0,14)]], upgradeFrom=self.T_ESPHERE_0 )
        self.T_ESPHERE_2 =       TurretInstallStats( ids.T_ESPHERE_2, 0,100,60*config.fps, 0,0, 2,0, 0.5*config.fps, 0.05, ids.TA_COMBAT_ROTATING, weapon=self.W_ESPHERE_0,weaponPositions=[[RPos(0,0),RPos(0,14),RPos(0,25)]], upgradeFrom=self.T_ESPHERE_1 )
        self.T_BURST_LASER_0 =       TurretInstallStats( ids.T_BURST_LASER_0, 0,100,10*config.fps, 0,0, 2,0, 0.5*config.fps, 0.05, ids.TA_COMBAT_ROTATING, weapon=self.W_BURST_LASER_0,weaponPositions=[[RPos(0,5)]] )
        self.T_BURST_LASER_1 =       TurretInstallStats( ids.T_BURST_LASER_1, 0,100,10*config.fps, 0,0, 2,0, 0.35*config.fps, 0.05, ids.TA_COMBAT_ROTATING, weapon=self.W_BURST_LASER_0,weaponPositions=[[RPos(0,5)]],upgradeFrom=self.T_BURST_LASER_0 )
        self.T_BURST_LASER_2 =       TurretInstallStats( ids.T_BURST_LASER_2, 0,100,10*config.fps, 0,0, 2,0, 0.20*config.fps, 0.05, ids.TA_COMBAT_ROTATING, weapon=self.W_BURST_LASER_0,weaponPositions=[[RPos(0,5)]],upgradeFrom=self.T_BURST_LASER_1 )
        self.T_OMNI_LASER_0 =       TurretInstallStats( ids.T_OMNI_LASER_0, 0,100,10*config.fps, 0,0, 2,0, 1, 0, ids.TA_COMBAT_STABLE, weapon=self.W_OMNI_LASER_0,weaponPositions=[[RPos(0,0)]] )
        self.T_OMNI_LASER_1 =       TurretInstallStats( ids.T_OMNI_LASER_1, 0,100,10*config.fps, 0,0, 2,0, 1, 0, ids.TA_COMBAT_STABLE, weapon=self.W_OMNI_LASER_1,weaponPositions=[[RPos(0,0)]],upgradeFrom=self.T_OMNI_LASER_0 )
        self.T_OMNI_LASER_2 =       TurretInstallStats( ids.T_OMNI_LASER_2, 0,100,10*config.fps, 0,0, 2,0, 1, 0, ids.TA_COMBAT_STABLE, weapon=self.W_OMNI_LASER_2,weaponPositions=[[RPos(0,0)]],upgradeFrom=self.T_OMNI_LASER_1 )
        self.T_SUBSPACE_WAVE_0 =       TurretInstallStats( ids.T_SUBSPACE_WAVE_0, 0,100,10*config.fps, 0,0, 2,0, 0.5*config.fps, 0.05, ids.TA_COMBAT_ROTATING, weapon=self.W_SUBSPACE_WAVE_0,weaponPositions=[[RPos(0,5)]] )
        self.T_SUBSPACE_WAVE_1 =       TurretInstallStats( ids.T_SUBSPACE_WAVE_1, 0,100,10*config.fps, 0,0, 2,0, 0.5*config.fps, 0.05, ids.TA_COMBAT_ROTATING, weapon=self.W_SUBSPACE_WAVE_1,weaponPositions=[[RPos(0,5)]],upgradeFrom=self.T_SUBSPACE_WAVE_0 )

        self.T_DARK_EXTRACTOR_0 = TurretInstallStats( ids.T_DARK_EXTRACTOR_0, 0,100,20*config.fps, 0.05,0, 0,0, 0.5*config.fps,0, None, darkExtractor=1 )
        self.T_DARK_EXTRACTOR_1 = TurretInstallStats( ids.T_DARK_EXTRACTOR_1, 0,100,20*config.fps, 0.1,0, 0,0, 0.5*config.fps,0, None, upgradeFrom=self.T_DARK_EXTRACTOR_0, darkExtractor=2 )
        self.T_DARK_ENGINE_0 = TurretInstallStats( ids.T_DARK_ENGINE_0, 0,100,20*config.fps, 0.1,0, 0,0, 0.5*config.fps,0, ids.TA_SOLAR, darkEngine=10, darkExtractor=0.2 )
        
        self.T_EVOLVED_MISSILE_0 = 	TurretInstallStats( ids.T_EVOLVED_MISSILE_0, 0,200,15*config.fps, 0,0, 0,0, 0.5*config.fps,0, ids.TA_COMBAT_STABLE, weapon=self.W_EVOLVED_MISSILE, weaponPositions=[[RPos(0,0)]] )
        self.T_EVOLVED_MISSILE_1 = 	TurretInstallStats( ids.T_EVOLVED_MISSILE_1, 0,400,15*config.fps, 0,0, 0,0, 0.5*config.fps,0, ids.TA_COMBAT_STABLE, weapon=self.W_EVOLVED_MISSILE, weaponPositions=[[RPos(pi/2,10),RPos(3*pi/2,10)]], upgradeFrom=self.T_EVOLVED_MISSILE_0 )
        self.T_EVOLVED_PULSE = TurretInstallStats( ids.T_EVOLVED_PULSE, 0,250,30*config.fps, 0,0, 0,0, 0.5*config.fps,0, ids.TA_MISSILE_SPECIAL, weapon=self.W_EVOLVED_PULSE,weaponPositions=[[RPos(0,0)]], special=ids.S_PULSE, specialValue=200 ) # range
        self.T_EVOLVED_COUNTER = TurretInstallStats( ids.T_EVOLVED_COUNTER, 0,150,30*config.fps, 0,0, 0,0, 0.5*config.fps,0, ids.TA_MISSILE_SPECIAL, weapon=self.W_EVOLVED_COUNTER,weaponPositions=[[RPos(0,0)]], special=ids.S_COUNTER, specialValue=200 ) # effect range
        
        # Nomad's
        self.T_DISCHARGER_0 = 	TurretInstallStats( ids.T_DISCHARGER_0, 0,250,10*config.fps, 0,0, 0.5,0, 1*config.fps,0.01, ids.TA_COMBAT_ROTATING, weapon=self.W_DISCHARGER_0,weaponPositions=[[RPos(0,33)]] )
        self.T_DISCHARGER_1 = 	TurretInstallStats( ids.T_DISCHARGER_1, 0,250,10*config.fps, 0,0, 0.5,0, 1 *config.fps,0.015, ids.TA_COMBAT_ROTATING, weapon=self.W_DISCHARGER_1,weaponPositions=[[RPos(0,33)]],upgradeFrom=self.T_DISCHARGER_0 )

        self.T_REPEATER_0 = 	TurretInstallStats( ids.T_REPEATER_0, 0,100,5*config.fps, 0,0, 0,1, 0.2*config.fps,0.05, ids.TA_COMBAT_ROTATING, weapon=self.W_MASS_SR_0,weaponPositions=[[RPos(0,15)]] )
        self.T_REPEATER_1 = 	TurretInstallStats( ids.T_REPEATER_1, 0,100,15*config.fps, 0,0, 0,1, 0.2*config.fps,0.05, ids.TA_COMBAT_ROTATING, weapon=self.W_MASS_SR_0,weaponPositions=[[RPos(0.2,15), RPos(-0.2,15)]], upgradeFrom=self.T_REPEATER_0 )
        self.T_REPEATER_2 = 	TurretInstallStats( ids.T_REPEATER_2, 0,100,45*config.fps, 0,0, 0,1, 0.2*config.fps,0.05, ids.TA_COMBAT_ROTATING, weapon=self.W_MASS_SR_0,weaponPositions=[[RPos(0.3,15), RPos(0,15), RPos(-0.3,15)]], upgradeFrom=self.T_REPEATER_1 )
        self.T_REPEATER_3 = 	TurretInstallStats( ids.T_REPEATER_3, 0,100,45*config.fps, 0,0, 0,1, 0.2*config.fps,0.05, ids.TA_COMBAT_ROTATING, weapon=self.W_MASS_SR_0,weaponPositions=[[RPos(0.4,15), RPos(0.2,15), RPos(-0.2,15), RPos(-0.4,15) ]], upgradeFrom=self.T_REPEATER_2 )

        self.T_NOMAD_CANNON_0 = 	TurretInstallStats( ids.T_NOMAD_CANNON_0, 0,200,10*config.fps, 0,0, 0,1, 0.8*config.fps,0.02, ids.TA_COMBAT_ROTATING, weapon=self.W_MASS_MR,weaponPositions=[[RPos(0,22)]] )
        self.T_NOMAD_CANNON_1 = 	TurretInstallStats( ids.T_NOMAD_CANNON_1, 0,200,10*config.fps, 0,0, 0,1, 0.8*config.fps,0.02, ids.TA_COMBAT_ROTATING, weapon=self.W_MASS_MR,weaponPositions=[[RPos(0.3,22),RPos(-0.3,22)]], upgradeFrom=self.T_NOMAD_CANNON_0 )
        self.T_NOMAD_CANNON_2 = 	TurretInstallStats( ids.T_NOMAD_CANNON_2, 0,200,10*config.fps, 0,0, 0,1, 0.8*config.fps,0.02, ids.TA_COMBAT_ROTATING, weapon=self.W_MASS_MR,weaponPositions=[[RPos(0.3,22),RPos(-0.3,22)]], upgradeFrom=self.T_NOMAD_CANNON_1 )

        self.T_NOMAD_MISSILE_0 = 	TurretInstallStats( ids.T_NOMAD_MISSILE_0, 0,100,15*config.fps, 0,0, 0,0, 0.5*config.fps,0, ids.TA_COMBAT_STABLE, weapon=self.W_MISSILE,weaponPositions=[[RPos(0,10)]] )
        self.T_NOMAD_MISSILE_1 = 	TurretInstallStats( ids.T_NOMAD_MISSILE_1, 0,350,60*config.fps, 0,0, 0,0, 0.5*config.fps,0, ids.TA_COMBAT_STABLE, weapon=self.W_MISSILE,weaponPositions=[[RPos(0.5,10),RPos(-0.5,10)]], upgradeFrom=self.T_NOMAD_MISSILE_0 )
        
        self.setDefaults()


    def setDefaults( self ):
        print "setting defaults"
        self.R_HUMAN = 	RaceStats( ids.R_HUMAN,
        [self.HUMAN_FS_0, self.HUMAN_FS_1, self.HUMAN_FS_2 ], 
        [ids.M_NORMAL, ids.M_NUKE, ids.M_PULSE, ids.M_MINER, ids.M_COUNTER ], 
        [self.HARVESTER, self.HUMAN_FIGHTER, self.HUMAN_BOMBER ], 
        [self.T_LASER_SR_1, self.T_LASER_SR_0, self.T_LASER_MR_1, self.T_LASER_MR_0,
        self.T_MASS_SR_2, self.T_MASS_SR_1, self.T_MASS_SR_0, self.T_MASS_LR, self.T_MASS_MR_1, self.T_MASS_MR_0,
        self.T_MISSILE_2, self.T_MISSILE_1, self.T_MISSILE_0, 
        self.T_NUKE, self.T_PULSE, self.T_MINER,
        self.T_COUNTER, self.T_INTERDICTOR, self.T_RADAR, self.T_GENERATOR, self.T_SOLAR_2, self.T_SOLAR_1, self.T_SOLAR_0, self.T_HANGAR, self.T_BIOSPHERE_1, self.T_BIOSPHERE, self.T_INERTIA, self.T_SUCKER, self.T_SAIL_2, self.T_SAIL_1, self.T_SAIL_0, self.T_JAMMER ],
        self.HARVESTER ) # WARNING turret upgrades must self.Be self.Before their parent, see game.py:updatePlayer turrets section

        self.R_AI = 		RaceStats( ids.R_AI, 
        [], 
        [ids.M_NUKE, ids.M_MINER, ids.M_COUNTER, ids.M_AI], 
        [self.AI_HARVESTER, self.AI_FIGHTER, self.AI_BOMBER],
        [#T_LASER_SR_1, self.T_LASER_SR_0, self.T_LASER_MR_1, self.T_LASER_MR_0,
        #T_MASS_SR_2, self.T_MASS_SR_1, self.T_MASS_SR_0, self.T_MASS_LR, self.T_MASS_MR_1, self.T_MASS_MR_0,
        self.T_AI_FLAK_0, self.T_AI_FLAK_1, self.T_AI_FLAK_2, self.T_AI_FLAK_3, 
        self.T_AI_OMNI_LASER_1, self.T_AI_OMNI_LASER_0,
        self.T_AI_MISSILE_3, self.T_AI_MISSILE_2, self.T_AI_MISSILE_1, self.T_AI_MISSILE_0,
        self.T_NUKE, self.T_MINER,
        self.T_COUNTER, self.T_INTERDICTOR, self.T_RADAR, self.T_GENERATOR, self.T_SOLAR_2, self.T_SOLAR_1, self.T_SOLAR_0, self.T_HANGAR, self.T_BIOSPHERE_1, self.T_BIOSPHERE, self.T_INERTIA, self.T_SUCKER, self.T_SAIL_2, self.T_SAIL_1, self.T_SAIL_0, self.T_JAMMER ],
        self.AI_HARVESTER )

        self.R_NOMAD = 	RaceStats( ids.R_NOMAD, 
        [self.HUMAN_FS_0, self.HUMAN_FS_1, self.HUMAN_FS_2 ], 
        [ids.M_NORMAL, ids.M_NUKE, ids.M_PULSE, ids.M_MINER, ids.M_COUNTER ], 
        [self.NOMAD_HARVESTER, self.NOMAD_HARVESTER_1, self.NOMAD_FIGHTER ], 
        [self.T_REPEATER_3, self.T_REPEATER_2, self.T_REPEATER_1, self.T_REPEATER_0, 
        self.T_NOMAD_CANNON_2, self.T_NOMAD_CANNON_1, self.T_NOMAD_CANNON_0,
        self.T_NOMAD_MISSILE_1, self.T_NOMAD_MISSILE_0,
        self.T_NUKE, self.T_PULSE,
        self.T_COUNTER, self.T_INTERDICTOR, self.T_RADAR, self.T_GENERATOR, self.T_SOLAR_2, self.T_SOLAR_1, self.T_SOLAR_0, self.T_HANGAR, self.T_BIOSPHERE_1, self.T_BIOSPHERE, self.T_INERTIA, self.T_SUCKER, self.T_SAIL_2, self.T_SAIL_1, self.T_SAIL_0, self.T_JAMMER,
        self.T_DISCHARGER_1, self.T_DISCHARGER_0 ],
        self.NOMAD_HARVESTER  )

        self.R_EXTRA = 	RaceStats( ids.R_EXTRA, 
        [], 
        [ids.M_LARVA], 
        [self.EXTRA_HARVESTER, self.EXTRA_FIGHTER, self.EXTRA_BOMBER], 
        [],
        self.EXTRA_HARVESTER )

        self.R_EVOLVED = 	RaceStats( ids.R_EVOLVED, 
        [], 
        [ids.M_EVOLVED, ids.M_EVOLVED_PULSE, ids.M_MINER, ids.M_EVOLVED_COUNTER ], 
        [self.EVOLVED_HARVESTER, self.EVOLVED_FIGHTER, self.EVOLVED_BOMBER],
        [self.T_EVOLVED_PULSE, self.T_MINER, self.T_EVOLVED_COUNTER, 
        self.T_INTERDICTOR, self.T_RADAR, self.T_SOLAR_2, self.T_SOLAR_1, self.T_SOLAR_0, self.T_HANGAR, self.T_BIOSPHERE_1, self.T_BIOSPHERE, self.T_INERTIA, self.T_SAIL_2, self.T_SAIL_1, self.T_SAIL_0, self.T_JAMMER,
        self.T_ESPHERE_2, self.T_ESPHERE_1, self.T_ESPHERE_0,
        self.T_BURST_LASER_2, self.T_BURST_LASER_1, self.T_BURST_LASER_0,
        self.T_OMNI_LASER_2, self.T_OMNI_LASER_1, self.T_OMNI_LASER_0,
        self.T_SUBSPACE_WAVE_0, self.T_SUBSPACE_WAVE_1,
        self.T_EVOLVED_MISSILE_1, self.T_EVOLVED_MISSILE_0, 
        self.T_DARK_EXTRACTOR_0, self.T_DARK_EXTRACTOR_1, self.T_DARK_ENGINE_0 ],
        self.EVOLVED_HARVESTER )
        
        self.Relations = { 
    self.R_HUMAN: 	{ self.R_HUMAN: 100, self.R_AI: 30, self.R_NOMAD: 30, self.R_EXTRA: -50, self.R_EVOLVED: 10 },
    self.R_AI: 	    { self.R_HUMAN: 10, self.R_AI: 40, self.R_NOMAD: 10, self.R_EXTRA: 10, self.R_EVOLVED: 10 },
    self.R_NOMAD: 	{ self.R_HUMAN: 30, self.R_AI: 10, self.R_NOMAD: 50, self.R_EXTRA: 5, self.R_EVOLVED: 75 },
    self.R_EXTRA: 	{ self.R_HUMAN: -50, self.R_AI: 10, self.R_NOMAD: -50, self.R_EXTRA: 20, self.R_EVOLVED: -50 },
    self.R_EVOLVED: { self.R_HUMAN: 25, self.R_AI: -20, self.R_NOMAD: 75, self.R_EXTRA: -50 , self.R_EVOLVED: 100 } }

        self.PlayableShips = { ids.S_HUMAN_FS_0: ShipChoice( self.HUMAN_FS_0, self.R_HUMAN, 0 ), 
                      ids.S_HUMAN_FS_1: ShipChoice( self.HUMAN_FS_1, self.R_HUMAN, 350 ), 
                      ids.S_HUMAN_FS_2: ShipChoice( self.HUMAN_FS_2, self.R_HUMAN, 400 ),

                      ids.S_EVOLVED_FS_0: ShipChoice( self.EVOLVED_FS_0, self.R_EVOLVED, 0 ),
                      ids.S_EVOLVED_FS_1: ShipChoice( self.EVOLVED_FS_1, self.R_EVOLVED, 200 ),
                      ids.S_EVOLVED_FS_2: ShipChoice( self.EVOLVED_FS_2, self.R_EVOLVED, 500 ),

                      ids.S_AI_FS_0: ShipChoice( self.AI_FS_0, self.R_AI, 0 ),
                      ids.S_AI_FS_1: ShipChoice( self.AI_FS_1, self.R_AI, 300 ),
                      ids.S_AI_FS_2: ShipChoice( self.AI_FS_2, self.R_AI, 650 ),

                      ids.S_NOMAD_FS_0: ShipChoice( self.NOMAD_FS_0, self.R_NOMAD, 0 ),
                      ids.S_NOMAD_FS_1: ShipChoice( self.NOMAD_FS_1, self.R_NOMAD, 200 ),
                      ids.S_NOMAD_FS_2: ShipChoice( self.NOMAD_FS_2, self.R_NOMAD, 500 ) }
        
        # Contains every interesting item indexed self.By their id
        self.statsDict = {}
        for k, v in self.__dict__.items():
            if isinstance( v, ObjectStats ):
                self.statsDict[ v.img ] = v
            if isinstance( v, TurretInstallStats ):
                self.statsDict[ v.type ] = v

    def __getitem__( self, i):
        return self.statsDict[ i ]
    def __setitem__( self, i, v ):
        self.statsDict = v
        
#if not globals().has_key( "stats" ):
#    stats = Stats()
#    stats.setDefaults()

