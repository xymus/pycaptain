from random import random, choice, randint
from math import sin, cos, pi

from common.comms import COInput
from common.orders import *
from common import config
from common import utils
from common import ids

class Player:
    def __init__(self, race, name):
        self.name = name
        self.race = race
        self.points = 0
        
        self.msgs = [] 

    def doTurn( self, game ):
        pass

class Human( Player ):
    def __init__(self, race, username="", password=""):
        Player.__init__( self, race, username ) 
        self.username = username
        self.password = password
        self.flagship = None
        self.justLoggedIn = False
        self.inputs = COInput()
        self.online = True
        self.inPlay = False

    def doTurn( self, game ):
        if self.flagship:
            for order in self.inputs.orders:
                if isinstance( order, OrderMove ):
                    self.flagship.ai.goTo( self.flagship, (order.x,order.y) )
                elif isinstance( order, OrderStopMove ):
                    self.flagship.ai.stop( self.flagship )
                elif isinstance( order, OrderRecallShips ):
                    self.flagship.ai.recallShips( self.flagship, game, order.type )
                elif isinstance( order, OrderLaunchShips ):
                    self.flagship.ai.launchShips( self.flagship, game, order.type )
                elif isinstance( order, OrderAttack ):
                    if game.uidsSent[ self ].has_key( order.obj ):
                        self.flagship.ai.attack( self.flagship, game.uidsSent[ self ][ order.obj ] )
                    else:
                        print "client - warning: dropped attack order due to unfound target id"
        #        elif isinstance( order, OrderStopAttack ):
        #            pass
                elif isinstance( order, OrderJumpNow ):
                    self.flagship.emergencyJump()
                elif isinstance( order, OrderJump ):
                    self.flagship.delayedJump( (order.x, order.y) )
                elif isinstance( order, OrderOrbit ):
                    self.flagship.ai.goTo( self.flagship, game.uidsSent[ self ][ order.obj ], orbitAltitude=2 )
                elif isinstance( order, OrderBuildTurret ):
                    if order.type:
                        self.flagship.buildTurret( self.flagship.turrets[ order.tp ], game.stats[ order.type ] )
                    else:
                        self.flagship.buildTurret( self.flagship.turrets[ order.tp ], None )
                elif isinstance( order, OrderBuildShip ):
                    self.flagship.buildShip( game, order.type, switch=True )
                elif isinstance( order, OrderBuildMissile ):
                    self.flagship.buildMissile( game, order.type, switch=True )
                elif isinstance( order, OrderLaunchMissile ):
                    self.flagship.launchMissile( order.type, (order.x,order.y) )
                elif isinstance( order, OrderActivateTurret ):
                    self.flagship.turrets[ order.turret ].activated = bool(order.activate)
                elif isinstance( order, OrderActivateShield ):
                    self.flagship.charging = bool(order.activate)
                elif isinstance( order, OrderActivateRepair ):
                    self.flagship.repairing = bool(order.activate)
                elif isinstance( order, OrderSetRelation ):
                    game.setRelationBetween( self, game.getPlayer( order.other ), (order.level)*2-100 ) # on the player side it is 0-100
                elif isinstance( order, OrderSelfDestruct ):
                    self.flagship.selfDestruct( game )
                elif isinstance( order, OrderBroadcast ):
                #    print order.text
                    game.communicationManager.addWideBroadcast( game, self, order.text, ship=self.flagship )
                #    self.flagship.selfDestruct( game )
                elif isinstance( order, OrderDirectedCast ):
                 #   print order.text
                    game.communicationManager.addDirectedBroadcast( game, self, order.text, (order.x,order.y), ship=self.flagship )
                 #   self.flagship.selfDestruct( game )
        self.inputs.orders = []

    def connect(self):
        self.needToUpdateRelations = True
        self.needToUpdatePossibles = True
        self.needToUpdateShipStats = True
        self.needToUpdateAstres = True

