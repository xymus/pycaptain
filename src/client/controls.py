from math import sin, cos, hypot, atan2, pi
from random import random

from common.comms import COInput

class ControlFrame:
    def __init__(self):
        self.controls = []
        self.selectables = []
        self.tabOrder = {}
        self.tabOrderReverse = {}
        self.selected = None
        self.eEnter = None
        self.inputs = None
        self.lastControlAdded = None
        self.inputs = COInput()

    def addControl( self, control ):
        self.controls.append( control )
        
        if control.selectable:
            if not self.selected: # same as not self.selectables
                self.selected = control
                self.tabOrder[ control ] = control
                self.tabOrderReverse[ control ] = control
            else:
                self.tabOrder[ self.selectables[ -1 ] ] = control
                self.tabOrder[ control ] = self.selectables[ 0 ]
                self.tabOrderReverse[ control ] = self.selectables[ -1 ]
                self.tabOrderReverse[ self.selectables[ 0 ] ] = control
            self.selectables.append( control )
                
    def addControls( self, controls ):
        for control in controls:
            self.addControl( control )

    def setControls( self, controls ):
        self.controls = []
        self.selectables = []
        self.tabOrder = {}
        self.tabOrderReverse = {}
        for control in controls:
            self.addControl( control )

    def keyInput( self, key, letter=None ):
        if letter == "\r":
            if not self.selected or not self.selected.eEnter:
                if self.eEnter:
                    self.eEnter( self, (0,0) )
            elif self.selected and self.selected.eEnter:
                self.selected.eEnter( self, (0,0) )
        if self.selected:
            if letter == "\t":
                prevSlected = self.selected
                self.selected = self.tabOrder[ self.selected ]
                while prevSlected != self.selected and not self.selected.enabled:
                    self.selected = self.tabOrder[ self.selected ]
            else:
                self.selected.keyInput( key, letter )
             
        else:
            for control in self.controls:
                if isinstance( control, KeyCatcher ):
                    control.keyInput( key, letter )

    def manageInputs( self, display ):
        (quit, self.inputs) = display.getInputs( self.inputs )

        if self.inputs.mouseUpped:
            up = self.inputs.mouseUpAt
        else:
            up = None
            
        if self.inputs.mouseDowned:
            down = self.inputs.mouseDownAt
        else:
            down = None
            
        if self.inputs.mouseUpped or self.inputs.mouseDowned:
            for control in self.controls:
                if control.hits( up=up, down=down ):
                #    print self.inputs.mouseUpped, self.inputs.mouseDowned, self.inputs.mouseUpAt, self.inputs.mouseDownAt
                    self.selected = control
                    break

        if self.inputs.keys:
            for k in self.inputs.keys:
                self.keyInput( k[0], k[1] )

        return quit
        
    def draw( self, display ):
        display.beginDraw()
        for control in self.controls:
            control.draw( display, 
                focused=(control==self.selected), 
                over=(control.fIn and control.fIn( self.inputs.mousePos )) 
                )
        display.finalizeDraw()
        # TODO be careful here as it might be used twice in some menus

class ControlBase:
    def __init__( self, fUpEvent=None, fDownEvent=None, uid=None ):
        self.fUpEvent = fUpEvent
        self.fDownEvent = fDownEvent
        self.uid = uid

    def hits( self, up=None, down=None ):
        return False

    def draw( self, display, focused=False, over=False ):
        pass

    def keyInput( self, key, letter=None ):
        pass

