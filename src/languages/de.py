# coding=UTF-8

from . import Language

class De( Language ):
    name = "de" # class name must be = to name.capitalize()
    title = u"Deutsch"
    author = u"erlehmann"
    reportMissing = True
    
    def __init__( self ):
        Language.__init__( self )
        
        self.texts = {
        
"Created by %s": u"Autor: %s",
"Some pictures courtesy NASA": u"Manche Bilder: NASA",
        
"Loading images": u"Lade Bilder",
"Loading sounds": u"Lade Geräusche",
"Loading preferences": u"Lade Einstellungen",
"Loading screens": u"Lade Bildschirme",
"Done": u"Fertig",

"Your name": u"Dein Name",
"Your password": u"Dein Passwort",
"Server address": u"Serveradresse",
"Server port": u"Serverport",
"Connect": u"Verbinden",
"Back to main menu": u"Zurück zum Hauptmenü",
"Admin password": u"Administratorpasswort",
"Server adresses seperated by spaces": u"Serveradressen, separiert durch Leerzeichen",
"Play": u"Spielen",
"Previous scenario": u"Vorheriges Szenario",
"Next scenario": u"Nächstes Szenario",
"Cancel": u"Abbrechen",
"Load": u"Laden",

"Race: %s": u"Rasse: %s",
"Ship class: %s": u"Schiffsklasse: %s",
"%i turrets": u"%i Geschütztürme",
"Equipped for faster than light jump": u"Ausgestattet für Sprung mit Überlichtgeschwindigkeit",

"Hangar size": u"Hangargröße",
"Shield": u"Schild",
"Hull": u"Hülle:",
"Civilian appreciation": u"Anerkennung durch Zivilisten",
"Speed": u"Geschwindigkeit",
        
"ore cost: %(ore)i\nenergy cost: %(energy)i\ntime to build: %(time).1fs\n\n%(description)s": \
    u"Erzkosten: %(ore)i\nEnergiekosten: %(energy)i\nBauzeit: %(time).1fs\n\n%(description)s",
    
"e %i": u"Energie %i",
"ore %i": u"Erz %i",

"Ok": u"Ok",
"Main menu": u"Hauptmenü",
"Next": u"Weiter",
"Prev": u"Zurück",

"Quick play": u"Sofort spielen",
"Load a game": u"Spiel laden",
"Select a scenario": u"Szenario auswählen",
"Join a game": u"Spiel beitreten",
"Select a campaign": u"Kampagne auswählen",
"Host a game": u"Spiel hosten",
"Options": u"Optionen",
"Quit": u"Beenden",

        
"Laser defense": u"Laser-Verteidigung",
"Short range laser canon.": u"Kurzstrecken-Laserkanone.",
"Laser defense x2": u"Laser-Verteidigung x2",
"Short range double laser canon.": u"Doppelte Kurzstrecken-Laserkanone.",
"Medium laser": u"Mittlerer Laser",
"Medium range laser canon.": u"Mittelstrecken-Laserkanone.",
"Heavy laser": u"Schwerer Laser",
"Medium range powerful laser canon.": u"Starke Mittelstrecken-Laserkanone.",

"Machine gun": u"Maschinengewehr",
"Machine gun x2": u"Maschinengewehr x2",
"Machine gun x3": u"Maschinengewehr x3",
"Mass cannon": u"Geschütz",
"Mass cannon x2": u"Geschütz x2",
"Mass driver": u"Elektromagnetisches Katapult",

"Missile launcher": u"Raketenwerfer",
"Missile launcher x2": u"Raketenwerfer x2",
"Missile launcher x3": u"Raketenwerfer x3",
"Missile launcher x4": u"Raketenwerfer x4",

"?": u"?",
"Jump interdictor": u"Sprung-Verhinderung",
"When activated, prevents ships within its range to jump away.": u"Wenn aktiv, verhindert, dass Schiffe innerhalb der Reichweite wegspringen können.",
"Nuclear launcher": u"Atomraketenwerfer",
"Allows the building and launch of nuclear missiles.": u"Ermöglicht Konstruktion und Start von mit Atomsprengköpfen bestückten Raketen.",
"Pulse launcher": u"Impulswerfer",
"Allows the building and launch of pulse missiles.": u"Ermöglicht Konstruktion und Start von Impulsraketen.",
"Radar": u"Radar",
"When activated, add to the ship's radar range.": u"Wenn aktiv, erhöht die Radar-Reichweite des Schiffes.",
"Hangar": u"Hangar",
"Adds hangar space to the ship. Allowing it to carry more fighters and missiles.": u"Erhöht die Hangarkapazität des Schiffes. Somit können mehr Schiffe und Raketen gelagert werden.",
"Solar panel": u"Solarmodul",
"When activated, will harvest more energy from nearby suns but will consume a little to operate.": u"Wenn aktiv, sammelt Energie von Sonnen von der Nähe, verbraucht aber ein bisschen Energie.",
"Large solar panel": u"Großes Solarmodul",
"Huge solar panel": u"Riesiges Solarmodul",
"Nuclear reactor": u"Kernreaktor",
"When activated, will convert ore to energy.": u"Wenn aktiv, wandelt Erz in Energie um.",
"Mine layer": u"Minenwerfer",
"Allows the building and launch of mine layer missiles.": u"Ermöglicht Konstruktion und Start von Minenleger-Raketen.",
"Counter defense": u"Abwehrraketenwerfer",
"Allows the building and launch of counter defense missiles.": u"Ermöglicht Konstruktion und Start von Abwehrraketen.",
"Bioshpere": u"Biosphäre",
"Increase your reputation with civilian ships. Helps counter the effects of nuclear weapons and bad racial tendencies.": u"Erhöht das Ansehen bei zivilen Schiffen. Hilft gegen die Effekte von Atomwaffen und rassisch bedingten Unsympathien.",
"Advanced Bioshpere": u"Fortgeschrittene Biosphäre",

"Nebula harvester": u"Nebelernter",
"When activated and in a nebula, will harvest raw ore direcly from the clouds.": u"Wenn aktiv und in einem Nebel, erntet Erz direkt aus den Wolken.",
"Jump battery": u"Sprungbatterie",
"Mass reducer": u"Massenreduktor",
"When activated, will reduce the mass of the ship and allow faster manoeuvering.": u"Wenn aktiv, reduziert die Masse des Schiffes und ermöglicht schnellere Manövrierung.",
"Solar sail": u"Solarsegel",
"When activated, will boost the ship's speed depending on the proximity of a sun.": u"Wenn aktiv, erhöht die Geschwindigkeit des Schiffes abhängig von der Nähe zu einer Sonne.",
"Solar sail x2": u"Solarsegel x2",
"When activated, will boost the ship's speed depending on the proximity of a sun.": u"Wenn aktiv, erhöht die Geschwindigkeit des Schiffes abhängig von der Nähe zu einer Sonne.",
"Solar sail x3": u"Solarsegel x3",
"When activated, will boost the ship's speed depending on the proximity of a sun.": u"Wenn aktiv, erhöht die Geschwindigkeit des Schiffes abhängig von der Nähe zu einer Sonne.",
"Missile jammer": u"Raketen-Störsender",

"Flak cannon": u"Flak",
"Flak cannon x2": u"Flak x2",
"Flak cannon x3": u"Flak x3",
"Flak cannon x4": u"Flak x4",
"Omni laser": u"Omni-Laser",
"Omni laser x2": u"Omni-Laser x2",
        
"Crypt module": u"Kryptomodul",
"When activated, will encrpyt all communications sent from this ship. Other ships will need crypt modules themselves to decrypt your messages.": u"Wenn aktiv, verschlüsselt die Kommunikation dieses Schiffs. Andere Schiffe brauchen ebenfalls Kryptomodule um deine Nachrichten zu entschlüsseln.",
"Crypt module x2": u"Kryptomodul x2",
"Crypt module x3": u"Kryptomodul x3",
"Crypt module x4": u"Kryptomodul x4",
        
"Active defense": u"Aktive Verteidigung",
"When activated, will automaticly fire counter defenses at incoming projectiles to enhance the shield resistance to mass attack.": u"Wenn aktiv, feuert automatisch Abwehrraketen auf ankommende Projektile, um die Resistenz gegen massebasierte Angriffe zu erhöhen.",
        
"E-Sphere launcher": u"E-Sphären-Werfer",
"E-Sphere launcher v2": u"E-Sphären-Werfer v2",
"E-Sphere launcher v3": u"E-Sphären-Werfer v3",
"Burst laser": u"Stoßlaser",
"Burst laser v2": u"Stoßlaser v2",
"Burst laser v3": u"Stoßlaser v3",
"Omnidirectional laser": u"Omnidirektionaler Laser",
"Omnidirectional laser v2": u"Omnidirektionaler Laser v2",
"Omnidirectional laser v3": u"Omnidirektionaler Laser v3",
"Subspace percuter": u"Subraum-Zerstörer",
"Subspace percuter v2": u"Subraum-Zerstörer v2",
"Dark-matter extractor": u"Dunkle-Materie-Extraktor",
"When activated, will extract energy from surrounding dark matter. Dark matter is stronger when in deep space, away from stars": u"Wenn aktiv, extrahiert Energie aus umgebender dunkler Materie. Dunkle Materie existiert tief im Raum, weit entfernt von Sternen.",
"Dark-matter extractor v2": u"Extraktor für dunkle Materie v2",
"Dark-matter engine": u"Dunkle-Materie-Antrieb",
"When activated, will drain surrounding dark matter to provide a speed boost. Dark matter is stronger when in deep space, away from stars.": u"Wenn aktiv, produziert verstärkten Schub durch Wechselwirkung mit umgebender dunkler Materie. Dunkle Materie existiert tief im Raum, weit entfernt von Sternen.",
        
"Missile launcher": u"Raketenwerfer",
"Double missile launcher": u"Doppelter Raketenwerfer",
"Pulse sphere launcher": u"Impulssphärenwerfer",
"Counter sphere launcher": u"Abwehrsphärenwerfer",
"Particle shield": u"Partikelschhild",
"When activated, will enhance the shield resistance against mass projectiles.": u"Wenn aktiv, erhöht die Resistenz gegen massebasierte Angriffe.",

"Discharger": u"Entlader",
"Heavy discharger": u"Schwerer Entlader",
"Repeater": u"Verstärker",
"Repeater 2x": u"Verstärker 2x",
"Repeater 3x": u"Verstärker 3x",
"Repeater 4x": u"Verstärker 4x",
"Canon": u"Kanone",
"Canon 2x": u"Kanone 2x",
"Canon 3x": u"Kanone 3x",
"Missile launcher": u"Raketenwerfer",
"Missile launcher 2x": u"Raketenwerfer 2x",
"Nebula harvester": u"Nebelernter",
"Nebula harvester 2x": u"Nebelernter 2x",
"Nebula harvester 3x": u"Nebelernter 3x",

"Hull electrifier": u"Hüllen-Elektrifizierung",
"When activated, electrifies the ship's hull to better absorb energy attacks.": u"Wenn aktiv, elektrifiziert die Schiffshülle, um energiebasierte Angriffe besser zu absorbieren.",

"Weapons": u"Waffen",
"Missiles": u"Raketen",
"Others": u"Andere",


"Frigate": u"Fregatte",
"Battleship": u"Schlachtschiff",
"Carrier": u"Träger",

"Transport Ship t-5": u"Transportschiff t-5",
"Colony Ship c-0": u"Kolonieschiff c-0",
"Colony Ship c-2": u"Kolonieschiff c-2",

"Model 4b6-0": u"Modell 4b6-0",
"Model 4b6-1": u"Modell 4b6-1",
"Model 4c1-2": u"Modell 4b6-2",

"Deep Space Farming Ship": u"Tiefraum-Farmschiff",
"Deep Space Carrier": u"Tiefraum-Träger",
"Deep Space Defense Ship": u"Tiefraum-Verteidigungsschiff",

"Earth humans": u"Erdenmenschen",
"Artificial intelligences": u"Künstliche Intelligenzen",
"Nomad groups": u"Nomadische Gruppen",
"Hostile extra-terrestrials": u"Feindliche Außerirdische",
"Evolved humans": u"Weiterentwickelte Menschen",
        
        }
        
