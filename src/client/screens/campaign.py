from math import pi
import os
import sys

from . import Screen
from client.controls import *
from client.specialcontrols import *
from client.specialcontrols.boxes import Box
from client.specialcontrols.campaign import Timeline

import campaigns

from common.comms import COInput
from common import ids
from client import imgs


class CampaignMenu( Screen ):
    def __init__( self, display, imgs, ePlay=None, eBack=None ):
        Screen.__init__( self )

        self.ePlayOut = ePlay
        self.imgBack = ImageHolder( imgs.splashBack, (0,0) )

        self.lblCampaignTitle =     Label( (250,56), "lblCampaignTitle", textSize=20 )
        self.lblCampaignPlayer =    Label( (256,82), "lblCampaignPlayer" )
        self.lblCampaignRace =      Label( (256,100), "lblCampaignRace" )
        self.lblCampaignDescription =      Label( (350,82), "lblCampaignDescription", maxWidth=540, maxHeight=100 )

        self.lblScenarioTitle =     Label( (50,306), "lblScenarioTitle", textSize=20 )
        self.lblScenarioYear =      Label( (66,330), "lblScenarioYear" )
        self.lblScenarioDescription =     Label( (58,350), "lblScenarioDescription", maxWidth=240, maxHeight=300 )

        self.ctrlPlay =     LightControlLeft( (260,550), self.ePlay, "Play", imgs )
        self.ctrlBack =     LightControlRight( (600,550), eBack, "Back to menu", imgs )
        
        self.ctrlCampaignUp =     LightControlDown( (-10,40), self.eCampaignUp, "", imgs )
        self.ctrlCampaignDown =   LightControlUp( (-10,90), self.eCampaignDown, "", imgs )
        
        self.ctrlTimeline =     Timeline( 220, display.resolution[0], imgs, display, self.eTimelineChanged )

        controls =   [  self.imgBack,

                        Box( imgs, (240,40), (650,100) ),
                        Box( imgs, (40,290), (400,260) ),

                        self.lblCampaignTitle,
                        self.lblCampaignPlayer,
                        self.lblCampaignRace,
                        self.lblCampaignDescription,

                        self.lblScenarioTitle,
                        self.lblScenarioYear,
                        self.lblScenarioDescription,

                        self.ctrlPlay,
                        self.ctrlBack,
                        self.ctrlCampaignUp,
                        self.ctrlCampaignDown,
                        self.ctrlTimeline,
                        
                        RotatingImageHolder( imgs[ ids.S_HUMAN_BASE ], (620,600), ri=0.015 ),

                        KeyCatcher( eBack, letter="q" ),
                        ]

        self.addControls( controls )
        
        self.reset()

    def reset( self ):
        self.campaigns = []
        
        ## load all previous campaigns
        for path in os.listdir( os.path.join( sys.path[0], "client", "saves", "campaigns" ) ):
            if ".campaign.pyfl" in path:
                campaign = campaigns.LoadCampaignHead( os.path.join( sys.path[0], "client", "saves", "campaigns", path ) )
                if campaign:
                    self.campaigns.append( campaign )
        
        ## list current campaigns
        for campaignName in campaigns.campaignNames:
            exec( "from campaigns.%s import %s as CampaignClass" % (campaignName,campaignName.capitalize()) ) 
            if not CampaignClass.uid in [ campaign.uid for campaign in self.campaigns ]:
                self.campaigns.append( CampaignClass() )
            
        if self.campaigns:
            self.campaign = self.campaigns[0]
        else:
            self.campaign = None
        
        self.updateCampaign( self.campaign )

    def updateCampaign( self, campaign=None, scenario=None ):
        if campaign:
            self.campaign = campaign
        
        self.lblCampaignTitle.text = self.campaign.title
        self.lblCampaignPlayer.text = self.campaign.player
        self.lblCampaignRace.text = self.campaign.race
        self.lblCampaignDescription.text = self.campaign.description
        self.ctrlTimeline.setValues( [Scenario.year for Scenario in self.campaign.scenarios] )
        self.ctrlTimeline.selectables = self.campaign.completedScenarios
        
        if campaign and not scenario:
            if self.campaign.completedScenarios >= len(self.campaign.scenarios):
                self.ctrlTimeline.selected = 0
            else:
                self.ctrlTimeline.selected = self.campaign.completedScenarios
            self.scenario = self.campaign.scenarios[ self.ctrlTimeline.selected ]
            
        if scenario:
            self.scenario = scenario
            
            k = self.campaign.scenarios.index( scenario )
            self.ctrlTimeline.selected = k
            
        self.lblScenarioTitle.text = self.scenario.title
        self.lblScenarioYear.text = "year %i" % self.scenario.year
        self.lblScenarioDescription.text = self.scenario.description
        
    def eCampaignUp( self, sender, pos ):
        k = self.campaigns.index( self.campaign )
        k = (k+1)%len( self.campaigns )
        self.updateCampaign( campaign=self.campaigns[k] )
        
    def eCampaignDown( self, sender, pos ):
        k = self.campaigns.index( self.campaign )
        k = (k-1)%len( self.campaigns )
        self.updateCampaign( campaign=self.campaigns[k] )
        
    def eTimelineChanged( self, sender, pos ):
        scenario = self.campaign.scenarios[ sender.selected ]
        self.updateCampaign( scenario=scenario )
        
    def ePlay( self, sender, pos ):
        if self.ePlayOut:
            if not self.campaign.fullyLoaded:
                kScenario = self.ctrlTimeline.selected
                campaign = campaigns.LoadCampaignFull( self.campaign.path )
                scenario = campaign.scenarios[ kScenario ]
                
                kCampaign = self.campaigns.index( self.campaign )
                self.campaigns[ kCampaign ] = campaign
                
                self.updateCampaign( campaign=campaign, scenario=scenario )
            
            self.ePlayOut( sender, pos )
        
