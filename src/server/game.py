from time import time
from random import randint

from players import *
from ships import * # Ship, FlagShip, Turret
from objects import Object, Asteroid, Planet, Sun, Nebula, BlackHole
from weapons import *
from ais import *
from common.comms import * # COPlayerStats, COGfxs, COTurret, COShips, COBuildable, CORadar, COPlayer, COPlayers
from common.utils import distBetweenObjects
from common import utils
from common.orders import *
from common.gfxs import * # temp
from common import ids
from common import config
import stats

# TODO refactoring: inconsistency in responsability over object -> cobject, with network

class Game:
    def __init__(self, scenarioType ):

        self.players = []

        self.objects = []
        self.astres = []
        self.harvestables = []

        self.newGfxs = []
        self.relations = {}

        self.tick = 0

        self.uidsSent = {}

      ### loading world according to scenario
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
        for o0 in utils.mY( self.objects, self.astres ): # self.objects: , self.harvestables
          if o0.alive:
            t0 = time()
            ( addedObjectsLocal, removedObjectsLocal, addedGfxsLocal ) =  o0.doTurn( self )

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
        self.objects = self.objects + addedObjects


        if not self.tick%(config.fps*5):

            ## calm tensions between computers and players
            for p0 in self.players:
             if not isinstance( p0, Computer ):
                for p1 in self.players:
                 if isinstance( p1, Computer ):
                    rel = self.getRelationBetween( p1, p0 )
                    if rel < stats.Relations[ p1.race ][ p0.race ]:
                       self.setRelationBetween( p1, p0, rel + 1)
                 #      self.setRelationBetween( p0, p1, rel + 1)

       ### Scenario balancing
        self.scenario.doTurn( self )

        self.newGfxs = addedGfxs

       ### advance frame count
        self.tick = self.tick + 1


    def getUpdates(self,player ):
        (x0,y0,x1,y1) = (player.inputs.xc,player.inputs.yc, player.inputs.xc+player.inputs.wc, player.inputs.yc+player.inputs.hc)
        cobjs = []
        cobjs1 = []
    #    print (x0,y0,x1,y1)

        t0 = time()

       ## objects + harvestable (-astres)
        if player.flagship:
          for obj in utils.mY( self.objects ): #, self.harvestables ): # , self.astres ):
            if obj.alive:
             if (obj.xp + obj.stats.maxRadius/2 >= x0 \
              and obj.xp - obj.stats.maxRadius/2 < x1 \
              and obj.yp + obj.stats.maxRadius/2 >= y0 \
              and obj.yp - obj.stats.maxRadius/2 < y1)\
              or obj.zp == -100:
                for cobj in obj.getCommObjects():
                    cobjs.append( (obj, cobj) )
             elif isinstance( obj, FlagShip ) \
              and distBetweenObjects( player.flagship, obj ) <= player.flagship.getRadarRange():
                cs = obj.getCommObjects()
                cobjs.append( (obj, cs[0]) )

        t1 = time()
        self.uidsSent[ player ] = []
        for (k,(obj,cobj)) in enumerate( cobjs ): #zip( xrange(len(cobjs)), cobjs ):
            cobj.uid = k
            if obj == player.flagship:
                cobj.relation = ids.U_FLAGSHIP
            # missile, sun or blackhole
            elif player.flagship and ( \
                    isinstance( obj, Mine ) or \
                    isinstance( obj, NukeMissile ) or \
                    isinstance( obj, PulseMissile ) ):
                    # TODO apply sun and black hole rule, doewn't work for now because astres are sent seperatly
                  #  (isinstance( obj, Sun ) and utils.distLowerThanObjects( player.flagship, obj, obj.stats.damageRadius) or \
                  #  (isinstance( obj, BlackHole ) and utils.distLowerThanObjects( player.flagship, obj, obj.stats.gravitationalRadius ) ) ) ):
                cobj.relation = ids.U_DEADLY
            elif obj.player == player:
                cobj.relation = ids.U_OWN
            elif obj.stats.orbitable:
                cobj.relation = ids.U_ORBITABLE
            elif obj.player == None:
                cobj.relation = ids.U_NEUTRAL
            elif obj.player != player:
                if self.getRelationBetween( obj.player, player ) < 0: 
                    cobj.relation = ids.U_ENNEMY
                else:
                    cobj.relation = ids.U_FRIENDLY

            self.uidsSent[ player ].append( obj )
            cobjs1.append( cobj )
            
        t2 = time()
        if player.flagship:
            oreProcess = [0]*20
            for ob in player.flagship.oreProcess:
                p = int(len(oreProcess)*ob.pos / player.flagship.processLength)
                oreProcess[ p ] = oreProcess[ p ] + ob.amount

            t3 = time()
           ## turrets
            turrets = []
            for turret in player.flagship.turrets:
                if turret.building:
                    t = turret.building.type
                    activable = False
                elif turret.install:
                    t = turret.install.stats.type
                    activable = (turret.install.stats.orePerFrame>0 or turret.install.stats.energyPerFrame>0 or turret.install.stats.energyPerUse>0 or turret.install.stats.orePerUse>0 or ( turret.install.stats.weapon!=None and turret.install.stats.ai == ids.TA_COMBAT_STABLE )) # TODO find better representation than ids.TA_COMBAT_STABLE || weapon.img == ids.W_MISSILE ))
                else:
                    t = 0
                    activable = False

                if turret.install and turret.activated:
                    energyUse = turret.install.stats.energyPerFrame or turret.install.stats.energyPerUse
                    oreUse = turret.install.stats.orePerFrame or turret.install.stats.orePerUse
                else:
                    energyUse = False
                    oreUse = False

                (x,y) = player.flagship.getTurretPos( turret )
                maxRange = 0
                if turret.weapon:
                    maxRange =  turret.weapon.stats.maxRange

                if turret.building:
                    buildPerc = 100*turret.build/turret.buildCost
                    energyRebate = turret.building.energyCostToBuild
                    oreRebate = turret.building.oreCostToBuild
                else:
                    buildPerc = -1
                    energyRebate = 0
                    oreRebate = 0

                buildables = []

             #   print player.race.turrets
                options = [o for o in player.race.turrets]

                if turret.install:
                    for option in turret.install.stats.overs+[turret.install.stats]:
                    #    print turret.install.stats.type, option.type, turret.install.stats.overs+[turret.install.stats]
                        options.remove( option )
                    #removedOptions = turret.install.stats.overs+[turret.install.stats]
                elif turret.building:
                    for option in turret.building.overs: # +[turret.building]:
                      if option != turret.building.upgradeFrom:
                        options.remove( option )
                    
                    #removedOptions = turret.building.overs+[turret.building]

                for bt in options: #player.race.turrets:
                  
              #-    if bt.upgradeFrom and turret.install and turret.install.stats == bt: # obsolete upgrade, doesn't care about building->allows cancel
              #        removedOptions.append( bt.upgradeFrom )

              #    if not bt in removedOptions or (turret.building and bt == turret.building.upgradeFrom):
                    if turret.install and turret.install.stats == bt.upgradeFrom: # upgradable
                        buildables.append( COBuildable( bt.type, player.flagship.energy >= bt.energyCostToBuild-energyRebate and player.flagship.ore >= bt.oreCostToBuild-oreRebate)) #, bt.energyCostToBuild, bt.oreCostToBuild, bt.category ) )
                   #     removedOptions.append( turret.install.stats )
                    elif (turret.install and turret.install.stats == bt) or (turret.building and turret.building == bt): # already there
                        buildables.append( COBuildable( bt.type, False )) #, bt.energyCostToBuild, bt.oreCostToBuild, bt.category ) )
                    elif not bt.upgradeFrom: # otherwise, not an upgrades
                        buildables.append( COBuildable( bt.type, player.flagship.energy >= bt.energyCostToBuild-energyRebate and player.flagship.ore >= bt.oreCostToBuild-oreRebate )) # , bt.energyCostToBuild, bt.oreCostToBuild, bt.category ) )
                if turret.building or turret.install:
                    buildables.append( COBuildable( 0, True )) # , -1*energyRebate, -1*oreRebate, ids.C_OTHER ) )
               
                turrets.append( COTurret( t, x, y, turret.stats.minAngle+player.flagship.ori, turret.stats.maxAngle+player.flagship.ori, buildPerc, maxRange, turret.activated, activable, energyUse, oreUse, energyRebate, oreRebate, buildables ) )

            t4 = time()
           ## small ships
            ships = []
            shipsSpace = 0
            for k in player.race.ships: 
                k = k.img
                sy = player.flagship.shipyards[ k ]
                if sy.building:
                    buildPerc = sy.build*100/sy.buildCost
                else:
                    buildPerc = -1
                ships.append( COShips( k, len(sy.docked)>0 or len(sy.away)>0, not player.flagship.ai.launching[ k ],  len(sy.docked) + len(sy.away), buildPerc, player.flagship.canBuild( k ), True ) )
                shipsSpace = shipsSpace + (len(sy.docked)+len(sy.away)) * stats.statsDict[ k ].hangarSpaceNeed

            t5 = time()
           ## missiles
            missiles = []
            missilesSpace = 0
            for missile in player.race.missiles:
                hasTurret = False
                for t in player.flagship.turrets:
                    if t.install and t.install.stats.weapon and t.install.stats.weapon.projectile and t.install.stats.weapon.projectile.img == missile:
                        hasTurret = True
                        break

                if player.flagship.missiles[missile].building:
                    buildPerc = 100*player.flagship.missiles[missile].build/player.flagship.missiles[missile].buildCost
                else:
                    buildPerc = -1

                missiles.append( COShips( missile,  missile != ids.M_NORMAL and hasTurret, player.flagship.missiles[missile].amount>0, player.flagship.missiles[missile].amount, buildPerc, hasTurret and player.flagship.canBuild( missile ), hasTurret ) )
                missilesSpace = missilesSpace + player.flagship.missiles[missile].amount*stats.statsDict[ missile ].hangarSpaceNeed

            t6 = time()
            radars = [ CORadar( (player.flagship.xp, player.flagship.yp), player.flagship.getRadarRange() ) ]
            
           ## stats if flagship
            pstats = COPlayerStats( self.tick, False, player.flagship.ore, player.flagship.stats.maxOre, player.flagship.energy, player.flagship.stats.maxEnergy, 
player.flagship.shield/player.flagship.stats.maxShield, player.flagship.hull/player.flagship.stats.maxHull,  player.flagship.canJump( self ),
player.flagship.repairing, player.flagship.charging, player.flagship.getHangarSpace(), shipsSpace, missilesSpace, 100*player.flagship.jumpCharge/player.flagship.jumpChargeDelay, 100*player.flagship.jumpRecover/player.flagship.jumpRecoverDelay, oreProcess, turrets, missiles, ships, radars )
            t7 = time()

            t = t7 - t0
           # print "objects: %.2f uids: %.2f flagship: %.2f turrets: %.2f ships: %.2f missiles: %.2f init: %.2f"%((t1-t0)/t,(t2-t1)/t,(t3-t2)/t,(t4-t3)/t,(t5-t4)/t,(t6-t5)/t,(t7-t5)/t)
        else:
           ## stats if flagship dead
            pstats = COPlayerStats( self.tick, True, 0, 0, 0, 0, 
0, 0,  0,
0, 0, 0, 0, 0, 0, 0,
[], [], [], [], [ CORadar( (0, 0), 1000 ) ] )

       ## fxs
        fxs = []
        for fx in self.newGfxs:
            if (fx.xp + fx.maxRadius >= x0 \
              and fx.xp - fx.maxRadius < x1 \
              and fx.yp + fx.maxRadius >= y0 \
              and fx.yp - fx.maxRadius < y1):
                fxs.append( fx )

       ## other players and relations 
        players = []
        if player.needToUpdateRelations:
            player.needToUpdateRelations = False
            for p in self.players:
                if player != p:
                    cop = COPlayer( p.name, p.race.type, (self.getRelationBetween(p, player)+100)/2, (self.getRelationBetween(player, p)+100)/2, isinstance( p, Human ) )
                    players.append( cop )

       ## possible ships to select
        possibles = []
        if player.needToUpdatePossibles:
            player.needToUpdatePossibles = False
            for p,c in stats.PlayableShips.items():
            #   c = stats.PlayableShips[ p ]
               print c.stats.img, player.points, c.points
               if player.points >= c.points:
                 possibles.append( COPossible( c.stats.img, c.race.type, c.turrets, c.speed, c.shield, c.hull, c.hangar, c.canJump, c.civilians  ) )
            
       ## astres
        astres = []
        if player.needToUpdateAstres:
            # sending astres
            player.needToUpdateAstres = False
            for obj in utils.mY( self.astres, self.harvestables ): # self.astres:
                for cobj in obj.getCommObjects():
                    cobj.relation = ids.U_ORBITABLE # NEUTRAL
                    cobj.uid = 0 #  ids.U_ORBITABLE
                    astres.append( cobj )

        return (cobjs1, pstats, COGfxs( fxs ), players, astres, possibles )

    def getBrief( self, player ):
        cobjs = []
        for obj in self.objects:
            cobjs.append( (obj, cobj) )

    def addRemotePlayer(self, username, password ):
        player = Human( stats.R_HUMAN, username, password )
        self.addPlayer( player )
        self.uidsSent[ player ] = []

        return player

    def giveShip( self, player, shipId ):
      if not player.flagship and player.points >= stats.PlayableShips[ shipId ].points:
        self.scenario.spawn( self, player, shipId )
      else:
          raise Exception( "giveShip aborted, already has ship (%s) or selected ship unplayable (%s)." % (not player.flagship, player.points >= stats.PlayableShips[ shipId ].points)  )

    def addPlayer( self, player ):
        self.relations[ player ] = {}
        for other in self.players:
            if isinstance( other, Human ):
                other.needToUpdateRelations = True
            if isinstance( player, Computer ) or isinstance( other, Computer ):
                self.relations[ player ][ other ] = stats.Relations[ player.race ][ other.race ]
                self.relations[ other ][ player ] = stats.Relations[ other.race ][ player.race ]
            else: ## if both are human players
                self.relations[ player ][ other ] = 20
                self.relations[ other ][ player ] = 20

        self.players.append( player )

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
            return self.relations[ p0 ][ p1 ]

    def setRelationBetween( self, p0, p1, rel=20 ): 
        if p0 and p1 and p0 != p1 and (isinstance( p0, Human ) or isinstance( p1, Human )):
            if isinstance( p0, Human ):
                p0.needToUpdateRelations = True
            if isinstance( p1, Human ):
                p1.needToUpdateRelations = True

            self.relations[ p0 ][ p1 ] = rel


    def saveToDisk( self, path ):
        pass

    def loadFromDisk( self, path ):
        pass

    def addShip( self, stat, ai, pos=None ):
        pass
        
    def executeCode( self, code ):
        eval( code )

