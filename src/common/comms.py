from orders import *
from gfxs import *
import ids

version = "v0.4.5"

if __debug__:
    print "Comms %s" % version

class AttackOrder:
    def __init__(self):
        self.target
        self.weapon

# inputs -> server
class COInput:
    def __init__(self,xc=0,yc=0,wc=320,hc=320):
        self.xc = xc
        self.yc = yc
        self.wc = wc
        self.hc = hc
    #    self.thrustLevel = 0 # 0-10
    #    self.gouvernail = 0.0
       # self.stance = 5 # 0-10
        self.orders = []

        self.mouseDownAt = (0,0)
        self.mouseUpAt = (0,0)
        self.mouseDownAtV = (0,0)
        self.mouseUpAtV = (0,0)
        self.mouseUpped = False


    def dump(self):
        dump = "%i;%i;%i;%i" % ( self.xc, self.yc, self.wc, self.hc )
	for order in self.orders:
            if isinstance( order, OrderMove ):
                dump = dump + ";%i:%i:%i:%7f" % ( ids.O_MOVE, order.x, order.y, order.ori )
            if isinstance( order, OrderStopMove ):
                dump = dump + ";%i:%.2f" % ( ids.O_STOP_MOVE, order.ori )
            elif isinstance( order, OrderRecallShips ):
                dump = dump + ";%i:%i" % ( ids.O_RECALL_SHIPS, order.type )
            elif isinstance( order, OrderLaunchShips ):
                dump = dump + ";%i:%i" % ( ids.O_LAUNCH_SHIPS, order.type )
            elif isinstance( order, OrderJumpNow ):
                dump = dump + ";%i" % ( ids.O_JUMP_NOW )
            elif isinstance( order, OrderJump ):
                dump = dump + ";%i:%i:%i" % ( ids.O_JUMP, order.x, order.y )
            elif isinstance( order, OrderLaunchMissile ):
                dump = dump + ";%i:%i:%i:%i" % ( ids.O_LAUNCH_MISSILE, order.type, order.x, order.y )
            elif isinstance( order, OrderAttack ):
                dump = dump + ";%i:%i" % ( ids.O_ATTACK, order.obj )
            elif isinstance( order, OrderOrbit ):
                dump = dump + ";%i:%i" % ( ids.O_ORBIT, order.obj )
            elif isinstance( order, OrderBuildTurret ):
                dump = dump + ";%i:%i:%i" % ( ids.O_BUILD_TURRET, order.tp, order.type )
            elif isinstance( order, OrderBuildShip ):
                dump = dump + ";%i:%i:%i" % ( ids.O_BUILD_SHIP, order.type, order.rate )
            elif isinstance( order, OrderBuildMissile ):
                dump = dump + ";%i:%i:%i" % ( ids.O_BUILD_MISSILE, order.type, order.rate )
            elif isinstance( order, OrderActivateTurret ):
                dump = dump + ";%i:%i:%i" % ( ids.O_TURRET_ACTIVATE, order.turret, order.activate )
            elif isinstance( order, OrderActivateShield ):
                dump = dump + ";%i:%i" % ( ids.O_CHARGE, order.activate )
            elif isinstance( order, OrderActivateRepair ):
                dump = dump + ";%i:%i" % ( ids.O_REPAIR, order.activate )
            elif isinstance( order, OrderSetRelation ):
                dump = dump + ";%i:%s:%i" % ( ids.O_RELATION, order.other, order.level )
            elif isinstance( order, OrderSelfDestruct ):
                dump = dump + ";%i" % ( ids.O_SELF_DESTRUCT )

        return dump

def CopyCOInput( input ):
    return COInput( input.xc, input.yc, input.wc, input.hc )

