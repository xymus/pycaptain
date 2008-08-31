# coding=UTF-8

from . import Language

class Fr( Language ):
    name = "fr" # class name must be = to name.capitalize()
    title = u"Français"
    author = u"Alexis Laferrière"
    reportMissing = True
    
    def __init__( self ):
        Language.__init__( self )
        
        self.texts = {
        
"Created by %s": u"Créé par %s",
"Some pictures courtesy NASA": u"Certaines photos gracieuseté NASA",
        
"Loading images": u"Chargement des images",
"Loading sounds": u"Chargement des sons",
"Loading preferences": u"Chargement des préférences",
"Loading screens": u"Chargement des fenêtres",
"Done": u"Complété",

"Your name": u"Ton nom",
"Your password": u"Ton mot de passe",
"Server address": u"Adresse du serveur",
"Server port": u"Port du serveur",
"Connect": u"Se connecter",
"Back to main menu": u"Retour au menu",
"Admin password": u"Mot de passe administrateur",
"Server adresses seperated by spaces": u"Adresses dus serveur, séparées par un espace.",
"Play": u"Lancer",
"Previous scenario": u"Scénario précédent",
"Next scenario": u"Scénario suivant",
"Cancel": u"Annuler",
"Load": u"Charger",

"Race: %s": u"Race: %s",
"Ship class: %s": u"Classe: %s",
"%i turrets": u"%i tourelles",
"Equiped for faster than light jump": u"Équippé pour sauts supraluminique",

"Hangar size": u"Taille du hangar",
"Shield": u"Bouclier",
"Hull": u"Coque",
"Civilian appreciation": u"Opinion des civils",
"Speed": u"Vitesse",
        
"ore cost: %(ore)i\nenergy cost: %(energy)i\ntime to build: %(time).1fs\n\n%(description)s": \
    u"Coût en matériaux: %(ore)i\nCoût en énergie: %(energy)i\nTemps pour construire: %(time).1fs\n\n%(description)s",
    
"e %i": u"é %i",
"ore %i": u"mat. %i",

"Ok": u"Ok",
"Main menu": u"Menu principal",
"Next": u"Suivant",
"Prev": u"Précédent",

"Quick play": u"Sauter dans le jeu",
"Load a game": u"Charger une partie",
"Select a scenario": u"Choisir un scénario",
"Join a game": u"Se joindre à une partie",
"Select a campaign": u"Choisir une campagne",
"Host a game": u"Héberger une partie",
"Options": u"Options",
"Quit": u"Quitter",

        
"Laser defense": u"Défense laser",
"Short range laser canon.": u"Canon laser courte portée.",
"Laser defense x2": u"Défense laser x2",
"Short range double laser canon.": u"Canon laser courte portée double.",
"Medium laser": u"Laser moyen",
"Medium range laser canon.": u"Canon laser de portée et force moyenne.",
"Heavy laser": u"Laser lourd",
"Medium range powerful laser canon.": u"Canon laser de portée moyenne et grade froce.",

"Machine gun": u"Mitraillette",
"Machine gun x2": u"Mitraillette x2",
"Machine gun x3": u"Mitraillette x3",
"Mass cannon": u"Canon",
"Mass cannon x2": u"Canon x2",
"Mass driver": u"Conducteur de masse",

"Missile launcher": u"Lance missile",
"Missile launcher x2": u"Lance missile x2",
"Missile launcher x3": u"Lance missile x3",
"Missile launcher x4": u"Lance missile x4",

"?": u"?",
"Jump interdictor": u"Interdicteur de saut",
"When activated, prevents ships within its range to jump away.": u"Lorsque activé, prévient les vaisseaux dans son rayon d'action de sauter à distance.",
"Nuclear launcher": u"Lanceur nucléaire",
"Allows the building and launch of nuclear missiles.": u"Permet la construction et le lancement de missiles nucléaires.",
"Pulse launcher": u"Lanceur d'impulsion",
"Allows the building and launch of pulse missiles.": u"Permet la construction et le lancement de missiles à impulsion.",
"Radar": u"Radar",
"When activated, add to the ship's radar range.": u"Lorsque activé, augmente la portée du radar.",
"Hangar": u"Hangar",
"Adds hangar space to the ship. Allowing it to carry more fighters and missiles.": u"Augmente la capacité du hangar. Permettant au vaisseau d'acceuillir plus de chasseurs et de missiles.",
"Solar panel": u"Panneau solaire",
"When activated, will harvest more energy from nearby suns but will consume a little to operate.": u"Lorsque activé, récolte plus d'énergie solaire des coleils avoisinants mais en consomme un peu pour opérer.",
"Large solar panel": u"Panneau solaire large",
"Huge solar panel": u"Panneau solaire géant",
"Nuclear reactor": u"Réacteur nucléaire",
"When activated, will convert ore to energy.": u"Lorsque activé, convertit matériaux en énergie",
"Mine layer": u"Semeur de mine",
"Allows the building and launch of mine layer missiles.": u"Permet la construction et le lancement de missiles semeur de mine",
"Counter defense": u"Lanceur de détourneur",
"Allows the building and launch of counter defense missiles.": u"Permet la construction et le lancement de missiles détourneur",
"Bioshpere": u"Biosphère",
"Increase your reputation with civilian ships. Helps counter the effects of nuclear weapons and bad racial tendencies.": u"Améliore votre réputation auprès des civils. Aide à contrer l'effect négatif des armes nucléaires et mauvaises tendances raciales.",
"Advanced Bioshpere": u"Biosphère avancée",

"Nebula harvester": u"Ceuilleur de nébuleuse",
"When activated and in a nebula, will harvest raw ore direcly from the clouds.": u"",
"Jump battery": u"",
"Mass reducer": u"Réducteur de masse",
"When activated, will reduce the mass of the ship and allow faster manoeuvering.": u"",
"Solar sail": u"Voile solaire",
"When activated, will boost the ship's speed depending on the proximity of a sun.": u"",
"Solar sail x2": u"Voile solaire x2",
"When activated, will boost the ship's speed depending on the proximity of a sun.": u"",
"Solar sail x3": u"Voile solaire x3",
"When activated, will boost the ship's speed depending on the proximity of a sun.": u"",
"Missile jammer": u"",

"Flak cannon": u"",
"Flak cannon x2": u"",
"Flak cannon x3": u"",
"Flak cannon x4": u"",
"Omni laser": u"",
"Omni laser x2": u"",
        
"Crypt module": u"Module d'encryption",
"When activated, will encrpyt all communications sent from this ship. Other ships will need crypt modules themselves to decrypt your messages.": u"",
"Crypt module x2": u"Module d'encryption x2",
"Crypt module x3": u"Module d'encryption x3",
"Crypt module x4": u"Module d'encryption x4",
        
"Active defense": u"Défense active",
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

"Weapons": u"Armements",
"Missiles": u"Missiles",
"Others": u"Autres",


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

"Earth humans": u"Humains terriens",
"Artificial intelligences": u"Intelligences artificielles",
"Nomad groups": u"Groupes nomades",
"Hostile extra-terrestrials": u"Extra-terrestres hostiles",
"Evolved humans": u"Humains évolués",
        
        }
        
