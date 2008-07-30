from math import sqrt, pow, atan2, pi, cos, sin, fabs, hypot
from random import randint, random

from common.comms import COObject
from common.utils import * # distBetweenObjects, angleBetweenObjects, angleDiff
from common import ids
from common import config

class Object:
    def __init__( self, stats, xp, yp, zp=0, ori=0, xi=0, yi=0, zi=0, ri=0 ):
        self.xp = xp
        self.yp = yp
        self.zp = zp

        self.ori = ori
        self.xi = xi
        self.yi = yi
        self.zi = zi
        self.ri = ri
        self.stats = stats

        self.alive = True
        self.maxOri = 2*pi
        self.player = None
        self.orbiting = None
        self.hull = None
        self.headed = False

        self.cobject = None
      #  self.cobject = None
      
    pos = property( fget=lambda self: (self.xp, self.yp) )

    def doTurn(self, game):
        if self.orbiting:
            angle = angleBetweenObjects( self, self.orbiting )
            dist = distBetweenObjects( self, self.orbiting )
            speed = hypot( self.xi, self.yi )

            nextAngle = angle + atan2(speed,dist)
            entryAngle = angleDiff( atan2(self.yi, self.xi), angle )
            if entryAngle > 0:
                newOri = ((angle+nextAngle)/2+pi/2-0.05)%(2*pi) # clockwise-0.1
         #       print "> 0"
            else:
                newOri = ((angle+nextAngle)/2-pi/2)%(2*pi)

            self.xi = speed * cos(newOri) + self.orbiting.xi
            self.yi = speed * sin(newOri) + self.orbiting.yi

            if self.headed:
                maxRi = 0.05
                noDiff = angleDiff( newOri, self.ori )
                if noDiff > maxRi:
                    self.ori = self.ori+maxRi
                elif noDiff < -1*maxRi:
                    self.ori = self.ori-maxRi
                else:
                    self.ori = newOri
            else:
                self.ori = (self.ori + self.ri) % self.maxOri
        else:
            self.ori = (self.ori + self.ri) % self.maxOri

      # inertia applied to position
     #   oldPos = (self.xp,self.yp)
        self.xp = self.xp + self.xi
        self.yp = self.yp + self.yi
        self.zp = self.zp + self.zi
     #   if not isinstance( self, Planet ):
     #       game.objects.update( self, oldPos, (self.xp,self.yp) )

        return ([],[],[])

    def collidesWith( self,obj ): # could be simplified by the use of simple and complex radius
        radius0 = self.getRadiusAt( atan2( (obj.yp-self.yp), (obj.xp-self.xp) ) )
        radius1 = obj.getRadiusAt( atan2( (self.yp-obj.yp), (self.xp-obj.xp) ) )
        return self.distWith( obj ) <= radius0 + radius1

    def distWith( self, obj ):
        return sqrt( pow(self.xp-obj.xp, 2)+pow(self.yp-obj.yp, 2)) # +pow(self.zp-obj.zp

    def getRadiusAt( self, angle, bob ): # absolute angle with other object
        return stats.radius

    def getCommObjects(self):
        if not self.cobject:
            self.cobject =  COObject( self.stats.img, self.xp, self.yp, self.zp, self.ori, None, self.stats.maxRadius )
        else:
            self.cobject.xp = self.xp
            self.cobject.yp = self.yp
            self.cobject.zp = self.zp
            self.cobject.ori = self.ori
        return [self.cobject]

    def hit( self, game, angle, sender, energy=0, mass=0, pulse=False ):
        return ([],[],[])

class Asteroid( Object ):
    def __init__( self, game, x, y, radius ):
        self.maxI = 0
        self.maxRI = 0.01
        self.maxDist = radius
        self.cx = x
        self.cy = y
        self.randomInit( game )

 #   def doTurn(self, game):
 #       if distBetweenObjects( self, self.player.flagship ) > self.maxDist:
 #           self.randomInit()
 #       return Object.doTurn(self, game)

    def randomInit( self, game ):
        dist = randint( 0, self.maxDist )
        angle = random()*2*pi

        x = int(self.cx + cos( angle )*dist)
        y = int(self.cy + sin( angle )*dist)

        s = game.stats.ASTEROIDS[ randint(0,len(game.stats.ASTEROIDS)-1) ] #stats.ASTEROIDS[randint(0,2)][randint(1,2)]
        Object.__init__( self, s, x, y, -10, random()*2*pi, (2*random()-1)*self.maxI, (2*random()-1)*self.maxI, 0, (2*random()-1)*self.maxRI )