class Control( ControlBase ):
    def __init__( self, img, topLeft, fIn, fUpEvent=None, fDownEvent=None, fOverEvent=None, uid=None ):
        self.img = img
        self.topLeft = topLeft
        self.fIn = fIn
        self.fUpEvent = fUpEvent
        self.fDownEvent = fDownEvent
        self.fOverEvent = fOverEvent
        self.uid = uid
        self.over = False
        self.enabled = True
        self.visible = True
        self.eEnter = None
        self.selectable = True

    def hits( self, up=None, down=None ):
        hit = False
        if self.enabled and self.fIn:
            if up and self.fIn( up ):
                hit = True
                if self.fUpEvent:
                    self.fUpEvent( self, up )
            if down and self.fIn( down ):
                hit = True
                if self.fDownEvent:
                    self.fDownEvent( self, down )
        return hit

    def draw( self, display, focused=False, over=False ):
      if self.visible and self.img:
        rect = (0,0,display.getWidth(self.img)/3,display.getHeight(self.img))

        if not self.enabled:
            rect = (rect[2]*2, rect[1], rect[2]*3, rect[3] )
        elif self.over:
            rect = (rect[2], rect[1], rect[2]*2, rect[3] )

        display.drawClipped( self.img, self.topLeft, rect )

    def keyInput( self, key, letter=None ):
   # def keyHits( self, key, letter=None ):
        pass

class RoundControl( Control ):
    def __init__( self, img, center, radius, fUpEvent, fDownEvent=None, uid=None ):
        def fIn( (x, y) ):
            dist = hypot( y-center[1], x-center[0] )
            return dist <= radius
        self.radius = radius
        Control.__init__( self, img, (center[0]-radius,center[1]-radius), fIn, fUpEvent, fDownEvent, uid=uid )

class RectControl( Control ):
     def __init__( self, img, (rx,ry), (rw,rh), fUpEvent, fDownEvent=None, uid=None ):
        def fIn( (x, y) ):
       #     print "%i, %i, %i, %i" % (rx, rw, x, y )
            return x >= rx \
               and y >= ry \
               and x <= rx + rw \
               and y <= ry + rh
        self.rw = rw
        self.rh = rh

        Control.__init__( self,img, (rx,ry), fIn, fUpEvent, fDownEvent, uid=uid )

class RectSwitch( RectControl ):
    def __init__( self, imgs, (rx,ry), (rw,rh), fUpEvent, fDownEvent=None, uid=None ):
        RectControl.__init__( self, imgs[0], (rx,ry), (rw,rh), fUpEvent, fDownEvent, uid=uid )
        self.imgs = imgs
        self.state = 0

    def draw( self, display, focused=False, over=False ):
      if self.visible:
        self.img = self.imgs[ self.state ]
        RectControl.draw( self, display )

class RoundSwitch( RoundControl ):
    def __init__( self, imgs, center, radius, fUpEvent, fDownEvent=None, uid=None ):
        RoundControl.__init__( self, imgs[0], center, radius, fUpEvent, fDownEvent, uid=uid )
        self.imgs = imgs
        self.state = 0

    def draw( self, display ):
      if self.visible:
        self.img = self.imgs[ self.state ]
        RoundControl.draw( self, display )

class RoundControlInvisible( Control ):
    def __init__( self, center, radius, fUpEvent, fDownEvent=None ):
        def fIn( (x, y) ):
            dist = hypot( y-center[1], x-center[0] )
            return dist <= radius

        Control.__init__( self, None, (center[0]-radius,center[1]-radius), fIn, fUpEvent, fDownEvent )

    def draw( self, display, focused=False, over=False ):
        pass

class TextBox( RectControl ):
    def __init__( self, (rx,ry), (rw,rh), defaultText="", password=False, numeric=False, forbidden=[] ):
        RectControl.__init__( self, None, (rx,ry), (rw,rh), None, None )
        self.text = defaultText
        self.selection = 0
        self.password = password
        self.numeric = numeric
        self.forbidden = forbidden
        
    def draw( self, display, focused=False, over=False ):
      if self.visible:
        display.drawLine( (255,255,255,255), (self.topLeft[0],self.topLeft[1]+self.rh), (self.topLeft[0]+self.rw,self.topLeft[1]+self.rh), 1 )
        
        if focused:
            display.drawLine( (255,255,255,255), (self.topLeft[0],self.topLeft[1]+self.rh+2), (self.topLeft[0]+self.rw,self.topLeft[1]+self.rh+2), 1 )
            
        if self.password:
            display.drawText( "*"*len(self.text), self.topLeft )
        else:
            display.drawText( self.text, self.topLeft )
    #    print "drawn"
        
    def keyInput( self, key, letter=None ):
      if key == 8:
        if len( self.text ) > 0:
          self.text = self.text[:-1]
      elif letter and letter != "\r": #len(: #key >= ord(" ") and  key < ord("z"):
    #    letter = chr(key)
        if not self.numeric or ( letter <= "9" and letter >= "0" ) and letter not in self.forbidden:
            self.text = self.text + letter
      else:
        print "unhandled  key:", key

