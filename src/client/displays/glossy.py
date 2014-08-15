import os
import sys
from math import degrees, pi, hypot, cos, sin, radians, fabs
from time import time

try:
    from gloss import *
except:
    print "Make sure Gloss is available to use the Gloss display"
    raise

from common.comms import COObject, COInput
from client.imgs import Animation

from . import Display

class Glossy( Display ):
    name = "glossy"
    title = "OpenGL via Gloss"
    
    def __init__(self, resolution=( 640, 640 ), fullscreen=False, title="Game"):
        Display.__init__(self)
        self.nfsResolution = resolution
        self.resolution = resolution
        
        self.gloss = Gloss()
        self.glossGame = GlossGame( title )
        
        self.resize(resolution)
        
        Gloss.enable_multisampling = True
        self.glossGame.gloss_initialise()
        
        self.fonts = {}
        
        self.z = 0
        
        self.drawna = 0
        self.avoideda = 0

    def load( self, imgPath, usePink=False ):
        
        pygameSurface = pygame.image.load(imgPath)
		
        openGlTexture = Texture( pygameSurface )
        
        return (openGlTexture, pygameSurface)

    def toggleFullscreen( self, fullscreen=None ):
        if fullscreen==None:
            fullscreen = not self.fullscreen

        if fullscreen:
            self.resolution = pygame.display.list_modes()[0]
            pygame.display.set_mode( self.resolution )
            self.fullscreen = pygame.display.toggle_fullscreen()
        else:
            self.fullscreen = fullscreen
            pygame.display.set_mode( self.nfsResolution )
        self.resize( self.resolution )
            
    def resize( self, resolution=(800, 600) ):
        Gloss.screen_resolution = resolution

    def getSubsurface( self, image, rect ):        
        pygameSurface = image[1].subsurface( rect )
		
        openGlTexture = Texture( pygameSurface )
        
        return (openGlTexture, pygameSurface)

    def beginDraw( self ):
        self.glossGame.begin()

    def _draw( self, img, pos ):
        img[0].draw( position=pos )

    def drawRo( self, img, pos, rotation ):
        img[0].draw( position=pos, rotation=self.getToDegrees(rotation), origin=None )

    def drawClipped( self, img, pos, src ):
        img[0].drawClipped( position=pos, clip=src )

    def _drawFont( self, text, font, color, pos, maxWidth=None, maxHeight=None, align="left" ):
        color=self.getGlossColor( color )
       
        if os.name == "nt":
            pos = (pos[0],pos[1]-6)
            
        if not maxWidth and not maxHeight:
            s = font.measure_string( text )
            if align == "left":
                font.draw( text=text, position=pos, color=color )
            elif align == "right":
                font.draw( text=text, position=(pos[0]-s[0],pos[1]), color=color )
            else: # align == "center":
                font.draw( text=text, position=(pos[0]-s[0]/2,pos[1]), color=color )
        else:
            lines = text.split( "\n" )
            lineNbr = 0
            for line in lines:
                words = line.split()
                while words and (not maxHeight or maxHeight > (lineNbr+1)*font.measure_string("M")[1]):
                    wordsOnLine = 1
                    while wordsOnLine <= len(words) and font.measure_string( " ".join( words[ :wordsOnLine ] ) )[0] < maxWidth:
                        wordsOnLine += 1
                    wordsOnLine -= 1
                    
                    lineText = " ".join( words[ :wordsOnLine ] )
                    words = words[ wordsOnLine: ]
                    
                    s = font.measure_string( text )
                    if align == "left":
                        font.draw( text=lineText, position=(pos[0],pos[1]+lineNbr*s[1]), color=color )
                    elif align == "right":
                        font.draw( text=lineText, position=(pos[0]-s[0],pos[1]+lineNbr*s[1]), color=color )
                    else: # align == "center":
                        font.draw( text=lineText, position=(pos[0]-s[0]/2,pos[1]+lineNbr*s[1]), color=color )
                    
                    lineNbr += 1
    
    def _loadFont( self, size, path=None ):
        return SpriteFont( os.path.join( sys.path[0], "client/fonts/FreeSans.ttf" ), size = size )

    def drawRect( self, rect, color, width=0 ):
        if width == 0:
            self.gloss.draw_box( position=(rect[0],rect[1]), width=rect[2], height=rect[3], color=self.getGlossColor(color) )
        else:
            lines = [ (rect[0],rect[1]), 
                      (rect[0]+rect[2],rect[1]), 
                      (rect[0]+rect[2],rect[1]+rect[3]), 
                      (rect[0],rect[1]+rect[3]) ]
            lines.append( lines[0] )
            self.gloss.draw_lines( lines, color=self.getGlossColor(color), width=width )

    def drawLine( self, color, o, d, width=1):
        self.gloss.draw_line( o, d, color=self.getGlossColor(color), width=width )

    def drawCircle( self, color, o, radius, width=0):
        # ignores fill
        if width == 0:
            width = 1
        
        lines = [ (o[0]-radius,o[1]), (o[0],o[1]-radius), (o[0]+radius,o[1]), (o[0],o[1]+radius) ]
        lines.append( lines[0] )
        self.gloss.draw_lines( lines, color=self.getGlossColor(color), width=width )

    def drawArc( self, color, o, radius, minAngle, maxAngle, width=1):
        lines = [ (o[0]+radius*cos(minAngle), o[1]+radius*sin(minAngle)), 
                  (o[0]+radius*cos((maxAngle+minAngle)/2), 
                   o[1]+radius*sin((maxAngle+minAngle)/2)),
                  (o[0]+radius*cos(maxAngle), o[1]+radius*sin(maxAngle)) ]
        self.gloss.draw_lines( lines, color=self.getGlossColor(color), width=width )

    def drawPoint( self, o, color):
        self.drawCircle( color, o, 1 )

    def finalizeDraw( self ):
        self.glossGame.end()
        
        self.drawna = 0
        self.avoideda = 0

    def clear( self, color=(0,0,0) ):
        self.gloss.clear( self.getGlossColor(color) )

    def getWidth(self, img):
        if isinstance( img, Animation ):
            img = img.getImage()
        return img[0].width

    def getHeight(self, img):
        if isinstance( img, Animation ):
            img = img.getImage()
        return img[0].height

    def getInputs(self, inputs=None):
        quit = False

        if not inputs:
            inputs = COInput()

        inputs.keys = []

        inputs.up = pygame.key.get_pressed()[ pygame.K_UP ]
        inputs.down = pygame.key.get_pressed()[ pygame.K_DOWN ]
        inputs.left = pygame.key.get_pressed()[ pygame.K_LEFT ]
        inputs.right = pygame.key.get_pressed()[ pygame.K_RIGHT ]
        inputs.mousePos = pygame.mouse.get_pos()

        inputs.mouseDowned = False
        inputs.mouseUpped = False
        
        inputs.mouseRightDowned = False
        inputs.mouseRightUpped = False

        e = pygame.event.poll()
        while e.type != pygame.NOEVENT:
            if e.type == pygame.QUIT:
                quit = True
            elif e.type == pygame.KEYDOWN:
                inputs.keys.append( [e.key, e.unicode] )

            elif e.type == pygame.MOUSEBUTTONDOWN:
              if e.button == 1:
                inputs.mouseDownAt = e.pos
                inputs.mouseDowned = True
              elif e.button == 3:
                inputs.mouseRightDowned = True

            elif e.type == pygame.MOUSEBUTTONUP:
              if e.button == 1:
                inputs.mouseUpAt = e.pos
                inputs.mouseUpped = True
              elif e.button == 3:
                inputs.mouseRightUpped = True

            e = pygame.event.poll()

        return (quit, inputs)

    def close(self):
        self.glossGame.quit()

    def _setCursor( self, cursor ):
        pass
        
    def showCursor( self, show ):
        pass

    def takeScreenshot( self, path=None ):
        if not path:
            path = os.path.join( sys.path[0], "screen-%i.bmp"%time() )
        save_screenshot(path)
        print "screenshot saved to %s" % path

    def drawRoNCutHalfVert( self, img, pos, rotation, part=0 ):
        img[0].drawPie( position=pos, perc=100 )

    def drawRoNCutQtl( self, img, pos, rotation ):
        img[0].drawPie( position=pos, perc=100 )

    def drawRoNCutQbl( self, img, pos, rotation ):
        img[0].drawPie( position=pos, perc=100 )

    def drawPie( self, img, pos, perc ):
        img[0].drawPie( position=pos, perc=perc )

    def drawIncompletePie( self, img, pos, perc0, angleRange=100, angleCut=60 ):
        img[0].drawPie( position=pos, perc=perc0 )

    def drawDoubleIncompletePie( self, (img0,img1), pos, (perc0,perc1) ):
        img0[0].drawPie( position=pos, perc=perc0 )
        img1[0].drawPie( position=pos, perc=perc1 )


    def drawRoIfIn( self, img, pos, rotation, (xm, ym), alpha=1 ):
        w = self.getWidth( img )
        h = self.getHeight( img )
        
        corrPosition = ( pos[0]-w/2, pos[1]-h/2 ) # correct to top left
        if corrPosition[0] < xm and corrPosition[0]+w > 0 \
          and corrPosition[1] < ym and corrPosition[1]+h > 0:
            img[0].draw( position=pos, rotation=self.getToDegrees(rotation), origin=None )
            self.drawna += 1
        else:
            self.avoideda += 1

    def drawRoRe( self, img, pos, resize ):
        img[0].draw( position=pos, rotation=self.getToDegrees(rotation), origin=None, scale=resize )
        
    def getGlossColor( self, rgb ):
        return Color( rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0 )
        
    def getToDegrees( self, a ):
        return a*-180/pi # Gloss.TWO_PI

    def drawRepeated( self, img, pos, repeatx=1, repeaty=1 ):
        img[0].drawRepeated( position=pos, repeatx=repeatx, repeaty=repeaty )