def LoadCOInput( text ):
    es = text.split(";")
    inputs = COInput( int(es[0]), int(es[1]), int(es[2]), int(es[3]) )
    if len(es[4:]) > 0:
      for e in es[4:]: #range(int(es[4])):
        os = e.split(":")
        if int(os[0]) == ids.O_MOVE:
     #       print "ordered to move"
            order = OrderMove( int(os[1]), int(os[2]), float(os[3]) )
        elif int(os[0]) == ids.O_STOP_MOVE:
            order = OrderStopMove( float(os[1]) )
        elif int(os[0]) == ids.O_RECALL_SHIPS:
     #       print "ordered to recall fighters"
            order = OrderRecallShips( int(os[1]) )
        elif int(os[0]) == ids.O_LAUNCH_SHIPS:
     #       print "ordered to launch fighters"
            order = OrderLaunchShips( int(os[1]) )
        elif int(os[0]) == ids.O_JUMP_NOW:
            order = OrderJumpNow()
        elif int(os[0]) == ids.O_JUMP:
            order = OrderJump( (int(os[1]), int(os[2])) )
        elif int(os[0]) == ids.O_LAUNCH_MISSILE:
            order = OrderLaunchMissile( int(os[1]), (int(os[2]), int(os[3])) )
        elif int(os[0]) == ids.O_ATTACK:
     #       print "attack %i" % int(os[1])
            order = OrderAttack( int(os[1]) )
        elif int(os[0]) == ids.O_ORBIT:
            order = OrderOrbit( int(os[1]) )
        elif int(os[0]) == ids.O_BUILD_TURRET:
            order = OrderBuildTurret( int(os[1]), int(os[2]) )
        elif int(os[0]) == ids.O_BUILD_SHIP:
            order = OrderBuildShip( int(os[1]), int(os[2]) )
        elif int(os[0]) == ids.O_BUILD_MISSILE:
            order = OrderBuildMissile( int(os[1]), int(os[2]) )
        elif int(os[0]) == ids.O_TURRET_ACTIVATE:
            order = OrderActivateTurret( int(os[1]), int(os[2]) )
        elif int(os[0]) == ids.O_CHARGE:
            order = OrderActivateShield( int(os[1]) )
        elif int(os[0]) == ids.O_REPAIR:
            order = OrderActivateRepair( int(os[1]) )
        elif int(os[0]) == ids.O_RELATION:
            order = OrderSetRelation( os[1], int(os[2]) )
        elif int(os[0]) == ids.O_SELF_DESTRUCT:
            order = OrderSelfDestruct()

    #    order = OrderMove( int(es[5+3*i]), int(es[6+3*i]), float(es[7+3*i]) )
        inputs.orders.append( order )
    return inputs


# objects -> client
class COObject:
    def __init__(self,type,xp,yp,zp,ori,uid,selectRadius,relation=ids.U_NEUTRAL):
        self.type = type
        self.xp = xp # int(xp+0.5)
        self.yp = yp # int(yp+0.5)
        self.zp = zp
        self.ori = ori

        self.uid = uid
        self.selectRadius = selectRadius
        self.relation = relation

    def dump(self):
      #  print ( self.type, self.xp, self.yp, self.zp, self.ori, self.uid, self.selectRadius, self.relation )
        dump = "%i;%i;%i;%i;%.2f;%i;%i;%i" % ( self.type, self.xp, self.yp, self.zp, self.ori, self.uid, self.selectRadius, self.relation )
        return dump
def LoadCOObject( text ):
    es = text.split(";")
    return COObject( int(es[0]), int(es[1]), int(es[2]), int(es[3]), float(es[4]), int(es[5]), int(es[6]), int(es[7]) )
class COObjects:
    def __init__(self,coobjects):
        self.coobjects = coobjects

    def dump(self):
        dumps = [ coobject.dump() for coobject in self.coobjects ]
        dump = ":".join(dumps)
        return dump
def LoadCOObjects( text ):
    bs = text.split(":")
    coobjects = []
    coobject = None
    for b in bs:
        try:
            coobject = LoadCOObject( b )
            coobjects.append( coobject )
        except Exception, ex:
            print "failed LoadCOOBject:", ex
    return COObjects( coobjects )


