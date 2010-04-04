from math import pi, sin, cos, hypot, sqrt, fabs

from client.controls import *
from client.specialcontrols import *
from client.specialcontrols.boxes import LabelImage
from common import utils
from common import ids
from common import config

class GuiBackPlay( RectControl ):
    pass

class GuiBackFullscreenRadar( RectControl ):
    pass
    
class UiPanel( Control ):
    pass
    
def ihypot( h, c ):
    i = h*h - c*c
    if i > 0:
        return sqrt( i )
    else:
        return 0
        
class RadarControl( Container ):
    def __init__( self, imgs, eOpenFullscreen=None, eCloseFullscreen=None, fUpdateCamera=None ):
        Container.__init__( self )
        
        self.eOutOpenFullscreen = eOpenFullscreen
        self.eOutCloseFullscreen = eCloseFullscreen
        self.fUpdateCamera = fUpdateCamera
        
        self.center = (66,65)
        self.radius = 66
        
        self.ctrlFullscreenDist = self.radius + 5
        self.ctrlFullscreenAngle = -pi/4.4
        self.ctrlFullscreenCenter = ( self.center[0]+self.ctrlFullscreenDist*cos(self.ctrlFullscreenAngle), 
                                      self.center[1]+self.ctrlFullscreenDist*sin(self.ctrlFullscreenAngle) )
        
        self.scanAngle = 0
        self.scanSpeed = -0.08
        
        self.ctrlOpenFullscreen = RoundControl( imgs.ctrlRadarOpen, self.ctrlFullscreenCenter, 16, fUpEvent=self.eOpen )
        self.ctrlCloseFullscreen = RoundControl( imgs.ctrlRadarClose, self.ctrlFullscreenCenter, 16, fUpEvent=self.eClose )
        self.ctrlRadarScreen = RoundControl( None, self.center, self.radius, fUpEvent=self.eRadar )
        
        lblRadius = self.radius+5
        self.lblX = LabelImage( imgs.ctrlLabelX, (self.center[0]+lblRadius*cos(0.4),self.center[1]+lblRadius*sin(0.4)), 60, "" )
        self.lblY = LabelImage( imgs.ctrlLabelY, (self.center[0]+lblRadius*cos(0.7),self.center[1]+lblRadius*sin(0.7)), 60, "" )
        self.lblRange = LabelImage( imgs.ctrlLabelRange, (self.center[0]+lblRadius*cos(0),self.center[1]+lblRadius*sin(0)), 45, "" )
       # self.lblX = LabelGlass( imgs, (self.center[0]+lblRadius*cos(0.2),self.center[1]+lblRadius*sin(0.2)), "" )
       # self.lblY = LabelGlass( imgs, (self.center[0]+lblRadius*cos(0.6),self.center[1]+lblRadius*sin(0.6)), "" )
       # self.lblRange = LabelGlass( imgs, (self.center[0]+lblRadius*cos(-0.4),self.center[1]+lblRadius*sin(-0.4)), "" )
        
        self.imgBack = imgs.ctrlRadarBack
        self.imgOver = imgs.ctrlRadarOver
        self.imgScan = imgs.ctrlRadarScan
        self.imgSelection = imgs.ctrlRadarSelection
        
        self.colors = { 
             ids.U_FLAGSHIP: (255,255,255,255),
             ids.U_OWN: (0,255,0,255),
             ids.U_FRIENDLY: (0,0,255,255),
             ids.U_ENNEMY: (255,0,0,255),
             ids.U_ORBITABLE: (127,127,127,255),
             None: (0,0,0,0) }
        self.viewColor = (64,64,64,255)
        
        self.reset()
        
    def reset( self ):
        Container.reset( self )
        
        self.controls = [self.ctrlRadarScreen, self.ctrlOpenFullscreen, self.lblX, self.lblY, self.lblRange]
        
        self.objects = []
        self.status = None
        self.camera = None
        self.resolution = (0,0)
        self.maxRadarRange = 0
        self.radarRange = 0
        
    def draw( self, display, focused=False, over=False, mouse=None ):
        self.resolution = display.resolution
    
        # background
        display.drawRo( self.imgBack, self.center, 0 )
        
        # scanning effect
        if self.radarRange > 100:
            self.scanAngle = (self.scanAngle+self.scanSpeed)%(2*pi)
            display.drawRo( self.imgScan, self.center, self.scanAngle )
        
        if self.objects and self.status and self.radarRange > 100:
            # draw objects
            for obj in self.objects:
                if self.colors.has_key( obj.relation ):
                    dist = hypot( obj.yp-self.status.yr, obj.xp-self.status.xr )
                    if dist <= self.radarRange:
                        pos = (int(self.center[0]+float(self.radius)*(obj.xp-self.status.xr)/self.radarRange),
                            int(self.center[1]-float(self.radius)*(obj.yp-self.status.yr)/self.radarRange))
                        if self.colors.has_key( obj.relation ):
                           display.drawPoint( pos, self.colors[ obj.relation ] )

            # draw viewed area
            left = float(self.radius)*(self.camera[0]-self.status.xr)/self.radarRange
            top = float(self.radius)*(self.camera[1]+display.resolution[1]-self.status.yr)/self.radarRange
            width = display.resolution[0]*float(self.radius)/self.radarRange
            height = display.resolution[1]*float(self.radius)/self.radarRange

            if width and height:
                display.drawClipped( self.imgSelection, 
                    (self.center[0]+left, self.center[1]-top), 
                    (self.radius+left, self.radius-top, width, height ) )

 
        
        # front / glass / over
        display.drawRo( self.imgOver, self.center, 0 )
        
        # all other controls
        Container.draw( self, display, focused, over, mouse )
        
       ### self.display.drawText( str( self.status.maxRadar ), (142,55), size=13 )
       ### self.display.drawText( "%0.1f  %0.1f"% ( self.status.xr/1000.0, self.status.yr/1000.0 ), (139,83), size=13 )
    
    def update( self, objects, status, camera ):
        self.objects = objects
        self.status = status
        self.camera = camera
        
        self.maxRadarRange = self.status.maxRadar
        self.radarRange = self.maxRadarRange
        
        self.lblX.text = "%.2f"%(self.status.xr/1000.0)
        self.lblY.text = "%.2f"%(self.status.yr/1000.0)
        self.lblRange.text = "%.1f"%(self.radarRange/1000.0)

    def hits( self, up=None, down=None ):
     #   print self
        return Container.hits( self, up=up, down=down )
        
    def eRadar( self, sender, (x,y) ):
        if self.status:
            if fabs( x-self.center[0] ) < 10 and fabs( y-self.center[1] ) < 10:
                self.centeredOnShip = True
            else:
                self.centeredOnShip = False

            self.camera = ( float(x-self.center[0])*self.status.maxRadar/self.radius-self.resolution[0]/2+self.status.xr,
                            -1*float(y-self.center[1])*self.status.maxRadar/self.radius-self.resolution[1]/2+self.status.yr)
                            
            if self.fUpdateCamera:
                self.fUpdateCamera( self.camera, self.centeredOnShip )
            
    
    def eOpen( self, sender, pos ):
        self.controls = [self.ctrlRadarScreen, self.ctrlCloseFullscreen, self.lblX, self.lblY, self.lblRange]
        self.eOutOpenFullscreen( sender, pos )
    
    def eClose( self, sender, pos ):
        self.controls = [self.ctrlRadarScreen, self.ctrlOpenFullscreen, self.lblX, self.lblY, self.lblRange]
        self.eOutCloseFullscreen( sender, pos )