class Label( Control ):
    def __init__( self, topLeft, text ):
        Control.__init__( self, None, topLeft, None, None, None, uid=None )
        self.text = text
        self.selectable = False

    def hits( self, up=None, down=None ):
        pass

    def draw( self, display, focused=False, over=False ):
      if self.visible:
        display.drawText( self.text, self.topLeft )

class LabelButton( RectControl ):
     def __init__( self, (rx,ry), (rw,rh), fUpEvent, text, fDownEvent=None, uid=None ):
        RectControl.__init__( self, None, (rx,ry), (rw,rh), fUpEvent, fDownEvent, uid=uid )
        self.text = text

     def draw( self, display, focused=False, over=False ):
      if self.visible:
        if self.enabled:
            color = (255,255,255,255)
        else:
            color = (128,128,128,255)
        display.drawText( self.text, (self.topLeft[0]+self.rw/3,self.topLeft[1]+4 ), color=color )
        display.drawRect( (self.topLeft[0], self.topLeft[1], self.rw, self.rh), color=color, width=1 )
        if focused:
            display.drawRect( (self.topLeft[0]+1, self.topLeft[1]+1, self.rw-2, self.rh-2), color=color, width=1 )
        #display.drawLine( (255,255,255,255), self.topLeft, (self.topLeft[0]+self.rw,self.topLeft[1]) )
        #display.drawLine( (255,255,255,255), self.topLeft, (self.topLeft[0],self.topLeft[1]+self.rh) )

        #display.drawLine( (255,255,255,255), (self.topLeft[0]+self.rw,self.topLeft[1]), (self.topLeft[0]+self.rw,self.topLeft[1]+self.rh) )
        #display.drawLine( (255,255,255,255), (self.topLeft[0],self.topLeft[1]+self.rh), (self.topLeft[0]+self.rw,self.topLeft[1]+self.rh) )

class ProgressBar( RectControl ):
     def __init__( self, (rx,ry), (rw,rh), uid=None ):
        RectControl.__init__( self, None, (rx,ry), (rw,rh), None, None, uid=uid )
        self.progress = 0
        self.selectable = False

     def draw( self, display, focused=False, over=False ):
      if self.visible:
        display.drawRect( (self.topLeft[0], self.topLeft[1], self.rw, self.rh), (255,255,255), 1 )
        display.drawRect( (self.topLeft[0]+2, self.topLeft[1]+2, (self.rw-4)*self.progress, self.rh-4), (255,255,255) )

class KeyCatcher( ControlBase ):
    def __init__( self, fUpEvent, key=None, letter=None, fDownEvent=None, uid=None ):
        ControlBase.__init__( self, fUpEvent, fDownEvent, uid=uid )
        self.key = key
        self.letter = letter
        self.selectable = False
        self.fIn = None

    def keyInput( self, key, letter=None ):
        if self.fUpEvent and (key and key == self.key) or (letter and letter == self.letter) :
            self.fUpEvent( self, (0,0) )

class Panel( ControlBase ):
    def __init__( self, img, (x,y) ):
        self.selectable = False

class ImageHolder( Control ):
    def __init__( self, img, topLeft ):
        Control.__init__( self, img, topLeft, None )
        self.enabled = False
        self.selectable = False

    def draw( self, display, focused=False, over=False ):
        if self.visible and self.img:
            display.draw( self.img, self.topLeft )
            
