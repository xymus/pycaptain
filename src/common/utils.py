from math import atan2, sqrt, pow, pi, hypot, fabs
#import cutils

dists = {}
angles = {}

i = 0
def angleBetween( (x0,y0), (x1, y1) ):
  #  if angles.has_key( ( (x0,y0), (x1, y1) ) ):
        
    return atan2( (y1-y0), (x1-x0) )%(2*pi)

def angleBetweenObjects( obj0, obj1 ):
    return atan2( (obj1.yp-obj0.yp), (obj1.xp-obj0.xp) )%(2*pi)

def distBetween( (x0,y0), (x1, y1) ):
    global i
    i = i+1
   # if dists.has_key( ( (x0,y0), (x1, y1) ) ):
   #     v = dists[ ( (x0,y0), (x1, y1) ) ]
  #  else:
    v = hypot( x1-x0, y1-y0 )
  #      dists[ ( (x0,y0), (x1, y1) ) ] = v
    return v

def distBetweenObjects( obj0, obj1 ):
    return hypot( obj1.xp-obj0.xp, obj1.yp-obj0.yp ) # sqrt( pow(obj1.xp-obj0.xp, 2)+pow(obj1.yp-obj0.yp, 2) )

def areOver( obj0, obj1 ):
    return distLowerThanObjects( obj0, obj1, obj0.stats.radius + obj1.stats.radius ) # distBetweenObjects( obj0, obj1 ) < obj0.stats.radius + obj1.stats.radius

def angleDiff( ang0, ang1 ):
    sDiff = (ang0 - ang1)%(2*pi)
    if sDiff < pi:
        return sDiff
    else:
        return sDiff-2*pi


def distLowerThan( (x0,y0), (x1,y1), val ):
    global i
    i = i+1
  #  print i
    if fabs(x1 - x0) > val:
        return False
    elif fabs(y1 - y0) > val:
        return False
    else:
        return distBetween( (x0,y0), (x1,y1) ) < val

def distGreaterThanObjects( obj0, obj1, val ):
    return distGreaterThan( (obj0.xp, obj0.yp), (obj1.xp, obj1.yp), val )

def distGreaterThan( (x0,y0), (x1,y1), val ):
    global i
    i = i+1
  #  print i
    if fabs(x1 - x0) > val:
        return True
    elif fabs(y1 - y0) > val:
        return True
    else:
        return distBetween( (x0,y0), (x1,y1) ) > val
    
def distLowerThanObjects( obj0, obj1, val ):
    return distLowerThan( (obj0.xp, obj0.yp), (obj1.xp, obj1.yp), val )

def distLowerThanReturn( (x0,y0), (x1,y1), val ):
    global i
    i = i+1
    if fabs(x1 - x0) > val:
        return False
    elif fabs(y1 - y0) > val:
        return False
    else:
        dist = distBetween( (x0,y0), (x1,y1) )
        if dist < val:
            return dist
        else:
            return False
    
def distLowerThanObjectsReturn( obj0, obj1, val ):
    return distLowerThanReturn( (obj0.xp, obj0.yp), (obj1.xp, obj1.yp), val )

def mY( *args ):
    for arg in args:
        for e in arg:
            yield e

def accumulate(  ):
    pass

