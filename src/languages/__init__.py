import os
import sys

from common import ids

languageFiles = filter( 
    lambda f: len( f )>3 and f[-3:]==".py" and f[0]!="_", 
    os.listdir( os.path.join( sys.path[0], "languages" ) ) )
languagesNames = [ n[:-3] for n in languageFiles]
languagesNames.sort()

class Language:
    name = "base"
    title = "Base language"
    author = ""
    reportMissing = False
    
    def __init__( self ):
    
        # varies with language
        self.texts = {}
        
        # default to all, used for transaltion
        self.descriptions = {} # int, str
        self.names = {} # int, str
        self.uis = {} # str, str
        
        self.loadAll()
        
    def getName( self, key ):
        try:
            return self.get( self.names[ key ] )
        except KeyError:
            return ""
        
    def getDescription( self, key ):
        try:
            return self.get( self.descriptions[ key ] )
        except KeyError:
            return ""
        
    def get( self, key ):
        try:
            text = self.texts[ key ]
            if text:
                return text#self.texts[ key ]
            else:
               # if self.reportMissing:
               #     print "language file %s missing \"%s\"" % (self.title,key)
                return key
        except KeyError:
            if self.reportMissing:
                print "language file %s missing \"%s\"" % (self.title,key)
            return key
        
    def __getitem__( self, key ):
        return self.get( key )
                
    def __setitem__( self, key, value ):
        self.texts[ key ] = value
        
    def install( self ):
        # install _() everywhere in the program
        import __builtin__
        __builtin__.__dict__['_'] = self.get

    def loadAll( self ):
        # default (english) texts, simplify use from interface
        self.names[ids.T_LASER_SR_0] 	= "Laser defense"
        self.descriptions[ids.T_LASER_SR_0] = "Short range laser canon."
        self.names[ids.T_LASER_SR_1] 	= "Laser defense x2"
        self.descriptions[ids.T_LASER_SR_1] = "Short range double laser canon."
        self.names[ids.T_LASER_MR_0] 	= "Medium laser"
        self.descriptions[ids.T_LASER_MR_0] = "Medium range laser canon."
        self.names[ids.T_LASER_MR_1] 	= "Heavy laser"
        self.descriptions[ids.T_LASER_MR_1] = "Medium range powerful laser canon."

        self.names[ids.T_MASS_SR_0] 	= "Machine gun"
        self.names[ids.T_MASS_SR_1] 	= "Machine gun x2"
        self.names[ids.T_MASS_SR_2] 	= "Machine gun x3"
        self.names[ids.T_MASS_MR_0] 	= "Mass cannon"
        self.names[ids.T_MASS_MR_1] 	= "Mass cannon x2"
        self.names[ids.T_MASS_LR] 	= "Mass driver"

        self.names[ids.T_MISSILES_0] 	= "Missile launcher"
        self.names[ids.T_MISSILES_1] 	= "Missile launcher x2"
        self.names[ids.T_MISSILES_2] 	= "Missile launcher x3"

        self.names[ids.T_HARVESTER] 	= "?"
        self.names[ids.T_INTERDICTOR] 	= "Jump interdictor"
        self.descriptions[ids.T_INTERDICTOR] = "When activated, prevents ships within its range to jump away."
        self.names[ids.T_NUKE]	 	= "Nuclear launcher"
        self.descriptions[ids.T_NUKE] = "Allows the building and launch of nuclear missiles."
        self.names[ids.T_PULSE] 		= "Pulse launcher"
        self.descriptions[ids.T_PULSE] = "Allows the building and launch of pulse missiles."
        self.names[ids.T_RADAR] 		= "Radar"
        self.descriptions[ids.T_RADAR] = "When activated, add to the ship's radar range."
        self.names[ids.T_HANGAR] 		= "Hangar"
        self.descriptions[ids.T_HANGAR] = "Adds hangar space to the ship. Allowing it to carry more fighters and missiles."
        self.names[ids.T_SOLAR_0] 		= "Solar panel"
        self.descriptions[ids.T_SOLAR_0] = "When activated, will harvest more energy from nearby suns but will consume a little to operate."
        self.names[ids.T_SOLAR_1] 		= "Large solar panel"
        self.descriptions[ids.T_SOLAR_1] = self.descriptions[ids.T_SOLAR_0]
        self.names[ ids.T_SOLAR_2 ] 		= "Huge solar panel"
        self.descriptions[ids.T_SOLAR_2] = self.descriptions[ids.T_SOLAR_0]
        self.names[ids.T_GENERATOR] 		= "Nuclear reactor"
        self.descriptions[ids.T_GENERATOR] = "When activated, will convert ore to energy."
        self.names[ids.T_MINER] 		= "Mine layer"
        self.descriptions[ids.T_MINER] = "Allows the building and launch of mine layer missiles."
        self.names[ids.T_COUNTER] 		= "Counter defense"
        self.descriptions[ids.T_COUNTER] = "Allows the building and launch of counter defense missiles."
        self.names[ids.T_BIOSPHERE] 		= "Bioshpere"
        self.descriptions[ids.T_BIOSPHERE] = "Increase your reputation with civilian ships. Helps counter the effects of nuclear weapons and bad racial tendencies."
        self.names[ ids.T_BIOSPHERE_1 ] 	= "Advanced Bioshpere"
        self.descriptions[ids.T_BIOSPHERE_1] = self.descriptions[ids.T_BIOSPHERE]

        self.names[ ids.T_SUCKER ] 		= "Nebula harvester"
        self.descriptions[ids.T_SUCKER] = "When activated and in a nebula, will harvest raw ore direcly from the clouds."
        self.names[ ids.T_EJUMP ] 		= "Jump battery"
        self.names[ ids.T_INERTIA ] 		= "Mass reducer"
        self.descriptions[ids.T_INERTIA] = "When activated, will reduce the mass of the ship and allow faster manoeuvering."
        self.names[ ids.T_SAIL_0 ] 		= "Solar sail"
        self.descriptions[ids.T_SAIL_0] = "When activated, will boost the ship's speed depending on the proximity of a sun."
        self.names[ ids.T_SAIL_1 ] 		= "Solar sail x2"
        self.descriptions[ids.T_SAIL_1] = "When activated, will boost the ship's speed depending on the proximity of a sun."
        self.names[ ids.T_SAIL_2 ] 		= "Solar sail x3"
        self.descriptions[ids.T_SAIL_2] = "When activated, will boost the ship's speed depending on the proximity of a sun."
        self.names[ ids.T_JAMMER ] 		= "Missile jammer"
        self.names[ ids.T_FRIGATE_BUILDER ] 		= "Frigate builder"

        self.names[ ids.T_AI_FLAK_0 ] = "Flak cannon"
        self.names[ ids.T_AI_FLAK_1 ] = "Flak cannon x2"
        self.names[ ids.T_AI_FLAK_2 ] = "Flak cannon x3"
        self.names[ ids.T_AI_FLAK_3 ] = "Flak cannon x4"
        self.names[ ids.T_AI_OMNI_LASER_0 ] = "Omni laser"
        self.names[ ids.T_AI_OMNI_LASER_1 ] = "Omni laser x2"
        self.names[ ids.T_AI_MISSILE_0 ] = "Missile launcher"
        self.names[ ids.T_AI_MISSILE_1 ] = "Missile launcher x2"
        self.names[ ids.T_AI_MISSILE_2 ] = "Missile launcher x3"
        self.names[ ids.T_AI_MISSILE_3 ] = "Missile launcher x4"
        
        self.names[ ids.T_AI_CRYPT_0 ] = "Crypt module"
        self.descriptions[ids.T_AI_CRYPT_0] = "When activated, will encrpyt all communications sent from this ship. Other ships will need crypt modules themselves to decrypt your messages."
        self.names[ ids.T_AI_CRYPT_1 ] = "Crypt module x2"
        self.descriptions[ids.T_AI_CRYPT_1] = self.descriptions[ids.T_AI_CRYPT_0]
        self.names[ ids.T_AI_CRYPT_2 ] = "Crypt module x3"
        self.descriptions[ids.T_AI_CRYPT_2] = self.descriptions[ids.T_AI_CRYPT_0]
        self.names[ ids.T_AI_CRYPT_3 ] = "Crypt module x4"
        self.descriptions[ids.T_AI_CRYPT_3] = self.descriptions[ids.T_AI_CRYPT_0]
        
        self.names[ ids.T_AI_ACTIVE_DEFENSE_0 ]   = "Active defense"
        self.descriptions[ids.T_AI_ACTIVE_DEFENSE_0] = "When activated, will automaticly fire counter defenses at incoming projectiles to enhance the shield resistance to mass attack."
        
        self.names[ ids.T_ESPHERE_0 ]	        = "E-Sphere launcher"
        self.names[ ids.T_ESPHERE_1 ]	        = "E-Sphere launcher v2"
        self.names[ ids.T_ESPHERE_2 ]	        = "E-Sphere launcher v3"
        self.names[ ids.T_BURST_LASER_0 ]	        = "Burst laser"
        self.names[ ids.T_BURST_LASER_1 ]	        = "Burst laser v2"
        self.names[ ids.T_BURST_LASER_2 ]	        = "Burst laser v3"
        self.names[ ids.T_OMNI_LASER_0 ]	        = "Omnidirectional laser"
        self.names[ ids.T_OMNI_LASER_1 ]	        = "Omnidirectional laser v2"
        self.names[ ids.T_OMNI_LASER_2 ]	        = "Omnidirectional laser v3"
        self.names[ ids.T_SUBSPACE_WAVE_0 ]	        = "Subspace percuter"
        self.names[ ids.T_SUBSPACE_WAVE_1 ]	        = "Subspace percuter v2"
        self.names[ ids.T_DARK_EXTRACTOR_0 ]	        = "Dark-matter extractor"
        self.descriptions[ids.T_DARK_EXTRACTOR_0] = "When activated, will extract energy from surrounding dark matter. Dark matter is stronger when in deep space, away from stars"
        self.names[ ids.T_DARK_EXTRACTOR_1 ]	        = "Dark-matter extractor v2"
        self.descriptions[ids.T_DARK_EXTRACTOR_1] = self.descriptions[ids.T_DARK_EXTRACTOR_0]
        self.names[ ids.T_DARK_ENGINE_0 ]	        = "Dark-matter engine"
        self.descriptions[ids.T_DARK_EXTRACTOR_0] = "When activated, will drain surrounding dark matter to provide a speed boost. Dark matter is stronger when in deep space, away from stars."
        
        self.names[ ids.T_EVOLVED_MISSILE_0 ]     = "Missile launcher"
        self.names[ ids.T_EVOLVED_MISSILE_1 ]     = "Double missile launcher"
        self.names[ ids.T_EVOLVED_PULSE ]         = "Pulse sphere launcher"
        self.names[ ids.T_EVOLVED_COUNTER ]       = "Counter sphere launcher"
        self.names[ ids.T_EVOLVED_PARTICLE_SHIELD_0 ] = "Particle shield"
        self.descriptions[ids.T_EVOLVED_PARTICLE_SHIELD_0] = "When activated, will enhance the shield resistance against mass projectiles."

        self.names[ ids.T_DISCHARGER_0 ]	        = "Discharger"
        self.names[ ids.T_DISCHARGER_1 ]	        = "Heavy discharger"
        self.names[ ids.T_REPEATER_0 ]	        = "Repeater"
        self.names[ ids.T_REPEATER_1 ]	        = "Repeater 2x"
        self.names[ ids.T_REPEATER_2 ]	        = "Repeater 3x"
        self.names[ ids.T_REPEATER_3 ]	        = "Repeater 4x"
        self.names[ ids.T_NOMAD_CANNON_0 ]	        = "Canon"
        self.names[ ids.T_NOMAD_CANNON_1 ]	        = "Canon 2x"
        self.names[ ids.T_NOMAD_CANNON_2 ]	        = "Canon 3x"
        self.names[ ids.T_NOMAD_MISSILE_0 ]	    = "Missile launcher"
        self.names[ ids.T_NOMAD_MISSILE_1 ]	    = "Missile launcher 2x"
        self.names[ ids.T_NOMAD_SUCKER_0 ]	    = "Nebula harvester"
        self.descriptions[ids.T_NOMAD_SUCKER_0] = self.descriptions[ids.T_SUCKER]
        self.names[ ids.T_NOMAD_SUCKER_1 ]	    = "Nebula harvester 2x"
        self.descriptions[ids.T_NOMAD_SUCKER_1] = self.descriptions[ids.T_SUCKER]
        self.names[ ids.T_NOMAD_SUCKER_2 ]	    = "Nebula harvester 3x"
        self.descriptions[ids.T_NOMAD_SUCKER_2] = self.descriptions[ids.T_SUCKER]

        self.names[ ids.T_NOMAD_HULL_ELECTRIFIER_0 ] = "Hull electrifier"
        self.descriptions[ids.T_NOMAD_HULL_ELECTRIFIER_0] = "When activated, electrifies the ship's hull to better absorb energy attacks."

        self.names[ids.C_WEAPON] 		= "Weapons"
        self.names[ids.C_MISSILE]		= "Missiles"
        self.names[ids.C_OTHER] 		= "Others"


        self.names[ids.S_HUMAN_FS_0] 		= "Frigate"
        self.names[ids.S_HUMAN_FS_1] 		= "Battleship"
        self.names[ids.S_HUMAN_FS_2] 		= "Carrier"

        self.names[ids.S_NOMAD_FS_0] 		= "Transport Ship t-5"
        self.names[ids.S_NOMAD_FS_1]	 	= "Colony Ship c-0"
        self.names[ids.S_NOMAD_FS_2] 		= "Colony Ship c-2"

        self.names[ids.S_AI_FS_0] 		= "Model 4b6-0"
        self.names[ids.S_AI_FS_1] 		= "Model 4b6-1"
        self.names[ids.S_AI_FS_2] 		= "Model 4c1-2"

        self.names[ids.S_EVOLVED_FS_0] 	= "Deep Space Farming Ship"
        self.names[ids.S_EVOLVED_FS_1] 	= "Deep Space Carrier"
        self.names[ids.S_EVOLVED_FS_2] 	= "Deep Space Defense Ship"

        self.names[ids.R_HUMAN] 		= "Earth humans"
        self.names[ids.R_AI] 			= "Artificial intelligences"
        self.names[ids.R_NOMAD] 		= "Nomad groups"
        self.names[ids.R_EXTRA] 		= "Hostile extra-terrestrials"
        self.names[ids.R_EVOLVED] 		= "Evolved humans"

        self.uiRaceS		= "Race: %s"
        self.uiShipS		= "Ship class: %s"
        self.uiTurretsI		= "%i turrets"
        self.uiCanJump		= "Equipped for faster than light jump"

        self.uiMaxOre		= "Ore capacity"
        self.uiHangarSize	= "Hangar size"
        self.uiMaxShield	= "Shield"
        self.uiMaxHull		= "Hull"
        self.uiCivilian		= "Civilian appreciation"
        self.uiSpeed		= "Speed"
        
        self.infoBuild = "ore cost: %(ore)i\nenergy cost: %(energy)i\ntime to build: %(time).1fs\n\n%(description)s"
        

