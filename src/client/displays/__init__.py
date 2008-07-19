__all__ = ["sdl"]

import os
import sys
from math import degrees, pi, hypot, cos, sin, radians, fabs
from time import time

from common.comms import COObject, COInput
from client.imgs import Animation

class Display:
    """Abstract Display class. Contains a few common functions.
       Inspire yourself from displays.sdl to implement another display engine."""
       
    def __init__(self, resolution=( 640, 640 ), fullscreen=False, title="Game"):
        self.fonts = {}
        
        self.cursorArrow = None

    def load( self, imgPath, usePink=False ):
        raise Exception( "Abstract function, should not be used" )

    def toggleFullscreen( self, fullscreen=None ):
        raise Exception( "Abstract function, should not be used" )

    def getSubsurface( self, image, rect ):
        raise Exception( "Abstract function, should not be used" )

    def beginDraw( self ):
        raise Exception( "Abstract function, should not be used" )

    def _draw( self, img, pos ):
        raise Exception( "Abstract function, should not be used" )

    def drawClipped( self, img, pos, src ):
        raise Exception( "Abstract function, should not be used" )
    
    def draw( self, img, pos ):
        if isinstance( img, Animation ):
            img = img.getImage()
        self._draw( img, pos )

    def drawRo( self, img, pos, rotation ):
        raise Exception( "Abstract function, should not be used" )
        
    def _drawFont( self, font, color ):
        raise Exception( "Abstract function, should not be used" )
    
    def _loadFont( self, size, path=None ):
        raise Exception( "Abstract function, should not be used" )

    def drawText( self, text, (x,y), color=(255,255,255,255), size=15, maxWidth=None, maxHeight=None ):
        if not self.fonts.has_key( size ):
            try:
                self.fonts[ size ] = self._loadFont( size, os.path.join( sys.path[0], "client/fonts/FreeSans.ttf" ) )
            except:
                self.fonts[ size ] = self._loadFont( size ) # pygame.font.get_default_font()

        self._drawFont( text, self.fonts[ size ], color, (x,y), maxWidth, maxHeight )

    def drawRect( self, rect, color, width=0 ):
        raise Exception( "Abstract function, should not be used" )

    def drawLine( self, color, o, d, width=1):
        raise Exception( "Abstract function, should not be used" )

    def drawCircle( self, color, o, radius, width=0):
        raise Exception( "Abstract function, should not be used" )

    def drawArc( self, color, o, radius, minAngle, maxAngle, width=1):
        raise Exception( "Abstract function, should not be used" )

    def drawPoint( self, o, color):
        raise Exception( "Abstract function, should not be used" )

    def finalizeDraw( self ):
        raise Exception( "Abstract function, should not be used" )

    def clear( self, color=(0,0,0) ):
        raise Exception( "Abstract function, should not be used" )

    def drawBackground( self, img, (ix, iy) ):
        bgx = ix % self.getWidth( self.background )
        bgy = iy % self.getHeight( self.background )
        for x in range( bgx - self.getWidth( self.background ), bgx+self.resolution[ 0 ], self.getWidth( self.background ) ):
            for y in range( bgy - self.getHeight( self.background ), bgy+self.resolution[ 1 ], self.getHeight( self.background ) ):
                self._draw( self.background, (x,y) )


    def getWidth(self, img):
        raise Exception( "Abstract function, should not be used" )

    def getHeight(self, img):
        raise Exception( "Abstract function, should not be used" )

    def getInputs(self, inputs=None):
        raise Exception( "Abstract function, should not be used" )

    def close(self):
        raise Exception( "Abstract function, should not be used" )
        
    def _setCursor( self, cursor ):
        raise Exception( "Abstract function, should not be used" )

    def setCursor( self, cursor=None ):
        if not cursor:
            cursor = self.cursorArrow
        self._setCursor( cursor )

    def takeScreenshot( self, path=None ):
        raise Exception( "Abstract function, should not be used" )

    def drawRoNCutHalfHorz( self, img, pos, rotation ):
        raise Exception( "Abstract function, should not be used" )

    def drawRoNCutHalfVert( self, img, pos, rotation, part=0 ):
        raise Exception( "Abstract function, should not be used" )

    def drawRoNCutQtl( self, img, pos, rotation ):
        raise Exception( "Abstract function, should not be used" )

    def drawRoNCutQbl( self, img, pos, rotation ):
        raise Exception( "Abstract function, should not be used" )

    def drawPie( self, img, pos, perc ):
        raise Exception( "Abstract function, should not be used" )

    def drawIncompletePie( self, img, pos, perc0, angleRange=100, angleCut=60 ):
        raise Exception( "Abstract function, should not be used" )

    def drawDoubleIncompletePie( self, (img0,img1), pos, (perc0,perc1) ):
        raise Exception( "Abstract function, should not be used" )


    def drawRoIfIn( self, img, pos, rotation, (xm, ym), alpha=1 ):
        raise Exception( "Abstract function, should not be used" )

    def drawRoRe( self, img, pos, resize ):
        raise Exception( "Abstract function, should not be used" )

