#from objects import Object

class Order:
	pass

class OrderRecallShips( Order ):
    def __init__( self, type ):
        self.type = type

class OrderLaunchShips( Order ):
    def __init__( self, type ):
        self.type = type

#class OrderToIntercept( Order ):
#    def __init__( self, obj, then ):
#        self.obj = obj
#        self.then = then

class OrderMove( Order ):
    def __init__( self, x, y, ori ):
        self.x = x
        self.y = y
        self.ori = ori

class OrderStopMove( Order ):
    def __init__( self, ori ):
        self.ori = ori

class OrderAttack( Order ):
    def __init__( self, obj ):
        self.obj = obj

#class OrderStopAttack( Order ):
#    def __init__( self ):
#        self.obj = obj

class OrderJumpNow( Order ):
	pass

class OrderJump( Order ):
    def __init__( self, (x, y) ):
        self.x = x
        self.y = y

class OrderLaunchMissile( Order ):
    def __init__( self, type, (x,y) ):
        self.x = x
        self.y = y
        self.type = type

class OrderOrbit( Order ):
    def __init__( self, obj ):
        self.obj = obj

class OrderBuildTurret( Order ):
    def __init__( self, tp, type ):
        self.tp = tp
        self.type = type

class OrderBuildShip( Order ):
    def __init__( self, type, rate ):
        self.type = type
        self.rate = rate

class OrderBuildMissile( Order ):
    def __init__( self, type, rate ):
        self.type = type
        self.rate = rate

# class OrderBuildShip( Order ):
# class OrderBuildMissile( Order ):

class OrderSetRelations( Order ):
    def __init__( self, other, level ):
        self.other = other
        self.level = level

class OrderActivateTurret( Order ):
    def __init__( self, turret, activate ):
        self.turret = turret
        self.activate = activate

class OrderActivateShield( Order ):
    def __init__( self, activate ):
        self.activate = activate

class OrderActivateRepair( Order ):
    def __init__( self,  activate ):
        self.activate = activate    

class OrderSetRelation( Order ):
    def __init__( self,  other, level ):
        self.other = other
        self.level = level

class OrderSelfDestruct( Order ):
    def __init__( self ):
        pass

class OrderBroadcast( Order ):
    def __init__( self, text ):
        self.text = text

class OrderDirectedCast( Order ):
    def __init__( self, text, (x,y) ):
        self.text = text
        self.x = x
        self.y = y

#class OrderReadyEJump( Order ):
#    def __init__( self,  activate ):
#        self.other = other
#        self.level = level