class Computer( Player ):
    def __init__( self, race, name, territories=[] ):
        Player.__init__( self, race, name ) 
        self.territories = territories
        self.flagship = None

    def doTurn( self, game ):
        if self.flagship:
            self.manageFagship( self.flagship, game )
       #     elif not self.flagship.ai.goingTo:

    def manageFagship( self, ship, game ):
        if not game.tick%50:
            ## activated turrets
            for turret in ship.turrets:
                turret.activated = True
        
            ## launch harvesters
            for k in ship.ai.launching:
                if isinstance( game.stats[ k ], game.stats.HarvesterShipStats ):
                    ship.ai.launching[ k ] = True

        if ship.ai.attacking: # in combat
            ## launch fighters
            for k in ship.ai.launching:
                if not isinstance( game.stats[ k ], game.stats.HarvesterShipStats ):
                    ship.ai.launching[ k ] = True

            ## maneuver
            dist = (ship.stats.maxRadius + ship.ai.attacking.stats.maxRadius)*1.5
            angle = utils.angleBetweenObjects( ship.ai.attacking, ship )+pi/8
            ship.ai.goTo( ship, (ship.ai.attacking.xp+cos(angle)*dist, ship.ai.attacking.yp+sin(angle)*dist) )

        else: # not in combat
            if not game.tick%(config.fps*10):
                needToFindOre = False
                needToFindEnergy = False
                
                ## recall fighters when not in combat
                for k in ship.ai.launching:
                    if not isinstance( game.stats[ k ], game.stats.HarvesterShipStats ):
                        ship.ai.recallShips( ship, game, k )  #ship.ai.launching[ k ] = False
            
                ## move closer to resources
                if sum( [ len(ship.shipyards[ shipyard ].docked)+len(ship.shipyards[ shipyard ].away) for shipyard in \
                  filter( lambda ship: isinstance( game.stats[ k ], game.stats.HarvesterShipStats ), ship.shipyards ) ] ): # if has any harvesters
                    closestAsteroid = game.harvestables.getClosestAccording( ship.pos, ship.getRadarRange() )
                    if closestAsteroid and not utils.distLowerThanObjects( ship, closestAsteroid, ship.stats.maxRadius*2 ):
                        dist=ship.stats.maxRadius*1.5
                        angle=random()*2*pi
                        ship.ai.goTo( ship, (closestAsteroid.xp+dist*cos(angle),closestAsteroid.yp+dist*sin(angle)) )
                    else: # nothing in range
                        if ship.ore < ship.stats.maxOre/10: # low on ore
                            needToFindOre = True
                        
              #  if ship.energy < ship.stats.maxEnergy/5 and # low on energy
              #      :
              
              #  if ship.ore > ship.stats.maxOre/3 \
              #     and len( filter( lambda turret: turret.building, ship.turrets ) < len(ship.turrets)/3: 
                   # if has ore
                   # if less than 1/3 of turrets are in construction
                    
                
               
            
                     
                    
                    
    def getStrongSide( self ):
        self.anglesMass = [0]*30
        self.anglesEnergy = [0]*30
        self.minRange = [0]*30
        self.maxRange = [10000]*30
        
        if self.flagship:
            for turret in self.flagship.turrents:
                if turret.install and turret.install.weapon:
                    if turret.install.stats.maxAngle < turret.install.stats.minAngle:
                        temprange = range( turret.install.stats.maxAngle, turret.install.stats.minAngle+2*pi )
                        frange = [ (a%2*pi)//(2*pi/len(self.angles)) for a in temprange ]
                    else:
                        frange = xrange( (turret.install.stats.minAngle)//(2*pi/len(self.angles)), turret.install.stats.maxAngle )
                        
                    for a in frange:
                        self.anglesMass[ a ] += turret.install.stats.massDamageValue
                        self.anglesEnergy[ a ] += turret.install.stats.energyDamageValue
                    self.minRange = max( self.minRange, turret.install.stats.weapon.minRange )
                    self.maxRange = min( self.maxRange, turret.install.stats.weapon.maxRange ) # Use a dist*value system to improve results
          #  bestAngle = 0
          #  for k in xrange( len(self.anglesMass) ):
          #      if 
                    
        else:
            self.strongAngle = None
            self.strongDist = None
                
                
class Faction( Computer ):
    def __init__(self, race, name, territories=None ):
        Computer.__init__( self, race, name, territories ) 
        self.bases = []
        self.ships = [] # these ships must have an Ai inheriting AiPilotFaction
        self.flagships = []
        self.protectsTheInnocent = False
        
   # flagship = property( fget=lambda self: self.flagships[0] )

    def doTurn( self, game ):
        for ship in self.flagships:
          if not ship.alive:
            self.flagships.remove( ship)
          else:
            self.manageFagship( ship, game )
            if ship.ai.idle and self.territories:
                territory = choice( self.territories )
                dist = randint( 0, territory.radius )
                angle = 2*pi*random()
                dest = (territory.x+cos(angle)*dist, territory.y+sin(angle)*dist)
                ship.ai.goTo( ship, dest )

        for ship in self.bases:
          if not ship.alive:
            self.bases.remove( ship)
          else:
            ship.energy = ship.stats.maxEnergy # cheating
            ship.ore = ship.stats.maxOre # cheating
            self.manageFagship( ship, game )

        for ship in self.ships:
          if not ship.alive:
            self.ships.remove( ship)
       #   else:
        
        for ship in utils.mY( self.bases, self.flagships, self.ships ):
            if ship.ai.attacking: #needsHelp( game ):
                for s1 in utils.mY( self.bases, self.flagships, self.ships ): # self.ships:
                    if ship != s1 and not s1.ai.attacking and utils.distLowerThanObjects( ship, s1, 300 ):
                        s1.ai.attack( s1, ship.ai.attacking )

      #  if self.flagship and self.territories:
      #      territory = choice( self.territories )

      #      angle = 2*pi*random()
      #      dist = randint( 0, territory.radius )

      #      dest = (territory.x+dist*cos(angle), territory.y+dist*sin(angle) )
      #      if utils.distBetween( (ship.xp,ship.yp), dest )> ship.stats.maxRadius*2:
      #          ship.ai.goTo( ship, dest )


def GetComputerPlayer( game ):
    return Computer( game.stats.R_HUMAN, choice(['Bob','Fred']) )

def KillComputerPlayer():
    pass

class Territory:
    def __init__( self, (x,y), radius ):
        self.x = x
        self.y = y
        self.radius = radius