class Planet( Object ):
    def __init__( self, stats, x, y ):
        Object.__init__( self, stats, x, y, -100, 0, 0, 0, 0, 0 )

#from ships import Ship
class Sun( Planet ):
    def __init__( self, stats, x, y ):
        Planet.__init__( self, stats, x, y )
        self.damaged = []

    def doTurn( self, game ):
       (ao, ro, ag) = ([],[],[])
       if game.tick%(config.fps/2)==8:
         self.damaged = []
         for obj in game.objects.getWithinArea( self, self.stats.damageRadius ): # objects:
           if obj.alive and obj.hull:
               dist = distLowerThanObjectsReturn( self, obj, self.stats.damageRadius )
               if dist: 
                   self.damaged.append( (obj,dist) )
       for obj, dist in self.damaged:
           if obj.alive:
               angle = angleBetweenObjects( obj, self )
               (ao1, ro1, ag1) = obj.hit( game, angle, None, energy=self.stats.maxDamage*(self.stats.damageRadius-dist)/self.stats.damageRadius )
               (ao, ro, ag) = (ao+ao1, ro+ro1, ag+ag1)
       return (ao, ro, ag)

class Nebula( Object ):
    def __init__( self, stats, x, y ): # , radius ):
        Object.__init__( self, stats, x, y, 0, 0, 0, 0, 0, 0 )
      #  radius = stats.radius
        self.maxRi = 0.04
        self.cloudRadius = 62
      #  for i in range( 30 ):
      #      angle = 2*pi*random()
     #       dist = random()*stats.radius
      #      if randint(0,1):
      #          z = randint(10,50)
      #      else:
      #          z = randint(-50,-10)
      #      cloud = COObject( ids.A_NEBULA, self.xp+dist*cos(angle), self.yp+dist*sin(angle), z, 2*pi*random(), None, self.cloudRadius )
      #      cloud.ri = self.maxRi*(-1+2*random())
      #      self.clouds.append( cloud )  #(randint(x-radius)) )
        self.clouds = [ COObject( ids.A_NEBULA_OVER, self.xp, self.yp, 50, 2*pi*random(), None, self.stats.maxRadius ),
			 COObject( ids.A_NEBULA_UNDER, self.xp, self.yp, -50, 2*pi*random(), None, self.stats.maxRadius ) ]
        
    def getCommObjects(self):
        return self.clouds 

    def doTurn( self, game ):
      #  for cloud in self.clouds:
      #      cloud.ori = cloud.ori + cloud.ri
        return ([],[],[])

class BlackHole( Object ):
    def __init__( self, stats, x, y ):
        Object.__init__( self, stats, x, y, -100, 0, 0, 0, 0, 0 )
        self.affected = []

    def doTurn( self, game ):
      (ao, ro, ag) = ([],[],[])
      if game.tick%(config.fps/3)==4:
        self.damaged = []
        for obj in game.objects.getWithinArea( self, self.stats.gravitationalRadius ):
            dist = distLowerThanObjectsReturn( self, obj, self.stats.gravitationalRadius )
            if dist:
                angle = angleBetweenObjects( obj, self )
                self.affected.append( (obj,dist,angle) )
      for obj, dist, angle in self.affected:
           if obj.alive:
                if dist < self.stats.damageRadius:
                    (ao0, ro0, ag0) = obj.hit( game, angle, None, mass=self.stats.maxDamage*(self.stats.gravitationalRadius-dist)/self.stats.gravitationalRadius )
                    (ao, ro, ag) = (ao+ao0, ro+ro0, ag+ag0)
                pull = self.stats.gravitationalStrength*(self.stats.gravitationalRadius-dist)/self.stats.gravitationalRadius
                obj.xi = (obj.xi+pull*cos( angle ))*dist/self.stats.gravitationalRadius #  * dist/self.stats.gravitationalRadius
                obj.yi = (obj.yi+pull*sin( angle ))*dist/self.stats.gravitationalRadius #  * dist/self.stats.gravitationalRadius
      return (ao, ro, ag)

