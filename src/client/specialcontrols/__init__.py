__all__ = [ "OptionButton", "TurretButton", "SelfDestructButton", "LightControlRight", "LightControlLeft", "RotatingImageHolder" ] 

from math import sin, cos, hypot, atan2, pi

from client.controls import *

class OptionButton( RectControl ):
    def __init__( self, img, (rx,ry), (rw,rh), fUpEvent, turretImg, text, fDownEvent=None, uid=None ):
        RectControl.__init__( self, img, (rx,ry), (rw,rh), fUpEvent, fDownEvent, uid=uid )
        self.turretImg = turretImg
        self.text = text
        self.r = 0
        self.ri = 0.02
        self.turretCenter = (rx+rw-rh/2,ry+rh/2)
         
    def draw( self, display, focused=False, over=False ):
      #  RectControl.draw( self, display, focused )
        if self.visible:
            rect = (0,0,display.getWidth(self.img),display.getHeight(self.img))
            display.drawClipped( self.img, self.topLeft, rect )

            if self.enabled:
                textColor = (255,255,255,255)
            else:
                textColor = (128,128,128,255)

            display.drawText( self.text, (self.topLeft[0]+16,self.topLeft[1]+8), textColor )
            if self.turretImg:
              display.drawRo( self.turretImg, self.turretCenter, self.r )
        self.r = (self.r + self.ri)%(2*pi)

class TurretButton( RoundControl ):
    def __init__( self, img, (cx,cy), radius, fUpEvent, turretImg, fDownEvent=None, uid=None ):
        RoundControl.__init__( self, img, (cx,cy), radius, fUpEvent, fDownEvent, uid=uid )
        self.turretImg = turretImg
        self.rx = self.topLeft[0]
        self.ry = self.topLeft[1]
        self.r = 0
        self.ri = 0.02
        self.turretCenter = (self.rx+self.radius,self.ry+self.radius)
         
    def draw( self, display, focused=False, over=False ):
        if self.visible:
          rect = (0,0,display.getWidth(self.img)/3,display.getHeight(self.img))

          display.drawClipped( self.img, self.topLeft, rect )
          if self.turretImg:
            display.drawRo( self.turretImg, self.turretCenter, self.r )
        self.r = (self.r + self.ri)%(2*pi)

class SelfDestructButton( RoundControl ):
    def __init__( self ):
        pass

class LightControl( RectControl ):
    def __init__( self, (rx,ry), fUpEvent, text, img, imgSelected, imgOver, imgDisabled, fDownEvent=None, uid=None ):
        (rw,rh) = ( 395,107 )
        
        RectControl.__init__( self, None, (rx,ry), (rw,rh), fUpEvent, fDownEvent, uid=uid )
        self.img = img
        self.imgSelected = imgSelected
        self.imgOver = imgOver
        self.imgDisabled = imgDisabled
        
        self.text = text
        self.color = (255,255,255)
        self.eEnter = fUpEvent

    def draw( self, display, focused=False, over=False ):
        if self.visible:
            if focused:
                display.draw( self.imgSelected, self.topLeft )
            if self.enabled:
                if over:
                    display.draw( self.imgOver, self.topLeft )
                else:
                    display.draw( self.img, self.topLeft )
            else:
                display.draw( self.imgDisabled, self.topLeft )
                
            display.drawText( self.text, (self.tx,self.ty ), color=self.color )
            
class LightControlRight( LightControl ):
    def __init__( self, (rx,ry), fUpEvent, text, imgs, fDownEvent=None, uid=None ):
        LightControl.__init__( self, (rx,ry), fUpEvent, text, imgs.ctrlLightRight, imgs.ctrlLightRightSelected, imgs.ctrlLightRightOver, imgs.ctrlLightRightDisabled, fDownEvent=None, uid=None )
        self.tx = self.topLeft[0]+self.rw/3
        self.ty = self.topLeft[1]+self.rh/2-8
    
class LightControlLeft( LightControl ):
    def __init__( self, (rx,ry), fUpEvent, text, imgs, fDownEvent=None, uid=None ):
        LightControl.__init__( self, (rx,ry), fUpEvent, text, imgs.ctrlLightLeft, imgs.ctrlLightLeftSelected, imgs.ctrlLightLeftOver, imgs.ctrlLightLeftDisabled, fDownEvent=None, uid=None )
        self.tx = self.topLeft[0]+2*self.rw/5
        self.ty = self.topLeft[1]+self.rh/2-8
      
class RotatingImageHolder( ImageHolder ):
    def __init__( self, img, center, ri=0, r=None ):
        ImageHolder.__init__( self, img, None )
        self.center = center
        self.ri = ri
        if r==None and ri:
            self.r = 2*pi*random()
        else:
            self.r = r

    def draw( self, display, focused=False, over=False ):
        if self.visible and self.img:
            display.drawRo( self.img, self.center, self.r )
            self.r += self.ri
            
              
