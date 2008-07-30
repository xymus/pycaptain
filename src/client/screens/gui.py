from math import pi, sqrt, cos, sin, hypot
from random import randint, random, choice
from time import time

from client.mixer import Mixer
from client.controls import *
from client.specialcontrols import *
from client.specialcontrols.gui import OldSelfDestructControl, SelfDestructControl, GameMenuControl, RadarControl, JumpControl, ChatControl, HangarControl
#from client.inputs import DisplayInput
from common.utils import *
from common import utils
from common.orders import *
from common.gfxs import *
from common.comms import COObject
from common import ids
from common import config

def ihypot( h, c ):
    i = h*h - c*c
    if i > 0:
        return sqrt( i )
    else:
        return 0

class Gui( ControlFrame ):
    def __init__( self, display, mixer, imgs, snds, texts, prefs, stats=None, eQuit=None, eSave=None, eScreenshot=None, eFullscreen=None ):
        ControlFrame.__init__( self )
        self.display = display
        self.mixer = mixer

        self.imgs = imgs
        self.snds = snds
        self.texts = texts
        self.prefs = prefs
        self.stats = stats
        
        self.eQuit = eQuit

        self.butCharge = RectControl( self.imgs.uiButCharge, (self.display.resolution[0]-58,96), (59,22), self.eChargeActivate)
        self.butCharge.stickLeft = False
        self.butRepair = RectControl( self.imgs.uiButRepair, (self.display.resolution[0]-59,self.display.resolution[1]-99-22), (58,22), self.eRepairActivate)
        self.butRepair.stickLeft = False
        self.butRepair.stickTop = False
        self.ctrlRelation = RoundControl(None, (34, self.display.resolution[1]-108), 68, self.eSetRelation)
        
        self.ctrlGameMenu = GameMenuControl( self.imgs, eQuitToMenu=eQuit, eSaveGame=eSave, eToggleFullscreen=eFullscreen )
        self.ctrlRadar = RadarControl( self.imgs, self.eRadarFullscreen, self.eRadarFullscreen, fUpdateCamera=self.fUpdateCamera )
        self.ctrlSelfDestruct = OldSelfDestructControl( self.imgs, (0, self.display.resolution[1]*2/5), self.eSelfDetruct )
       # self.ctrlSelfDestruct = SelfDestructControl( self.imgs, self.ctrlRadar.center, self.eSelfDetruct )
        self.ctrlJump = JumpControl( self.imgs, (self.display.resolution[0]/2+100,30), fJump=self.fJump )
        self.ctrlChat = ChatControl( self.imgs, (50, self.display.resolution[1]), 
            fBroadcast=self.fBroadcast, fDirectedCast=self.fDirectedCast, eOpen=self.eChatOpen, eClose=None )
        self.ctrlHangar = HangarControl( self.imgs, (self.display.resolution[0]/2,self.display.resolution[1]), 
            eLaunchMissile=self.launchMissile, eLaunchShip=self.launchShips, eRecallShip=self.recallShips, eBuildShip=self.buildShip, eBuildMissile=self.buildMissile )
        self.ctrlHangar.stickTop = False

        self.controlsMain = [#self.butCallFighters,
                         # self.butCallHarvesters,
                          self.butRepair,
                          self.butCharge,
                    #      self.ctrlRelation,
                          self.ctrlSelfDestruct,
                          self.ctrlJump,
                          self.ctrlChat,
                          self.ctrlRadar,
                          self.ctrlHangar,
                          self.ctrlGameMenu,
                          KeyCatcher( eSave, letter="s" ),
                          KeyCatcher( eQuit, letter="q" ),
                          KeyCatcher( eScreenshot, letter="p" ),
                          KeyCatcher( eFullscreen, letter="f" ) ]
        self.controls = self.controlsMain

        self.msgsTTL = 15

        self.camera = ( 0, 0 )
        self.cameraSpeed = 10

        self.backgroundDiv = 20

        self.shieldAngle = pi/12

        self.perspective = 2
        self.zv = 200

        self.oreMaxs = []

        self.categories = {
			ids.T_LASER_SR_0	: 2,
			ids.T_LASER_SR_1	: 2,
			ids.T_LASER_MR_0 	: 2,
			ids.T_LASER_MR_1 	: 2,
			ids.T_MASS_MR_0		: 2,
			ids.T_MASS_MR_1		: 2,
			ids.T_MASS_SR_0 	: 2,
			ids.T_MASS_SR_1 	: 2,
			ids.T_MASS_SR_2 	: 2,
			ids.T_MASS_LR 		: 2,
			ids.T_MISSILES_0 	: 2,
			ids.T_MISSILES_1 	: 2,
			ids.T_MISSILES_2 	: 2,

			ids.T_NUKE	 	: 1,
			ids.T_PULSE 		: 1,
			ids.T_MINER 		: 1,
			ids.T_COUNTER 		: 1,

			ids.T_INTERDICTOR 	: 0,
			ids.T_RADAR 		: 0,
			ids.T_GENERATOR 	: 0,
			ids.T_SOLAR_0 		: 0,
			ids.T_SOLAR_1 		: 0,
			ids.T_SOLAR_2 		: 0,
			ids.T_HANGAR 		: 0,
			ids.T_REPAIR 		: 0,
			ids.T_SHIELD_RECHARGE 	: 0,
			ids.T_MAXSHIELD 	: 0,
			ids.T_BIOSPHERE		: 0,
			ids.T_BIOSPHERE_1	: 0,
			ids.T_INERTIA		: 0,
			ids.T_SUCKER		: 0,
			ids.T_SAIL_0		: 0,
			ids.T_SAIL_1		: 0,
			ids.T_SAIL_2		: 0,
			ids.T_JAMMER		: 0,

			ids.T_AI_FLAK_0	    : 2,
			ids.T_AI_FLAK_1	    : 2,
			ids.T_AI_FLAK_2	    : 2,
			ids.T_AI_FLAK_3	    : 2,
			ids.T_AI_OMNI_LASER_0	: 2,
			ids.T_AI_OMNI_LASER_1	: 2,
			ids.T_AI_MISSILE_0	: 2,
			ids.T_AI_MISSILE_1	: 2,
			ids.T_AI_MISSILE_2	: 2,
			ids.T_AI_MISSILE_3	: 2,
			
			ids.T_AI_CRYPT_0	: 0,
			ids.T_AI_CRYPT_1	: 0,
			ids.T_AI_CRYPT_2	: 0,
			ids.T_AI_CRYPT_3	: 0,
			           
			ids.T_ESPHERE_0 	: 2,
			ids.T_ESPHERE_1 	: 2,
			ids.T_ESPHERE_2 	: 2,
			ids.T_BURST_LASER_0 	: 2,
			ids.T_BURST_LASER_1 	: 2,
			ids.T_BURST_LASER_2 	: 2,
			ids.T_OMNI_LASER_0 	: 2,
			ids.T_OMNI_LASER_1 	: 2,
			ids.T_OMNI_LASER_2 	: 2,
			ids.T_SUBSPACE_WAVE_0 	: 2,
			ids.T_SUBSPACE_WAVE_1 	: 2,
			
			ids.T_DARK_EXTRACTOR_0 		: 0,
			ids.T_DARK_EXTRACTOR_1 		: 0,
			ids.T_DARK_ENGINE_0 		: 0,
			
            ids.T_EVOLVED_MISSILE_0 	: 2,
            ids.T_EVOLVED_MISSILE_1 	: 2,
            ids.T_EVOLVED_PULSE 	    : 1,
            ids.T_EVOLVED_COUNTER    	: 1,

			ids.T_DISCHARGER_0 	: 2,
			ids.T_DISCHARGER_1 	: 2,
			ids.T_REPEATER_0 	: 2,
			ids.T_REPEATER_1 	: 2,
			ids.T_REPEATER_2 	: 2,
			ids.T_REPEATER_3 	: 2,
			ids.T_NOMAD_CANNON_0 	: 2,
			ids.T_NOMAD_CANNON_1 	: 2,
			ids.T_NOMAD_CANNON_2 	: 2,
			ids.T_NOMAD_MISSILE_0 	: 2,
			ids.T_NOMAD_MISSILE_1 	: 2,
			ids.T_NOMAD_SUCKER_0 	: 0,
			ids.T_NOMAD_SUCKER_1 	: 0,
			ids.T_NOMAD_SUCKER_2 	: 0,

			0	: 0,
			-1	: 0}
    #    self.ctr = ( 78, 26 )

    #    self.notToBeRotated = [ ids. ]

        self.sPlayerPos = None
        self.sPlayer = None
        self.sPlayerLength = 0

        self.laserColors = { ids.R_HUMAN: (255,0,0,0),
                             ids.R_AI: (0,255,0,0),
                     
                             ids.R_NOMAD: (255,255,255,0),
                             ids.R_EXTRA: (127,127,0,0),
                             ids.R_EVOLVED: (0,255,0,0) }
                             
        self.informAbout = None
        
        self.anchorBottom = display.resolution[0]/2
        self.orders = []
        
        self.reset()
        
    def reset( self ):
        self.butsShipLaunch = []
        self.butsMissileLaunch = []
        self.butsShipBuild = []
        self.butsMissileBuild = []
        self.butsBuildTurret = []
        self.butsBuildOption = []
        self.butsActivate = []
        self.ctrlsBuildGauge = []
        
        self.fullscreenRadar = False
        self.msgs = []
        self.oreMaxs = []
        
        self.aim = None
        self.build = None
        self.quit = False
        self.lastStats = None
        self.centeredOnShip = True
        
        ControlFrame.reset(self)

    def getViewportPos( self, (x,y), z=0 ):
            (x,y) = ( x-self.camera[0], self.display.resolution[1]-(y-self.camera[1]) )
            dx = x - self.display.resolution[0]/2
            dy = y - self.display.resolution[1]/2
            x = self.display.resolution[0]/2 + dx * self.zv /(self.zv-z)
            y = self.display.resolution[1]/2 + dy * self.zv /(self.zv-z)
            return (x,y)

    def getVirtualPos( self, (x,y) ):
      if self.fullscreenRadar:
        dx = dy = max( float(config.universeWidth)*2/self.display.resolution[0], float(config.universeHeight)*2/ self.display.resolution[1] )
        return ( (x-self.display.resolution[0]/2)*dx, (-1*y+self.display.resolution[1]/2)*dy )
      else:
        return ( x+self.camera[0], -1*y+self.display.resolution[1]+self.camera[1] )

    def drawObject( self, obj ):
        if obj.type in self.imgs.notToRotate:
            ori = 0
        else:
            ori = obj.ori
        alpha = 1

        self.display.drawRoIfIn( self.imgs[ obj.type ], self.getViewportPos( (obj.xp, obj.yp ), obj.zp ), ori, self.display.resolution, alpha )

    def drawGfx( self, gfx ):

        if isinstance( gfx, GfxLaser ): # (255,0,0,int(255*gfx.intensity))
            self.display.drawLine( self.laserColors[ gfx.color ], self.getViewportPos((gfx.xp,gfx.yp)), self.getViewportPos((gfx.xd,gfx.yd)), gfx.width)

        elif isinstance( gfx, GfxExplosion ):
          if gfx.delai == 0:
            self.display.drawCircle( (255,255,255,255),  self.getViewportPos((gfx.xp,gfx.yp)), gfx.radius )
            if gfx.sound:
                self.mixer.play( self.snds[ gfx.sound ] )
                
        elif isinstance( gfx, GfxJump ):
          if gfx.delai == 0:
            self.display.drawCircle( (255,255,255,255),  self.getViewportPos((gfx.xp,gfx.yp)), gfx.radius ) 
            self.display.drawLine( (255,255,255,255), self.getViewportPos((gfx.xp,gfx.yp)), self.getViewportPos((gfx.xp+2*gfx.radius*cos(gfx.angle),gfx.yp+2*gfx.radius*sin(gfx.angle))), 4 )
            self.mixer.play( self.snds[ ids.S_EX_JUMP ] )

        elif isinstance( gfx, GfxLightning ):
            if gfx.delai == 0:
                self.display.drawRo( self.imgs[ ids.G_LIGHTNING ], self.getViewportPos((gfx.xp,gfx.yp)), atan2( gfx.yd-gfx.yp, gfx.xd-gfx.xp ) )
            self.display.drawLine( (255,255,255,255), self.getViewportPos((gfx.xp,gfx.yp)), self.getViewportPos((gfx.xd,gfx.yd)), gfx.strength)
            if gfx.sound:
                self.mixer.play( self.snds[ gfx.sound ] )

        elif isinstance( gfx, GfxShield ):
        #    self.display.drawCircle( (0,0,255,255),  self.getViewportPos((gfx.xp,gfx.yp)), gfx.radius, 1 )
            arca = gfx.hit*self.shieldAngle
        #    print gfx.angle - arca, gfx.angle + arca
            self.display.drawArc( (65,65,255,255),  self.getViewportPos((gfx.xp,gfx.yp)), gfx.radius, gfx.angle - arca, gfx.angle + arca, 2 )

        elif isinstance( gfx, GfxExhaust ):
            pass
     #       gfx.type = choice( imgs.exhausts )
 #           self.drawObject( gfx )

        elif isinstance( gfx, GfxFragment ):
            self.drawObject( gfx )

    def draw(self, display ): # self.objects,self.astres,self.gfxs,self.playerStatus,self.players, self.lag):
        if self.playerStatus:
            self.playerStatus.xr = self.playerStatus.radars[0].xr
            self.playerStatus.yr = self.playerStatus.radars[0].yr
            self.playerStatus.maxRadar = self.playerStatus.radars[0].range
            self.lastStats = self.playerStatus
        elif self.lag > 1: # network troubles
            self.playerStatus = self.lastStats

        if not self.playerStatus:
            return None

        self.ctrlsBuildGauge = []
        if self.centeredOnShip:
            self.camera = ( self.playerStatus.xr-self.display.resolution[0]/2,
                            self.playerStatus.yr-self.display.resolution[1]/2 )

        if self.fullscreenRadar:
            d = max( float(config.universeWidth)*2/self.display.resolution[0], float(config.universeHeight)*2/ self.display.resolution[1] )
            screenVirtualSize = (-d*self.display.resolution[0]/2,-d*self.display.resolution[1]/2,
                                d*self.display.resolution[0],d*self.display.resolution[1])
        else: #if not self.fullscreenRadar:
            screenVirtualSize = (self.camera[0],self.camera[1],self.display.resolution[0],self.display.resolution[1])
            
        self.ctrlJump.update( screenVirtualSize, canRegularJump=self.playerStatus.canJump )
        self.ctrlChat.update( screenVirtualSize )
        self.ctrlHangar.update( self.playerStatus, screenVirtualSize )
            
        if not self.fullscreenRadar:
        
            ### background
            bgw = self.display.getWidth(self.imgs.background)
            bgh = self.display.getHeight(self.imgs.background)
            bgx = (-1*(self.camera[0]/self.backgroundDiv)) % bgw
            bgy = (self.camera[1]/self.backgroundDiv) % bgh
            for x in range( bgx - bgw, bgx+self.display.resolution[ 0 ], bgw ):
               for y in range( bgy - bgh, bgy+self.display.resolution[ 1 ], bgh ):
                   self.display.draw( self.imgs.background, (x,y) )

            ### 
            ogfx = []
            for gfx in self.gfxs:
                if isinstance( gfx, GfxFragment ):
                    ogfx.append( gfx )

            ### astral objects
            astresInView = []
            for astre in self.astres:
                pos = self.getViewportPos((astre.xp,astre.yp), astre.zp)
                if pos[0] > -1*astre.selectRadius and pos[0] < self.display.resolution[ 0 ]+astre.selectRadius \
                 and pos[1] > -1*astre.selectRadius and pos[1] < self.display.resolution[ 1 ]+astre.selectRadius:
                        astresInView.append( astre )
            ogfx = ogfx+self.objects+astresInView

            zOrder = -100
            oneHigher = True
            while oneHigher:
                nextZOrder = 1000
                oneHigher = False
                for obj in ogfx:
                    if obj.zp == zOrder:
                        if isinstance( obj, Gfx ):
                            self.drawGfx( obj )
                        else:
                            self.drawObject( obj )
                    elif obj.zp > zOrder and obj.zp < nextZOrder:
                        oneHigher = True
                        nextZOrder = obj.zp
                zOrder = nextZOrder
        
            for gfx in self.gfxs:
                self.drawGfx( gfx )

    #    self.display.drawGui(self.playerStatus)
          

        # turrets
            if isinstance(self.build, int ):
                turret = self.playerStatus.turrets[ self.build ]
                minRange = 10
                o = self.getViewportPos( (turret.xp, turret.yp) )
                if turret.maxAngle < turret.minAngle:
                    minAngle = turret.minAngle
                    maxAngle = turret.maxAngle+2*pi
                else:
                    minAngle = turret.minAngle
                    maxAngle = turret.maxAngle

                if turret.range:
                    self.display.drawArc( (255,255,255,255), o, turret.range, minAngle, maxAngle, 1 )
                    maxRange = turret.range
                else:
                    maxRange = 500
                o1 = ( o[0]+cos(minAngle)*minRange, o[1]-sin(minAngle)*minRange )
                o2 = ( o[0]+cos(maxAngle)*minRange, o[1]-sin(maxAngle)*minRange )
                d1 = ( o[0]+cos(minAngle)*maxRange, o[1]-sin(minAngle)*maxRange )
                d2 = ( o[0]+cos(maxAngle)*maxRange, o[1]-sin(maxAngle)*maxRange )
                self.display.drawLine( (255,255,255,255), o1, d1, 1 )
                self.display.drawLine( (255,255,255,255), o2, d2, 1 )
                self.display.drawCircle( (255,255,255,255), o, minRange, 2 )
        else:
    ### fullscreen radar
            self.display.clear()
            dx = dy = max( float(config.universeWidth)*2/self.display.resolution[0], float(config.universeHeight)*2/ self.display.resolution[1] )
            
            # radar
            if self.playerStatus.maxRadar > 100:
                self.display.drawCircle( (255,255,255,255), (self.display.resolution[0]/2+self.playerStatus.xr/dx,self.display.resolution[1]/2-self.playerStatus.yr/dy), self.playerStatus.maxRadar/dx, 1 )
            for obj in utils.mY(self.astres,self.objects):
                if self.ctrlRadar.colors.has_key( obj.relation ):
                    pos = (int(self.display.resolution[0]/2+(obj.xp)/dx),
                    int(self.display.resolution[1]/2-(obj.yp)/dx))
                    self.display.drawCircle( self.ctrlRadar.colors[ obj.relation ], pos, obj.selectRadius/dx )
                
                
        ### messages section
        for msg in self.msgs:
            if time()-msg[0] > self.msgsTTL:
                self.msgs.remove( msg )
            else: break

        o = 0
        for p in range( 0, len(self.msgs) ): #len(self.msgs)-1,-1,-1 ):
            self.display.drawText(  self.msgs[p][1], (7, (o+1)*(20)+149 ), color=(0,0,0) )
            self.display.drawText(  self.msgs[p][1], (9, (o+1)*(20)+151 ), color=(0,0,0) )
            self.display.drawText(  self.msgs[p][1], (8, (o+1)*(20)+150 ) )
            o = o + 1



    ### energy and shield
        if self.playerStatus.maxEnergy:
            self.display.drawRoNCutQbl( self.imgs.uiEnergyFill, (self.display.resolution[0]-72, 22), (1-float(self.playerStatus.energy)/self.playerStatus.maxEnergy)*pi/2 )
        self.display.drawRoNCutQbl( self.imgs.uiShieldFill, (self.display.resolution[0]-72, 22), (1-self.playerStatus.shieldIntegrity)*pi/2 )

        if self.playerStatus.maxEnergy and 1.0*self.playerStatus.energy/self.playerStatus.maxEnergy < 0.2:
            self.display.draw( self.imgs.uiAlertYellowLarge, (self.display.resolution[0]-72-self.display.getWidth( self.imgs.uiAlertYellowLarge )/2, 22-self.display.getHeight( self.imgs.uiAlertYellowLarge )/2) )

        if self.playerStatus.shieldIntegrity < 0.25:
            self.display.draw( self.imgs.uiAlertRed, (self.display.resolution[0]-72-self.display.getWidth( self.imgs.uiAlertRed )/2, 22-self.display.getHeight( self.imgs.uiAlertRed )/2) )

        if self.playerStatus.maxOre and 1.0*self.playerStatus.ore/self.playerStatus.maxOre < 0.2:
            self.display.draw( self.imgs.uiAlertYellowLarge, (self.display.resolution[0]-74-self.display.getWidth( self.imgs.uiAlertYellowLarge )/2, self.display.resolution[1]-24-self.display.getHeight( self.imgs.uiAlertYellowLarge )/2) )

  #      print self.playerStatus.hullIntegrity
        if self.playerStatus.hullIntegrity < 0.5:
            self.display.draw( self.imgs.uiAlertRed, (self.display.resolution[0]-74-self.display.getWidth( self.imgs.uiAlertRed )/2, self.display.resolution[1]-24-self.display.getHeight( self.imgs.uiAlertRed )/2) )

        if self.playerStatus.maxOre:
            self.display.drawRoNCutQtl( self.imgs.uiOreFill, (self.display.resolution[0]-74, self.display.resolution[1]-24), (1-float(self.playerStatus.ore)/self.playerStatus.maxOre)*pi/2 )
   #     print float(self.playerStatus.ore)/self.playerStatus.maxOre
        if self.playerStatus.hullIntegrity >= 0.5:
            hullImg = self.imgs.uiHullFill0
        elif self.playerStatus.hullIntegrity >= 0.25:
            hullImg = self.imgs.uiHullFill1
        else:
            hullImg = self.imgs.uiHullFill2
        self.display.drawRoNCutQtl( hullImg, (self.display.resolution[0]-74, self.display.resolution[1]-24), -1*(1-self.playerStatus.hullIntegrity)*pi/2 )

        self.display.draw( self.imgs.uiTopRight0, (self.display.resolution[0]-self.display.getWidth(self.imgs.uiTopRight0),0) )
        self.display.draw( self.imgs.uiBottomRight0, (self.display.resolution[0]-self.display.getWidth(self.imgs.uiBottomRight0),self.display.resolution[1]-self.display.getHeight(self.imgs.uiBottomRight0)) )


      # relation
        if self.players and False: # temporaely removed relation control
            if self.sPlayerPos == None:
                self.sPlayerPos = 0
            elif self.sPlayerPos >= len( self.players ):
                self.sPlayerPos = len( self.players )-1
            self.sPlayer = self.players[ self.sPlayerPos ]

            self.sPlayerLength = len(self.players)
            relIn = self.sPlayer.relIn
            relOut = self.sPlayer.relOut

            if relIn >= 80:
                relationFillImg = self.imgs.uiRelationFill2
            elif relIn >= 50:
                relationFillImg = self.imgs.uiRelationFill1
            else:
                relationFillImg = self.imgs.uiRelationFill0
            cRelation = (34, self.display.resolution[1]-108)
            if relIn:
                self.display.drawIncompletePie( relationFillImg, cRelation, (1-float(relIn)/100)*pi/2, relIn ) # min(self.rel,10) )
            relOutLength = 76
            relOutAngle = (relOut*100*pi/180/100)-(40*pi/180)
            self.display.drawLine( (32,32,32,255), cRelation, (cRelation[0]+relOutLength*cos(relOutAngle),cRelation[1]-relOutLength*sin(relOutAngle)), 3 )

     ## tube fill
        oreToMissiles = False
        for missile in self.playerStatus.missiles:
            if missile.buildPerc >= 0:
                oreToMissiles = True
                break
        if oreToMissiles:
            y = self.display.resolution[1]-5
            self.display.drawLine( (0,0,255,255), (self.display.resolution[0]/2,y), (self.display.resolution[0],y), 6 )

        oreToShips = False
        for ship in self.playerStatus.ships:
            if ship.buildPerc >= 0:
                oreToShips = True
                break
        if oreToShips:
            y = self.display.resolution[1]-15
            self.display.drawLine( (0,0,255,255), (self.display.resolution[0]/2,y), (self.display.resolution[0],y), 6 )

        oreUpTo = 1000
        energyDownTo = -1
        for k,turret in zip( range(len(self.playerStatus.turrets)),self.playerStatus.turrets):
            if (turret.buildPerc >= 0 or turret.useOre) and k < oreUpTo:
                oreUpTo = k
            if turret.useEnergy and k > energyDownTo:
                energyDownTo = k

        if self.playerStatus.charging:
           self.display.draw( self.imgs.uiChargeFill0, (self.display.resolution[0]-23,55) )
           if self.playerStatus.shieldIntegrity < 1:
               self.display.draw( self.imgs.uiChargeFill1, (self.display.resolution[0]-72,105) )

        if self.playerStatus.repairing:
           self.display.draw( self.imgs.uiRepairFill0, (self.display.resolution[0]-23,self.display.resolution[1]-100) )
           if self.playerStatus.hullIntegrity < 1:
               self.display.draw( self.imgs.uiRepairFill1, (self.display.resolution[0]-74,self.display.resolution[1]-112) )


     ## tubes
        # radar charge
        l = 130
        if self.playerStatus.maxRadar > 100:
            self.display.draw( self.imgs.uiTubeTopLeftFill, (l,0) )
            self.display.drawLine( (0,255,0,255), (l+self.display.getWidth( self.imgs.uiTubeTopLeft ),5), (self.display.resolution[0]-80,5), 5 )
            
        self.display.draw( self.imgs.uiTubeTopLeft, (l,0) )
        for i in range( l+self.display.getWidth( self.imgs.uiTubeTopLeft ), self.ctrlJump.center[0] ): # top-left
            self.display.draw( self.imgs.uiTubeTop1, (i,0) )
        
        # jump charge
        if self.playerStatus.jumpCharge:
            self.display.drawLine( (0,255,0,255), (self.ctrlJump.center[0],14), (self.display.resolution[0]-80,14), 6 )
        for i in range( self.ctrlJump.center[0], self.display.resolution[0]-165 ): # top-right
            self.display.draw( self.imgs.uiTubeTop2, (i,0) )


     ## jump charge
        jumpCenter = self.ctrlJump.center # (self.display.resolution[0]/2+100, 30)
        if self.playerStatus.jumpRecover:
           # self.display.draw( self.imgs.uiAlertYellow, (self.ctrlJump.center[0]-self.display.getHeight( self.imgs.uiAlertYellow )/2, 30-self.display.getHeight( self.imgs.uiAlertYellow )/2) )
            # draw green fill self.imgs.uiJumpRecover
            self.display.drawRoNCutHalfVert( self.imgs.uiJumpFillRecover, jumpCenter, (100-self.playerStatus.jumpRecover)*2*pi/3/100, part=1 )
         #   print self.playerStatus.jumpRecover
    
        elif self.playerStatus.jumpCharge:
            # draw green fill self.imgs.uiJumpCharging
            self.display.drawRoNCutHalfVert( self.imgs.uiJumpFillCharging, jumpCenter, (100-self.playerStatus.jumpCharge)*2*pi/3/100, part=1 )
            
        # draw jump glass
        self.display.drawRo( self.imgs.uiJumpGlass, jumpCenter, 0 )

       # ennemyInRange = self.playerStatus.ennemy False
      #  deadlyInRange = False
       # for obj in self.objects:
       #     if obj.relation == ids.U_ENNEMY:
       #         ennemyInRange = True
        #    if obj.relation == ids.U_DEADLY:
        #        deadlyInRange = True
        #    if ennemyInRange and deadlyInRange:
        #        break

        if self.playerStatus.dangerInRadar:
            self.display.draw( self.imgs.uiAlertRadarYellow, (self.ctrlRadar.center[0]+self.ctrlRadar.radius/2-self.display.getHeight( self.imgs.uiAlertRadarYellow )/2, 0-self.display.getHeight( self.imgs.uiAlertRadarYellow )/2) )
          #  self.display.draw( self.imgs.uiAlertRadarYellow, (self.ctrlRadar.center[0]-self.display.getHeight( self.imgs.uiAlertRadarYellow )/2, self.ctrlRadar.center[1]-self.display.getHeight( self.imgs.uiAlertRadarYellow )/2) )
        if self.playerStatus.ennemyInRadar:
            self.display.draw( self.imgs.uiAlertRadarRed, (self.ctrlRadar.center[0]+self.ctrlRadar.radius/2-self.display.getHeight( self.imgs.uiAlertRadarRed )/2, 0-self.display.getHeight( self.imgs.uiAlertRadarRed )/2) )
          #  self.display.draw( self.imgs.uiAlertRadarRed, (self.ctrlRadar.center[0]-self.display.getHeight( self.imgs.uiAlertRadarRed )/2, self.ctrlRadar.center[1]-self.display.getHeight( self.imgs.uiAlertRadarRed )/2) )
            

     ## main uis     
        self.display.draw( self.imgs.uiTopRight1, (self.display.resolution[0]-self.display.getWidth(self.imgs.uiTopRight1),0) )
        self.display.draw( self.imgs.uiBottomRight1, (self.display.resolution[0]-self.display.getWidth(self.imgs.uiBottomRight1),self.display.resolution[1]-self.display.getHeight(self.imgs.uiBottomRight1)) )
       # self.display.draw( self.imgs.uiBottomLeft, (0,self.display.resolution[1]-self.display.getHeight(self.imgs.uiBottomLeft)) )

      # relations (return)
       # if self.sPlayer:
       #     self.display.drawText( self.sPlayer.name, (8,self.display.resolution[1]-130), size=13 )
       #     self.display.drawText( self.texts[ self.sPlayer.race ], (8,self.display.resolution[1]-104), size=11 )


    ## hangars
        for i in range( self.anchorBottom+100, self.display.resolution[0]-self.display.getWidth( self.imgs.uiBottomRight1 ) ): # bottom-right
            self.display.draw( self.imgs.uiTubeBottom2, (i, self.display.resolution[1]-20) )
            
     ## turrets
        p = self.display.getHeight( self.imgs.uiTopRight0 )+10

        if len(self.butsBuildTurret) != len( self.playerStatus.turrets ):
        #  for control in self.butsBuildTurret:
        #    self.removeControl( control )
          self.butsBuildTurret = []
          
        #  for control in self.butsActivate:
        #    self.removeControl( control )
          self.butsActivate = []
          
          for k, turret in zip( range( 0, len( self.playerStatus.turrets ) ), self.playerStatus.turrets ):
            if turret.type:
                img =  self.imgs[turret.type]
            else:
                img = None
            butTurret = TurretButton( self.imgs.uiTurret, (self.display.resolution[0]-59+16,p+16), 16, self.eBuildTurret, img, uid=k )
            butTurret.stickLeft = False
            self.butsBuildTurret.append( butTurret )
           # self.addControl( butTurret )
            
            butActivate = RectControl(  None, (self.display.resolution[0]-47+22,p+5), (177-22,33+10), self.eActivate, uid=k )
            butActivate.stickLeft = False
            self.butsActivate.append( butActivate )
           # self.addControl( butActivate )
            p = p+33+8
      #    for k, turret in zip( range( 0, tc ), self.playerStatus.turrets ):
      #      self.display.draw( self.imgs.uiTurret, (self.display.resolution[0]-59, p) )


        p = self.display.getHeight( self.imgs.uiTopRight0 )+10
        for k, turret in zip( range( 0, len( self.playerStatus.turrets ) ), self.playerStatus.turrets ):
          if turret.type:
              turretImg =  self.imgs[turret.type]
          else:
              turretImg = None

          if turret.activable:
              if turret.on:
                  img = self.imgs.uiTurretOn
              else:
                  img = self.imgs.uiTurretOff
          else:
              img = self.imgs.uiTurret

          self.butsBuildTurret[ k ].img = img
          self.butsBuildTurret[ k ].turretImg = turretImg
                
          if turret.buildPerc != -1:
                self.ctrlsBuildGauge.append( ((self.display.resolution[0]-59+16,p+16), turret.buildPerc) )
          p = p+33+8


     ## build options
        if self.build and len(self.lastOptions) == len(self.playerStatus.turrets[ self.build ].buildables):
            for k, v in zip( xrange(len(self.lastOptions)), self.lastOptions ):
                if v.type != self.playerStatus.turrets[ self.build ].buildables[ k ].type:
                    self.createBuildOptions()
                    # readding build options
                    break

        for b in self.butsBuildOption:
            if b.uid > 0:
                for o in self.playerStatus.turrets[ self.build ].buildables:
                    if o.type == b.uid:
                        b.enabled = o.canBuild
                        break

        # updating radar control
        self.ctrlRadar.update( self.objects, self.playerStatus, self.camera )

                        
        self.setControls( self.butsShipLaunch+self.butsMissileLaunch+self.butsBuildTurret+ \
            self.butsShipBuild+self.butsMissileBuild+self.butsBuildOption+self.controlsMain+self.butsActivate )
            
     ## buttons
        ControlFrame.draw( self, display, skipFinalize=True )

        self.display.drawText( "ore %i" % self.playerStatus.ore, (self.display.resolution[0]-80,self.display.resolution[1]-29), (50,50,255,255) )
        self.display.drawText( "e %i" % self.playerStatus.energy, (self.display.resolution[0]-80,20), (0,255,0,255) )

       ## ore process
        if self.playerStatus.oreInProcess:
          maxOo = max( self.playerStatus.oreInProcess )

          self.oreMaxs.insert( 0, maxOo )
          if len(self.oreMaxs) > config.fps*3:
            self.oreMaxs.pop()
          maxO = max( self.oreMaxs )
          if maxO > 0:
            for (p,o) in zip( range(len(self.playerStatus.oreInProcess)), self.playerStatus.oreInProcess ):
                if o: 
                    h = int(30*o/maxO)
                    self.display.drawRect( 
                     (self.display.resolution[0]-84+p*4,self.display.resolution[1]-61+30-h,2,h), ( 50, 50, 255, 255) )

     ## turrets tubes
        p = self.display.getHeight( self.imgs.uiTopRight0 )+10
        if energyDownTo != -1:
            self.display.drawLine( (0,255,0,255), (self.display.resolution[0]-9,62), (self.display.resolution[0]-9,p+3), 6 )
        for i in range( 62, p+4 ):
            self.display.draw( self.imgs.uiTubeRightB, (self.display.resolution[0]-12,i) )
        p = p+self.display.getHeight( self.imgs.uiTurret )+8

        for k in range( 0, len( self.playerStatus.turrets ) ):
           if k < len( self.playerStatus.turrets )-1:
              if energyDownTo > k:
                  self.display.drawLine( (0,255,0,255), (self.display.resolution[0]-9,p-8-5), (self.display.resolution[0]-9,p+3), 6 )
              if oreUpTo <= k:
                  self.display.drawLine( (0,0,255,255), (self.display.resolution[0]-19,p-8-5), (self.display.resolution[0]-19,p+3), 6 )
              for i in range( p-8-5, p+4 ):
                self.display.draw( self.imgs.uiTubeRight2, (self.display.resolution[0]-23,i) )
              p = p+self.display.getHeight( self.imgs.uiTurret )+8

        if oreUpTo <= len( self.playerStatus.turrets ):
            self.display.drawLine( (0,0,255,255), (self.display.resolution[0]-19,p-8-5), (self.display.resolution[0]-19,self.display.resolution[1]-150), 6 )
            self.display.draw( self.imgs.uiTubeRightCurveFill, (self.display.resolution[0]-21,self.display.resolution[1]-150) )

        for i in range( p-8-5, self.display.resolution[1]-150 ):
            self.display.draw( self.imgs.uiTubeRightA, (self.display.resolution[0]-23,i) )
        self.display.draw( self.imgs.uiTubeRightCurve, (self.display.resolution[0]-21,self.display.resolution[1]-150) )

    ## build gauges
        for g in self.ctrlsBuildGauge:
            self.display.drawPie( self.imgs.uiBuildFill, g[0], g[1] )
            self.display.drawRo( self.imgs.uiBuildGlass, g[0], 0 )

    # draw radar

        if self.informAbout:
            self.displayStats( self.informAbout )
            
    # finalize!
        self.display.finalizeDraw()

    def manageInputs( self, display ):
        ControlFrame.manageInputs( self, display )
        inputs = self.inputs
        
        quit = self.quit

        hit = self.hit
        
        if inputs.mouseRightUpped:
            self.aim = None
            self.display.setCursor()
            self.butsBuildOption = []
            self.build = None

        if inputs.mouseUpped:
            inputs.mouseUpped = False
            
            if not hit:
                inputs.mouseDownAtV = self.getVirtualPos( inputs.mouseDownAt )
                inputs.mouseUpAtV = self.getVirtualPos( inputs.mouseUpAt )

                if self.aim:
                  inputs.mouseDownAtV = self.getVirtualPos( inputs.mouseDownAt )
                  order = OrderLaunchMissile( self.aim, inputs.mouseDownAtV )
                  self.orders.append( order )
                  
                  self.aim = None
                  self.display.setCursor()
                  hit = True

                if not hit:
                  for o in self.objects:
                    if distBetween( inputs.mouseUpAtV, ( o.xp, o.yp ) ) <= o.selectRadius:
                        order = None

                        if o.relation == ids.U_ENNEMY or o.relation == ids.U_FRIENDLY:
                            order = OrderAttack( o.uid )
                        elif o.relation == ids.U_FLAGSHIP: # or o.relation == ids.U_FLAGSHIP_TURRET:
                            order = OrderStopMove( 0 )
                        elif o.relation == ids.U_ORBITABLE:
                            pass #   order = OrderOrbit( o.uid )

                        if order:
                            hit = True
                            self.orders.append( order )
                            break

            if not hit and not self.aim:
                inputs.mouseUpped = False
                if distBetween(inputs.mouseDownAtV, inputs.mouseUpAtV) < 5:
                    angle = -1
                else:
                    angle = angleBetween( inputs.mouseDownAtV, inputs.mouseUpAtV )

                order = OrderMove( inputs.mouseDownAtV[0], inputs.mouseDownAtV[1], angle )
                self.orders.append( order )

                
        inputs.orders = self.orders
        self.orders = []

        inputs.wc = self.display.resolution[0]
        inputs.hc = self.display.resolution[1]

        inputs.xc = self.camera[0] + inputs.right * self.cameraSpeed
        inputs.xc = inputs.xc - inputs.left * self.cameraSpeed
        inputs.yc = self.camera[1] + inputs.up * self.cameraSpeed
        inputs.yc = inputs.yc - inputs.down * self.cameraSpeed

        if self.camera != (inputs.xc, inputs.yc):
            self.centeredOnShip = False
            self.camera = (inputs.xc, inputs.yc)
      
        self.informAbout = None
        if self.build != None:
            for but in self.butsBuildOption:
                if but.fIn( but, inputs.mousePos ):
                    self.informAbout = but.uid
                    
        for but in self.butsShipBuild:
            if but.fIn( but, inputs.mousePos ):
                self.informAbout = but.uid
                    
        for but in self.butsMissileBuild:
            if but.fIn( but, inputs.mousePos ):
                self.informAbout = but.uid
                
        return (quit,inputs, False)
          #  hits = button.hits()
          
       