# stats -> client
class COPlayerStats:
    def __init__(self, gameTick, dead, ore, maxOre, energy, maxEnergy, shieldIntegrity, hullIntegrity, canJump, repairing, charging, hangarSpace, shipsSpace, missilesSpace, jumpCharge, jumpOverheat, oreInProcess, turrets, missiles, ships, radars ): # , buildableTurrets
         self.gameTick = gameTick
         self.dead = dead
         self.ore = ore
         self.maxOre = maxOre
         self.energy = energy
         self.maxEnergy = maxEnergy
         self.shieldIntegrity = shieldIntegrity
         self.hullIntegrity = hullIntegrity
         self.hangarSpace = hangarSpace
         self.shipsSpace = shipsSpace
         self.missilesSpace = missilesSpace
         self.oreInProcess = oreInProcess
         self.canJump = canJump
         self.jumpCharge = jumpCharge
         self.jumpOverheat = jumpOverheat
    #     self.xr = xr
    #     self.yr = yr
    #     self.maxRadar = maxRadar
         self.turrets = turrets
         self.missiles = missiles
         self.ships = ships
         self.radars = radars
      #   self.buildableTurrets = buildableTurrets

         self.repairing = repairing
         self.charging = charging

    def dump(self):
      if self.dead:
        dump = "%i" % ( self.gameTick )
      else:
        dump = "%i;%i;%i;%i;%i;%.2f;%.2f;%i;%i;%i;%i;%i;%i;%i;%i" % ( self.gameTick, self.ore, self.maxOre, self.energy, self.maxEnergy, self.shieldIntegrity, self.hullIntegrity, self.canJump, self.repairing, self.charging, self.hangarSpace, self.shipsSpace, self.missilesSpace, self.jumpCharge, self.jumpOverheat )

        dump = dump + ";"
        for oip in self.oreInProcess:
            dump = dump + "%i:"% oip

        dump = dump + ";"
        for turret in self.turrets:
            dump = dump + "%i:%i:%i:%.2f:%.2f:%i:%i:%i:%i:%i:%i:%i:%i:" % ( turret.type, turret.xp, turret.yp, turret.minAngle, turret.maxAngle, turret.buildPerc,turret.range,turret.on,turret.activable,turret.useEnergy,turret.useOre,turret.energyRebate, turret.oreRebate )
            for bt in turret.buildables:
                dump = dump + "%i_%i/" % ( bt.type, bt.canBuild ) # , bt.energyCost, bt.oreCost, bt.category )
            dump = dump + "|"

        dump = dump + ";"
        for ship in self.missiles:
            dump = dump + "%i:%i:%i:%i:%i:%i:%i|" % ( ship.type, ship.usable, ship.canLaunch, ship.nbr, ship.buildPerc, ship.canBuild, ship.show )

        dump = dump + ";"
        for ship in self.ships:
            dump = dump + "%i:%i:%i:%i:%i:%i:%i|" % ( ship.type, ship.usable, ship.canLaunch, ship.nbr, ship.buildPerc, ship.canBuild, ship.show )

      dump = dump + ";"
      for radar in self.radars:
          dump = dump + "%i:%i:%i|" % ( radar.xr, radar.yr, radar.range )

      return dump
    
def LoadCOPlayerStats( text ):
  es = text.split(";")
  oreInProcess = []
  turrets = []
  missiles = []
  ships = []
  buildableTurrets = []
  radars = []

  if len(es)==2: # dead
    for o in es[ 1 ].split("|"):
      if len( o ) > 0:
        i = o.split(":")
        radars.append( CORadar( (int(i[0]), int(i[1])), int(i[2]) ) )
    stats = COPlayerStats( int(es[0]), True, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0,0, 0, oreInProcess, turrets, missiles, ships, radars )
  else:
   # print text
    for o in es[ 15 ].split(":"): # range(co):
      if len( o ) > 0:
        oreInProcess.append( int(o) ) #  int(es[16+o]) )

    for o in es[ 16 ].split("|"):
      if len( o ) > 0:
        i = o.split(":")
        buildables = []
     #   print i
        for b in i[ 13 ].split("/"):
           if len( b ) > 0:
              bi = b.split("_")
      #        print bi
              buildables.append( COBuildable( int(bi[0]), int(bi[1]) ) )
        turrets.append( COTurret( int(i[0]), int(i[1]), int(i[2]), float(i[3]), float(i[4]), int(i[5]), int(i[6]), int(i[7]), int(i[8]), int(i[9]), int(i[10]), int(i[11]), int(i[12]), buildables ) )

    for o in es[ 17 ].split("|"):
      if len( o ) > 0:
        i = o.split(":")
        missiles.append( COShips( int(i[0]), int(i[1]), int(i[2]), int(i[3]), int(i[4]), int(i[5]), int(i[6]) ) )

    for o in es[ 18 ].split("|"):
      if len( o ) > 0:
        i = o.split(":")
        ships.append( COShips( int(i[0]), int(i[1]), int(i[2]), int(i[3]), int(i[4]), int(i[5]), int(i[6]) ) )

    for o in es[ 19 ].split("|"):
      if len( o ) > 0:
        i = o.split(":")
        radars.append( CORadar( (int(i[0]), int(i[1])), int(i[2]) ) )

    stats = COPlayerStats( int(es[0]), False, int(es[1]), int(es[2]), int(es[3]), int(es[4]), float(es[5]), float(es[6]), int(es[7]), int(es[8]), int(es[9]), int(es[10]), int(es[11]), int(es[12]), int(es[13]), int(es[14]), oreInProcess, turrets, missiles, ships, radars )

  return stats


