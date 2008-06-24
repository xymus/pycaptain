from math import pi

from client.controls import *
from client.specialcontrols import *
from common.comms import COInput
from common import ids
from client import imgs

class MainMenu( ControlFrame ):
    def __init__(self, display, imgs ):
        ControlFrame.__init__( self )
        
        self.ctrlQuickPlay = LightControlLeft( (100,200), self.eQuickPlay, "Quick play", imgs )
        self.ctrlLoad =     LightControlRight( (460,200), self.eLoad, "Load a game", imgs )
        self.ctrlScenario = LightControlLeft( (60,300), self.eScenario, "Select a scenario", imgs )
        self.ctrlJoin =     LightControlRight( (420,300), self.eJoin, "Join a game", imgs )
        self.ctrlCampaign = LightControlLeft( (40,350), self.eCampaign, "Select a campaign", imgs )
        self.ctrlHost =     LightControlRight( (400,350), self.eHost, "Host a game", imgs )
        
        self.ctrlOptions =  LightControlLeft( (260,550), self.eOptions, "Options", imgs )
        self.ctrlQuit =     LightControlRight( (600,550), self.eQuit, "Quit", imgs )
        
        self.ctrlLoad.enabled = False
        self.ctrlScenario.enabled = False
        self.ctrlCampaign.enabled = False
        self.ctrlHost.enabled = False
        self.ctrlOptions.enabled = False
        
        controls =   [  ImageHolder( imgs.splashBack, (0,0) ),
                        ImageHolder( imgs.gameTitle, (40,40) ),
                        self.ctrlQuickPlay,
                        self.ctrlLoad,
                        self.ctrlScenario,
                        self.ctrlJoin,
                        self.ctrlCampaign,
                        self.ctrlHost,
                        self.ctrlOptions,
                        self.ctrlQuit,
                        RotatingImageHolder( imgs[ ids.S_HUMAN_BASE ], (620,600), ri=0.015 ),
                        RotatingImageHolder( imgs[ ids.S_HUMAN_FS_1 ], (445,330), r=pi*3/8 ),
                        KeyCatcher( self.eQuit, letter="q" )
                        ]

        self.addControls( controls )

   
    def manageInputs( self, display ):
        self.quit = False
        self.quickPlay = False
        self.join = False
        self.quit = ControlFrame.manageInputs( self, display ) or self.quit

    def eQuickPlay( self, sender, (x,y) ):
        self.quickPlay = True
        
    def eLoad( self, sender, (x,y) ):
        print "eLoad"

    def eScenario( self, sender, (x,y) ):
        print "eScenario"
        
    def eJoin( self, sender, (x,y) ):
        self.join = True
        
    def eCampaign( self, sender, (x,y) ):
        print "eCampaign"
        
    def eHost( self, sender, (x,y) ):
        print "eHost"
        
    def eOptions( self, sender, (x,y) ):
        print "eOptions"
        
    def eQuit( self, sender, (x,y) ):
        print "quit"
        self.quit = True

