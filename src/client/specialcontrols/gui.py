from math import pi, sin, cos, hypot

from client.controls import *
from common import utils
from common import ids
from common import config

class GuiBackPlay( RectControl ):
    pass

class GuiBackFullscreenRadar( RectControl ):
    def __init__( self, universeWidth, universeHeight ):
        self.universeWidth = universeWidth
        self.universeHeight = universeHeight
        self.playerStats = None
        self.astres = None
        self.objects = None
        
        self.radarColors = { 
             ids.U_FLAGSHIP: (255,255,255,255),
             ids.U_OWN: (0,255,0,255),
             ids.U_FRIENDLY: (0,0,255,255),
             ids.U_ENNEMY: (255,0,0,255),
             ids.U_ORBITABLE: (127,127,127,255) }
        
    def draw( self, display, focused=False, over=False ):
        if self.visible:
            display.clear()
            if self.playerStats:
                dx = dy = max( float(self.universeWidth)*2/display.resolution[0], float(self.universeHeight)*2/ display.resolution[1] )
                display.drawCircle( (255,255,255,255), (display.resolution[0]/2+self.playerStats.xr/dx,display.resolution[1]/2-self.playerStats.yr/dy), self.playerStats.maxRadar/dx, 1 )
                for obj in utils.mY(self.astres,self.objects):
                    if self.radarColors.has_key( obj.relation ):
                        pos = (int(display.resolution[0]/2+(obj.xp)/dx),
                        int(display.resolution[1]/2-(obj.yp)/dx))
                        display.drawCircle( self.radarColors[ obj.relation ], pos, obj.selectRadius/dx )
                
                
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
    
class UiPanel( Control ):
    pass
    
class Radar( Control ):
    def draw( self, display, focused=False, over=False ):
    
        for obj in self.objects:
            if self.radarColors.has_key( obj.relation ):
                dist = hypot( obj.yp-self.playerStats.yr, obj.xp-self.playerStats.xr )
                if dist <= self.playerStats.maxRadar:
                    pos = (int(self.radarCenter[0]+float(self.radarRadius)*(obj.xp-self.playerStats.xr)/self.playerStats.maxRadar),
                        int(self.radarCenter[1]-float(self.radarRadius)*(obj.yp-self.playerStats.yr)/self.playerStats.maxRadar))
                    self.display.drawPoint( pos, self.radarColors[ obj.relation ] )

        viewRect = (self.radarCenter[0]+float(self.radarRadius)*(self.camera[0]-self.playerStats.xr)/self.playerStats.maxRadar,
                    self.radarCenter[1]-float(self.radarRadius)*(self.camera[1]+self.display.resolution[1]-self.playerStats.yr)/self.playerStats.maxRadar,
                    self.display.resolution[0]*float(self.radarRadius)/self.playerStats.maxRadar,
                    self.display.resolution[1]*float(self.radarRadius)/self.playerStats.maxRadar)

        left = self.radarCenter[0]+float(self.radarRadius)*(self.camera[0]-self.playerStats.xr)/self.playerStats.maxRadar
        top = self.radarCenter[1]-float(self.radarRadius)*(self.camera[1]+self.display.resolution[1]-self.playerStats.yr)/self.playerStats.maxRadar
        right = left+self.display.resolution[0]*float(self.radarRadius)/self.playerStats.maxRadar
        bottom = top+self.display.resolution[1]*float(self.radarRadius)/self.playerStats.maxRadar

        self.display.drawLine( self.radarViewColor, # top
             ( max( left, self.radarCenter[0]-ihypot(self.radarRadius, top-self.radarCenter[1])), top ),
             ( min( right, self.radarCenter[0]+ihypot(self.radarRadius, top-self.radarCenter[1])), top ) )
        self.display.drawLine( self.radarViewColor, # bottom
             ( max( left, self.radarCenter[0]-ihypot(self.radarRadius, self.radarCenter[1]-bottom)), bottom ),
             ( min( right, self.radarCenter[0]+ihypot(self.radarRadius, self.radarCenter[1]-bottom)), bottom ) )
        self.display.drawLine( self.radarViewColor, # left
             ( left, max( top, self.radarCenter[1]-ihypot(self.radarRadius, self.radarCenter[0]-left)) ),
             ( left, min( bottom, self.radarCenter[1]+ihypot(self.radarRadius, self.radarCenter[0]-left)) ) )
        self.display.drawLine( self.radarViewColor,  # right
             ( right, max( top, self.radarCenter[1]-ihypot(self.radarRadius, self.radarCenter[0]-right)) ),
             ( right, min( bottom, self.radarCenter[1]+ihypot(self.radarRadius, self.radarCenter[0]-right)) ) )

 
        self.display.drawText( str( self.playerStats.maxRadar ), (142,55), size=13 )
        self.display.drawText( "%0.1f  %0.1f"% ( self.playerStats.xr/1000, self.playerStats.yr/1000 ), (139,83), size=13 )


class SelfDestructControl( Control ):
    def __init__( self, imgs, center, explodeEvent, uid=None ):
        Control.__init__( self, None, None, fIn=None, uid=uid )
        self.center = center
        self.open = False
        self.rotation = 0
        self.rotationSpeed = 2*pi/config.fps
        
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
        
    def draw( self, display, focused=False, over=False ):
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
            if control.hits( up=up, down=down ):
                return True
        return False
        
    def eOpen( self, sender, (x,y) ):
        self.open = True
        
    def eClose( self, sender, (x,y) ):
        self.open = False
        