class SelfDestructControl( Container ):
    def __init__( self, imgs, center, explodeEvent, uid=None ):
        Control.__init__( self, None, None, fIn=None, uid=uid )
        self.center = center
        self.rotationSpeed = 2*pi/config.fps/5
        self.openRotation = -pi/6
        
        self.img = imgs.ctrlSelfDestructBack
        self.ctrlBack = ImageHolder( imgs.ctrlSelfDestructBack, (-4,self.center[1]-23) )
        self.ctrlOver = RotatingImageHolder( imgs.ctrlSelfDestructOver, self.center )
        
       # self.alert = imgs.uiAlertYellow
        self.alert = imgs.uiAlertYellow
        
        self.ctrlOpen = RoundControl( imgs.ctrlSelfDestructOpen, (self.center[0]-42,self.center[1]+64), 16, fUpEvent=self.eOpen )
        self.ctrlClose = RoundControl( imgs.ctrlSelfDestructClose, (self.center[0]-42,self.center[1]+64), 16, fUpEvent=self.eClose )
        self.ctrlExplode = RoundControl( imgs.ctrlSelfDestructExplode, (self.center[0]-42,self.center[1]+118), 29, fUpEvent=explodeEvent )
        self.controls = []
        
        self.reset()
        
    def draw( self, display, focused=False, over=False, mouse=None ):
        if self.open:
            self.controls = [
                self.ctrlBack,
                self.ctrlExplode,
                self.ctrlOver,
                self.ctrlClose, ]
            if self.rotation != self.openRotation:
                if self.rotation - self.rotationSpeed < self.openRotation:
                    self.rotation = self.openRotation
                else:
                    self.rotation -= self.rotationSpeed
        else:
            self.controls = [
                self.ctrlBack,
                self.ctrlExplode,
                self.ctrlOver,
                self.ctrlOpen, ]
            if self.rotation != 0:
                self.rotation = min( 2*pi, self.rotation+self.rotationSpeed ) % (2*pi)
           
        self.ctrlOver.r = self.rotation
       
        if self.rotation != 0:
            display.draw( self.alert, (self.ctrlExplode.center[0]-display.getWidth(self.alert)/2, self.ctrlExplode.center[1]-display.getHeight(self.alert)/2) )
       #     display.draw( self.alert, (self.center[0]-display.getWidth(self.alert)/2, self.center[1]-display.getHeight(self.alert)/2) )
        
        Container.draw( self, display, focused=focused, over=over, mouse=mouse )
        
      #  display.drawRo( self.img, self.center, self.rotation )
        
       # for control in self.controls: 
       #     angle = control.angleFromMain-self.rotation
       #     control.topLeft = (
       #         self.center[0]-control.radius+cos(angle)*control.distFromMain, 
        #        self.center[1]-control.radius+sin(angle)*control.distFromMain )  
       #     control.center = (
       #         self.center[0]+cos(angle)*control.distFromMain, 
       #         self.center[1]+sin(angle)*control.distFromMain )    
       #     control.draw( display )
            
   # def hits( self, up=None, down=None ):
   #     for control in self.controls: 
   #         print up, down
   #         if control.hits( up=up, down=down ):
   #             return True
   #     return False
        
    def eOpen( self, sender, (x,y) ):
        self.open = True
      #  print "eOpen!!"
      #  self.controls = [
      #      self.ctrlExplode,
      #      self.ctrlBack,
      #      self.ctrlClose, ]
        
    def eClose( self, sender, (x,y) ):
        self.open = False
      #  print "eClose!!"
      #  self.controls = [
      #      self.ctrlExplode,
      #      self.ctrlBack,
      #      self.ctrlOpen, ]
        
    def reset( self ):
        self.rotation = 0
        self.open = False
       # self.controls = [
       #     self.ctrlExplode,
       #     self.ctrlBack,
       #     self.ctrlOpen, ]
        
        
