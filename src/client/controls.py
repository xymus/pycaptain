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
        
        self.lastResolution = None

    def addControl( self, control ):
        self.controls.append( control )
        
        if control.selectable:
            if not self.selectables: # same as not self.selected
                self.tabOrder[ control ] = control
                self.tabOrderReverse[ control ] = control
                if not self.selected:
                    self.selected = control
            else:
                self.tabOrder[ self.selectables[ -1 ] ] = control
                self.tabOrder[ control ] = self.selectables[ 0 ]
                self.tabOrderReverse[ control ] = self.selectables[ -1 ]
                self.tabOrderReverse[ self.selectables[ 0 ] ] = control
            self.selectables.append( control )
                
    def addControls( self, controls ):
        for control in controls:
            self.addControl( control )
            
    def removeControl( self, control ):
        self.controls.remove( control )
        for k,v in self.tabOrder.iteritems():
            if v == control:
                self.tabOrder[ k ] = self.tabOrder[control]
                del self.tabOrder[ control ]
                break
        for k,v in self.tabOrderReverse.iteritems():
            if v == control:
                self.tabOrderReverse[ k ] = self.tabOrderReverse[control]
                del self.tabOrderReverse[ control ]
                break
        

    def setControls( self, controls ):
        self.controls = []
        self.selectables = []
        self.tabOrder = {}
        self.tabOrderReverse = {}
        for control in controls:
            self.addControl( control )

    def keyInput( self, key, letter=None ):
        used = False
        if letter == "\r":
            if not self.selected or not self.selected.eEnter:
                if self.eEnter:
                    self.eEnter( self, (0,0) )
            elif self.selected and self.selected.eEnter:
                self.selected.eEnter( self, (0,0) )
        if self.selected:
            if letter == "\t":
                prevSlected = self.selected
                if self.tabOrder.has_key( self.selected ):
                    self.selected = self.tabOrder[ self.selected ]
                    while prevSlected != self.selected and not self.selected.enabled:
                        self.selected = self.tabOrder[ self.selected ]
            else:
               # print self.selected, key, letter
                used = self.selected.keyInput( key, letter )
               # print "kaey a", used
             
        if not used:
           # print "kaey c"
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
            
        #print up, down
           
        self.hit = False # TODO hack, remove when back of gui impklemented as control
        if self.inputs.mouseUpped or self.inputs.mouseDowned:
            for control in [ self.controls[ k ] for k in xrange( len(self.controls)-1, -1, -1 ) ]:
          #  for control in self.controls:
                select = control.hits( up=up, down=down )
                if select: # control.hits( up=up, down=down ):
                    self.hit = True
                #    print self.inputs.mouseUpped, self.inputs.mouseDowned, self.inputs.mouseUpAt, self.inputs.mouseDownAt
                    if select.selectable:
                        self.selected = select
                   # print select, select.selectable
                    break

        if self.inputs.keys:
            for k in self.inputs.keys:
                self.keyInput( k[0], k[1] )

        return quit
        
    def draw( self, display, skipFinalize=False ):
        display.cursorDrawn = False
        if not self.lastResolution:
            self.lastResolution = display.resolution
        elif self.lastResolution != display.resolution:
        #    print "moving controls"
            diffWidth = display.resolution[0]-self.lastResolution[0]
            diffHeight = display.resolution[1]-self.lastResolution[1]
         #   print diffWidth, diffHeight, self.lastResolution, display.resolution
            for control in self.controls:
                if isinstance( control, Control ):
                    if not control.stickLeft: # sticks to the right of the screen
                        control.topLeft = ( control.topLeft[0]+diffWidth, control.topLeft[1] )
                    if not control.stickTop: # sticks to the bottom of the screen
                        control.topLeft = ( control.topLeft[0], control.topLeft[1]+diffHeight )
            self.lastResolution = display.resolution
                
        display.beginDraw()
        for control in self.controls:
            control.draw( display, 
                focused=(control==self.selected), 
                over=(control.fIn and control.fIn( control, self.inputs.mousePos )),
                mouse=self.inputs.mousePos
                )
                
        display.showCursor( not display.cursorDrawn )
        
        if not skipFinalize:
            display.finalizeDraw()
        
    def reset( self ):
        for control in self.controls:
            control.reset()

class ControlBase:
    def __init__( self, fUpEvent=None, fDownEvent=None, uid=None ):
        self.fUpEvent = fUpEvent
        self.fDownEvent = fDownEvent
        self.uid = uid

    def hits( self, up=None, down=None ):
        return False

    def draw( self, display, focused=False, over=False, mouse=None ):
        pass

    def keyInput( self, key, letter=None ):
        return False
        
    def reset( self ):
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
        
        self.stickLeft = True
        self.stickTop = True

    def hits( self, up=None, down=None ):
        hit = False
        if self.fIn:
            if up and self.fIn( self, up ):
                hit = self
                if self.enabled and self.fUpEvent:
                    self.fUpEvent( self, up )
            if down and self.fIn( self, down ):
                hit = self
                if self.enabled and self.fDownEvent:
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

    def keyInput( self, key, letter=None ):
        return False

