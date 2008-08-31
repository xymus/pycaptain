from client.controls import *
from client.specialcontrols import *
from client.specialcontrols.boxes import *

class Selector( Container ):
    def __init__( self, topLeft, display, imgs, title, items, eSelectedChanged=None ):
        Container.__init__( self )
        self.title = title
        self.items = items # being a list of (value,"display value")
        self.eSelectedChanged = eSelectedChanged
        
        self.size = (300,175)
        
        self.topLeft = topLeft
        self.centerTextY = self.topLeft
        
        self.titleOffset = (8, self.size[1]/2-9 )
        self.listOffset = (self.size[0]-8, self.size[1]/2-9 )
        
        self.ctrlListUp = LightControlDown( (self.topLeft[0], self.topLeft[1]+8), self.eListUp, "", imgs )
        self.ctrlListDown = LightControlUp( (self.topLeft[0], self.topLeft[1]+self.size[1]-LightControlUp.height-8), self.eListDown, "", imgs )
        
        self.controls = [
            Box( imgs, self.topLeft, self.size ),
            self.ctrlListUp,
            self.ctrlListDown
            ]
            
        self.textColor = (255,255,255,255)
        
        self.reset( items )
        
    selected = property( fget=lambda self: self.items[ self.kSelected ][ 0 ] )
        
    def reset( self, items=None ):
        if items != None:
            self.items = items
            
        self.changeSelected()
        
    def setDefault( self, value ):
        key = None
        for k, item in enumerate( self.items ):
            if item[0] == value:
                key = k
                break
                
        if key != None:
            self.changeSelected( key )
        
    def changeSelected( self, kSelected=0 ):
        self.kSelected = kSelected
        
        self.ctrlListUp.enabled = self.kSelected != 0
        self.ctrlListDown.enabled = self.kSelected != len(self.items)-1
            
    
    def eListUp( self, sender, (x,y) ):
        self.changeSelected( self.kSelected-1 )
        
    def eListDown( self, sender, (x,y) ):
        self.changeSelected( self.kSelected+1 )
        
    def draw( self, display, focused=False, over=False, mouse=None ):
        Container.draw( self, display, focused, over, mouse )
        if self.visible:
            display.drawText( self.title, 
                (self.topLeft[0]+self.titleOffset[0],self.topLeft[1]+self.titleOffset[1]), 
                self.textColor, size=20, align="left" )
                
            if self.items:
                for k in range( 0, self.kSelected ) + range( self.kSelected+1, len(self.items) ):
                    d = k - self.kSelected
                    dy = d*18
                    if dy > -1*self.listOffset[1] and dy < self.listOffset[1]:
                        display.drawText( self.items[ k ][1], 
                            (self.topLeft[0]+self.listOffset[0],self.topLeft[1]+self.listOffset[1]+dy), 
                            self.textColor, size=14, align="right" )
                
                display.drawText( self.items[ self.kSelected ][1], 
                    (self.topLeft[0]+self.listOffset[0],self.topLeft[1]+self.listOffset[1]), 
                    self.textColor, size=20, align="right" )
                    
               # for k in xrange( self.kSelected+1, len(self.items) ):
               #     d = k - self.kSelected
               #     display.drawText( self.items[ k ], 
               #         (self.topLeft[0]+self.listOffset[0],self.topLeft[1]+self.listOffset[1]+d*18), 
               #         self.textColor, size=14, align="right" )
                
        