class OldSelfDestructControl( Control ):
    def __init__( self, imgs, center, explodeEvent, uid=None ):
        Control.__init__( self, None, None, fIn=None, uid=uid )
        self.center = center
        self.rotationSpeed = 2*pi/config.fps
       # self.open = False
       # self.rotation = 0
        self.reset()
        
        self.img = imgs.ctrlSelfDestructBack
        
       # self.alert = imgs.uiAlertYellow
        self.alert = imgs.uiAlertYellowLarge
        
        self.ctrlOpen = RoundControl( imgs.ctrlSelfDestructOpen, (0,0), 20, fUpEvent=self.eOpen )
        self.ctrlOpen.distFromMain = 25
        self.ctrlOpen.angleFromMain = 0
        
        self.ctrlClose = RoundControl( imgs.ctrlSelfDestructClose, (0,0), 20, fUpEvent=self.eClose )
        self.ctrlClose.distFromMain = 35
        self.ctrlClose.angleFromMain = 25*pi/20
        
        self.ctrlExplode = RoundControl( imgs.ctrlSelfDestructExplode, (0,0), 29, fUpEvent=explodeEvent )
        self.ctrlExplode.distFromMain = 45
        self.ctrlExplode.angleFromMain = 16*pi/20
        
        self.controls = [
            self.ctrlOpen,
            self.ctrlClose,
            self.ctrlExplode ]
        
    def draw( self, display, focused=False, over=False, mouse=None ):
        if self.open:
            if self.rotation != pi:
                if self.rotation + self.rotationSpeed > pi:
                    self.rotation = pi
                else:
                    self.rotation += self.rotationSpeed
        else:
            if self.rotation != 0:
                self.rotation = min( 2*pi, self.rotation+self.rotationSpeed ) % (2*pi)
           
        if self.rotation != 0:
       #     display.draw( self.alert, (self.ctrlExplode.center[0]-display.getWidth(self.alert)/2, self.ctrlExplode.center[1]-display.getHeight(self.alert)/2) )
            display.draw( self.alert, (self.center[0]-display.getWidth(self.alert)/2, self.center[1]-display.getHeight(self.alert)/2) )
        
        display.drawRo( self.img, self.center, self.rotation )
        
        
        for control in self.controls: 
            angle = control.angleFromMain-self.rotation
            control.topLeft = (
                self.center[0]-control.radius+cos(angle)*control.distFromMain, 
                self.center[1]-control.radius+sin(angle)*control.distFromMain )  
            control.center = (
                self.center[0]+cos(angle)*control.distFromMain, 
                self.center[1]+sin(angle)*control.distFromMain )    
            control.draw( display )
            
    def hits( self, up=None, down=None ):
        for control in self.controls: 
            select = control.hits( up=up, down=down )
            if select:
                return select
        return False
        
    def eOpen( self, sender, (x,y) ):
        self.open = True
        
    def eClose( self, sender, (x,y) ):
        self.open = False
        
    def reset( self ):
        self.rotation = 0
        self.open = False
        
class GameMenuControl( Container ):
    def __init__( self, imgs, eQuitToMenu=None, eSaveGame=None, eToggleFullscreen=None, eOpen=None, eClose=None ):
        Container.__init__( self )
        self.eOutOpen = eOpen
        self.eOutClose = eClose
        
        self.closedControls = [
            RoundControl( imgs.ctrlMenuOpen, (13,18), 16, fUpEvent=self.eOpen )
            ]
        self.menuControls = [ # moving controls
            LightControlRight( (0,0), eToggleFullscreen, "Toggle fullscreen", imgs ), # eToggleFullscreen
            LightControlRight( (0,0), eSaveGame, "Save game", imgs ), # eSaveGame
            LightControlRight( (0,0), eQuitToMenu, "Quit to main menu", imgs ), # eQuitToMenu
            LightControlRight( (0,0), self.eClose, "Close menu", imgs ), # close/leave menu
        ]
        self.menuDecorations = [ RotatingImageHolder( imgs[ ids.S_HUMAN_FIGHTER ], (0,0) ) for i in xrange( len(self.menuControls)) ]
        self.openedControls = [
            ImageHolder( imgs.ctrlMenuFade, (0,0), size=(1600,1200) ), # back
            RoundControl( imgs.ctrlMenuOpen, (13,18), 16, fUpEvent=self.eClose ) # close/leave menu
            ] + self.menuControls + self.menuDecorations
        self.controls = self.closedControls
        
        self.menuRadius = 300
        self.menuCenter = (0,0)
        self.menuAngleBetweenItems = pi/9
        self.menuAngleOpened = pi/12
        self.menuAngleClosed = -pi/3
        self.menuAngleClosedEnd = 4*pi/3
        self.menuAngleDiffByFrame = 0.07
        self.menuDecorationCorrection = (10,LightControlRight.height/2)
        self.reset()
        
    def reset( self ):
        self.open = False
        self.menuAngle = self.menuAngleClosed
            
    def draw( self, display, focused=False, over=False, mouse=None ):
        if self.open:
            if self.menuAngle < self.menuAngleOpened:
                self.menuAngle += self.menuAngleDiffByFrame
                
                
            p = 0
            for control in self.menuControls:
                angle = self.menuAngle + p*self.menuAngleBetweenItems
                pos = ( self.menuRadius * cos(angle), self.menuRadius * sin(angle) )
                control.topLeft = pos
                self.menuDecorations[ p ].center = (pos[0]+self.menuDecorationCorrection[0], pos[1]+self.menuDecorationCorrection[1])
                self.menuDecorations[ p ].r = -1*(angle+pi/2)
                p += 1
        else:
            if self.menuAngle > self.menuAngleClosed:
                self.menuAngle -= self.menuAngleDiffByFrame
            
        Container.draw( self, display, focused=focused, over=over, mouse=mouse )
        
    def eOpen( self, sender, mousePos ):
        self.controls = self.openedControls
        self.open = True
        if self.eOutOpen:
            self.eOutOpen( self, mousePos )
            
    def eClose( self, sender, (x,y) ):
        self.controls = self.closedControls
        self.open = False
        if self.eOutClose:
            self.eOutClose( self, mousePos )

