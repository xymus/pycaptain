from client.controls import *

class Timeline( RectControl ):
    def __init__( self, vCenter, width, imgs, display, eSelectedChanged ):
        self.vCenter = vCenter
        RectControl.__init__( self, None, (0, self.vCenter-display.getHeight(imgs.ctrlTimelineBack)/2), (width, display.getHeight(imgs.ctrlTimelineBack)), self.eHit )
        self.eSelectedChanged = eSelectedChanged
        self.imgs = imgs
        self.setValues( [] )
        
    def setValues( self, values ):
        self.values = values
        self.selected = 0
        self.selectables = 0
        
        if len( values ) > 1:
            diff = values[ -1 ] - values[ 0 ]
            divisions = float(diff)/(len(values)+2)
            self.min = values[ 0 ]-divisions
            self.max = values[ -1 ]+divisions
            
        elif len( values ):
            self.min = values[ 0 ]-100
            self.max = values[ 0 ]+100
            
        else:
            self.min = 0
            self.max = 1
        print "min max", self.min, self.max
       
    def draw( self, display, focused=False, over=False, mouse=None ):
        for x in xrange( 0, self.rw, display.getWidth(self.imgs.ctrlTimelineBack) ):
            display.draw( self.imgs.ctrlTimelineBack, 
                (self.rx+x, self.vCenter-display.getHeight(self.imgs.ctrlTimelineBack)/2) )
                
        for k,v in enumerate(self.values):
            if k == self.selected:
                img = self.imgs.ctrlTimelineSelected
                pos = ( self.rx+ self.rw*(v-self.min)/(self.max-self.min) -display.getWidth(img)/2,
                       self.vCenter-display.getHeight(img)/2)
                display.draw( img,
                              pos )
                              
            if k == self.selectables:
                img = self.imgs.ctrlTimelineNext
            elif k < self.selectables:
                img = self.imgs.ctrlTimelineAvailable
            else:
                img = self.imgs.ctrlTimelineUnavailable
            
            pos = ( self.rx+ self.rw*(v-self.min)/(self.max-self.min) -display.getWidth(img)/2,
                   self.vCenter-display.getHeight(img)/2)
            display.draw( img,
                          pos )
            
    def eHit( self, sender, pos ):
        oldSelected = self.selected
        
        year = self.min+ (self.max-self.min)*(pos[0]-self.rx)/self.rw
         
        bestDist = None
        for k,value in enumerate(self.values):
            diff = abs(value-year)
            if bestDist == None \
              or diff < bestDist:
                bestDist = diff
                self.selected = k
                
        if self.selected > self.selectables:
            self.selected = self.selectables
         
        if self.selected != oldSelected \
          and self.eSelectedChanged:
           self.eSelectedChanged( self, pos )

