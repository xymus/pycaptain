from time import time
from random import randint
import pickle # using pickle instead of cPickle for saving/loading since cpickle raised undescriptive errors

from players import *
from ships import * # Ship, FlagShip, Turret
from objects import Object, Asteroid, Planet, Sun, Nebula, BlackHole
from weapons import *
from ais import *
from common.comms import *
from common.utils import distBetweenObjects
from common import utils
from common.orders import *
from common.gfxs import * # temp
from common import ids
from common import config
from objectmanager import ObjectManager



class Game:
    def __init__(self, scenarioType=None ):

        self.players = []

        self.objects = ObjectManager()
        self.harvestables = ObjectManager()
        self.astres = []

        self.newGfxs = []
        self.relations = {}

        self.tick = 0

        self.uidsSent = {}

      ### loading world according to scenario
        if scenarioType:
            self.scenario = scenarioType( self )
        

    def doTurn(self,playerInputs):
        addedObjects = []
        removedObjects = []
        addedGfxs = []
        
       ### manage inputs
        for (player,inputs) in playerInputs:
            player.inputs = inputs
                 
       ### players play
        for player in self.players:
            player.doTurn( self )

       ### move objects
        ts = {}
        for o0 in utils.mY( self.objects.objects, self.astres ):
          if o0.alive:
            t0 = time()
            
            oldPos = o0.pos
            ( addedObjectsLocal, removedObjectsLocal, addedGfxsLocal ) =  o0.doTurn( self )
            self.objects.update( o0, oldPos, o0.pos )

            if addedObjectsLocal:
                addedObjects = addedObjects + addedObjectsLocal
            if removedObjectsLocal:
                removedObjects = removedObjects + removedObjectsLocal 
            if addedGfxsLocal:
                addedGfxs = addedGfxs+addedGfxsLocal 
            t1 = time()
            ts[ o0 ] = t1-t0
        # tests delai for each objects
        ho = None
        bt = 0
        for k in ts:
            if ts[ k ] > bt:
                bt = ts[ k ]
                ho = k
       # print ho
        if __debug__ and not self.tick%(config.fps):
            print utils.i
            utils.i = 0

      ### remove dead objects
        for o1 in removedObjects:
            if isinstance( o1, FlagShip ):
             #   print o1.player
                if isinstance( o1.player, Human ):
               #     print "definately human"
                    o1.player.flagship = None
                    o1.player.needToUpdatePossibles = True
                elif not isinstance( o1.player, Faction ):
                    print "not human"
                    self.removePlayer( o1.player )

            
            self.objects.remove( o1 ) # WARNING: this assumes harvestable and astres objects won't be removed
            
        for obj in addedObjects:
            self.objects.append( obj )


        if not self.tick%(config.fps*5):

            ## calm tensions between computers and players
            for p0 in self.players:
             if not isinstance( p0, Computer ):
                for p1 in self.players:
                 if isinstance( p1, Computer ):
                    rel = self.getRelationBetween( p1, p0 )
                    if rel < self.stats.Relations[ p1.race ][ p0.race ]:
                       self.setRelationBetween( p1, p0, rel + 1)
                 #      self.setRelationBetween( p0, p1, rel + 1)

       ### Scenario
        self.scenario.doTurn( self )

        self.newGfxs = addedGfxs

       ### advance frame count
        self.tick = self.tick + 1
        
    def getBrief( self, player ):
        cobjs = []
        for obj in self.objects.objects:
            cobjs.append( (obj, cobj) )

    def addRemotePlayer(self, username, password ):
        player = Human( self.stats.R_HUMAN, username, password )
        self.addPlayer( player )
        self.uidsSent[ player ] = []

        return player

    def giveShip( self, player, shipId ):
        if not player.flagship and player.points >= self.stats.PlayableShips[ shipId ].points:
            self.scenario.spawn( self, player, shipId )
        else:
            raise Exception( "giveShip aborted, already has ship (%s) or selected ship unplayable (%s)." % (player.flagship, player.points < self.stats.PlayableShips[ shipId ].points)  )

    def addPlayer( self, player ):
        self.relations[ player ] = {}
        for other in self.players:
            if isinstance( other, Human ):
                other.needToUpdateRelations = True
            if isinstance( player, Computer ) or isinstance( other, Computer ):
                self.relations[ player ][ other ] = self.stats.Relations[ player.race ][ other.race ]
                self.relations[ other ][ player ] = self.stats.Relations[ other.race ][ player.race ]
            else: ## if both are human players
                self.relations[ player ][ other ] = 20
                self.relations[ other ][ player ] = 20

        self.players.append( player )
        
        if isinstance( player, Human ):
            if len( self.stats.PlayableShips ) == 1:
                self.scenario.spawn( self, player, self.stats.PlayableShips.keys(0) )
            if len( self.stats.PlayableShips ) == 0:
                self.scenario.spawn( self, player )

    def getPlayer( self, name ):
        for p in self.players:
        #    if isinstance( p, Human ) and p.username == username:
            if p.name == name:
                return p

    def removePlayer( self, player ):
     #   self.players.remove( player )
        pass
     #   print "removing player"
    #    for k, r in self.relations:
     #       if k == player: # r.has_key( player ):
     #           del( r[ player ] )
      #  del( self.relations[ player ] )


    def getRelationBetween( self, p0, p1 ):
   #     print p0, p1
        if p0 == p1:
            return 101
        else:
           # try:
                return self.relations[ p0 ][ p1 ]
         #   except KeyError, e:
         #       print "KeyError in getRelationBetween for", p0, p1, e 
         #       return 0

    def setRelationBetween( self, p0, p1, rel=20 ): 
        if p0 and p1 and p0 != p1 and (isinstance( p0, Human ) or isinstance( p1, Human )):
            if isinstance( p0, Human ):
                p0.needToUpdateRelations = True
            if isinstance( p1, Human ):
                p1.needToUpdateRelations = True

            self.relations[ p0 ][ p1 ] = rel
        
    def executeCode( self, code ):
        eval( code )
        
    def save( self, path ):
    #    import cPickle as pickle
        
        f = open( path, "w" )
        if f:
            if self.scenario.steps:
                hadSteps = True
                steps = self.scenario.steps
                step = self.scenario.step
                stepsIter = self.scenario.stepsIter
                self.scenario.step = self.scenario.steps.index( self.scenario.step )
                self.scenario.steps = None
                self.scenario.stepsIter = None
            else:
                hadSteps = False
                
            try:
            
                title = self.scenario.title
                year = self.scenario.year
                timePlayed = self.tick/config.fps
                description = self.scenario.description
                player = filter( lambda player: isinstance( player, Human ), self.players )[0]
                username = player.username
                if player.flagship:
                    ship = player.flagship.stats.img
                else:
                    ship = 0
            
                pickle.dump( title, f )
                pickle.dump( year, f )
                pickle.dump( timePlayed, f )
                pickle.dump( description, f )
                pickle.dump( username, f )
                pickle.dump( ship, f )
                
                pickle.dump( self, f )
                success = True
            except Exception, ex:
                print "failed to save game:", ex
                success = False
            f.close()
        
            if hadSteps:
                self.scenario.steps = steps
                self.scenario.step = step
                self.scenario.stepsIter = stepsIter
        else:
            success = False
        
        return success
        
        
def LoadGame( path ):
    import cPickle as pickle
    f = open( path, "r" )
    if f:
        try:
            title = pickle.load( f )
            year = pickle.load( f )
            timePlayed = pickle.load( f )
            description = pickle.load( f )
            username = pickle.load( f )
            ship = pickle.load( f )
            
            game = pickle.load( f )
            if game.scenario.name:
                exec( "from scenarios.%s import %s as Scenario" % (game.scenario.name.lower(), game.scenario.name) )
                dummyGame = Game( Scenario )
                if dummyGame.scenario.steps:
                    game.scenario.steps = dummyGame.scenario.steps
                    game.scenario.stepsIter = iter( game.scenario.steps[ game.scenario.step: ] )
                    game.scenario.step = game.scenario.stepsIter.next()
                    
        except Exception, ex:
            print "failed to load game:", ex
            game = None
        f.close()
        
    return game
