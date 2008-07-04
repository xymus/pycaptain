from ais import *
from weapons import *
from common.comms import COBuildable
# from players import Human

class Turret:
    def __init__( self, stats, ship ): # the stats duplicates the turret stats from the ship stats, the turret install's stats are in install.stats
        self.stats = stats
        self.ship = ship
        
        self.install = None
        self.weapon = None
        self.ai = None
        
        self.activated = True
        
        self.rr = (self.stats.maxAngle+self.stats.minAngle)/2   
        
class BuildableTurret( Turret ):
    def __init__( self, stats, ship ): # the stats duplicates the turret stats from the ship stats, the turret install's stats are in install.stats
        Turret.__init__( self, stats, ship )
        
        self.building = None
        self.buildCost = 0
        
        self.updateBuildingOptions() # calls self.updateBuildingOptionsPossibles()
                                                          
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
        
        if turretStats.darkEngine: # TODO better than that
            self.rr = pi
        
        self.updateBuildingOptions()

    def updateBuildingOptions( self ):
        if self.ship.player: #  and isinstance( self.ship.player, Human ):
            """To be updated when turret ordered to build, built or destroyed."""
            if self.building:
                self.energyRebate = self.building.energyCostToBuild
                self.oreRebate = self.building.oreCostToBuild
            else:
                self.energyRebate = 0
                self.oreRebate = 0
                
            self.buildingOptions = [o for o in self.ship.player.race.turrets]
            
            if self.install:
                for option in self.install.stats.overs+[self.install.stats]:
                    self.buildingOptions.remove( option )
            elif self.building:
                for option in self.building.overs:
                  if option != self.building.upgradeFrom:
                    self.buildingOptions.remove( option )
                    
            self.updateBuildingOptionsPossibles()
        else:
            self.buildingOptions = []
            
                
    def updateBuildingOptionsPossibles( self ):
        """To be updated when ore and energy changes."""
        self.buildingOptionsPossibles = []
        for bt in self.buildingOptions: 
            if self.install and self.install.stats == bt.upgradeFrom: # upgradable
                self.buildingOptionsPossibles.append( COBuildable( bt.type, self.ship.energy >= bt.energyCostToBuild-self.energyRebate and self.ship.ore >= bt.oreCostToBuild-self.oreRebate))
            elif (self.install and self.install.stats == bt) or (self.building and self.building == bt): # already there
                self.buildingOptionsPossibles.append( COBuildable( bt.type, False ))
            elif not bt.upgradeFrom: # otherwise, not an upgrades
                self.buildingOptionsPossibles.append( COBuildable( bt.type, self.ship.energy >= bt.energyCostToBuild-self.energyRebate and self.ship.ore >= bt.oreCostToBuild-self.oreRebate )) 
                
        if self.building or self.install:
            self.buildingOptionsPossibles.append( COBuildable( 0, True )) 

class TurretInstall:
    # may be used for advanced civilian turrets
    def __init__( self, stats ):
        self.stats = stats

