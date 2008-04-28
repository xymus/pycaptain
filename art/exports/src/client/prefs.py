import sys
import os

server = "localhost"
username = "xymus"
hashedPassword = "0"

import ids

class Prefs:
    def __init__( self ):
        self.__dict__ = {}
        self.wd = sys.path[0]
        self.user = None
        self.password = None
        self.user = None

        self.path = os.path.join( self.wd, "prefs.cfg" )


    def __getitem__(self, i):
        return self.__dict__[ i ]

    def __setitem__(self, i, v):
        self.__dict__[ i ] = v

    def loadAll( self ):
        yield 0
        try:
            f = open( self.path, "r" )
        except Exception, ex:
            print "failed prefs.load:", ex
            f = None

        yield 33
        if f:
            lines = f.readlines()
            f.close()
            if len( lines ) >= 3:
                words = [ line.strip().split() for line in lines ]
                self.user = " ".join( words[0][2:])
                self.password = " ".join(words[1][2:])
                self.server = words[2][2]

        yield 66
        if not self.user:
            self.user = ""
            self.password = ""
            self.server = "localhost"
        yield 100

    def save( self, user, password, server ):        
      try:
        f = open( self.path, "w+" )
        f.write( "user = %s\n" % user )
        f.write( "password = %s\n" % password )
        f.write( "server = %s\n" % server )
        f.close()
      except Exception, ex:
          print "failed prefs.save:", ex



