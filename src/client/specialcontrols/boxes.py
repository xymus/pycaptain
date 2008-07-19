from client.controls import *
from client.specialcontrols import *

class MessageBox( Control ):
    def __init__( self, display, imgs, text, buttons=[], img=None, width=240, height=400, center=None ): 
        """buttons format = [("text", eFunc( sender, (x,y) ))]"""
        
        if not center:
            center = (display.resolution[0]/2, display.resolution[1]/2)
            
        self.topLeft = (center[0]-width/2, center[1]-height/2)
        Control.__init__( self, None, self.topLeft, None )
        
        b = 8
        
        self.label = Label( (self.topLeft[0]+b,self.topLeft[1]+b), text, maxWidth=width-2*b )
        
        self.controls = [ ImageHolder( imgs.boxBack, self.topLeft ),
                          self.label ]
        p = 0
        for but in buttons:
            self.controls.append( LightControlDown( (self.topLeft[0]+width*p/len(buttons)-LightControlDown.width/2,self.topLeft[1]+height-LightControlDown.height), but[1], but[0], imgs ) )
            p += 1
            
    def draw( self, display, focused=False, over=False ):
        for control in self.controls: 
            control.draw( display )

    def hits( self, up=None, down=None ):
        for control in self.controls: 
            if control.hits( up=up, down=down ):
                return True
        return False
        
