__all__ = [ "OptionButton", "TurretButton", "SelfDestructButton", "LightControlRight", "LightControlLeft", "LightControlDown", "LightControlUp", "RotatingImageHolder" ] 

from math import sin, cos, hypot, atan2, pi

from client.controls import *

class OptionButton( RectControl ):
    def __init__( self, img, (rx,ry), fUpEvent, turretImg, text, fDownEvent=None, uid=None ):
        (rw,rh) = ( 187, 59 )
        RectControl.__init__( self, img, (rx,ry), (rw,rh), fUpEvent, fDownEvent, uid=uid )
        self.turretImg = turretImg
        self.text = text
        self.r = 0
        self.ri = 0.02
        self.turretCenter = (rx+rw-18,ry+rh/2)
         
    def draw( self, display, focused=False, over=False, mouse=None ):
      #  RectControl.draw( self, display, focused )
        if self.visible:
            rect = (0,0,display.getWidth(self.img),display.getHeight(self.img))
            display.drawClipped( self.img, self.topLeft, rect )

            if self.enabled:
                textColor = (255,255,255,255)
            else:
                textColor = (0,0,0,255)

            display.drawText( self.text, (self.topLeft[0]+self.rw-40,self.topLeft[1]+22), textColor, align="right" )
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
        
    turretCenter = property( fget=lambda self: ( self.topLeft[0]+self.radius, self.topLeft[1]+self.radius ) )
         
    def draw( self, display, focused=False, over=False, mouse=None ):
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
    def __init__( self, (rx,ry), (rw,rh), fUpEvent, text, img, imgSelected, imgOver, imgDisabled, fDownEvent=None, uid=None ):
        
        RectControl.__init__( self, None, (rx,ry), (rw,rh), fUpEvent, fDownEvent, uid=uid )
        self.img = img
        self.imgSelected = imgSelected
        self.imgOver = imgOver
        self.imgDisabled = imgDisabled
        
        self.text = text
        self.color = (0,0,0) #(255,255,255)
        self.eEnter = fUpEvent

    def draw( self, display, focused=False, over=False, mouse=None ):
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
    width = 395
    height = 70
    def __init__( self, (rx,ry), fUpEvent, text, imgs, fDownEvent=None, uid=None ):
        ry += 23
        (rw,rh) = ( 395,70 )
        LightControl.__init__( self, (rx,ry), (rw,rh), fUpEvent, text, imgs.ctrlLightRight, imgs.ctrlLightRightSelected, imgs.ctrlLightRightOver, imgs.ctrlLightRightDisabled, fDownEvent=None, uid=uid )
    tx = property( fget=lambda self: self.topLeft[0]+self.rw/3 )
    ty = property( fget=lambda self: self.topLeft[1]+self.rh/2-8 )
    
class LightControlLeft( LightControl ):
    width = 395
    height = 70
    def __init__( self, (rx,ry), fUpEvent, text, imgs, fDownEvent=None, uid=None ):
        ry += 23
        (rw,rh) = ( 395,70 )
        LightControl.__init__( self, (rx,ry), (rw,rh), fUpEvent, text, imgs.ctrlLightLeft, imgs.ctrlLightLeftSelected, imgs.ctrlLightLeftOver, imgs.ctrlLightLeftDisabled, fDownEvent=None, uid=uid )
    tx = property( fget=lambda self: self.topLeft[0]+2*self.rw/5 )
    ty = property( fget=lambda self: self.topLeft[1]+self.rh/2-8 )
        
class LightControlDown( LightControl ):
    width = 241
    height = 60
    def __init__( self, (rx,ry), fUpEvent, text, imgs, fDownEvent=None, uid=None ):
        (rw,rh) = ( 241,60 )
        LightControl.__init__( self, (rx,ry), (rw,rh), fUpEvent, text, imgs.ctrlLightDown, imgs.ctrlLightDownSelected, imgs.ctrlLightDownOver, imgs.ctrlLightDownDisabled, fDownEvent=None, uid=uid )
    tx = property( fget=lambda self: self.topLeft[0]+self.rw/3 )
    ty = property( fget=lambda self: self.topLeft[1]+self.rh/2-8 )
        
class LightControlUp( LightControl ):
    width = 241
    height = 60
    def __init__( self, (rx,ry), fUpEvent, text, imgs, fDownEvent=None, uid=None ):
        (rw,rh) = ( 241,60 )
        LightControl.__init__( self, (rx,ry), (rw,rh), fUpEvent, text, imgs.ctrlLightUp, imgs.ctrlLightUpSelected, imgs.ctrlLightUpOver, imgs.ctrlLightUpDisabled, fDownEvent=None, uid=uid )
    tx = property( fget=lambda self: self.topLeft[0]+self.rw/3 )
    ty = property( fget=lambda self: self.topLeft[1]+self.rh/2-8 )
      
class RotatingImageHolder( ImageHolder ):
    def __init__( self, img, center, ri=0.0, r=0.0 ):
        ImageHolder.__init__( self, img, None )
        self.center = center
        self.ri = ri
        if r==None and ri:
            self.r = 2*pi*random()
        else:
            self.r = r

    def draw( self, display, focused=False, over=False, mouse=None ):
        if self.visible and self.img:
            display.drawRo( self.img, self.center, self.r )
            self.r += self.ri
            
class ListControl( RectControl ):
    def __init__( self, (rx,ry), uid=None ):
        self.controls
        
    def hits( self, up=None, down=None ):
        hit = False
        if self.enabled and self.fIn:
            if up and self.fIn( self, up ):
                hit = True
                if self.fUpEvent:
                    self.fUpEvent( self, up )
            if down and self.fIn( self, down ):
                hit = True
                if self.fDownEvent:
                    self.fDownEvent( self, down )
        return hit
        
    def draw( self, display, focused=False, over=False, mouse=None ):
      if self.visible and self.img:
        rect = (0,0,display.getWidth(self.img)/3,display.getHeight(self.img))

        if not self.enabled:
            rect = (rect[2]*2, rect[1], rect[2]*3, rect[3] )
        elif self.over:
            rect = (rect[2], rect[1], rect[2]*2, rect[3] )

        display.drawClipped( self.img, self.topLeft, rect )    
