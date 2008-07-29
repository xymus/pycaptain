from math import pi, sin, cos, ceil
from random import random
import sys, os

from common import utils # TODO remove
from common import config
from server.stats import Stats
from server.communications import MessageArchived
from server.objects import Asteroid, Planet, Sun

scenarioFiles = filter( 
    lambda f: len( f )>3 and f[-3:]==".py" and f[0]!="_", 
    os.listdir( os.path.join( sys.path[0], "scenarios" ) ) )
scenarioNames = [ n[:-3] for n in scenarioFiles]
scenarioNames.sort()

__all__ = [ "Scenario", "Step" ]


class Step:
    def __init__( self, goal=None, failure=None, onBegin=None, text=None, texts=None ):
      #  could not use texts=[], was shard somehow, python bug?
        self.goal = goal
        self.failure = failure
        self.onBegin = onBegin
        
        if texts:
            self.texts = texts
        else:
            self.texts =  []
            
        if text:
            self.texts.append( (0, text) )
            
            
class Scenario:
    title = None
    description = None
    year = None
    name = None
    
    defaultTextTiming = 4*config.fps
    
    def __init__(self, game, steps=None, stats=None):
        self.steps = steps
        
        if self.steps:
            self.step = None
            self.stepsIter = iter(steps)
            
        self.failed = False
        self.over = False
        self.msgs = []
        self.lastStepAt = 0
            
        
        if stats == None:
          #  stats.setDefaults()
            game.stats = Stats()
        else:
            game.stats = stats

    def addRandomNpc( self, game, race=None, loc=None ):
        pass

    def doTurn( self, game ):
        if self.steps and self.player:
        
            ## test goal
            if self.step and self.step.goal and self.step.goal( self, game ):
                self.nextStep( game )
                if self.over:
                    self.msgs.append( MessageArchived( "Scenario", "Scenario completed", game.tick, game.tick ) )
                    
            ## test failure
            if self.step and self.step.failure and self.step.failure( self, game ):
                self.msgs.append( MessageArchived( "Scenario", "Scenario failed", game.tick, game.tick ) )
                self.failed = True
                self.over = True
                self.step = None
                    
            ## send text
            if self.step and self.step.texts:
                for t, text in self.step.texts:
                    if game.tick == self.lastStepAt+t:
                        for line in text.split("\n"):
                            self.msgs.append( MessageArchived( "Scenario", line, game.tick, game.tick ) )
                    

    def spawn( self, game, player, shipId=None ):
        self.player = player
        player.needToUpdateRelations = True
        if self.steps and not self.step:
            self.nextStep( game )

    def nextStep( self, game ):
        self.lastStepAt = game.tick
        try:
            self.step = self.stepsIter.next()
        except StopIteration:
            self.over = True
            self.step = None
            
        if self.step:
            if self.step.onBegin:
                self.step.onBegin( self, game ) 
                
    def getOrbitingPlanet( self, orbiterStats, orbitted, dist, angle=None ):
        if angle == None:
            angle = 2*pi*random()
            
        if not orbitted is tuple:
            orbitted = orbitted.pos
            
        planet = Planet( orbiterStats, orbitted[0]+dist*cos(angle), orbitted[1]+dist*sin(angle) )
        return planet
    
    
