from md5 import md5

from controls import *
from common.comms import COInput
import imgs

class LoginMenu( ControlFrame ):
    def __init__(self, display, imgs, user="", password="", server="", port=""):
        ControlFrame.__init__( self )
        self.display = display
        self.imgs = imgs

        self.quit = False
        self.ok = False
        self.local = False
        self.toggleFullscreen = False
        self.focus = None

        self.inputs = COInput()

        diff = 8
        height = 24
        
        self.cUser = TextBox( (120,100), (160,height), user, forbidden=[":",";","|"] )
        self.cPassword = TextBox( (120,100+(diff+height)), (160,height), password, password=True )
        self.cServer = TextBox( (120,100+(diff+height)*2), (160,height), server )
        self.cPort = TextBox( (120,100+(diff+height)*3), (160,height), str(port), numeric=True )

        self.cOk = LabelButton( (120+diff+60,100+(diff+height)*4), (60, height), self.eOk, "Ok" )
        self.cQuit = LabelButton( (120,100+(diff+height)*4), (60, height), self.eQuit, "Quit" )
        self.cLocal = LabelButton( (120+(diff+60)*3+diff,100), (200, height), self.eLocal, "Single player" )
        self.cFullscreen = LabelButton( (120+(diff+60)*3+diff,200), (200, height), self.eFullscreen, "Toggle Fullscreen" )

        self.cError = Label( (40,100+(diff+height)*5), " " )

        controls = [    self.cUser,
                        self.cPassword,
                        self.cServer,
                        self.cPort,
                        self.cOk,
                        self.cLocal,
                        self.cFullscreen,
                        self.cQuit,
                        Label( (40,100), "user" ),
                        Label( (40,100+(diff+height)), "password" ),
                        Label( (40,100+(diff+height)*2), "server" ),
                        Label( (40,100+(diff+height)*3), "port" ),
                        self.cError
                        ]

        self.addControls( controls )
        self.eEnter = self.eOk

        self.initialPassword = password

    def draw( self ):
        self.display.beginDraw()

      #  self.display.clear( (0,0,0) )
        self.display.draw( self.imgs.splashBack, ( (self.display.resolution[0]-self.display.getWidth(self.imgs.splashBack))/2, (self.display.resolution[1]-self.display.getHeight(self.imgs.splashBack))/2 ) )
        for control in self.controls:
            control.draw( self.display )

        self.display.finalizeDraw()

    def getUpdates( self ):
#        (quit,self.inputs) = self.display.getInputs( self.inputs )
#        self.quit = self.quit or quit

        self.quit = self.manageInputs( self.display ) or self.quit
#        if self.inputs.mouseUpped:
#            for control in self.controls:
#                if control.hits( self.inputs.mouseUpAt ):
#                    self.selected = control
#                    break

#        if self.inputs.keys:
#          for k in self.inputs.keys:
#            self.keyInput( k[0], k[1] )

        if self.quit:
            self.quit = False
            return (True, False, None, None, None, False, False)
        elif self.ok:
            self.ok = False
            if self.cPassword.text == self.initialPassword:
                password = self.initialPassword
            else:
                password = md5(self.cPassword.text).hexdigest()
            return (False, self.cUser.text, password, self.cServer.text,int(self.cPort.text), False, False)
        elif self.local:
            self.local = False
            return (False,False, None, None, None, True, False)
        elif self.toggleFullscreen:
            self.toggleFullscreen = False
            return (False,False, None, None, None, False, True)
        else:
            return (False,False, None, None, None, False, False)

 
    def clear(self):
        pass

    def eOk( self, sender, (x,y) ):
        self.ok = True

    def eLocal( self, sender, (x,y) ):
        self.local = True

    def eQuit( self, sender, (x,y) ):
        self.quit = True

    def eFullscreen( self, sender, (x,y) ):
        self.toggleFullscreen = True

    def setError( self, text ):
        self.cError.text = text
       # print text

