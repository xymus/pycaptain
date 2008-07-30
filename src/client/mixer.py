#!/usr/bin/python

import pygame

class Mixer:
    def __init__( self ):	
        try:
            pygame.mixer.init()
            pygame.mixer.set_num_channels( 16 )
            self.inited = True
        except Exception, ex:
            print "Failed to initialize sound device:", ex,"\nTry to install package libsdl1.2-debian-all"
            self.inited = False
        self.setVolume()

    def load( self, path ):
        if self.inited:
            return pygame.mixer.Sound( path )

    def play( self, sound, volume=100 ):
      if self.inited:
        c = pygame.mixer.find_channel()
        if c:
            c.set_volume( self.globalVolume*volume/100 ) 
            c.play( sound )

    def close( self ):
      if self.inited:
        pygame.mixer.quit()
        
    def setVolume( self, volume=100 ):
      if self.inited:
        self.globalVolume = float(volume)/100


