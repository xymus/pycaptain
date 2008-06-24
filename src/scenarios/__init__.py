__all__ = [ "Scenario", "Step" ]

class Step:
    def __init__( self, goal=None, failure=None, onBegin=None, text=None,  ):
        self.goal = goal
        self.failure = failure
        self.onBegin = onBegin
        self.text = text
        
def listIter( list ):
    for e in list:
        yield e

class Scenario:
    def __init__(self, game, steps=None, name=None, description=None, year=0):
        self.steps = steps
        self.name = name
        self.description = description
        self.year = year
        
        if self.steps:
            self.stepsIter = listIter( steps )
            self.step = self.stepsIter.next()
            
        self.over = False

    def addRandomNpc( self, game, race=None, loc=None ):
        pass

    def doTurn( self, game ):
        if self.steps:
            if step.goal and step.goal( game ):
                try:
                    self.step = self.stepsIter.next()
                except StopIteration:
                    self.over = True
                    self.step = None
                    
                if self.step:
                    if self.step.text:
                        pass # TODO send messages to user, or simply advise of next goal
                        
                    if self.step.onBegin:
                        self.step.onBegin( game ) 

    def spawn( self, game, player, shipId=None ):
        pass


