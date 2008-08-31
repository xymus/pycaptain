from math import pi

from . import Screen
from client.controls import *
from client.specialcontrols import *
from common import ids

class MainMenu( Screen ):
    def __init__(self, display, imgs, eQuickPlay=None, eLoad=None, eScenario=None, eJoin=None, eCampaign=None, eHost=None, eOptions=None, eQuit=None ):
        ControlFrame.__init__( self )
        
        self.ctrlQuickPlay = LightControlLeft( (100,200), eQuickPlay, _("Quick play"), imgs )
        self.ctrlLoad =     LightControlRight( (460,200), eLoad, _("Load a game"), imgs )
        self.ctrlScenario = LightControlLeft( (80,275), eScenario, _("Select a scenario"), imgs )
        self.ctrlJoin =     LightControlRight( (430,275), eJoin, _("Join a game"), imgs )
        self.ctrlCampaign = LightControlLeft( (40,350), eCampaign, _("Select a campaign"), imgs )
        self.ctrlHost =     LightControlRight( (400,350), eHost, _("Host a game"), imgs )
        
        self.ctrlOptions =  LightControlLeft( (260,550), eOptions, _("Options"), imgs )
        self.ctrlQuit =     LightControlRight( (600,550), eQuit, _("Quit"), imgs )
        
       # self.ctrlCampaign.enabled = False
       # self.ctrlOptions.enabled = False
        self.ctrlHost.enabled = False
        
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
                        KeyCatcher( eQuit, letter="q" )
                        ]

        self.addControls( controls )

   
   # def manageInputs( self, display ):
   #     self.quit = ControlFrame.manageInputs( self, display ) or self.quit


