from math import sin, cos, hypot, atan2, pi

from controls import *

class OptionButton( RectControl ):
    def __init__( self, img, (rx,ry), (rw,rh), fUpEvent, turretImg, text, fDownEvent=None, uid=None ):
        RectControl.__init__( self, img, (rx,ry), (rw,rh), fUpEvent, fDownEvent, uid=uid )
        self.turretImg = turretImg
        self.text = text
        self.r = 0
        self.ri = 0.02
        self.turretCenter = (rx+rw-rh/2,ry+rh/2)
         
    def draw( self, display, focused=False ):
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
         
    def draw( self, display, focused=False ):
        if self.visible:
          rect = (0,0,display.getWidth(self.img)/3,display.getHeight(self.img))

          display.drawClipped( self.img, self.topLeft, rect )
          if self.turretImg:
            display.drawRo( self.turretImg, self.turretCenter, self.r )
        self.r = (self.r + self.ri)%(2*pi)

class SelfDestructButton( RoundControl ):
    def __init__( self ):
        pass

