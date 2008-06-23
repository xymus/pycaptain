from client.imgs import Imgs
from client.texts import Texts
from client.snds import Snds
from client.prefs import Prefs
from client.mixer import Mixer

class LoadingScreen:
    def __init__( self, display ):
        self.display = display
        
    def loadAll( self ):
       
        self.imgs = Imgs( self.display )
        
        self.mixer = Mixer()
        self.snds = Snds( self.mixer )
        
        self.texts = Texts()
        self.prefs = Prefs()

        self.txtTitle = u"PyCaptain"
        self.txtAuthor = self.texts.createdBy % "Alexis Laferriere"
        self.txtWebsite = "http://xymus.net/pyfl/"
        self.txtThanksNasa = self.texts.courtesyNasa

        loadingTextPos = (self.display.resolution[0]/8, self.display.resolution[1]/2-30)

        self.drawStaticSplash()
        self.display.drawText( self.texts.loadingImages, loadingTextPos, color=(255,255,255), size=16 )
        for i in self.imgs.loadAll( self.display ):
            self.drawProgress( i*0.8 )

        self.drawStaticSplash( 80 )
        self.display.drawText( self.texts.loadingSounds, loadingTextPos, color=(255,255,255), size=16 )
        for i in self.snds.loadAll( self.mixer ):
            self.drawProgress( 80+i*0.1 )

        self.drawStaticSplash( 90 )
        self.display.drawText( self.texts.loadingTexts, loadingTextPos, color=(255,255,255), size=16 )
        for i in self.texts.loadAll():
            self.drawProgress( 90+i*0.05 )

        self.drawStaticSplash( 95 )
        self.display.drawText( self.texts.loadingPreferences, loadingTextPos, color=(255,255,255), size=16 )
        for i in self.prefs.loadAll():
            self.drawProgress( 95+i*0.05 )
            
        return self.mixer, self.imgs, self.snds, self.texts, self.prefs
            
            
    def drawStaticSplash( self, defPerc=0 ):
        self.display.beginDraw()
        self.display.draw( self.imgs.splashBack, ( (self.display.resolution[0]-self.display.getWidth(self.imgs.splashBack))/2, (self.display.resolution[1]-self.display.getHeight(self.imgs.splashBack))/2 ) )
        self.display.drawText( self.txtTitle, (self.display.resolution[0]/2-200+2, 200+2), color=(0,0,0), size=52 )
        self.display.drawText( self.txtTitle, (self.display.resolution[0]/2-200, 200), color=(255,255,255), size=52 )
        self.display.drawText( self.txtAuthor, (self.display.resolution[0]-200+2, self.display.resolution[1]-80+2), color=(0,0,0), size=14 )
        self.display.drawText( self.txtAuthor, (self.display.resolution[0]-200, self.display.resolution[1]-80), color=(255,255,255), size=14 )
        self.display.drawText( self.txtWebsite, (self.display.resolution[0]-200+2, self.display.resolution[1]-60+2), color=(0,0,0), size=13 )
        self.display.drawText( self.txtWebsite, (self.display.resolution[0]-200, self.display.resolution[1]-60), color=(255,255,255), size=13 )
        self.display.drawText( self.txtThanksNasa, (self.display.resolution[0]-200+2, self.display.resolution[1]-40+2), color=(0,0,0), size=12 )
        self.display.drawText( self.txtThanksNasa, (self.display.resolution[0]-200, self.display.resolution[1]-40), color=(255,255,255), size=12 )
        self.display.drawRect( (self.display.resolution[0]/8-2, self.display.resolution[1]/2-10-2, self.display.resolution[0]*6/8+4, 20+4), (255,255,255), 1 )
        self.display.drawRect( (self.display.resolution[0]/8, self.display.resolution[1]/2-10, float(defPerc)/100*self.display.resolution[0]*6/8, 20), (255,255,255) )
        self.display.finalizeDraw()

    def drawProgress( self, i ):
        self.display.beginDraw()
        self.display.drawRect( (self.display.resolution[0]/8, self.display.resolution[1]/2-10, float(i)/100*self.display.resolution[0]*6/8, 20), (255,255,255) )
        self.display.finalizeDraw()
