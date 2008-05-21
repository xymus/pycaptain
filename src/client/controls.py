from math import sin, cos, hypot, atan2, pi

class ControlFrame:
    def __init__(self):
        self.controls = []
        self.selected = None
        self.eEnter = None
        self.tabOrder = {}
        self.tabOrderReverse = {}

    def addControl( self, control ):
        if len( self.controls ) > 0:
            self.tabOrder[ self.controls[-1] ] = control

        self.controls.append( control )

        if len( self.controls ) > 1:
            self.tabOrderReverse[ control ] = self.controls[-2]

    def addControls( self, controls ):
        for control in controls:
            self.addControl( control )

    def setControls( self, controls ):
        self.controls = []
        self.tabOrder = []
        self.tabOrderReverse = []
        for control in controls:
            self.addControl( control )

    def keyInput( self, key, letter=None ):
        if letter == "\r" and (not self.selected or not self.selected.useEnter):
            if self.eEnter:
                self.eEnter( self, (0,0) )

        if self.selected:
            #if letter == "\t" and 
            self.selected.keyInput( key, letter )
        else:
            for control in self.controls:
                if isinstance( control, KeyCatcher ):
                    control.keyInput( key, letter )

   # def mouse( self, pos, goingDown=False, goingUp=False, butLeft=False, butRight=False ):
   #     if goingUp:
   #         for control in self.controls:
   #             if control.hits( self.inputs.mouseUpAt ):
   #                 self.focus = control
   #                 break


class ControlBase:
    def __init__( self, fUpEvent, fDownEvent=None, uid=None ):
        self.fUpEvent = fUpEvent
        self.fDownEvent = fDownEvent
        self.uid = uid

    def hits( self, (x,y) ):
        return False

    def draw( self, display, focused=False ):
        pass

    def keyInput( self, key, letter=None ):
        pass

class Control:
    def __init__( self, img, topLeft, fIn, fUpEvent=None, fDownEvent=None, fOverEvent=None, uid=None ):
        self.img = img
        self.topLeft = topLeft
        self.fIn = fIn
        self.fUpEvent = fUpEvent
        self.fDownEvent = fDownEvent
        self.fOverEvent = fOverEvent
        self.uid = uid
    #    self.down = False
        self.over = False
        self.enabled = True
        self.visible = True
        self.useEnter = False

    def hits( self, (x,y) ):
        res = self.fIn( (x,y) )
        if res and self.enabled and self.fUpEvent:
            self.fUpEvent( self, (x,y) )
        return res

    def draw( self, display, focused=False ):
      if self.visible and self.img:
        rect = (0,0,display.getWidth(self.img)/3,display.getHeight(self.img))

        if not self.enabled:
            rect = (rect[2]*2, rect[1], rect[2]*3, rect[3] )
        elif self.over:
            rect = (rect[2], rect[1], rect[2]*2, rect[3] )

        display.drawClipped( self.img, self.topLeft, rect )

    def keyInput( self, key, letter=None ):
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

    def draw( self, display, focused=False ):
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

    def draw( self, display, focused=False ):
        pass

class TextBox( RectControl ):
    def __init__( self, (rx,ry), (rw,rh), defaultText="", password=False, numeric=False, forbidden=[] ):
        RectControl.__init__( self, None, (rx,ry), (rw,rh), None, None )
        self.text = defaultText
        self.selection = 0
        self.password = password
        self.numeric = numeric
        self.forbidden = forbidden
        
    def draw( self, display, focused=False ):
      if self.visible:
        display.drawLine( (255,255,255,255), (self.topLeft[0],self.topLeft[1]+self.rh), (self.topLeft[0]+self.rw,self.topLeft[1]+self.rh), 1 )
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

    def hits( self, (x,y) ):
        pass

    def draw( self, display, focused=False ):
      if self.visible:
        display.drawText( self.text, self.topLeft )

class LabelButton( RectControl ):
     def __init__( self, (rx,ry), (rw,rh), fUpEvent, text, fDownEvent=None, uid=None ):
        RectControl.__init__( self, None, (rx,ry), (rw,rh), fUpEvent, fDownEvent, uid=uid )
        self.text = text

     def draw( self, display, focused=False ):
      if self.visible:
        if self.enabled:
            color = (255,255,255,255)
        else:
            color = (128,128,128,255)
        display.drawText( self.text, (self.topLeft[0]+8,self.topLeft[1]+8 ), color=color )
        display.drawLine( (255,255,255,255), self.topLeft, (self.topLeft[0]+self.rw,self.topLeft[1]) )
        display.drawLine( (255,255,255,255), self.topLeft, (self.topLeft[0],self.topLeft[1]+self.rh) )

        display.drawLine( (255,255,255,255), (self.topLeft[0]+self.rw,self.topLeft[1]), (self.topLeft[0]+self.rw,self.topLeft[1]+self.rh) )
        display.drawLine( (255,255,255,255), (self.topLeft[0],self.topLeft[1]+self.rh), (self.topLeft[0]+self.rw,self.topLeft[1]+self.rh) )

class ProgressBar( RectControl ):
     def __init__( self, (rx,ry), (rw,rh), uid=None ):
        RectControl.__init__( self, None, (rx,ry), (rw,rh), None, None, uid=uid )
        self.progress = 0

     def draw( self, display, focused=False ):
      if self.visible:
        display.drawRect( (self.topLeft[0], self.topLeft[1], self.rw, self.rh), (255,255,255), 1 )
        display.drawRect( (self.topLeft[0]+2, self.topLeft[1]+2, (self.rw-4)*self.progress, self.rh-4), (255,255,255) )


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

class KeyCatcher( ControlBase ):
    def __init__( self, fUpEvent, key, fDownEvent=None, uid=None ):
        ControlBase.__init__( self, fUpEvent, fDownEvent, uid=uid )
        self.key = key

    def keyInput( self, key, letter=None ):
        if key == self.key and self.fUpEvent:
            self.fUpEvent( self, (0,0) )

