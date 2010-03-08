# Automaticaly saves every variable from __dict__ to file.
# Save and laod everything as a string.

import sys
import os

# default values
defaultDict = {
    "user": "",
    "password": "",
    "server": "localhost",
    
    "language": "en",
    "display": "sdl",
    "resolution": "800x600",
    "fullscreen": "False",
    
    "lastGame": "",
    "lastCampaign": "",
}

path = os.path.join( sys.path[0], "prefs.cfg" )

class Prefs:
    def __init__( self ):       
        # copy defaultDict to __dict__
        for key, value in defaultDict.items():
            self.__dict__[ key ] = value

    def loadAll( self ):
        yield 0
        
        if os.path.exists( path ):
        
            # read pref file
            f = open( path, "r" )
            lines = f.readlines()
            f.close()
            
            yield 33
            
            # convert values
            for line in lines: # line = "key = value\n"
                key = line.split()[0]
                value = line[ line.find("=")+2:-1] # passed the "= " and before "\n"
                self.__dict__[ key ] = value
        else:
            f = None
        
        yield 100
        
    def set( self, key, value ):
        self.__dict__[ key ] = value

    def save( self ):        
        try:
            f = open( path, "w+" )
            for key, value in self.__dict__.items():
                f.write( "%s = %s\n" % (key,value) )
            f.close()
            
        except Exception, ex:
            print "failed prefs.save:", ex
            
    def shallowCopy( self ):
        newPref = Prefs()
        for key, value in self.__dict__.items():
            newPref.set( key, value )
        return newPref
        
            