class RoundControl( Control ):
    def __init__( self, img, center, radius, fUpEvent, fDownEvent=None, uid=None ):
        def fIn( self, (x, y) ):
            dist = hypot( y-self.center[1], x-self.center[0] )
            return dist <= self.radius
        
        self.radius = radius
        Control.__init__( self, img, (center[0]-radius,center[1]-radius), fIn, fUpEvent, fDownEvent, uid=uid )
    center = property( fget=lambda self: (self.topLeft[0]+self.radius, self.topLeft[1]+self.radius ) )

class RectControl( Control ):
     def __init__( self, img, (rx,ry), (rw,rh), fUpEvent, fDownEvent=None, uid=None ):
        def fIn( self, (x, y) ):
            return x >= self.topLeft[0] \
               and y >= self.topLeft[1] \
               and (self.rw == -1 or x <= self.topLeft[0] + self.rw) \
               and (self.rh == -1 or y <= self.topLeft[1] + self.rh)
        self.rw = rw
        self.rh = rh
        self.rx = rx
        self.ry = ry
        Control.__init__( self,img, (rx,ry), fIn, fUpEvent, fDownEvent, uid=uid )

class RectSwitch( RectControl ):
    def __init__( self, imgs, (rx,ry), (rw,rh), fUpEvent, fDownEvent=None, uid=None ):
        RectControl.__init__( self, imgs[0], (rx,ry), (rw,rh), fUpEvent, fDownEvent, uid=uid )
        self.imgs = imgs
        self.state = 0

    def draw( self, display, focused=False, over=False, mouse=None ):
      if self.visible:
        self.img = self.imgs[ self.state ]
        RectControl.draw( self, display, focused, over, mouse )

class RoundSwitch( RoundControl ):
    def __init__( self, imgs, center, radius, fUpEvent, fDownEvent=None, uid=None ):
        RoundControl.__init__( self, imgs[0], center, radius, fUpEvent, fDownEvent, uid=uid )
        self.imgs = imgs
        self.state = 0

    def draw( self, display, focused=False, over=False, mouse=None ):
      if self.visible:
        self.img = self.imgs[ self.state ]
        RoundControl.draw( self, display, focused, over, mouse )

class RoundControlInvisible( Control ):
    def __init__( self, center, radius, fUpEvent, fDownEvent=None ):
        def fIn( self, (x, y) ):
            dist = hypot( y-self.center[1], x-self.center[0] )
            return dist <= radius

    #    self.center = center
        self.radius = radius
        Control.__init__( self, None, (center[0]-radius,center[1]-radius), fIn, fUpEvent, fDownEvent )
    center = property( fget=lambda self: (self.topLeft[0]+self.radius, self.topLeft[1]+self.radius ) )

    def draw( self, display, focused=False, over=False, mouse=None ):
        pass

class TextBox( RectControl ):
    def __init__( self, (rx,ry), (rw,rh), defaultText="", password=False, numeric=False, forbidden=[], eTextChanged=None, eEnter=None ):
        RectControl.__init__( self, None, (rx,ry), (rw,rh), None, None )
        self.defaultText = defaultText
        self.text = defaultText
        self.selection = 0
        self.password = password
        self.numeric = numeric
        self.forbidden = forbidden
        
        self.eTextChanged = eTextChanged
        self.eEnter = eEnter
        
    def draw( self, display, focused=False, over=False, mouse=None ):
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
        used = False
        if key == 8:
            if len( self.text ) > 0:
                self.text = self.text[:-1]
                used = True
        elif letter:
            if letter == "\r":
                if self.eEnter:
                    self.eEnter( self, (0,0 ) )
                    used = True
            else: #len(: #key >= ord(" ") and  key < ord("z"):
        #    letter = chr(key)
                if not self.numeric or ( letter <= "9" and letter >= "0" ) and letter not in self.forbidden:
                    self.text = self.text + letter
                    used = True
        if used:
            if self.eTextChanged:
                self.eTextChanged( self, (0,0 ) )
        else:
            print "unhandled  key:", key
        return used
      
    def reset( self ):
        self.text = self.defaultText
        if self.eTextChanged:
            self.eTextChanged( self, (0,0 ) )
        

class Label( Control ):
    def __init__( self, topLeft, text, textSize=15, maxWidth=None, maxHeight=None ):
        Control.__init__( self, None, topLeft, None, None, None, uid=None )
        self.text = text
        self.selectable = False
        self.textSize = textSize
        self.maxWidth = maxWidth
        self.maxHeight = maxHeight

    def hits( self, up=None, down=None ):
        return False

    def draw( self, display, focused=False, over=False, mouse=None ):
        if self.visible:
            display.drawText( self.text, self.topLeft, size=self.textSize, maxWidth=self.maxWidth, maxHeight=self.maxHeight )

