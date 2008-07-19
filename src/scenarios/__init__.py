import sys, os
from common import utils # TODO remove
from common import config
from server.stats import Stats

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
                    self.msgs.append( "Scenario completed" )
                    
            ## test failure
            if self.step and self.step.failure and self.step.failure( self, game ):
                self.msgs.append( "Scenario failed" )
                self.failed = True
                self.over = True
                self.step = None
                    
            ## send text
            if self.step and self.step.texts:
                for t, text in self.step.texts:
                    if game.tick == self.lastStepAt+t:
                        for line in text.split("\n"):
                            self.msgs.append( line )
                    
                    
                        

    def spawn( self, game, player, shipId=None ):
        self.player = player
        if self.steps:
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
    
    
