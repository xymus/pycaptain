#!/usr/bin/python

from rc import Rc

import os
import sys

import ids

class Snds( Rc ):
    def __init__( self, mixer ):
        Rc.__init__( self )
        self.mixer = mixer

    def loadSound( self, path ):
        return self.mixer.load( os.path.join( self.wd, "snds", path ) )

    def loadAll( self, mixer ):
        yield 0
        self[ ids.S_EX_FIRE ] = self.loadSound( "explosions/fire.wav" )
        yield 20
        self[ ids.S_EX_JUMP ] = self.loadSound( "explosions/jump.wav" )
        yield 40
        self[ ids.S_EX_SHIP ] = self.loadSound( "explosions/ship.wav" )
        yield 60
        self[ ids.S_EX_NUKE ] = self.loadSound( "explosions/nuke.wav" )
        yield 80
        self[ ids.S_EX_PULSE ] = self.loadSound( "explosions/pulse.wav" )
        yield 100


