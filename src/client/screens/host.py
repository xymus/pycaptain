from client.controls import *
from client.specialcontrols import *
from common.comms import COInput
from common import ids
from common import config

from client.specialcontrols.boxes import *

class HostMenu( ControlFrame ):
    def __init__(self, display, imgs, eOk=None, eBack=None):
        ControlFrame.__init__( self )
        self.imgs = imgs

        diff = 8
        height = 24
        
        self.cUser = TextBox( (200,300), (160,height), "", forbidden=[":",";","|"] )
        self.cAdminPassword = TextBox( (200,300+(diff+height)), (160,height), "", password=True )
        self.cServerAdresses = TextBox( (200,300+(diff+height)*2), (160,height), "localhost" )
        self.cPort = TextBox( (200,300+(diff+height)*3), (160,height), str(config.port), numeric=True )

        self.cError = Label( (40,400+(diff+height)*5), " " )
        
        self.ctrlOk =   LightControlLeft( (260,550), eOk, _("Connect"), imgs )
        self.ctrlBack = LightControlRight( (600,550), eBack, _("Back to main menu"), imgs )

            
        controls = [    ImageHolder( imgs.splashBack, (0,0) ),
                        ImageHolder( imgs.gameTitle, (40,40) ),
                        self.cUser,
                        self.cAdminPassword,
                        self.cServerAdresses,
                        self.cPort,
                        Label( (120,300), _("Your name") ),
                        Label( (120,300+(diff+height)), _("Admin password") ),
                        Label( (120,300+(diff+height)*2), _("Server adresses seperated by spaces") ),
                        Label( (120,300+(diff+height)*3), _("Server port") ),
                        self.ctrlOk,
                        self.ctrlBack,
                        RotatingImageHolder( imgs[ ids.S_HUMAN_BASE ], (620,600), ri=0.015 ),
                        self.cError,
                        KeyCatcher( eBack, letter="q" ),
                        
                       # MessageBox( display, imgs, "Server adresses seperated by spaces Server adresses seperated by spaces Server adresses seperated by spaces Server adresses seperated by spaces", buttons=[("ok", None),("cancel", None)] )
                        ]

        self.addControls( controls )
        self.eEnter = eOk