class COPossible:
    def __init__( self, ship, race, nbrTurrets, speed, shield, hull, hangar, canJump, civilians ):
        self.ship = ship
        self.race = race
        self.nbrTurrets = nbrTurrets
        self.speed = speed
        self.shield = shield
        self.hull = hull
        self.hangar = hangar
        self.canJump = canJump
        self.civilians = civilians
class COPossibles:
    def __init__( self, ships ):
        self.ships = ships
    def dump(self):
        strings = [ "%i;%i;%i;%i;%i;%i;%i;%i;%i"%(ship.ship, ship.race, ship.nbrTurrets, ship.speed, ship.shield, ship.hull, ship.hangar, ship.canJump, ship.civilians) for ship in self.ships ]
        return ":".join( strings )
def LoadCOPossibles( text ):
    ss = text.split(":")
    ships = []
    for s in ss:
      if len( s ) > 0:
        es = s.split(";")
        ships.append( COPossible( int(es[0]), int(es[1]), int(es[2]), int(es[3]), int(es[4]), int(es[5]), int(es[6]), int(es[7]), int(es[8]) ) )
    return COPossibles( ships )


class COPlayer:
    def __init__( self, name, race, relIn, relOut, isHuman ):
        self.name = name
        self.race = race
        self.relIn = relIn
        self.relOut = relOut
        self.isHuman = isHuman
class COPlayers:
    def __init__( self, players ):
        self.players = players
    def dump(self):
        strings = [ "%s;%i;%i;%i;%i"%(player.name,player.race,player.relIn,player.relOut,player.isHuman) for player in self.players ]
        return ":".join( strings )
def LoadCOPlayers( text ):
    ss = text.split(":")
    players = []
    for s in ss:
      if len( s ) > 0:
    #    print s
        es = s.split(";")
        players.append( COPlayer( es[0], int(es[1]), int(es[2]), int(es[3]), int(es[4]) ) )
  #  print "loaded", players
    return COPlayers( players ) # COPlayers( [ es = s.split(";"); COPlayer( es[0], int(es[1]), int(es[2]), int(es[3]), int(es[4]) ) for s in ss ] )


class COTurret:
    def __init__( self, type, xp, yp, minAngle, maxAngle, buildPerc, range, on, activable, useEnergy, useOre, energyRebate, oreRebate, buildables ):
        self.type = type
        self.xp = xp
        self.yp = yp
        self.minAngle = minAngle
        self.maxAngle = maxAngle
        self.buildPerc = buildPerc
        self.range = range
        self.on = on
        self.activable = activable
        self.useEnergy = useEnergy
        self.useOre = useOre
        self.buildables = buildables

        self.energyRebate = energyRebate
        self.oreRebate = oreRebate

class COShips:
    def __init__( self, type, usable, canLaunch, nbr, buildPerc, canBuild, show ):
        self.type = type
        self.usable = usable
        self.canLaunch = canLaunch
        self.nbr = nbr
        self.buildPerc = buildPerc
        self.canBuild = canBuild
        self.show = show

class COBuildable:
    def __init__( self, type, canBuild ): # , energyCost, oreCost, category
        self.type = type
        self.canBuild = canBuild
      #  self.energyCost = energyCost
      #  self.oreCost = oreCost
      #  self.category = category

