#!/usr/bin/python

from rc import Rc

from common import ids

class Texts( Rc ):
    def __init__( self ):
        Rc.__init__( self )
        self.createdBy = "created by %s"
        self.courtesyNasa = "Some pictures courtesy NASA"
        self.loadingImages = "Loading images"
        self.loadingSounds = "Loading sounds"
        self.loadingTexts = "Loading texts"
        self.loadingPreferences = "Loading preferences"
        self.loadingScreens = "Loading screens"
        self.loadingDone = "Done"

    def loadAll( self ): # useless with the current system
        yield 0
        self.uiOk	= "Ok"
        self.uiQuit	= "Quit"
        self.uiNext	= "Next"
        self.uiPrev	= "Prev"
        
        self[0] 	= "Destroy"
        self[-1] 	= "Cancel"

        self[ids.T_LASER_SR_0] 	= "Laser defense"
        self[ids.T_LASER_SR_1] 	= "Laser defense x2"
        self[ids.T_LASER_MR_0] 	= "Medium laser"
        self[ids.T_LASER_MR_1] 	= "Heavy laser"

        self[ids.T_MASS_SR_0] 	= "Machine gun"
        self[ids.T_MASS_SR_1] 	= "Machine gun x2"
        self[ids.T_MASS_SR_2] 	= "Machine gun x3"
        self[ids.T_MASS_MR_0] 	= "Mass cannon"
        self[ids.T_MASS_MR_1] 	= "Mass cannon x2"
        self[ids.T_MASS_LR] 	= "Mass driver"

        self[ids.T_MISSILES_0] 	= "Missile launcher"
        self[ids.T_MISSILES_1] 	= "Missile launcher x2"
        self[ids.T_MISSILES_2] 	= "Missile launcher x3"
        yield 33

        self[ids.T_HARVESTER] 	= "?"
        self[ids.T_INTERDICTOR] 	= "Jump interdictor"
        self[ids.T_NUKE]	 	= "Nuclear launcher"
        self[ids.T_PULSE] 		= "Pulse launcher"
        self[ids.T_RADAR] 		= "Radar"
        self[ids.T_HANGAR] 		= "Hangar"
        self[ids.T_SOLAR_0] 		= "Solar array"
        self[ids.T_SOLAR_1] 		= "Large solar array"
        self[ ids.T_SOLAR_2 ] 		= "Huge solar array"
        self[ids.T_GENERATOR] 		= "Nuclear reactor"
        self[ids.T_MINER] 		= "Mine layer"
        self[ids.T_COUNTER] 		= "Counter defense"
        self[ids.T_BIOSPHERE] 		= "Bioshpere"
        self[ ids.T_BIOSPHERE_1 ] 	= "Advanced Bioshpere"
        yield 66

        self[ ids.T_SUCKER ] 		= "Nebula harvester"
        self[ ids.T_EJUMP ] 		= "Jump battery"
        self[ ids.T_INERTIA ] 		= "Mass reducer"
        self[ ids.T_SAIL_0 ] 		= "Solar sail"
        self[ ids.T_SAIL_1 ] 		= "Solar sail x2"
        self[ ids.T_SAIL_2 ] 		= "Solar sail x3"
        self[ ids.T_JAMMER ] 		= "Missile jammer"

        self[ ids.T_AI_FLAK_0 ] = "Flak cannon"
        self[ ids.T_AI_FLAK_1 ] = "Flak cannon x2"
        self[ ids.T_AI_FLAK_2 ] = "Flak cannon x3"
        self[ ids.T_AI_FLAK_3 ] = "Flak cannon x4"
        self[ ids.T_AI_OMNI_LASER_0 ] = "Omni laser"
        self[ ids.T_AI_OMNI_LASER_1 ] = "Omni laser x2"
        self[ ids.T_AI_MISSILE_0 ] = "Missile launcher"
        self[ ids.T_AI_MISSILE_1 ] = "Missile launcher x2"
        self[ ids.T_AI_MISSILE_2 ] = "Missile launcher x3"
        self[ ids.T_AI_MISSILE_3 ] = "Missile launcher x4"
        
        self[ ids.T_AI_CRYPT_0 ] = "Crypt module"
        self[ ids.T_AI_CRYPT_1 ] = "Crypt module x2"
        self[ ids.T_AI_CRYPT_2 ] = "Crypt module x3"
        self[ ids.T_AI_CRYPT_3 ] = "Crypt module x4"
        
        self[ ids.T_AI_ACTIVE_DEFENSE_0 ]   = "Active defense"
        
        self[ ids.T_ESPHERE_0 ]	        = "E-Sphere launcher"
        self[ ids.T_ESPHERE_1 ]	        = "E-Sphere launcher v2"
        self[ ids.T_ESPHERE_2 ]	        = "E-Sphere launcher v3"
        self[ ids.T_BURST_LASER_0 ]	        = "Burst laser"
        self[ ids.T_BURST_LASER_1 ]	        = "Burst laser v2"
        self[ ids.T_BURST_LASER_2 ]	        = "Burst laser v3"
        self[ ids.T_OMNI_LASER_0 ]	        = "Omnidirectional laser"
        self[ ids.T_OMNI_LASER_1 ]	        = "Omnidirectional laser v2"
        self[ ids.T_OMNI_LASER_2 ]	        = "Omnidirectional laser v3"
        self[ ids.T_SUBSPACE_WAVE_0 ]	        = "Subspace percuter"
        self[ ids.T_SUBSPACE_WAVE_1 ]	        = "Subspace percuter v2"
        self[ ids.T_DARK_EXTRACTOR_0 ]	        = "Dark-matter extractor"
        self[ ids.T_DARK_EXTRACTOR_1 ]	        = "Dark-matter extractor v2"
        self[ ids.T_DARK_ENGINE_0 ]	        = "Dark-matter engine"
        
        self[ ids.T_EVOLVED_MISSILE_0 ]     = "Missile launcher"
        self[ ids.T_EVOLVED_MISSILE_1 ]     = "Double missile launcher"
        self[ ids.T_EVOLVED_PULSE ]         = "Pulse sphere launcher"
        self[ ids.T_EVOLVED_COUNTER ]       = "Counter sphere launcher"
        self[ ids.T_EVOLVED_PARTICLE_SHIELD_0 ] = "Particle shield"

        self[ ids.T_DISCHARGER_0 ]	        = "Discharger"
        self[ ids.T_DISCHARGER_1 ]	        = "Heavy discharger"
        self[ ids.T_REPEATER_0 ]	        = "Repeater"
        self[ ids.T_REPEATER_1 ]	        = "Repeater 2x"
        self[ ids.T_REPEATER_2 ]	        = "Repeater 3x"
        self[ ids.T_REPEATER_3 ]	        = "Repeater 4x"
        self[ ids.T_NOMAD_CANNON_0 ]	        = "Canon"
        self[ ids.T_NOMAD_CANNON_1 ]	        = "Canon 2x"
        self[ ids.T_NOMAD_CANNON_2 ]	        = "Canon 3x"
        self[ ids.T_NOMAD_MISSILE_0 ]	    = "Missile launcher"
        self[ ids.T_NOMAD_MISSILE_1 ]	    = "Missile launcher 2x"
        self[ ids.T_NOMAD_SUCKER_0 ]	    = "Nebula harvester"
        self[ ids.T_NOMAD_SUCKER_1 ]	    = "Nebula harvester 2x"
        self[ ids.T_NOMAD_SUCKER_2 ]	    = "Nebula harvester 3x"

        self[ ids.T_NOMAD_HULL_ELECTRIFIER_0 ] = "Hull electrifier"

        self[ids.C_WEAPON] 		= "Weapons"
        self[ids.C_MISSILE]		= "Missiles"
        self[ids.C_OTHER] 		= "Others"


        self[ids.S_HUMAN_FS_0] 		= "Frigate"
        self[ids.S_HUMAN_FS_1] 		= "Battleship"
        self[ids.S_HUMAN_FS_2] 		= "Carrier"

        self[ids.S_NOMAD_FS_0] 		= "Transport Ship t-5"
        self[ids.S_NOMAD_FS_1]	 	= "Colony Ship c-0"
        self[ids.S_NOMAD_FS_2] 		= "Colony Ship c-2"

        self[ids.S_AI_FS_0] 		= "Model 4b6-0"
        self[ids.S_AI_FS_1] 		= "Model 4b6-1"
        self[ids.S_AI_FS_2] 		= "Model 4c1-2"

        self[ids.S_EVOLVED_FS_0] 	= "Deep Space Farming Ship"
        self[ids.S_EVOLVED_FS_1] 	= "Deep Space Carrier"
        self[ids.S_EVOLVED_FS_2] 	= "Deep Space Defense Ship"

        self[ids.R_HUMAN] 		= "Earth humans"
        self[ids.R_AI] 			= "Artificial intelligences"
        self[ids.R_NOMAD] 		= "Nomad groups"
        self[ids.R_EXTRA] 		= "Hostile extra-terrestrials"
        self[ids.R_EVOLVED] 		= "Evolved humans"

        self.uiRaceS		= "Race: %s"
        self.uiShipS		= "Ship class: %s"
        self.uiTurretsI		= "%i turrets"
        self.uiCanJump		= "Equiped for faster than light jump"

        self.uiMaxOre		= "Ore capacity"
        self.uiHangarSize	= "Hangar size"
        self.uiMaxShield	= "Shield"
        self.uiMaxHull		= "Hull"
        self.uiCivilian		= "Civilian appreciation"
        self.uiSpeed		= "Speed"
        
        self.infoBuild = "ore cost: %(ore)i\nenergy cost: %(energy)i\ntime to build: %(time).1fs"

        yield 100