class LabelButton( RectControl ):
     def __init__( self, (rx,ry), (rw,rh), fUpEvent, text, fDownEvent=None, uid=None ):
        RectControl.__init__( self, None, (rx,ry), (rw,rh), fUpEvent, fDownEvent, uid=uid )
        self.text = text

     def draw( self, display, focused=False, over=False, mouse=None ):
        if self.visible:
            if self.enabled:
                color = (255,255,255,255)
            else:
                color = (128,128,128,255)
            display.drawText( self.text, (self.topLeft[0]+self.rw/3,self.topLeft[1]+4 ), color=color )
            display.drawRect( (self.topLeft[0], self.topLeft[1], self.rw, self.rh), color=color, width=1 )
            if focused:
                display.drawRect( (self.topLeft[0]+1, self.topLeft[1]+1, self.rw-2, self.rh-2), color=color, width=1 )

class ProgressBar( RectControl ):
     def __init__( self, (rx,ry), (rw,rh), uid=None ):
        RectControl.__init__( self, None, (rx,ry), (rw,rh), None, None, uid=uid )
        self.progress = 0
        self.selectable = False

     def draw( self, display, focused=False, over=False, mouse=None ):
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
        if self.fUpEvent and (key and key == self.key) or (letter and letter == self.letter):
            self.fUpEvent( self, (0,0) )
            return True
        return False

class Container( Control ):
    def __init__( self ):
        Control.__init__( self, None, (0,0), None )
        self.selectable = False
        self.controls = []
        self.fIn = None
        
    def draw( self, display, focused=False, over=False, mouse=(0,0) ):
        for control in self.controls: 
            control.draw( display, over=(control.fIn and control.fIn( control, mouse )), mouse=mouse )

    def hits( self, up=None, down=None ):
        for control in [ self.controls[ k ] for k in xrange( len(self.controls)-1, -1, -1 ) ]:
            select = control.hits( up=up, down=down )
            if select:
                return select
        return False
        
    def keyInput( self, key, letter=None ):
        return False

class ImageHolder( RectControl ):
    def __init__( self, img, topLeft, size=(0,0) ):
        if not topLeft:
            topLeft=(0,0)
        RectControl.__init__( self, img, topLeft, size, None )
        self.enabled = False
        self.selectable = False

    def draw( self, display, focused=False, over=False, mouse=None ):
        if self.visible and self.img:
            display.draw( self.img, self.topLeft )
            
class Slider( RectControl ):
    def __init__( self, imgs, topLeft, width, values, defaultValue=None, eChangedValue=None, rounded=False ):
        RectControl.__init__( self, None, topLeft, (width,20), self.eClick )
        self.imgs = imgs
        self.values = values # min, max
        self.rounded = rounded
        self.eChangedValue = eChangedValue
        if defaultValue == None:
            self.value = self.values[0]
        else:
            self.value = defaultValue
        
    def eClick( self, sender, (x,y) ):
        oldValue = self.value
        self.value = self.values[0]+ 1.0*(self.values[1]-self.values[0])*(x-self.rx)/self.rw
        if self.rounded:
            self.value = round( self.value )
            
        if self.eChangedValue and self.value != oldValue:
            self.eChangedValue( self, (x,y) )
        
    def draw( self, display, focused=False, over=False, mouse=None ):
        if self.rw%display.getWidth(self.imgs.ctrlSliderCenter):
            self.rw = (self.rw//display.getWidth(self.imgs.ctrlSliderCenter)) *display.getWidth(self.imgs.ctrlSliderCenter)
            
        for x in xrange( 0, self.rw, display.getWidth(self.imgs.ctrlSliderCenter) ):
            display.draw( self.imgs.ctrlSliderCenter, 
                (self.rx+x,
                 self.ry+self.rh/2-display.getHeight(self.imgs.ctrlSliderCenter)/2) )
             
        display.draw( self.imgs.ctrlSliderLeft, 
            (self.rx-display.getWidth(self.imgs.ctrlSliderLeft)/2,
             self.ry+self.rh/2-display.getHeight(self.imgs.ctrlSliderLeft)/2) )
        display.draw( self.imgs.ctrlSliderRight, 
            (self.rx+self.rw-display.getWidth(self.imgs.ctrlSliderRight)/2,
             self.ry+self.rh/2-display.getHeight(self.imgs.ctrlSliderRight)/2) )
             
        sx = self.rw*(self.value-self.values[0])/(self.values[1]-self.values[0])
        display.draw( self.imgs.ctrlSliderSelect, 
            (self.rx+sx-display.getWidth(self.imgs.ctrlSliderSelect)/2,
             self.ry+self.rh/2-display.getHeight(self.imgs.ctrlSliderSelect)/2) )