class JumpControl( Container ):
    def __init__( self, imgs, center, fJump=None ):
        Container.__init__( self )
        
        self.center = center
        self.fJump = fJump
        
        self.butOpen = RoundControl(imgs.ctrlJumpRegular, center, 29, self.eOpen)
        self.butClose = RoundControl(imgs.ctrlJumpReturn, center, 29, self.eClose)
       # self.ctrlBack = RectControl( None, (0,0), (1600, 1200), self.eJumpTarget ) # self.eJumpTarget, fDownEvent=self.eClose )
        self.ctrlBack = TargettingScreen( imgs, eLeftClick=self.eJumpTarget )
        
        self.reset()
        
    def draw( self, display, focused=False, over=False, mouse=(0,0) ):
      #  if self.justOpened:
      #      self.justOpened = False
      #      display.setCursor( display.cursorAim )
      #  elif self.justClosed:
      #      self.justClosed = False
      #      display.setCursor()
            
        Container.draw( self, display, focused=focused, over=over, mouse=mouse )
        
    def reset( self ):
     #   self.justOpened = False
     #   self.justClosed = False
        self.eClose( self, (0,0) )
        
    def update( self, (left, top, width, height), canRegularJump=False,  ):
        self.ctrlBack.update( (left, top, width, height) )
        self.butOpen.enabled = canRegularJump
        if self.open and not canRegularJump:
            self.eClose( self, (0,0) )
        
    def eOpen( self, sender, (x,y) ):
        self.open = True
     #   self.justOpened = True
        self.controls = [ self.ctrlBack, self.butClose ]
        
    def eClose( self, sender, (x,y) ):
        self.open = False
     #   self.justClosed = True
        self.controls = [ self.butOpen ]
        
    def eJumpTarget( self, sender, (x,y) ):
        if self.fJump:
            self.fJump( (x,y) )
        self.eClose( sender, (x,y) )

    def eSwitch( self, sender, (x,y) ):
        if self.open:
            self.eClose( sender, (x,y) )
        else: # close
            self.eOpen( sender, (x,y) )
       
class ChatBox( Container ):
    def __init__( self, imgs, topLeft, width=540, eBroadcast=None, eDirectedCast=None, eReturn=None ):
        Container.__init__( self ) #TextBox.__init__( self, topLeft, (width,18) ) #, forbidden=["\n"] )
        self.topLeft = topLeft
        self.width = width
        self.radius = 14 # self.width/2
        
        self.eEnter = eBroadcast
        self.eReturn = eReturn
        
        self.ctrlBroadcast = RoundControl(imgs.ctrlChatBroadcast, (0,0), 20, eBroadcast)
        self.ctrlDirectedCast = RoundControl(imgs.ctrlChatDirectedCast, (0,0), 20, eDirectedCast)
        self.ctrlReturn = RoundControl(imgs.ctrlChatReturn, (0,0), 20, eReturn)
        self.textBox = TextBox( (self.topLeft[0]+40, self.topLeft[1]+4), (width-120,16), forbidden="\n;:|", eTextChanged=self.eTextChanged, eEnter=eBroadcast ) #, ["\n"] )
        
        self.controlsNonTargetting = [
            self.ctrlBroadcast,
            self.ctrlDirectedCast,
            self.textBox
            ]
        self.controlsTargetting = [
            self.ctrlBroadcast,
            self.ctrlReturn,
            self.textBox
            ]
        self.relativeControls = [
            ( self.textBox, 40, 8 ),
            ]
        self.relativeControlsInv = [
            ( self.ctrlBroadcast, -64, self.radius-self.ctrlBroadcast.radius ),
            ( self.ctrlDirectedCast, -20, self.radius-self.ctrlBroadcast.radius ),
            ( self.ctrlReturn, -20, self.radius-self.ctrlBroadcast.radius ),
        ]
        
        self.imgs = imgs
    #    self.eTextChanged( self, (0,0) )
        self.reset()
    text = property( fget=lambda self: self.textBox.text )
    
    def reset( self ):
        self.textBox.reset()
        self.setTargetting( False )
        
    def draw( self, display, focused=False, over=False, mouse=(0,0) ):
        display.draw( self.imgs.ctrlChatBackLeft, self.topLeft )
       # for i in xrange( 0,  ):
       #     display.draw( self.imgs., ()+i,) )

        display.drawRepeated( self.imgs.ctrlChatBackCenter, 
                    ( self.topLeft[0]+display.getWidth( self.imgs.ctrlChatBackLeft ), self.topLeft[1] ),
                    repeatx=self.width-display.getWidth( self.imgs.ctrlChatBackLeft )-display.getWidth( self.imgs.ctrlChatBackRight ) )
                        
        display.draw( self.imgs.ctrlChatBackRight, (self.topLeft[0]+self.width-display.getWidth( self.imgs.ctrlChatBackRight ), self.topLeft[1] ) )
        
        for control, xd, yd in self.relativeControls:
            control.topLeft = ( self.topLeft[0]+xd, self.topLeft[1]+yd )
        for control, xd, yd in self.relativeControlsInv:
            control.topLeft = ( self.topLeft[0]+self.width+xd, self.topLeft[1]+yd )
        
        Container.draw( self, display, focused=focused, over=over, mouse=mouse )
        
    def eTextChanged( self, sender, (x,y) ):
        if self.textBox.text:
            self.ctrlBroadcast.enabled = True
            self.ctrlDirectedCast.enabled = True
        else:
            self.ctrlBroadcast.enabled = False
            self.ctrlDirectedCast.enabled = False
           # if self.eReturn:
           #     self.eReturn( self, (x,y) )
            
    def setTargetting( self, targetting ):
        if targetting:
            self.controls = self.controlsTargetting
        else:
            self.controls = self.controlsNonTargetting
            
