from common.utils import distLowerThan, distLowerThanReturn
from objects import Object

class ObjectManager:
    def __init__( self ):
        self.areas = {}
        self.areaSize = 1000
        self.objects = []
        self.defaultMaxDist = 100000
        
    def append( self, obj ):
        area = self.getArea( (obj.xp, obj.yp), create=True, std=True )
            
        area.append( obj )
        self.objects.append( obj )
        
    def getWithinRadius( self, pos, dist ):
        """Does not sort by proximity, there's no garantee the results order will be constant.""" # TODO currently does not care about objects overlaping area borders from radius
        if isinstance( pos, Object ):
            pos = pos.pos
            
        for x in xrange( int(pos[0]-dist), int(pos[0]+dist)+self.areaSize, self.areaSize):
            x = int(x)//self.areaSize
            for y in xrange( int(pos[1]-dist), int(pos[1]+dist)+self.areaSize, self.areaSize):
                y = int(y)//self.areaSize
                area = self.getArea( (x, y) )
                if area:
                    for obj in area:
                        if distLowerThan( pos, obj.pos, dist+obj.stats.maxRadius ):
                            yield obj
        
    def getWithin( self, pos, dist ):
        """Does not sort by proximity, there's no garantee the results order will be constant."""
        if isinstance( pos, Object ):
            pos = pos.pos
            
        for x in xrange( int(pos[0]-dist), int(pos[0]+dist)+self.areaSize, self.areaSize):
            x = int(x)//self.areaSize
            for y in xrange( int(pos[1]-dist), int(pos[1]+dist)+self.areaSize, self.areaSize):
                y = int(y)//self.areaSize
                area = self.getArea( (x, y) )
                if area:
                    for obj in area:
                        if distLowerThan( pos, obj.pos, dist ):
                            yield obj
                            
    def getWithinArea( self, pos, dist ):
        """Does not sort by proximity, there's no garantee the results order will be constant."""
        if isinstance( pos, Object ):
            pos = pos.pos
            
        for x in xrange( int(pos[0]-dist), int(pos[0]+dist)+self.areaSize, self.areaSize):
            x = int(x)//self.areaSize
            for y in xrange( int(pos[1]-dist), int(pos[1]+dist)+self.areaSize, self.areaSize):
                y = int(y)//self.areaSize
                area = self.getArea( (x, y) )
                if area:
                    for obj in area:
                        yield obj
                
    def getAccording( self, pos, dist=None, func=None ):
        """Useless? same as a filter"""
        for obj in self.getWithin( pos, dist ):
            if func( obj ):
                yield obj
    
    def getClosestAccording( self, pos, maxDist=None, func=None ):
        if isinstance( pos, Object ):
            pos = pos.pos
            
        if maxDist == None:
            dist = self.defaultMaxDist
        else:
            dist = maxDist
            
        closestObj = None
        for x in xrange( int(pos[0]-dist), int(pos[0]+dist+self.areaSize), int(self.areaSize)):
            x = int(x)//self.areaSize
            for y in xrange( int(pos[1]-dist), int(pos[1]+dist+self.areaSize), int(self.areaSize)):
                y = int(y)//self.areaSize
                area = self.getArea( (x, y) )
                if area:
                    for obj in area:
                        rdist = distLowerThanReturn( pos, obj.pos, dist )
                        if rdist and (not func or func( obj )):
                            dist = rdist
                            closestObj = obj
                        #    return obj
        return closestObj
        
    def update( self, obj, oldPos, newPos ):
        oldAreaPos = (int(oldPos[0])//self.areaSize, int(oldPos[1])//self.areaSize)
        newAreaPos = (int(newPos[0])//self.areaSize, int(newPos[1])//self.areaSize)
        if oldAreaPos != newAreaPos:
            oldArea = self.getArea( oldAreaPos )
            newArea = self.getArea( newAreaPos, create=True )
            if not oldArea or not obj in oldArea:
                print "Error, Update, obj not in area", obj
            else:
                oldArea.remove( obj )
            newArea.append( obj )
        
    #def updateAll( self ):
    #    for obj in self.objects.objects:
    #        self.update
        
    def cleanUp( self ):
        xKeysToDel = []
        for xk, xv in self.areas.items():
            yKeysToDel = []
            for yk, yv in self.areas[x].items():
                if not len( yv ):
                    yKeysToDel.append( yk )
                    
            if len( yKeysToDel ) == len( self.areas[x] ):
                xKeysToDel.append( xk )
            else:
                for k in yKeysToDel:
                    self.areas[x].pop( k )
                    
        for k in xKeysToDel:
            self.areas.pop( k )
                
    def getArea( self, (x,y), create=False, std=False ):
        if std:
            x = int(x)//self.areaSize
            y = int(y)//self.areaSize
        
        if not self.areas.has_key( x ):
            if create:
                self.areas[ x ] = {}
            else:
                return None
        
        if not self.areas[ x ].has_key( y ):
            if create:
                self.areas[ x ][ y ] = []
            else:
                return None
                
        return self.areas[x][y]
    
    def remove( self, obj ):   
        area = self.getArea( obj.pos, std=True )
        if area:
            if not obj in area:
                print "Error, obj not in area", obj
            else:
                area.remove( obj )
            
        if not obj in self.objects:
            print "Error, obj not in manager", obj
        else:
            self.objects.remove( obj )
        
