#!/usr/bin/python

import os

from common import config
from common import comms

verbose = True
svnServerUrl = "http://xymus.net/pyfls/updates"
updateCommand "svn %s co trunck/src/" % svnServerUrl

class Updater:
    def __init__(self):
        pass

    def run( self ):
        # returns "Game updated", "Up to date" or "failed: message"
        # check latest version
        currentVersion = comms.version
        try:
            latestVersion = None
        except Exception, ex:
            if verbose: print ""

        if latestVersion > currentVersion:
            os.system( updateCommand )
        else:
            if verbose: print "Already at latest version."



if __name__ == "__main__":