class TargettingScreen( Container ):
    def __init__( self, imgs, eLeftClick=None, eRightClick=None ):
    #    RectControl.__init__( self, None, (0,0), (1600, 1200), eLeftClick )
        Container.__init__( self )
        
        self.imgCenter = imgs.ctrlAimCenter
        self.imgArm = imgs.ctrlAimArm
        self.offset = ( (0,56) ) # center position
       # self.offset = ( (76,73) ) # center position
        
        self.ctrlBack = RectControl( None, (0,0), (1600, 1200), eLeftClick )
        self.lblRadius = 60
        self.lblX = LabelImage( imgs.ctrlLabelX, (0,0), 60, "" )
        self.lblY = LabelImage( imgs.ctrlLabelY, (0,0), 60, "" )
        
        self.controls = [ self.ctrlBack, self.lblX, self.lblY ]
        (self.left, self.top, self.width, self.height) = (0, 0, 0, 0)
        
    def draw( self, display, focused=False, over=False, mouse=(0,0) ):
        if mouse != (0,0):
            ix = mouse[0]-self.offset[0]
            iy = mouse[1]-self.offset[1]
          #  for y in xrange( iy-display.getHeight(self.imgArm), 0-display.getHeight(self.imgArm), -1*display.getHeight(self.imgArm) ):
          #      display.draw( self.imgArm, (ix+1,y) )
            display.draw( self.imgCenter, (ix,iy) )
            
            self.lblX.topLeft = (mouse[0]+self.lblRadius*cos(0.2),mouse[1]+self.lblRadius*sin(0.2))
            self.lblY.topLeft = (mouse[0]+self.lblRadius*cos(0.58),mouse[1]+self.lblRadius*sin(0.58))
            if self.width and self.height:
                x = self.left+1.0*self.width*mouse[0]/display.resolution[0]
                y = self.top+self.height*(1-1.0*mouse[1]/display.resolution[1])
                self.lblX.text = "%.2f"%(x/1000.0)
                self.lblY.text = "%.2f"%(y/1000.0)
            
                Container.draw( self, display, focused=focused, over=over, mouse=mouse )
            display.cursorDrawn = True
        
    def update( self, (left, top, width, height) ):
        (self.left, self.top, self.width, self.height) = (left, top, width, height)
            
