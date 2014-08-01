from time import time

from . import Converter
from common.comms import * 
from server.players import Player, Human
from server.ships import FlagShip, ShipWithTurrets
from server.weapons import *
from common import utils
from server.stats import BuilderMissileStats

class RemoteConverter( Converter ):
    def convert( self, game, player ):
        (x0,y0,x1,y1) = (player.inputs.xc,player.inputs.yc, player.inputs.xc+player.inputs.wc, player.inputs.yc+player.inputs.hc)
        cobjs = []
        cobjs1 = []

        t0 = time()

       ## objects + harvestable (-astres)
        if player.flagship:
          for obj in game.objects.getWithin( player.flagship, player.flagship.getRadarRange() ):
            if obj.alive:
             if (obj.xp + obj.stats.maxRadius/2 >= x0 \
              and obj.xp - obj.stats.maxRadius/2 < x1 \
              and obj.yp + obj.stats.maxRadius/2 >= y0 \
              and obj.yp - obj.stats.maxRadius/2 < y1)\
              or obj.zp == -100:
                for cobj in obj.getCommObjects():
                    cobjs.append( (obj, cobj) )
             elif isinstance( obj, FlagShip ): 
         #     and utils.distBetweenObjects( player.flagship, obj ) <= player.flagship.getRadarRange():
                cs = obj.getCommObjects()
                cobjs.append( (obj, cs[0]) )

        t1 = time()
        game.uidsSent[ player ] = []
        for (k,(obj,cobj)) in enumerate( cobjs ):
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
                if game.getRelationBetween( obj.player, player ) < 0: 
                    cobj.relation = ids.U_ENNEMY
                else:
                    cobj.relation = ids.U_FRIENDLY

            game.uidsSent[ player ].append( obj )
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

                td = time()
                if turret.building:
                    buildPerc = 100*turret.build/turret.buildCost
                else:
                    buildPerc = -1
                    
                turrets.append( COTurret( t, x, y, turret.stats.minAngle+player.flagship.ori, turret.stats.maxAngle+player.flagship.ori, buildPerc, maxRange, turret.activated, activable, energyUse, oreUse, turret.energyRebate, turret.oreRebate, turret.buildingOptionsPossibles ) )

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
                ships.append( COShips( k, len(sy.docked)>0 or len(sy.away)>0, not player.flagship.ai.launching[ k ],  len(sy.docked) + len(sy.away), buildPerc, player.flagship.canBuild( game, k ), True ) )
                shipsSpace = shipsSpace + (len(sy.docked)+len(sy.away)) * game.stats[ k ].hangarSpaceNeed

            t5 = time()
           ## missiles
            missiles = []
            missilesSpace = 0
            for missile in player.race.missiles:
                hasTurret = False
                builder = isinstance( game.stats[ missile ], BuilderMissileStats )

                for t in player.flagship.turrets:
                    if t.install and t.install.stats.weapon and \
                        ( ( not builder and t.install.stats.weapon.projectile and t.install.stats.weapon.projectile.img == missile ) \
                        or ( builder and t.install.stats.special == ids.S_BUILDER and game.stats[ missile ].buildType in t.install.stats.specialValue ) ):
                            hasTurret = True
                            break

                if player.flagship.missiles[missile].building:
                    buildPerc = 100*player.flagship.missiles[missile].build/player.flagship.missiles[missile].buildCost
                else:
                    buildPerc = -1

                missiles.append( COShips( missile,  missile != ids.M_NORMAL and missile != ids.M_AI and missile != ids.M_LARVA and missile != ids.M_EVOLVED and hasTurret, player.flagship.missiles[missile].amount>0, player.flagship.missiles[missile].amount, buildPerc, hasTurret and player.flagship.canBuild( game, missile ), hasTurret or player.flagship.missiles[missile].amount > 0 ) ) # TODO Remove hack to identify "usable missile"
                missilesSpace = missilesSpace + player.flagship.missiles[missile].amount* game.stats[ missile ].hangarSpaceNeed

            t6 = time()
            radars = [ CORadar( (player.flagship.xp, player.flagship.yp), player.flagship.getRadarRange() ) ]
            
           ## stats if flagship
            if player.flagship.stats.maxShield:
                shieldStrength = player.flagship.shield/player.flagship.stats.maxShield
            else:
                shieldStrength = 0
                
            # detect dangers in radar
            ennemyInRadar = False
            dangerInRadar = False
            for obj in game.objects.getWithinRadius( player.flagship.pos, player.flagship.getRadarRange() ):
                if obj.player and (game.getRelationBetween( obj.player, player ) < 0 or game.getRelationBetween( player, obj.player ) < 0 ):
                    ennemyInRadar = True
                    if dangerInRadar:
                        break
                elif isinstance( obj, NukeMissile ) or isinstance( obj, Mine ):
                    dangerInRadar = True
                    if ennemyInRadar:
                        break
                
                
            pstats = COPlayerStatus( game.tick, False, player.flagship.ore, player.flagship.stats.maxOre, player.flagship.energy, player.flagship.stats.maxEnergy, 
shieldStrength, player.flagship.hull/player.flagship.stats.maxHull,  player.flagship.canJump( game ),
player.flagship.repairing, player.flagship.charging, player.flagship.getHangarSpace(), shipsSpace, missilesSpace, 100*player.flagship.jumpCharge/player.flagship.jumpChargeDelay, 100*player.flagship.jumpRecover/player.flagship.jumpRecoverDelay, oreProcess, turrets, missiles, ships, radars, ennemyInRadar, dangerInRadar )
            t7 = time()

        else:
           ## stats if flagship dead
            pstats = COPlayerStatus( game.tick, True, 0, 0, 0, 0, 
                0, 0,  0,
                0, 0, 0, 0, 0, 0, 0,
                [], [], [], [], [ CORadar( (0, 0), 1000 ) ] )

        t8 = time()
       ## fxs
        fxs = []
        for fx in game.newGfxs:
            if (fx.xp + fx.maxRadius >= x0 \
              and fx.xp - fx.maxRadius < x1 \
              and fx.yp + fx.maxRadius >= y0 \
              and fx.yp - fx.maxRadius < y1):
                fxs.append( fx )

        t9 = time()
       ## other players and relations 
        players = []
        if player.needToUpdateRelations:
            player.needToUpdateRelations = False
            for p in game.players:
                if player != p:
                    cop = COPlayer( p.name, p.race.type, (game.getRelationBetween(p, player)+100)/2, (game.getRelationBetween(player, p)+100)/2, isinstance( p, Human ) )
                    players.append( cop )

        t10 = time()
       ## possible ships to select
        possibles = []
        if player.needToUpdatePossibles:
            player.needToUpdatePossibles = False
            for p,c in game.stats.PlayableShips.items():
            #   c = stats.PlayableShips[ p ]
               if player.points >= c.points:
                 possibles.append( COPossible( c.stats.img, c.race.type, c.turrets, c.speed, c.shield, c.hull, c.hangar, c.canJump, c.civilians  ) )
            
        t11 = time()
       ## astres
        astres = []
        if player.needToUpdateAstres:
            # sending astres
            player.needToUpdateAstres = False
            for obj in utils.mY( game.astres, game.harvestables.objects ):
                for cobj in obj.getCommObjects():
                    cobj.relation = ids.U_ORBITABLE # NEUTRAL
                    cobj.uid = 0 #  ids.U_ORBITABLE
                    astres.append( cobj )

        t12 = time()
        t = t12 - t0
        
        
       ### messages
        msgs = []
        for msg in player.msgs+game.scenario.msgs:
            msgs.append( (msg.sender, msg.sentAt, msg.receivedAt, msg.text) )
        player.msgs = []
        
       # for msg in self.game.scenario.msgs:
       #     msgs.append( (msg[0], game.tick, game.tick, msg[1]))
        game.scenario.msgs = [] # assumes only one player
        
     #   if player.flagship:
     #       print "dt=%.3f getObjects=%i%% uids=%i%% ore=%i%% turrets=%i%% smallships=%i%% missiles=%i%% stats=%i%% fxs=%i%% possibles=%i%% players=%i%% astres=%i%% fin=%i%%" % (t, (t1-t0)*100/t, (t2-t1)*100/t, (t3-t2)*100/t, (t4-t3)*100/t, (t5-t4)*100/t, (t6-t5)*100/t, (t7-t6)*100/t, (t8-t7)*100/t, (t9-t8)*100/t, (t10-t9)*100/t, (t11-t10)*100/t, (t12-t11)*100/t)
            
        return (cobjs1, pstats, COGfxs( fxs ), players, astres, possibles, msgs )