### self.stats display logic ####   
    def displayStats( self, k ):
        if self.stats and self.stats.has_key( k ):
            rect = (100,self.display.resolution[1]-200, 160, 80)
            self.display.drawRect( rect, (30,30,30,128) )
            self.display.drawRect( rect, (50,50,50,200), width=1 )
            
            ore = self.stats[ k ].oreCostToBuild
            energy = self.stats[ k ].energyCostToBuild
            time = self.stats[ k ].timeToBuild/config.fps
            text = self.texts.infoBuild%locals()
            vpos = rect[1]+8
            for line in text.split("\n"):
                self.display.drawText( line, (rect[0]+8,vpos), size=13 )
                vpos += 16
    
#### button commands ####
   # def eJumpNow(self, sender, (x,y)):
   #     order = OrderJumpNow()
   #     self.orders.append( order )

    def launchShips(self, type ):
        order = OrderLaunchShips( type )
        self.orders.append( order )
        
    def recallShips(self, type ):
        order = OrderRecallShips( type )
        self.orders.append( order )

   # def eLaunchMissile( self, type ): #sender, (x,y)):
   #     self.aim = sender.uid
   #    self.display.setCursor( self.display.cursorAim )

    def buildMissile( self, type ): # sender, (x,y)):
        self.orders.append( OrderBuildMissile( type, 0 ) )

    def buildShip( self, type ): # sender, (x,y)):
        self.orders.append( OrderBuildShip( type, 0  ))
        
    def launchMissile( self, type, pos ):
        order = OrderLaunchMissile( type, self.getVirtualPos( pos ) )
        self.orders.append( order )
    
    def fUpdateCamera( self, camera, centeredOnShip ):
        self.camera = camera
        self.centeredOnShip = centeredOnShip

    def eBuildTurret( self, sender, (x,y) ):
    #    print sender, sender.uid
        self.build = sender.uid
        self.createBuildOptions()

    def createBuildOptions( self ):
        self.lastOptions = self.lastStats.turrets[ self.build ].buildables
        ps = [0,]*3
        self.butsBuildOption = []
        for option in self.lastStats.turrets[ self.build ].buildables+[-1,]:
         #   print option, type(option), 
            if isinstance(option, int ):
                c = self.categories[ option ]
            else:
                c = self.categories[ option.type ]

            x = self.display.resolution[0]-260-(c)*180
            y = 120+ps[c]*40
            ps[c] += 1

            if option == -1:
                self.butsBuildOption.append( OptionButton( self.imgs.option, (x,y), (166,32), self.eBuildOptions, None, self.texts[option], uid=option ) )
            elif option.type == 0:
                self.butsBuildOption.append( OptionButton( self.imgs.option, (x,y), (166,32), self.eBuildOptions, None, self.texts[option.type], uid=option.type ) )
            else:
                self.butsBuildOption.append( OptionButton( self.imgs.option, (x,y), (166,32), self.eBuildOptions, self.imgs[option.type], self.texts[option.type], uid=option.type ) )
            

    def eBuildOptions( self, sender, (x,y) ):
        self.butsBuildOption = []
    #    print sender.uid
        if sender.uid != -1:
            order = OrderBuildTurret( self.build, sender.uid )
            self.orders.append( order )
        self.build = None

    def eActivate( self, sender, (x,y)):
        if self.lastStats.turrets[sender.uid].activable:
            order = OrderActivateTurret( sender.uid, not self.lastStats.turrets[sender.uid].on )
            self.orders.append( order )

    def eRadarActivate( self, sender, (x,y)):
        self.fullscreenRadar = not self.fullscreenRadar

    def eRadarFullscreen( self, sender, (x,y)):
        self.fullscreenRadar = not self.fullscreenRadar

    def eRepairActivate( self, sender, (x,y)):
        self.orders.append( OrderActivateRepair( not self.lastStats.repairing ) )
     #   print "repairing,", not self.lastStats.repairing

    def eChargeActivate( self, sender, (x,y)):
        self.orders.append( OrderActivateShield( not self.lastStats.charging ) )
     #   print "charging,", not self.lastStats.charging

    def eSetRelation( self, sender, (x,y)):
      if self.sPlayer:
        found = False
        (cx, cy) = (34, self.display.resolution[1]-108)
        dist = distBetween( (cx, cy), (x,y) )
        if dist > 48 and dist < 68:
            angle = angleBetween( (cx, cy), (x,y) )
            if angle < 40*pi/180 or angle > 300*pi/180:
                order = OrderSetRelation( self.sPlayer.name, (100-int(((angle*180/pi+60)%360)*100/100)) )
          #      print (100-int(((angle*180/pi+60)%360)*100/100))
                self.orders.append( order )
                found = True

        if not found and dist < 66: # TODO, this is a temporary hack :(
            if y>cy+27:
                self.ePlayerDown( sender, (x,y))
            elif y<cy-27:
                self.ePlayerUp( sender, (x,y))

    def ePlayerUp( self, sender, (x,y)):
        if self.sPlayerPos != None:
            self.sPlayerPos = (self.sPlayerPos+1)%self.sPlayerLength
    def ePlayerDown( self, sender, (x,y)):
        if self.sPlayerPos != None:
            self.sPlayerPos = (self.sPlayerPos-1)%self.sPlayerLength
                
    def eSelfDetruct( self, sender, (x,y) ):
        self.orders.append( OrderSelfDestruct() )
        
    def fJump( self, pos ):
        order = OrderJump( self.getVirtualPos( pos ) )
        self.orders.append( order )
        
    def fBroadcast( self, text ):
        order = OrderBroadcast( text )
        self.orders.append( order )
        
    def fDirectedCast( self, text, pos ):
        order = OrderDirectedCast( text, self.getVirtualPos( pos ) )
        self.orders.append( order )

    def close(self):
        self.display.close()
        
    def eChatOpen( self, sender, (x,y) ):
        self.selected = self.ctrlChat.chatBox.textBox

    def addMsg( self, msg ):
        self.msgs.append( (time(),msg) )

    def addDelayedMsg( self, msg, sender, sentAt, receivedAt ):
        if sentAt == receivedAt:
            self.msgs.append( (time(),"%s: %s"%(sender,msg)) )
        else:
            secsDiff = float(receivedAt-sentAt)/config.fps
            if secsDiff < 60:
                timeStr = "%.0fs"%secsDiff
            else: # if secsDiff < 60*60:
                timeStr = "%.1fm"%(secsDiff/60)
            self.msgs.append( (time(),"%s, %s ago: %s"%(sender,timeStr,msg)) )

