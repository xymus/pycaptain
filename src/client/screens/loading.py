# coding=UTF-8

from client.imgs import Imgs
from client.snds import Snds
from client.prefs import Prefs
from client.mixer import Mixer

class LoadingScreen:
    """This screen loads imgs, snds, texts and prefs and displays the progress."""
    def __init__( self, display, texts, eDone=None ):
        self.display = display
        
        self.txtAuthor = texts.get( "Created by %s" ) % u"Alexis Laferrière"
        self.txtWebsite = "http://xymus.net/pyfl/"
        self.txtThanksNasa = texts.get( "Some pictures courtesy NASA" )
        
        self.loadingTextPos = (self.display.resolution[0]/8, self.display.resolution[1]/2-30)
            
    def drawStaticSplash( self, defPerc=0, text=None ):
        self.display.beginDraw()

        rx = self.display.resolution[0] / self.display.getWidth(self.imgs.splashBack) + 1
        ry = self.display.resolution[1] / self.display.getHeight(self.imgs.splashBack) + 1
        self.display.drawRepeated(self.imgs.splashBack, (0, 0), repeatx=rx, repeaty=ry)

        self.display.draw( self.imgs.gameTitle, (40,40) )
        self.display.drawText( self.txtAuthor, (self.display.resolution[0]-200+2, self.display.resolution[1]-80+2), color=(0,0,0), size=14 )
        self.display.drawText( self.txtAuthor, (self.display.resolution[0]-200, self.display.resolution[1]-80), color=(255,255,255), size=14 )
        self.display.drawText( self.txtWebsite, (self.display.resolution[0]-200+2, self.display.resolution[1]-60+2), color=(0,0,0), size=13 )
        self.display.drawText( self.txtWebsite, (self.display.resolution[0]-200, self.display.resolution[1]-60), color=(255,255,255), size=13 )
        self.display.drawText( self.txtThanksNasa, (self.display.resolution[0]-200+2, self.display.resolution[1]-40+2), color=(0,0,0), size=12 )
        self.display.drawText( self.txtThanksNasa, (self.display.resolution[0]-200, self.display.resolution[1]-40), color=(255,255,255), size=12 )
        self.display.drawRect( (self.display.resolution[0]/8-2, self.display.resolution[1]/2-10-2, self.display.resolution[0]*6/8+4, 20+4), (255,255,255), 1 )
        self.display.drawRect( (self.display.resolution[0]/8, self.display.resolution[1]/2-10, float(defPerc)/100*self.display.resolution[0]*6/8, 20), (255,255,255) )
        if text:
            self.display.drawText( text, self.loadingTextPos, color=(255,255,255), size=16 )
        self.display.finalizeDraw()

    def drawProgress( self, i ):
        self.display.beginDraw()
        self.display.drawRect( (self.display.resolution[0]/8, self.display.resolution[1]/2-10, float(i)/100*self.display.resolution[0]*6/8, 20), (255,255,255) )
        self.display.finalizeDraw()