class COAstre:
    def __init__(self, type, xp, yp, radius=0 ):
         self.type = type
         self.xp = xp
         self.yp = yp
         self.radius = radius

    def dump(self):
        dump = "%i;%i;%i;%i;" % ( self.type, self.xp, self.yp, self.radius )
        return dump

class CORadar:
    def __init__( self, (xr,yr), range ):
        self.xr = xr
        self.yr = yr
        self.range = range

def LoadCOAstre( text ):
    es = text.split(";")
    co = int(es[4])
    return COAstre( int(es[0]), int(es[1]), int(es[2]), int(es[3]) )


class COGfxs:
    def __init__(self, gfxs ):
         self.gfxs = gfxs

    def dump(self):
        dump = "%i" % ( len(self.gfxs) )
    #    print len( self.gfxs )
        for gfx in self.gfxs:
            if isinstance( gfx, GfxLaser ):
                dump = dump + ";%i:%i:%i:%i:%i:%i:%i:%i" % (ids.G_LASER_SMALL, gfx.xp,gfx.yp,gfx.z,gfx.xd,gfx.yd, gfx.width, gfx.color)
       #         print "laser!"
            elif isinstance( gfx, GfxExplosion ):
                dump = dump + ";%i:%i:%i:%i:%i:%i" % (ids.G_EXPLOSION, gfx.xp,gfx.yp,gfx.radius,gfx.sound,gfx.delai)
      #          print "explosion!"
            elif isinstance( gfx, GfxShield ):
                dump = dump + ";%i:%i:%i:%i:%i:%.3f:%.3f" % (ids.G_SHIELD, gfx.xp,gfx.yp,gfx.radius,gfx.strength,gfx.angle,gfx.hit)
     #           print "shield!"
            elif isinstance( gfx, GfxExhaust ): # careful, GfxExhaust inherits of GfxFragment
                pass # TODO, removed because not used on client side
          #      dump = dump + ";%i:%i:%i:%i:%.2f:%.2f:%.2f:%.2f:%i" % (ids.G_EXHAUST, gfx.xp,gfx.yp,gfx.zp,gfx.ori,gfx.xi,gfx.yi,gfx.ri,gfx.type)
            elif isinstance( gfx, GfxFragment ):
                dump = dump + ";%i:%i:%i:%i:%.2f:%.2f:%.2f:%.2f:%i:%i" % (ids.G_FRAGMENT, gfx.xp,gfx.yp,gfx.zp,gfx.ori,gfx.xi,gfx.yi,gfx.ri,gfx.type,gfx.ttl)
    #            print "fragment!"
     #           print "shield"
        return dump

def LoadCOGfxs( text ): # TODO
    gfxs = []
    es = text.split(";")
    n = int(es[0])
    for e in es[1:]:
      #  print e
        ss = e.split(":")

        if int(ss[ 0 ]) == ids.G_LASER_SMALL:
            gfx = GfxLaser( (int(ss[1]),int(ss[2])), int(ss[3]), (int(ss[4]),int(ss[5])), int(ss[6]), int(ss[7]) )
        elif int(ss[ 0 ]) == ids.G_EXPLOSION:
            gfx = GfxExplosion( (int(ss[1]),int(ss[2])), int(ss[3]), int(ss[4]), int(ss[5]) )
        #    print "ex"
        elif int(ss[ 0 ]) == ids.G_SHIELD:
            gfx = GfxShield( (int(ss[1]),int(ss[2])), int(ss[3]), int(ss[4]), float(ss[5]), float(ss[6]) )
        elif int(ss[ 0 ]) == ids.G_FRAGMENT:
            gfx = GfxFragment( (int(ss[1]),int(ss[2])), int(ss[3]), float(ss[4]), float(ss[5]), float(ss[6]), float(ss[7]), int(ss[8]), int(ss[9]) )
        elif int(ss[ 0 ]) == ids.G_EXHAUST:
            gfx = GfxExhaust( (int(ss[1]),int(ss[2])), int(ss[3]), float(ss[4]), float(ss[5]), float(ss[6]), float(ss[7]) )
     #       print "fragment!"

        else: print int(ss[ 0 ])
        gfxs.append( gfx )
    return gfxs # COGfx( int(es[0]), int(es[1]), int(es[2]), int(es[3]) )



