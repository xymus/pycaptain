from math import pi

from client.controls import *
from client.specialcontrols import *
from common.comms import COInput
from common import ids
from client import imgs

class WaitingScreen( ControlFrame ):
    """Displays a rotating ship and text in a label"""
    def __init__(self, display, imgs, eCancel=None ):
        ControlFrame.__init__( self )

        self.ctrlCancel =  LightControlLeft( (600,550), eCancel, _("Cancel"), imgs )
        self.lblMsg = Label( (display.resolution[0]/2,display.resolution[1]-100), _("waiting for server...") )
        
        controls =   [  ImageHolder( imgs.splashBack, (0,0) ),
                        ImageHolder( imgs.gameTitle, (40,40) ),
                        
                        self.ctrlCancel,
                        
                        RotatingImageHolder( imgs[ ids.S_AI_FS_1 ], (display.resolution[0]/2, display.resolution[1]/2), ri=0.015 ),
                        self.lblMsg,
                        KeyCatcher( eCancel, letter="q" )
                        ]

        self.addControls( controls )

