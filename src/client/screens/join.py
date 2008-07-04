from client.controls import *
from client.specialcontrols import *
from common.comms import COInput
from common import ids

class JoinMenu( ControlFrame ):
    def __init__(self, display, imgs, user="", password="", server="", port="", eOk=None, eBack=None):
        ControlFrame.__init__( self )
        self.imgs = imgs

        diff = 8
        height = 24
        
        self.cUser = TextBox( (200,300), (160,height), user, forbidden=[":",";","|"] )
        self.cPassword = TextBox( (200,300+(diff+height)), (160,height), password, password=True )
        self.cServer = TextBox( (200,300+(diff+height)*2), (160,height), server )
        self.cPort = TextBox( (200,300+(diff+height)*3), (160,height), str(port), numeric=True )

        self.cError = Label( (40,400+(diff+height)*5), " " )
        
        self.ctrlOk =  LightControlLeft( (260,550), eOk, "Connect", imgs )
        self.ctrlBack =     LightControlRight( (600,550), eBack, "Back to menu", imgs )

            
        controls = [    ImageHolder( imgs.splashBack, (0,0) ),
                        ImageHolder( imgs.gameTitle, (40,40) ),
                        self.cUser,
                        self.cPassword,
                        self.cServer,
                        self.cPort,
                        Label( (120,300), "user" ),
                        Label( (120,300+(diff+height)), "password" ),
                        Label( (120,300+(diff+height)*2), "server" ),
                        Label( (120,300+(diff+height)*3), "port" ),
                        self.ctrlOk,
                        self.ctrlBack,
                        RotatingImageHolder( imgs[ ids.S_HUMAN_BASE ], (620,600), ri=0.015 ),
                        self.cError,
                        KeyCatcher( eBack, letter="q" )
                        ]

        self.addControls( controls )
        self.eEnter = eOk

        self.initialPassword = password


    def setError( self, text ):
        self.cError.text = text

