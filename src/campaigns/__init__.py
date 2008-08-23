__all__ = [ "Campaign" ]

from gzip import open
import cPickle as pickle
import os
import sys

from scenarios import Scenario
from server.game import Load

campaignFolders = filter( 
    lambda f: len( f )>1 and f[0] !="." and os.path.isdir( os.path.join( sys.path[0], "campaigns", f ) ), 
    os.listdir( os.path.join( sys.path[0], "campaigns" ) ) )
campaignNames = campaignFolders
campaignNames.sort()
print os.listdir( os.path.join( sys.path[0], "campaigns" ) ), campaignFolders

class Campaign:
    title = None
    name = None
    uid = None
    description = None
    scenarios = []
    
    def __init__( self ):
        self.games = {}
        self.completedScenarios = 0
        self.fullyLoaded = True
        
    def scenarioEnded( self, scenario, game, success ):
        if success:
            self.games[ scenario.name ] = game
            self.completedScenarios = len( self.games )
            print "self.completedScenarios", self.completedScenarios

    def save( self ):
        path = os.path.join( sys.path[0], "client", "saves", "campaigns", "%s.campaign.pyfl" % self.uid )
        
        f = open( path, "w+:bz2" )
        success = False
        if f:
            success = self.dump( f )
            f.close()
        
        return success

    def dump( self, f ):
       # try:
        games = self.games
        self.games = None

        data = pickle.dump( self, f )

        self.games = games

        for k,game in games.items():
            pickle.dump( k, f )
            game.dump( f )
        
        success = True
       # except Exception, ex:
       #     print "failed to save campaign:", ex
       #     data = None
        
        return success
        
def LoadCampaignHead( path ):
    f = open( path, "r" )
    if f:
        try:
            campaign = pickle.load( f )
            campaign.path = path
            campaign.fullyLoaded = False
                    
        except Exception, ex:
            print "failed to load campaign head:", ex
            campaign = None
        f.close()
        
    return campaign

def LoadCampaignFull( path ):
    f = open( path, "r" )
    if f:
        try:
            campaign = pickle.load( f )
            
            campaign.games = {}
            game = True
            for i in xrange( campaign.completedScenarios ):
                k = pickle.load( f )
                game = Load( f, prefixScenarioPath="campaigns.%s" % campaign.name )
                if game:
                    campaign.games[ k ] = game
                print k, game
                    
            campaign.fullyLoaded = True
            print "campaign.fullyLoaded", campaign.fullyLoaded
                    
        except Exception, ex:
            print "failed to load campaign full:", ex
            campaign = None
        f.close()
        
    return campaign
    
