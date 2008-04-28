#!/usr/bin/python

#from os import getcwdu
import sys
from os import path

class Rc:
    def __init__( self ):
        self.__dict__ = {}
        self.wd = path.join( sys.path[0], "client" )

    def __getitem__(self, i):
        return self.__dict__[ i ]

    def __setitem__(self, i, v):
        self.__dict__[ i ] = v

    def loadAll( self ):
        pass