class ChatControl( Container ):
    def __init__( self, imgs, center, fBroadcast=None, fDirectedCast=None, eOpen=None, eClose=None ):
        Container.__init__( self )
        self.center = center
        
        self.fOutBroadcast = fBroadcast # args = text
        self.fOutDirectedCast = fDirectedCast # args = text, dest
        self.eOutOpen = eOpen
        self.eOutClose = eClose
    
        self.ctrlSupport = RotatingImageHolder( imgs.ctrlChatSupport, center )
        self.ctrlOpen = RoundControl(imgs.ctrlChatOpen, center, 16, self.eOpen)
        self.ctrlClose = RoundControl(imgs.ctrlChatClose, center, 16, self.eClose)
        self.chatBox = ChatBox( imgs, center, eBroadcast=self.eBroadcast, eDirectedCast=self.eDirectedCast, eReturn=self.eReturn ) #, forbidden=["\n"] )
        self.ctrlLog = RoundControl(imgs.ctrlChatOpenLog, center, 16, self.eOpenLog)
        self.ctrlBack = TargettingScreen( imgs, eLeftClick=self.eDirectedCastTarget )
        
        self.movingControls = [
            (self.chatBox, 80, pi/2 ),
            (self.ctrlClose, 80, pi/2 ),
            (self.ctrlLog, 40, pi/2 ),
            (self.ctrlOpen, 28, 3*pi/2 ),
            ]
        
        self.stickTop = False
        self.rotationSpeed = 0.6*2*pi/config.fps
        self.reset()
            
    def reset( self ):
        self.rotation = 0
        self.eClose( self, (0,0) )
        self.setTargetting( False )
        
    def setTargetting( self, targetting ):
        self.chatBox.setTargetting( targetting )
        if targetting:
            self.controls = [
                self.ctrlBack,
                self.ctrlSupport,
                self.chatBox,
                self.ctrlOpen,
                self.ctrlClose,
                self.ctrlLog,
            ]
        else:
            self.controls = [
                self.ctrlSupport,
                self.chatBox,
                self.ctrlOpen,
                self.ctrlClose,
                self.ctrlLog,
            ]
        
    def update( self, (left, top, width, height) ):
        self.ctrlBack.update( (left, top, width, height) )
        # detect if untouched for a while and close then
        
    def eOpen( self, sender, (x,y) ):
        self.open = True
        if self.eOutOpen:
            self.eOutOpen( sender, (x,y) )
     #   self.controls = self.controlsOpened
        
    def eClose( self, sender, (x,y) ):
        self.open = False
        if self.eOutClose:
            self.eOutClose( sender, (x,y) )
    #    self.controls = self.controlsClosed
        
    def eBroadcast( self, sender, (x,y) ):
        if self.chatBox.textBox.text:
            self.fOutBroadcast( self.chatBox.textBox.text )
            self.chatBox.textBox.reset() #.text = ""
        
    def eDirectedCast( self, sender, (x,y) ):
        if self.chatBox.textBox.text:
            self.setTargetting( True )
        
    def eDirectedCastTarget( self, sender, (x,y) ):
        if self.chatBox.textBox.text:
            self.fOutDirectedCast( self.chatBox.textBox.text, (x,y) )
            self.chatBox.textBox.reset()
        self.setTargetting( False )
        
    def eOpenLog( self, sender, (x,y) ):
        pass
        
    def eReturn( self, sender, (x,y) ):
        self.setTargetting( False )
        
    def draw( self, display, focused=False, over=False, mouse=(0,0) ):
    
        if self.open:
            if self.rotation < pi:
                self.rotation = min( pi, self.rotation+self.rotationSpeed)%(2*pi)
        else: # not self.open:
            if self.rotation > 0:
                self.rotation = max( 0, self.rotation-self.rotationSpeed)%(2*pi)
                
        self.ctrlSupport.r = self.rotation
        self.ctrlSupport.center = (self.center[0]+self.topLeft[0], self.center[1]+self.topLeft[1])  
      #  print self.topLeft
        
        for control, dist, angleDiff in self.movingControls:
            angle = angleDiff-self.rotation
            control.topLeft = (
                self.center[0]+self.topLeft[0]-control.radius+cos(angle)*dist, 
                self.center[1]+self.topLeft[1]-control.radius+sin(angle)*dist )  
                
    #    if self.justOpened:
    #        self.justOpened = False
    #        display.setCursor( display.cursorAim )
    #    elif self.justClosed:
    #        self.justClosed = False
    #        display.setCursor()
            
        Container.draw( self, display, focused=focused, over=over, mouse=mouse )
        
        
        
        
class SlotButton( RectControl ):
    def __init__( self, imgs, slot, eBuild=None, uid=None ):
        RectControl.__init__( self, None, slot[:2], slot[2:], eBuild, uid=uid )
        self.imgs = imgs
        self.imgOver = None
        self.buildPerc = -1
        self.quantity = -1
    
    def draw( self, display, focused=False, over=False, mouse=(0,0) ):
        display.draw( self.imgs.ctrlHangarSlot, (self.topLeft[0], self.topLeft[1]) )
        if self.imgOver:
            display.draw( self.imgOver, 
            (self.topLeft[0]+self.rw/2-display.getWidth( self.imgOver )/2,
             self.topLeft[1]+self.rh/2-display.getHeight( self.imgOver )/2) )
            if self.quantity >= 0:
                display.drawText( str(self.quantity), (self.topLeft[0]+self.rw/2,self.topLeft[1]+self.rh-10), size=10, align="center" )
        if self.buildPerc >= 0:
            display.drawPie( self.imgs.uiBuildFill, (self.topLeft[0]+self.rw/2,self.topLeft[1]+self.rh/2), self.buildPerc )
            display.drawRo( self.imgs.uiBuildGlass, (self.topLeft[0]+self.rw/2,self.topLeft[1]+self.rh/2), 0 )
             
       # RectControl.draw( self, display, focused, over, mouse )

