from ais import *
from weapons import *

class Turret:
    def __init__( self, stats ): # the stats duplicates the stats from ship, the turret install's stats are in install.stats
        self.stats = stats
        self.install = None
        self.weapon = None
        self.ai = None
        self.rr = (self.stats.maxAngle+self.stats.minAngle)/2   
                                                          
    def buildInstall( self, turretStats ): 
        self.weapon = None
        if turretStats.weapon:
            if turretStats.weapon.weaponType == ids.WT_MASS:
                self.weapon = MassWeaponTurret( turretStats.weapon )
            elif turretStats.weapon.weaponType == ids.WT_OMNI_LASER:
                self.weapon = OmniLaserWeaponTurret( turretStats.weapon )
            elif turretStats.weapon.weaponType == ids.WT_LASER:
                self.weapon = LaserWeaponTurret( turretStats.weapon )
            elif turretStats.weapon.weaponType == ids.WT_MISSILE:
                self.weapon = MissileWeaponTurret( turretStats.weapon )
            elif turretStats.weapon.weaponType == ids.WT_MISSILE_SPECIAL:
                self.weapon = SpecialMissileWeaponTurret( turretStats.weapon )

        self.ai = None
        if turretStats.ai:
            if turretStats.ai == ids.TA_COMBAT_STABLE:
                self.ai = AiWeaponTurretStable()
            elif turretStats.ai == ids.TA_COMBAT_ROTATING:
                self.ai = AiWeaponTurret()
            elif turretStats.ai == ids.TA_ROTATING:
                self.ai = AiRotatingTurret()
            elif turretStats.ai == ids.TA_SOLAR:
                self.ai = AiSolarTurret()
            elif turretStats.ai == ids.TA_MISSILE_SPECIAL:
                self.ai = AiSpecialMissileTurret()

        self.install = TurretInstall( turretStats )
        self.activated = True
        self.building = None


class TurretInstall:
    # may be used for advanced civilian turrets
    def __init__( self, stats ):
        self.stats = stats

