# coding=UTF-8

from . import Language

class Fr( Language ):
    name = "fr" # class name must be = to name.capitalize()
    title = u"Français" # full language name
    author = u"Author" # translator name
    
    def __init__( self ):
        Language.__init__( self )
        
        self.texts = {
        
"Created by %s": u"",
"Some pictures courtesy NASA": u"",
        
"Loading images": u"",
"Loading sounds": u"",
"Loading preferences": u"",
"Loading screens": u"",
"Done": u"",

"Your name": u"",
"Your password": u"",
"Server address": u"",
"Server port": u"",
"Connect": u"",
"Back to main menu": u"",
"Admin password": u"",
"Server adresses seperated by spaces": u"",
"Play": u"",
"Previous scenario": u"",
"Next scenario": u"",
"Cancel": u"",
"Load": u"",

"Race: %s": u"",
"Ship class: %s": u"",
"%i turrets": u"",
"Equipped for faster than light jump": u"",

"Hangar size": u"",
"Shield": u"",
"Hull": u"",
"Civilian appreciation": u"",
"Speed": u"",
        
"ore cost: %(ore)i\nenergy cost: %(energy)i\ntime to build: %(time).1fs\n\n%(description)s": u"",
    
"e %i": u"é %i",
"ore %i": u"mat. %i",

"Ok": u"",
"Main menu": u"",
"Next": u"",
"Prev": u"",

"Quick play": u"",
"Load a game": u"",
"Select a scenario": u"",
"Join a game": u"",
"Select a campaign": u"",
"Host a game": u"",
"Options": u"",
"Quit": u"",

        
"Laser defense": u"",
"Short range laser canon.": u"",
"Laser defense x2": u"",
"Short range double laser canon.": u"",
"Medium laser": u"",
"Medium range laser canon.": u"",
"Heavy laser": u"",
"Medium range powerful laser canon.": u"",

"Machine gun": u"",
"Machine gun x2": u"",
"Machine gun x3": u"",
"Mass cannon": u"",
"Mass cannon x2": u"",
"Mass driver": u"",

"Missile launcher": u"",
"Missile launcher x2": u"",
"Missile launcher x3": u"",

"?": u"",
"Jump interdictor": u"",
"When activated, prevents ships within its range to jump away.": u"",
"Nuclear launcher": u"",
"Allows the building and launch of nuclear missiles.": u"",
"Pulse launcher": u"",
"Allows the building and launch of pulse missiles.": u"",
"Radar": u"",
"When activated, add to the ship's radar range.": u"",
"Hangar": u"",
"Adds hangar space to the ship. Allowing it to carry more fighters and missiles.": u"",
"Solar panel": u"",
"When activated, will harvest more energy from nearby suns but will consume a little to operate.": u"",
"Large solar panel": u"",
"Huge solar panel": u"",
"Nuclear reactor": u"",
"When activated, will convert ore to energy.": u"",
"Mine layer": u"",
"Allows the building and launch of mine layer missiles.": u"",
"Counter defense": u"",
"Allows the building and launch of counter defense missiles.": u"",
"Bioshpere": u"",
"Increase your reputation with civilian ships. Helps counter the effects of nuclear weapons and bad racial tendencies.": u"",
"Advanced Bioshpere": u"",

"Nebula harvester": u"",
"When activated and in a nebula, will harvest raw ore direcly from the clouds.": u"",
"Jump battery": u"",
"Mass reducer": u"",
"When activated, will reduce the mass of the ship and allow faster manoeuvering.": u"",
"Solar sail": u"",
"When activated, will boost the ship's speed depending on the proximity of a sun.": u"",
"Solar sail x2": u"",
"When activated, will boost the ship's speed depending on the proximity of a sun.": u"",
"Solar sail x3": u"",
"When activated, will boost the ship's speed depending on the proximity of a sun.": u"",
"Missile jammer": u"",

"Flak cannon": u"",
"Flak cannon x2": u"",
"Flak cannon x3": u"",
"Flak cannon x4": u"",
"Omni laser": u"",
"Omni laser x2": u"",
"Missile launcher": u"",
"Missile launcher x2": u"",
"Missile launcher x3": u"",
"Missile launcher x4": u"",
        
"Crypt module": u"",
"When activated, will encrpyt all communications sent from this ship. Other ships will need crypt modules themselves to decrypt your messages.": u"",
"Crypt module x2": u"",
"Crypt module x3": u"",
"Crypt module x4": u"",
        
"Active defense": u"",
"When activated, will automaticly fire counter defenses at incoming projectiles to enhance the shield resistance to mass attack.": u"",
        
"E-Sphere launcher": u"",
"E-Sphere launcher v2": u"",
"E-Sphere launcher v3": u"",
"Burst laser": u"",
"Burst laser v2": u"",
"Burst laser v3": u"",
"Omnidirectional laser": u"",
"Omnidirectional laser v2": u"",
"Omnidirectional laser v3": u"",
"Subspace percuter": u"",
"Subspace percuter v2": u"",
"Dark-matter extractor": u"",
"When activated, will extract energy from surrounding dark matter. Dark matter is stronger when in deep space, away from stars": u"",
"Dark-matter extractor v2": u"",
"Dark-matter engine": u"",
"When activated, will drain surrounding dark matter to provide a speed boost. Dark matter is stronger when in deep space, away from stars.": u"",
        
"Missile launcher": u"",
"Double missile launcher": u"",
"Pulse sphere launcher": u"",
"Counter sphere launcher": u"",
"Particle shield": u"",
"When activated, will enhance the shield resistance against mass projectiles.": u"",

"Discharger": u"",
"Heavy discharger": u"",
"Repeater": u"",
"Repeater 2x": u"",
"Repeater 3x": u"",
"Repeater 4x": u"",
"Canon": u"",
"Canon 2x": u"",
"Canon 3x": u"",
"Missile launcher": u"",
"Missile launcher 2x": u"",
"Nebula harvester": u"",
"Nebula harvester 2x": u"",
"Nebula harvester 3x": u"",

"Hull electrifier": u"",
"When activated, electrifies the ship's hull to better absorb energy attacks.": u"",

"Weapons": u"",
"Missiles": u"",
"Others": u"",


"Frigate": u"",
"Battleship": u"",
"Carrier": u"",

"Transport Ship t-5": u"",
"Colony Ship c-0": u"",
"Colony Ship c-2": u"",

"Model 4b6-0": u"",
"Model 4b6-1": u"",
"Model 4c1-2": u"",

"Deep Space Farming Ship": u"",
"Deep Space Carrier": u"",
"Deep Space Defense Ship": u"",

"Earth humans": u"",
"Artificial intelligences": u"",
"Nomad groups": u"",
"Hostile extra-terrestrials": u"",
"Evolved humans": u"",
        
        }
        
