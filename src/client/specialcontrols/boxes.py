from client.controls import *
from client.specialcontrols import *


class Box( RectControl ):
    def __init__( self, imgs, topLeft, size ):
        RectControl.__init__( self, None, topLeft, size, None )
       #  self, None, (center[0]-radius,center[1]-radius), fIn, fUpEvent, fDownEvent, uid=uid )
       # self.topLeft = topLeft
       # self.size = size
        self.imgs = imgs
        
    def draw( self, display, focused=False, over=False, mouse=(0,0) ):
        if self.rw%display.getWidth(self.imgs.ctrlBoxCenter):
            self.rw = (self.rw//display.getWidth(self.imgs.ctrlBoxCenter) )*display.getWidth(self.imgs.ctrlBoxTop)
        if self.rh%display.getHeight(self.imgs.ctrlBoxCenter):
            self.rh = (self.rh//display.getHeight(self.imgs.ctrlBoxCenter) )*display.getHeight(self.imgs.ctrlBoxCenter)
            
            
        display.draw( self.imgs.ctrlBoxTopLeft, 
            (self.rx-display.getWidth(self.imgs.ctrlBoxTopLeft), self.ry-display.getHeight(self.imgs.ctrlBoxTopLeft)) )
        display.draw( self.imgs.ctrlBoxTopRight, 
            (self.rx+self.rw, self.ry-display.getHeight(self.imgs.ctrlBoxTopRight)) )
        display.draw( self.imgs.ctrlBoxBottomLeft, 
            (self.rx-display.getWidth(self.imgs.ctrlBoxBottomLeft), self.ry+self.rh) )
        display.draw( self.imgs.ctrlBoxBottomRight, 
            (self.rx+self.rw, self.ry+self.rh) )
        
        for x in xrange( 0, self.rw, display.getWidth(self.imgs.ctrlBoxCenter) ):
            display.draw( self.imgs.ctrlBoxTop, 
                (self.rx+x, self.ry-display.getHeight(self.imgs.ctrlBoxTop)) )
            display.draw( self.imgs.ctrlBoxBottom, 
                (self.rx+x, self.ry+self.rh) )
        
        for y in xrange( 0, self.rh, display.getHeight(self.imgs.ctrlBoxCenter) ):
            display.draw( self.imgs.ctrlBoxLeft, 
                (self.rx-display.getWidth(self.imgs.ctrlBoxLeft), self.ry+y) )
            display.draw( self.imgs.ctrlBoxRight, 
                (self.rx+self.rw, self.ry+y) )
                
        for x in xrange( 0, self.rw, display.getWidth(self.imgs.ctrlBoxCenter) ):
            for y in xrange( 0, self.rh, display.getHeight(self.imgs.ctrlBoxCenter) ):
                display.draw( self.imgs.ctrlBoxCenter, 
                    (self.rx+x, self.ry+y) )

class MessageBox( Container ):
    def __init__( self, display, imgs, text, buttons=[], img=None, width=240, height=400, center=None ): 
        """buttons format = [("text", eFunc( sender, (x,y) ))]"""
        
        if not center:
            center = (display.resolution[0]/2, display.resolution[1]/2)
            
        self.topLeft = (center[0]-width/2, center[1]-height/2)
        Container.__init__( self )
        
        b = 8
        
        self.label = Label( (self.topLeft[0]+b,self.topLeft[1]+b), text, maxWidth=width-2*b )
        
        self.controls = [ #ImageHolder( imgs.boxBack, self.topLeft ),
                          self.label ]
        p = 0
        for but in buttons:
            self.controls.append( LightControlDown( (self.topLeft[0]+width*p/len(buttons)-LightControlDown.width/2,self.topLeft[1]+height-LightControlDown.height), but[1], but[0], imgs ) )
            p += 1
            
class LabelGlass( RectControl ):
    def __init__( self, img, topLeft, text ):
        RectControl.__init__( self, None, topLeft, (60,20), None )
        self.imgs = imgs
        self.text = text
        self.selectable = False
        self.textSize = 12
        self.offset = (4,4)
       # self.maxWidth = self.rw
       # self.maxHeight = maxHeight
        
    def draw( self, display, focused=False, over=False, mouse=(0,0) ):
        display.draw( self.imgs.ctrlLabelBack, self.topLeft )
        display.drawText( self.text, (self.topLeft[0]+self.offset[0],self.topLeft[1]+self.offset[1]), size=self.textSize )
        
class LabelImage( RectControl ):
    def __init__( self, img, topLeft, width, text ):
        RectControl.__init__( self, img, topLeft, (width,20), None )
        self.text = text
        self.selectable = False
        self.textSize = 12
        self.offset = (4,3)
       # self.maxWidth = self.rw
       # self.maxHeight = maxHeight
        
    def draw( self, display, focused=False, over=False, mouse=(0,0) ):
    #    RectControl.draw( self, display, focused, over, mouse )
        display.draw( self.img, self.topLeft )
        display.drawText( self.text, 
            (self.topLeft[0]-self.offset[0]+self.rw,self.topLeft[1]+self.offset[1]), 
            size=self.textSize, align="right" )
        
