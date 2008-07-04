from math import pi, sin, cos
from random import randint, random

from scenarios import Scenario, Step
from server.objects import Asteroid, Planet, Sun
from server.ships import *
from server.weapons import *
from server.ais import *
from server.players import Computer, Faction, Territory
from server.stats import Stats

from common import utils

class Tutorial3( Scenario ):
    title = "Tutorial 3 - advanced combat"
    description = "As the commander of the only orbital base around Earth, your mission is to defend yourself from the incoming pirate ships."
    year = 2275
    name = "Tutorial3"
        
    def __init__(self, game, steps=None, name=None, description=None, year=0):
    
        stats = Stats()
        stats.R_HUMAN.turrets = [ stats.T_LASER_SR_1, stats.T_LASER_SR_0, stats.T_LASER_MR_0,
    stats.T_MASS_SR_1, stats.T_MASS_SR_0, stats.T_MASS_LR, stats.T_MASS_MR_0,
    stats.T_MISSILE_1, stats.T_MISSILE_0,
    stats.T_PULSE, stats.T_MINER, 
    stats.T_SOLAR_0,  ]
        stats.R_HUMAN.missiles = [ids.M_NORMAL, ids.M_PULSE, ids.M_MINER]
        stats.R_HUMAN.ships = [ stats.HARVESTER, stats.HUMAN_FIGHTER ]
        stats.PlayableShips = {}
        
        
        steps = []
        
        ### missiles
        steps.append( Step( 
            goal=lambda self, game: filter( lambda turret: turret.install and turret.install.stats==stats.T_MISSILE_0, self.player.flagship.turrets ),
            failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
            onBegin=lambda self, game: self.addEnnemyShip( game, (self.player.flagship.xp+stats.T_MASS_MR_0.weapon.maxRange+100, self.player.flagship.yp), None ),
            texts = [(0,"There's an ennemy ship on the other side of Earth, directly to your right."),
                (config.fps*4, "It is too far away to reach with your current weapons."),
                (config.fps*8, "Select an empty turret, on the right of the screen, and build a missile launcher."),
                (config.fps*16, "It would also be a good idea to begin harvesting the asteroid close by."),
                (config.fps*20, "Build more harvester if you feel that it's necessary." )] ) )
        steps.append( Step( 
            goal=lambda self, game: self.player.flagship.missiles[ids.M_NORMAL].amount >= 10,
            failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
            texts = [(0,"Now that the launcher is ready you will need some missiles!"),
                (config.fps*4, "Click on the missile icon at the botom of the screen to start building them."),
                (config.fps*8, "10 should be enough to initiate the combat.") ] ) )
        steps.append( Step( 
            goal=lambda self, game: not self.ennemyShip.alive,
            failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
            onBegin=lambda self, game: (game.setRelationBetween( self.player, self.ennemy, 1 ), game.setRelationBetween( self.ennemy, self.player, 1 )),
            texts = [(0,"Now attack it!"),
                (config.fps*4, "It is the blue dot on the radar screen, left-click on it to begin the attack." ) ] ) )
            
        ### mass turret / upgrading
        steps.append( Step( 
            goal=lambda self, game: filter( lambda turret: turret.install and turret.install.stats==stats.T_MASS_LR, self.player.flagship.turrets ),
            failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
            onBegin=lambda self, game: self.addEnnemyShip( game, (self.player.flagship.xp+stats.T_MASS_LR.weapon.maxRange-400, self.player.flagship.yp), None ),
            texts = [(0,"One appeared even further away!"),
                (config.fps*4, "Upgrade at least one of your mass cannon to a mass driver turret." ) ] ) )
        steps.append( Step( 
            goal=lambda self, game: not self.ennemyShip.alive,
            failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
            onBegin=lambda self, game: (game.setRelationBetween( self.player, self.ennemy, 1 ), game.setRelationBetween( self.ennemy, self.player, 1 )),
            text = "Now that you can reach it, attack it!" ) )
            
        ### fighters
        steps.append( Step( 
            goal=lambda self, game: self.player.flagship.shipyards[ ids.S_HUMAN_FIGHTER ].getCount() >= 5,
            failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
            onBegin=lambda self, game: self.addEnnemyShips( game, (self.player.flagship.xp+stats.T_MASS_LR.weapon.maxRange+1000, self.player.flagship.yp), 200, count=2 ),
            texts = [(0,"There's another one too far away for your turrets."),
            (config.fps*4, "You need to build at leats 5 fighters."),
            (config.fps*8, "To do so, click on the fighter icon, at the bottom of the screen next to the harvester." )] ) )
        steps.append( Step( 
            goal=lambda self, game: self.player.flagship.ai.launching[ ids.S_HUMAN_FIGHTER ],
            failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
            texts = [(0,"Launch your fighters."),
            (config.fps*4, "To do so, press the blue arrow button at the bottom of the screen." )] ) )
        steps.append( Step( 
            goal=lambda self, game: not self.ennemy.flagships,
            failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
            onBegin=lambda self, game: (game.setRelationBetween( self.player, self.ennemy, 1 ), game.setRelationBetween( self.ennemy, self.player, 1 )),
            text = "Now order your fighters to attack it by left-clicking on it." ) )
         
         ### mines
        steps.append( Step( 
            goal=lambda self, game: filter( lambda turret: turret.install and turret.install.stats==stats.T_MINER, self.player.flagship.turrets ),
            failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
            texts = [(0, "The pirates always come from the same direction."),
                (config.fps*4, "Let's think ahead and build a mine field."),
                (config.fps*8, "First, build a mine layer turret."),
                (config.fps*12, "It would be a good idea to recall your fighters before laying the mine field."),
                (config.fps*16, "To do so, press  onthe green arrow over the fighter icon." )] ) )
        steps.append( Step( 
            goal=lambda self, game: self.player.flagship.missiles[ids.M_MINER].amount >= 1,
            failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
            text = "Build 8 or more miner missiles.\nThe button appeared next to the missile button." ) )
        steps.append( Step( 
            goal=lambda self, game: filter( lambda obj: isinstance( obj, MinerMissile ), game.objects.objects ),
            failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
            text = "A missile is ready.\nShoot it by clicking on the red targetting button over its icon.",
            texts= [
    (config.fps*4,"Then click on the target, in this case target at a little distance to the right of the station."),
    (config.fps*8,"You can always cancel the launch of a missile by right clicking on the screen when targetting.")
                    ] ) )
        steps.append( Step( 
            goal=lambda self, game: len( filter( lambda obj: isinstance( obj, Mine ), game.objects.objects ) ) >= stats.T_MINER.specialValue[1]*8,
            failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
            text = "Build and deploy a total of at least 8 missiles." ) )
            
         ### pulse
        steps.append( Step( 
            goal=lambda self, game: filter( lambda turret: turret.install and turret.install.stats==stats.T_PULSE, self.player.flagship.turrets ),
            failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
           onBegin=lambda self, game: self.addEnnemyShips( game, (self.player.flagship.xp+stats.T_MASS_LR.weapon.maxRange+200, self.player.flagship.yp), 200, count=4 ),
            texts = [(0, "A group of pirates can now be seen far away."),
            (config.fps*4, "To trap them and give us a head start let's hit them with an EMP weapon first!"),
            (config.fps*8, "Build a pulse launcher.") ] ) )
        steps.append( Step( 
            goal=lambda self, game: self.player.flagship.missiles[ids.M_PULSE].amount >= 1,
            failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
            text = "Build at least one pulse missile." ) )
        steps.append( Step( 
            goal=lambda self, game: filter( lambda obj: isinstance( obj, PulseMissile ), game.objects.objects ),
            failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
            text = "A missile is ready.\nShoot it in the middle of the pirates." ) )
        steps.append( Step( 
            goal=lambda self, game: not filter( lambda obj: isinstance( obj, PulseMissile ), game.objects.objects ),
            failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
            onBegin=lambda self, game: (game.setRelationBetween( self.player, self.ennemy, 1 ), game.setRelationBetween( self.ennemy, self.player, 1 )),
            texts = [(0,"Wait for them to get hit."),
            (config.fps*4, "Every ship caught in the explosion will have its engines disabled for a few seconds..."),
            (config.fps*8, "its shield will also be badly hit.")] ) )
        steps.append( Step( 
            goal=lambda self, game: not self.ennemy.flagships,
            failure=lambda self, game: not self.player.flagship or not self.player.flagship.alive,
            texts = [(0,"Wait for them to recover from the EMP and to get caught in the mine field!"),
                (config.fps*4, "Then finish them.")] ) )
            
        
        Scenario.__init__(self, game, steps=steps, stats=stats )
        
        
        self.sol = Sun( game.stats.S_SOL, 0, 0 )
        self.mercury = Planet( game.stats.P_MERCURY, -4100, 1400 )
        self.venus = Planet( game.stats.P_VENUS, 5000, 2300 )
        self.earth = Planet( game.stats.P_EARTH, -3100, 6700 )
        self.mars = Planet( game.stats.P_MARS_1, -7800, -2300 )
        self.moon = Planet( game.stats.P_MOON, -3900, 6400 )
        self.jupiter = Planet( game.stats.P_JUPITER, -13000, -4800 )
        self.saturn = Planet( game.stats.P_SATURN, 13000, 2500 )
        self.neptune = Planet( game.stats.P_NEPTUNE, 15000, 7000 )
        
        self.moon.zp = -50
        self.moon.yi = 0.1
        self.moon.orbiting = self.earth
        
        # asteroids near the station
        for i in xrange( 1 ):
            asteroid = Asteroid( game, self.moon.xp+200, self.moon.yp+430, 0 )
            game.harvestables.append( asteroid )
        
        for i in xrange( 10 ): # civilians around self.earth
            dist = randint( 100, 800 )
            angle = 2*pi*random()

            (x,y) = (self.earth.xp+dist*cos(angle), self.earth.yp+dist*sin(angle))
            s = Ship( game.stats.CIVILIAN_0, AiCivilian(), x, y, -20 )
            game.objects.append( s )

        for i in range( 50 ): # asteroids outer self.mars
            dist = 9000
            angle = (1-2*random())*pi/8+pi*9/8
            asteroid = Asteroid( game, self.sol.xp+dist*cos(angle), self.sol.yp+dist*sin(angle), 300 )
            game.harvestables.append( asteroid )

        game.astres = [self.sol, self.mercury, self.venus, self.earth, self.moon, self.mars, self.jupiter, self.saturn, self.neptune, self.moon ]
        
      #  dist = self.earth.stats.maxRadius*1.2
      #  angle = 7/8*pi
     #   self.orbitalbase = OrbitalBase( None, game.stats.HUMAN_BASE, None, self.earth.xp+dist*cos(angle),self.earth.yp+dist*sin(angle))
      #  self.orbitalbase.ri = -0.013
      #  game.objects.append( self.orbitalbase )
        
        self.player = None
      #  self.ennemy = Faction( game.stats.R_HUMAN, "Pirate lambda" )
        
    def addEnnemyShip( self, game, (x,y), attackedShip ):
        player = Computer( game.stats.R_HUMAN, "Pirate lambda" )
        flagship = FlagShip( player, game.stats.HUMAN_PIRATE, AiCaptain( player ),x,y )
        flagship.ore = flagship.stats.maxOre
        for t in flagship.turrets:
            t.buildInstall( game.stats.T_MASS_SR_1 )
            
        if attackedShip:
            flagship.ai.attack( flagship, attackedShip )
            
        flagship.energy = 0
     #   flagship.shield = 0
     #   flagship.hull = flagship.stats.maxHull/4  
        
        player.flagship = flagship
        self.ennemyShip = flagship
        self.ennemy = player
        game.addPlayer( self.ennemy )
        game.objects.append( self.ennemyShip )
        
    def addEnnemyShips( self, game, (x,y), radius=100, attackedShip=None, count=1 ):
        player = Faction( game.stats.R_HUMAN, "Pirate lambda", [Territory( (x,y), radius )] )
        for i in xrange( 0, count ):
            ship = FlagShip( player, game.stats.HUMAN_PIRATE, AiCaptain( player ),x,y )
            
            if attackedShip:
                ship.ai.attack( ship, attackedShip )
            player.flagships.append( ship )   
            for t in ship.turrets:
                t.buildInstall( game.stats.T_MASS_SR_1 )
            ship.ore = ship.stats.maxOre
            game.objects.append( ship )
        # ship.hull = flagship.stats.maxHull/3  
        
        #player.flagship = flagship
        #self.ennemyShip = flagship
        self.ennemy = player
        game.addPlayer( self.ennemy )
        #game.objects.append( self.ennemyShip )
        
    def addEnnemyShips2( self, game, (x,y), radius=100, attackedShip=None, count=1 ):
        player = Faction( game.stats.R_HUMAN, "Pirate lambda", Territory( (x,y), radius ) )
        for i in xrange( 0, count ):
            ship = ShipSingleWeapon( player, game.stats.HUMAN_FIGHTER, AiPilotDefense((x,y),radius),x,y )
            
            if attackedShip:
                ship.ai.attack( ship, attackedShip )
            player.ships.append( ship )   
            ship.shield = 0
            game.objects.append( ship )
        # ship.hull = flagship.stats.maxHull/3  
        
        #player.flagship = flagship
        #self.ennemyShip = flagship
        self.ennemy = player
        game.addPlayer( self.ennemy )
        #game.objects.append( self.ennemyShip )
        
    def setLowRelationWithEnnemy( self, game ):
        game.setRelationBetween( self.player, self.ennemy, -100 )
        
    def addRandomNpc( self, game, race=None, loc=None ):
        pass

    def doTurn( self, game ):
        Scenario.doTurn( self, game )

    def spawn( self, game, player, shipId=None ):
        
        player.race = game.stats.R_HUMAN
        shipStats = game.stats.HUMAN_BASE_MINING

        (x,y) = ( self.earth.xp-320, self.earth.yp+380 )

        flagship = OrbitalBase( player, shipStats, AiGovernor( player ),x,y,0, 0, 0.0,0.0,0.0, 0)
        flagship.ore = 5000
        flagship.energy = 1000
        flagship.ri = -0.01

        flagship.turrets[3].buildInstall( game.stats.T_MASS_MR_0 )
        flagship.turrets[1].buildInstall( game.stats.T_MASS_MR_0 )

        player.flagship = flagship        
        game.objects.append( flagship )

        for i in xrange( 6 ):
           harvester = HarvesterShip(player, player.race.defaultHarvester, AiPilotHarvester(flagship), 0,0,0, 4, 0.0,0.0,0.0, 0)
           flagship.shipyards[ harvester.stats.img ].docked.append( harvester )

        player.needToUpdateRelations = True
        Scenario.spawn( self, game, player, shipId )
        