class HangarControl( Container ):
    def __init__( self, imgs, center, eLaunchMissile=None, eLaunchShip=None, eRecallShip=None, eBuildMissile=None, eBuildShip=None ):
        Container.__init__( self )
        self.imgs = imgs
        self.center = center
        
        self.eOutLaunchMissile = eLaunchMissile # type, dest
        self.eOutLaunchShip = eLaunchShip # type
        self.eOutRecallShip = eRecallShip # type 
        self.eOutBuildMissile = eBuildMissile # type # , build(True/False)
        self.eOutBuildShip = eBuildShip # type # , build(True/False)
        
        self.ctrlBack = TargettingScreen( imgs, eLeftClick=self.eTargetMissile )
        
        self.reset()
        
        self.topLeft = self.center

        self.builderMissilesId = [ ids.M_FRIGATE_BUILDER,
                                   ids.M_BUILDER_BASE_CARGO,
                                   ids.M_BUILDER_BASE_MILITARY,
                                   ids.M_BUILDER_BASE_HEAVY_MILITARY,
                                   ids.M_BUILDER_BASE_CARRIER ]
        
    def reset( self ):
       # self.missiles = []
       # self.ships = []
        
        self.butsShipLaunch = []
        self.butsShipBuild = []
        self.butsMissileLaunch = []
        self.butsMissileBuild = []
        
        self.missileSlots = []
        self.shipSlots = []
        
        self.size = (0,0)
            
        self.targetting = None
        
    def update( self, playerStatus, (left, top, width, height) ):
        self.playerStatus = playerStatus
        self.ctrlBack.update( (left, top, width, height) )
        
       ## missiles
        # do only when missile list changes
        if len(self.butsMissileLaunch) != len( self.playerStatus.missiles ) \
            or filter( lambda k: self.playerStatus.missiles[k].type != self.butsMissileLaunch[k].uid, 
                       xrange( 0, len(self.playerStatus.missiles ) ) ):
            self.butsMissileLaunch = []
            self.butsMissileBuild = []
            
            for missile,slot in zip( self.playerStatus.missiles, self.missileSlots ):
                builder = self.missileIsBuilder( missile )

                butLaunch = RoundControl( self.imgs.uiButAim, (slot[0]+slot[2]/2,slot[1]-6), 12, self.eSwitchLaunchMissile, uid=missile.type)
                butBuild = SlotButton( self.imgs, slot, eBuild=self.eBuildMissile, uid=missile.type )
                self.butsMissileLaunch.append( butLaunch )
                self.butsMissileBuild.append( butBuild )

        # do at every frame
        for missile,butBuild,butLaunch in zip( self.playerStatus.missiles, self.butsMissileBuild, self.butsMissileLaunch ):
            butBuild.buildPerc = missile.buildPerc
            butBuild.enabled = missile.canBuild or missile.buildPerc >= 0
            
            if missile.show or missile.buildPerc != -1:
                butBuild.imgOver = self.imgs.missilesIcons[ missile.type ]
                butBuild.quantity = missile.nbr
            else:
                butBuild.imgOver = None
                butBuild.quantity = -1
            
            butLaunch.enabled = missile.usable and missile.canLaunch
            butLaunch.visible = missile.usable
        
        
       ## ships
        # do only when ship list changes
        if len(self.butsShipLaunch) != len( self.playerStatus.ships ) \
            or filter( lambda k: self.playerStatus.ships[k].type != self.butsShipLaunch[k].uid, 
                       xrange( 0, len(self.playerStatus.ships ) ) ):
            self.butsShipLaunch = []
            self.butsShipBuild = []
            
            for ship,slot in zip( self.playerStatus.ships, self.shipSlots ):
                butLaunch = RoundSwitch( [self.imgs.ctrlHangarRecall,self.imgs.ctrlHangarLaunch], (slot[0]+slot[2]/2,slot[1]-6), 12, self.eLaunchShip, uid=ship.type)
                butBuild = SlotButton( self.imgs, slot, eBuild=self.eBuildShip, uid=ship.type )
                self.butsShipLaunch.append( butLaunch )
                self.butsShipBuild.append( butBuild )
                

        # do at each frame
        for ship,butBuild,butLaunch in zip( self.playerStatus.ships, self.butsShipBuild, self.butsShipLaunch ):
            if ship.show:
                butBuild.imgOver = self.imgs.shipsIcons[ ship.type ]
                butBuild.quantity = ship.nbr
            else:
                butBuild.imgOver = None
                butBuild.quantity = -1

           # if ship.canBuild or ship.buildPerc >= 0:
            butLaunch.enabled = \
             butLaunch.visible = ship.nbr #  or ship.buildPerc >= 0 ) and ship.usable
                  
            butLaunch.state = ship.canLaunch
                
            butBuild.buildPerc = ship.buildPerc
            
            
        if self.targetting:
            self.controls = [
                self.ctrlBack,
            ]
        else:
            self.controls = [
            ]
        self.controls+=self.butsShipBuild+self.butsShipLaunch+self.butsMissileBuild+self.butsMissileLaunch
        
        
    def draw( self, display, focused=False, over=False, mouse=(0,0) ):
        if self.topLeft != self.center:
            for ctrl in self.butsShipBuild+self.butsShipLaunch+self.butsMissileBuild+self.butsMissileLaunch:
                ctrl.topLeft = (ctrl.topLeft[0]+self.topLeft[0]-self.center[0], ctrl.topLeft[1]+self.topLeft[1]-self.center[1] )
            self.center = self.topLeft
    
        self.display = display
       # self.slotWidth = display.getWidth(self.imgs.ctrlHangarSlot)
        self.missileSlots = []
        self.shipSlots = []
    
        self.size = (display.getWidth(self.imgs.ctrlHangarLeft)+display.getWidth(self.imgs.ctrlHangarCenter)+display.getWidth(self.imgs.ctrlHangarRight)+display.getWidth(self.imgs.ctrlHangarSlot)*(len(self.playerStatus.missiles)+len(self.playerStatus.ships)),
                     display.getHeight(self.imgs.ctrlHangarCenter))
        
        display.draw( self.imgs.ctrlHangarLeft, 
            (self.center[0]-display.getWidth(self.imgs.ctrlHangarLeft)-display.getWidth(self.imgs.ctrlHangarCenter)/2-(len(self.playerStatus.missiles)+1)*display.getWidth(self.imgs.ctrlHangarSlot),
             self.center[1]-display.getHeight(self.imgs.ctrlHangarLeft)) )
        
        # missiles
        builderCount = 0
        builderTotal = len( filter( self.missileIsBuilder, self.playerStatus.missiles ) )
        combatCount = 0
        combatTotal = len( self.playerStatus.missiles ) - builderTotal

        for missile in self.playerStatus.missiles:
            if self.missileIsBuilder( missile ): # builder missile 
                slotLeft = self.center[0]-display.getWidth(self.imgs.ctrlHangarCenter)/2-(builderTotal-builderCount+1+combatTotal)*display.getWidth(self.imgs.ctrlHangarSlot)
                builderCount += 1
            else: # conbat missile
                slotLeft = self.center[0]-display.getWidth(self.imgs.ctrlHangarCenter)/2-(combatTotal-combatCount)*display.getWidth(self.imgs.ctrlHangarSlot)
                combatCount += 1
            
            self.missileSlots.append( (
                slotLeft,
                self.center[1]-display.getHeight(self.imgs.ctrlHangarSlot),
                display.getWidth(self.imgs.ctrlHangarSlot),
                display.getHeight(self.imgs.ctrlHangarSlot)) )
                
        display.draw( self.imgs.uiHangarMissilesSeparator, 
            (self.center[0]-display.getWidth(self.imgs.ctrlHangarCenter)/2-(combatTotal+1)*display.getWidth(self.imgs.ctrlHangarSlot),
             self.center[1]-display.getHeight(self.imgs.ctrlHangarCenter)) )
        
        display.draw( self.imgs.ctrlHangarCenter, 
            (self.center[0]-display.getWidth(self.imgs.ctrlHangarCenter)/2,
             self.center[1]-display.getHeight(self.imgs.ctrlHangarCenter)) )
        
        for k,ship in enumerate( self.playerStatus.ships ):
            self.shipSlots.append( (
                self.center[0]+display.getWidth(self.imgs.ctrlHangarCenter)/2+k*display.getWidth(self.imgs.ctrlHangarSlot),
                self.center[1]-display.getHeight(self.imgs.ctrlHangarSlot),
                display.getWidth(self.imgs.ctrlHangarSlot),
                display.getHeight(self.imgs.ctrlHangarSlot)) )
                
           # display.draw( self.imgs.ctrlHangarSlot, 
           #     (self.center[0]+display.getWidth(self.imgs.ctrlHangarCenter)/2+k*display.getWidth(self.imgs.ctrlHangarSlot),
           #      self.center[1]-display.getHeight(self.imgs.ctrlHangarSlot)) )
        
        display.draw( self.imgs.ctrlHangarRight, 
            (self.center[0]+display.getWidth(self.imgs.ctrlHangarCenter)/2+len(self.playerStatus.ships)*display.getWidth(self.imgs.ctrlHangarSlot),
             self.center[1]-display.getHeight(self.imgs.ctrlHangarRight)) )
             
        if self.playerStatus.hangarSpace:
            self.display.drawDoubleIncompletePie( (self.imgs.ctrlHangarMissilesFill, self.imgs.ctrlHangarShipsFill), (self.center[0], self.center[1] - 23), (100*self.playerStatus.missilesSpace/self.playerStatus.hangarSpace,100*self.playerStatus.shipsSpace/self.playerStatus.hangarSpace) ) 
        display.draw( self.imgs.ctrlHangarOver, 
            (self.center[0]-display.getWidth(self.imgs.ctrlHangarOver)/2,
             self.center[1]-display.getHeight(self.imgs.ctrlHangarOver)) )
            
        Container.draw( self, display, focused=focused, over=over, mouse=mouse )
        
   # def setTargetting( self, targetting ):
   #     if targetting:
   #         self.controls = [
   #             self.ctrlBack,
   #         ]
   #     else:
   #         self.controls = [
   #         ]
   #     self.controls+=self.butsShipBuild+self.butsShipLaunch+self.butsMissileBuild+self.butsMissileLaunch

    def eSwitchLaunchMissile( self, sender, (x,y) ):
        self.switchLaunchMissile( sender.uid )

    def switchLaunchMissile( self, type ):
        if self.targetting == type:
            self.targetting = None
        else:
            self.targetting = type
        
    def eTargetMissile( self, sender, (x,y) ):
        if self.eOutLaunchMissile:
            self.eOutLaunchMissile( self.targetting, (x,y) )
        self.targetting = None
        
    def eLaunchShip( self, sender, (x,y) ):
        if sender.state:
            if self.eOutLaunchShip:
                self.eOutLaunchShip( sender.uid )
        else:
            if self.eOutRecallShip:
                self.eOutRecallShip( sender.uid )
        
    def eBuildMissile( self, sender, (x,y) ):
        if self.eOutBuildMissile:
            self.eOutBuildMissile( sender.uid )
        
    def eBuildShip( self, sender, (x,y) ):
        if self.eOutBuildShip:
            self.eOutBuildShip( sender.uid )
        
    def hits( self, up=None, down=None ):
        hit = Container.hits( self, up=up, down=down )
        if not hit \
            and ((up \
                and up[0]>self.center[0]-self.size[0]/2 and up[0]<self.center[0]+self.size[0]/2 \
                and up[1]>self.center[1]-self.size[1] and up[1]<self.center[1]) \
            or (down \
                and down[0]>self.center[0]-self.size[0]/2 and down[0]<self.center[0]+self.size[0]/2 \
                and down[1]>self.center[1]-self.size[1] and down[1]<self.center[1])):
            hit = self
        return hit

    def getHovered( self, mouse ):
        for control in [ self.controls[ k ] for k in xrange( len(self.controls)-1, -1, -1 ) ]:
            if control.fIn and control.fIn( control, mouse ):
                return control

        return None
    
    def missileIsBuilder( self, missile ):
        return missile.type in self.builderMissilesId
        
