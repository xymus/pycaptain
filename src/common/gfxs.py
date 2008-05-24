from random import choice, random, randint

import ids

class Gfx:
    def doTurn( self ):
        return []

class GfxLaser( Gfx ):
    def __init__( self, (xp,yp), z, (xd,yd), width=1, color=ids.R_HUMAN ):
        self.xp = xp
        self.yp = yp
        self.z = z
        self.xd = xd
        self.yd = yd
        self.width = width
        self.color = color
        self.intensity = 1
        self.intensityDecrRate = 0.5
        self.maxRadius = 10

    def doTurn( self ):
        Gfx.doTurn( self )
        self.intensity = self.intensity - self.intensityDecrRate
        if self.intensity <= 0:
            return [ self ]
        else:
            return []

class GfxExplosion( Gfx ):
    def __init__( self, (xp,yp), radius, sound=0, delai=0 ):
        self.xp = xp
        self.yp = yp
        self.radius = radius
        self.delai = delai
        self.sound = sound
        self.maxRadius = radius

    def doTurn( self ):
        if self.delai == 0:
            return [ self ] + Gfx.doTurn( self )
        else:
            self.delai = self.delai - 1
            return Gfx.doTurn( self )

class GfxFragment( Gfx ):
    def __init__( self, (xp,yp), zp, ori, xi,yi,ri, type, time ):
        self.xp = xp
        self.yp = yp
        self.zp = zp
        self.ori = ori
        self.xi = xi
        self.yi = yi
        self.ri = ri
        self.type = type

        self.ttl = time #randint(20, 36)
        self.maxRadius = 100

    def doTurn( self ):
      if self.ttl == 0:
        return [ self ] + Gfx.doTurn( self )
      else:
        self.xp = self.xp + self.xi
        self.yp = self.yp + self.yi
        self.ori = self.ori + self.ri
        self.ttl = self.ttl - 1
        return Gfx.doTurn( self )

class GfxFragmentUnavoidable( GfxFragment ):
    pass

class GfxShield( Gfx ):
    def __init__( self, (xp,yp), radius, strength, angle, hit ):
        self.xp = xp
        self.yp = yp
        self.radius = radius
        self.strength = strength
        self.angle = angle
        self.hit = hit
        self.ttl = 2
        self.maxRadius = radius

    def doTurn( self ):
        self.ttl = self.ttl - 1
        if self.ttl == 0:
            return [ self ] + Gfx.doTurn( self )
        else:
            return Gfx.doTurn( self )

class GfxExhaust( GfxFragment ):
    def __init__( self, (xp,yp), zp, ori, xi,yi,ri ):
        GfxFragment.__init__( self, (xp,yp), zp, ori, xi,yi,ri, choice( [ids.E_0, ids.E_1, ids.E_2] ), randint( 20,30) )
        self.alpha = 1
        self.ii = 1.0/self.ttl
        self.maxRadius = 0

    def doTurn( self ):
        self.alpha = self.alpha - self.ii
        return GfxFragment.doTurn( self )

class GfxLightning( Gfx ):
    def __init__( self, (xp, yp), z, (xd,yd), strength=1 ):
        self.xp = xp
        self.yp = yp
        self.z = z
        self.xd = xd
        self.yd = yd
        self.width = width
        self.color = color
        self.strength = strength
        self.maxRadius = 10

    def doTurn( self ):
        Gfx.doTurn( self )
        return [ self ]

