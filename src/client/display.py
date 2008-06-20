import os
import sys
from math import degrees, pi, hypot, cos, sin, radians, fabs
from time import time
import pygame

#from visible import VisibleObject
from common.comms import COObject, COInput
from imgs import Animation

class Display:
    def __init__(self, resolution=( 640, 640 ), fullscreen=False):
        self.nfsResolution = resolution
        self.resolution = resolution
    #    self.backgroundColor = ( 0, 0, 0, 1 )

        if __debug__:
            print "SDL v%i.%i.%i" % pygame.get_sdl_version()
        
        pygame.init()
        self.toggleFullscreen( fullscreen )

        self.screen = pygame.display.get_surface()

        self.fonts = {}

        self.cursorArrow = pygame.cursors.arrow
        self.cursorAim = pygame.cursors.broken_x
          

    def load( self, imgPath, usePink=False ):
        img = pygame.image.load( imgPath )
        if usePink:
            color = img.get_at( (0,0) )
            img.set_colorkey( color )
            img = img.convert()
        else:
            img = img.convert_alpha()
        return img

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

    def getSubsurface( self, image, rect ):
        return image.subsurface( rect )

    def beginDraw( self ):
        pass

    def draw( self, img, pos ):
        if isinstance( img, Animation ):
            img = img.getImage()
        self.screen.blit( img, pos )

    def drawRo( self, img, pos, rotation ):
        if img is Animation:
            img = img.getImage()
        if rotation != 0:
            tempSurface = pygame.transform.rotate( img, degrees(rotation) )
        else:
            tempSurface = img

        corrPosition = ( pos[0]-tempSurface.get_width()/2, pos[1]-tempSurface.get_height()/2 ) # correct to top left
        self.screen.blit( tempSurface, corrPosition )

    def drawClipped( self, img, pos, src ):
	    self.screen.blit( img, pos, src )

    def drawText( self, text, (x,y), color=(255,255,255,255), size=15 ):
        if not self.fonts.has_key( size ):
            try:
                self.fonts[ size ] = pygame.font.Font( os.path.join( sys.path[0], "client/fonts/FreeSans.ttf" ), size )
            except:
                self.fonts[ size ] = pygame.font.Font( None, size ) # pygame.font.get_default_font()

        s = self.fonts[ size ].render( text, True, color )
        self.screen.blit( s, (x,y) )

    def drawRect( self, rect, color, width=0 ):
        if width == 0:
            self.screen.fill( color, rect )
        else:
            pygame.draw.rect( self.screen, color, rect, width )

    def drawLine( self, color, o, d, width=1):
        pygame.draw.line( self.screen, color, o, d, width )

    def drawCircle( self, color, o, radius, width=0):
        pygame.draw.circle( self.screen, color, o, radius, width )

    def drawArc( self, color, o, radius, minAngle, maxAngle, width=1):
        pygame.draw.arc( self.screen, color, (o[0]-radius, o[1]-radius, 2*radius, 2*radius ), minAngle, maxAngle, width )

    def drawPoint( self, o, color):
        self.screen.set_at(o, color )

    def finalizeDraw( self ):
        pygame.display.flip()

    def clear( self, color=(0,0,0) ):
        self.screen.fill( color )

    def drawBackground( self, img, (ix, iy) ):
        bgx = ix % self.background.get_width()
        bgy = iy % self.background.get_height()
        for x in range( bgx - self.background.get_width(), bgx+self.resolution[ 0 ], self.background.get_width() ):
            for y in range( bgy - self.background.get_height(), bgy+self.resolution[ 1 ], self.background.get_height() ):
                self.screen.blit( self.background, (x,y) )


    def getWidth(self, img):
        if isinstance( img, Animation ):
            img = img.getImage()
        return img.get_width()

    def getHeight(self, img):
        if isinstance( img, Animation ):
            img = img.getImage()
        return img.get_height()

    def getInputs(self, inputs=None):
        quit = False

        if not inputs:
            inputs = COInput()

        inputs.keys = []

       # inputs.up = pygame.key.get_pressed()[ pygame.K_UP ]
       # inputs.down = pygame.key.get_pressed()[ pygame.K_DOWN ]
       # inputs.left = pygame.key.get_pressed()[ pygame.K_LEFT ]
       # inputs.right = pygame.key.get_pressed()[ pygame.K_RIGHT ]

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
        pygame.display.quit()

    def setCursor( self, cursor=None ):
        if not cursor:
            cursor = self.cursorArrow
        pygame.mouse.set_cursor( cursor[0], cursor[1], cursor[2], cursor[3] )

    def takeScreenshot( self, path=None ):
        if not path:
            path = os.path.join( sys.path[0], "screen-%i.bmp"%time() )
        print "screenshot saved to %s" % path
        pygame.image.save( self.screen, path )



    def drawRoNCutHalfHorz( self, img, pos, rotation ):
        if rotation != 0:
            tempSurface = pygame.transform.rotate( img, degrees(rotation) )
        else:
            tempSurface = img

        corrPosition = ( pos[0]-tempSurface.get_width()/2, pos[1]-tempSurface.get_height()/2 ) # correct to top left
	self.screen.blit( tempSurface, corrPosition, ( 0, 0, self.getWidth( tempSurface )/2, self.getHeight( tempSurface ) ) )

    def drawRoNCutHalfVert( self, img, pos, rotation, part=0 ):
        """pos: center position
           rotation: rotation cw, in radians
           part: 0==upper part or 1==down"""
        if rotation != 0:
            tempSurface = pygame.transform.rotate( img, degrees(rotation) )
        else:
            tempSurface = img

        corrPosition = ( pos[0]-tempSurface.get_width()/2, pos[1]-tempSurface.get_height()/2+self.getHeight(tempSurface)/2*part ) # correct to top left
	self.screen.blit( tempSurface, corrPosition, ( 0, self.getHeight( tempSurface )/2*part, self.getWidth( tempSurface ), self.getHeight( tempSurface )/2*(part+1) ) )

    def drawRoNCutQtl( self, img, pos, rotation ):
        if rotation != 0:
            tempSurface = pygame.transform.rotate( img, degrees(rotation) )
        else:
            tempSurface = img

        corrPosition = ( pos[0]-tempSurface.get_width()/2, pos[1]-tempSurface.get_height()/2 ) # correct to top left
	self.screen.blit( tempSurface, corrPosition, ( 0, 0, self.getWidth( tempSurface )/2, self.getHeight( tempSurface )/2 ) )

    def drawRoNCutQbl( self, img, pos, rotation ):
        if rotation != 0:
            tempSurface = pygame.transform.rotate( img, degrees(rotation) )
        else:
            tempSurface = img

        corrPosition = ( pos[0]-tempSurface.get_width()/2, pos[1] ) # correct to top left-tempSurface.get_height()/2
	self.screen.blit( tempSurface, corrPosition, ( 0, self.getHeight( tempSurface )/2, self.getWidth( tempSurface )/2, self.getHeight( tempSurface ) ) )

    def drawPie( self, img, pos, perc ):
        if perc <= 50:
            tempSurface = pygame.transform.rotate( img, degrees(perc*pi/50) )
            corrPosition = ( pos[0], pos[1]-tempSurface.get_height()/2 )
	    self.screen.blit( tempSurface, corrPosition, ( self.getWidth( tempSurface )/2, 0, self.getWidth( tempSurface )/2, self.getHeight( tempSurface ) ) )
        else:
            tempSurface = pygame.transform.rotate( img, degrees(pi) )
            corrPosition = ( pos[0]-tempSurface.get_width()/2, pos[1]-tempSurface.get_height()/2 )
	    self.screen.blit( tempSurface, corrPosition ) # static

            tempSurface = pygame.transform.rotate( img, degrees(perc*pi/50) )
            corrPosition = ( pos[0]-tempSurface.get_width()/2, pos[1]-tempSurface.get_height()/2 )
	    self.screen.blit( tempSurface, corrPosition, ( 0, 0, self.getWidth( tempSurface )/2, self.getHeight( tempSurface ) ) )

    def drawIncompletePie( self, img, pos, perc0, angleRange=100, angleCut=60 ):
        if perc0 > 100:
            perc0 = 100

        radius = self.getHeight( img )/2
        if True:
            roSurface = pygame.transform.rotate( img, (100.0-perc0)*-1*(angleRange+angleCut)/100 )
            tempSurface = roSurface.subsurface(  ( 0, 0, self.getWidth( roSurface )/2, self.getHeight( roSurface ) ) )
            finalSurface = pygame.transform.rotate( tempSurface, (100-perc0)*(angleRange+angleCut)/100 )
            angle = ((100-perc0)*((angleRange+angleCut)*-2*pi/360)/100-pi)%(2*pi)
            
            x0 = tempSurface.get_height()*sin(angle)
            y1 = tempSurface.get_width()*sin(angle)
        #    print angle, pi
            if angle < pi/2:
                corrPosition = ( pos[0]-x0/2, pos[1]-(finalSurface.get_height()-y1)/2 )
            else:
                corrPosition = ( pos[0]-finalSurface.get_width()+x0/2, pos[1]-(finalSurface.get_height()-y1)/2 )
	    self.screen.blit( finalSurface, corrPosition )

    def drawDoubleIncompletePie( self, (img0,img1), pos, (perc0,perc1) ):
        if perc0 > 100:
            perc0 = 100
        if perc1 > 100:
            perc1 = 100

      #  print perc0, perc1
        if perc0 <= 50:
            roSurface = pygame.transform.rotate( img0, (50-perc0)*-120/50 )
            tempSurface = roSurface.subsurface(  ( 0, 0, self.getWidth( roSurface )/2, self.getHeight( roSurface ) ) )
            finalSurface = pygame.transform.rotate( tempSurface, (50-perc0)*120/50 )
            angle = (50-perc0)*(pi*2/3)/50 
            
        #    y0 = tempSurface.get_height()*cos(angle)
            x0 = tempSurface.get_height()*sin(angle)
            y1 = tempSurface.get_width()*sin(angle)
        #    x1 = tempSurface.get_width()*cos(angle)
            if angle < pi/2:
                corrPosition = ( pos[0]-finalSurface.get_width()+x0/2, pos[1]-(finalSurface.get_height()-y1)/2 )
            else:
                corrPosition = ( pos[0]-x0/2, pos[1]-(finalSurface.get_height()-y1)/2 )
	    self.screen.blit( finalSurface, corrPosition )
        else:
            tempSurface = img0 # pygame.transform.rotate( img0, 0 )
            corrPosition = ( pos[0]-tempSurface.get_width()/2, pos[1]-tempSurface.get_height()/2 )
	    self.screen.blit( tempSurface, corrPosition ) # static

            tempSurface = pygame.transform.rotate( img0, (perc0-50)*-120/50 )
            corrPosition = ( pos[0], pos[1]-tempSurface.get_height()/2 )
	    self.screen.blit( tempSurface, corrPosition, ( self.getWidth( tempSurface )/2, 0, self.getWidth( tempSurface )/2, self.getHeight( tempSurface ) ) )

        if perc1 <= 50:
            roSurface = pygame.transform.rotate( img1, (50-perc1)*120/50 )
            tempSurface = roSurface.subsurface(  ( self.getWidth( roSurface )/2, 0, self.getWidth( roSurface )/2, self.getHeight( roSurface ) ) )
            finalSurface = pygame.transform.rotate( tempSurface, (50-perc1)*-120/50 )
            angle = ((50-perc1)*(pi*-2/3)/50-pi)%(2*pi)
            
            x0 = tempSurface.get_height()*sin(angle)
            y1 = tempSurface.get_width()*sin(angle)
            if angle > pi/2:
                corrPosition = ( pos[0]-x0/2, pos[1]-(finalSurface.get_height()-y1)/2 )
            else:
                corrPosition = ( pos[0]-finalSurface.get_width()+x0/2, pos[1]-(finalSurface.get_height()-y1)/2 )
	    self.screen.blit( finalSurface, corrPosition )
        else:
            tempSurface = img1
            corrPosition = ( pos[0]-tempSurface.get_width()/2, pos[1]-tempSurface.get_height()/2 )
	    self.screen.blit( tempSurface, corrPosition ) # static

            tempSurface = pygame.transform.rotate( img1, (perc1-50)*120/50 )
            corrPosition = ( pos[0]-tempSurface.get_width()/2, pos[1]-tempSurface.get_height()/2 )
	    self.screen.blit( tempSurface, corrPosition, ( 0, 0, self.getWidth( tempSurface )/2, self.getHeight( tempSurface ) ) )


    def drawRoIfIn( self, img, pos, rotation, (xm, ym), alpha=1 ):
        if rotation != 0:
            tempSurface = pygame.transform.rotate( img, degrees(rotation) )
        else:
            tempSurface = img

     #   if alpha != 1:
     #       tempSurface.set_alpha( int(alpha*255), pygame.RLEACCEL )
        #    print alpha*255

        w = tempSurface.get_width()
        h = tempSurface.get_height()
        corrPosition = ( pos[0]-w/2, pos[1]-h/2 ) # correct to top left
        if corrPosition[0] < xm and corrPosition[0]+w > 0 \
          and corrPosition[1] < ym and corrPosition[1]+h > 0:
	    self.screen.blit( tempSurface, corrPosition )

    def drawRoRe( self, img, pos, resize ):
        tempSurface = pygame.transform.rotozoom( img, degrees(rotation), resize )
        corrPosition = ( pos[0]-tempSurface.get_width()/2, pos[1]-tempSurface.get_height()/2 ) # correct to top left
	self.screen.blit( tempSurface, corrPosition )

