from math import pi

from client.controls import *
from client.specialcontrols import *
from common.comms import *
from common import ids

class MenuShips( ControlFrame ):
    def __init__( self, display, imgs, texts ):
       ControlFrame.__init__( self )
       self.imgs = imgs
       self.texts = texts

       self.quit = False
       self.choice = None

       border = 50
       butsSize = (60,24)
       pbsSize = ((display.resolution[0]-3*border)/2,18) # 24
       
       self.options = [  COPossible( ids.S_HUMAN_FS_0, ids.R_HUMAN, 4, 15, 25, 30, 40, 50, 10 ) ] # TODO remove when implemented with stats object
       self.pOption = 0 

       self.ctrlOk =    LightControlLeft( (260,550), self.eOk, texts.uiOk, imgs )
       self.ctrlQuit =  LightControlRight( (600,550), self.eQuit, texts.uiQuit, imgs )
       self.ctrlPrev =  LightControlRight( (-30,100), self.ePrev, texts.uiPrev, imgs )
       self.ctrlNext =  LightControlRight( (-30,500), self.eNext, texts.uiNext, imgs )
       
       self.ctrlShip = RotatingImageHolder( None, (display.resolution[0]/4,display.resolution[1]/2), ri=0.01 )
       

        
       controls = [    ImageHolder( imgs.splashBack, (0,0) ),
                      # ImageHolder( imgs.gameTitle, (40,40) ),
                       
                       self.ctrlOk,
                       self.ctrlQuit,
                       self.ctrlPrev,
                       self.ctrlNext,
                       
                       self.ctrlShip,
                       RotatingImageHolder( imgs[ ids.S_HUMAN_BASE ], (620,600), ri=0.015 ), ]

       x = (display.resolution[0]+border)/2

       y = border
       controls.append( Label( (x,y), texts.uiHangarSize ) )
       self.pbHangar = ProgressBar( (x,y+18), pbsSize )
       controls.append( self.pbHangar )

       y += border
       controls.append( Label( (x,y), texts.uiMaxShield ) )
       self.pbShield = ProgressBar( (x,y+18), pbsSize )
       controls.append( self.pbShield )

       y += border
       controls.append( Label( (x,y), texts.uiMaxHull ) )
       self.pbHull = ProgressBar( (x,y+18), pbsSize )
       controls.append( self.pbHull )

       y += border
       controls.append( Label( (x,y), texts.uiCivilian ) )
       self.pbCivilian = ProgressBar( (x,y+18), pbsSize )
       controls.append( self.pbCivilian )

       y += border
       controls.append( Label( (x,y), texts.uiSpeed ) )
       self.pbSpeed = ProgressBar( (x,y+18), pbsSize )
       controls.append( self.pbSpeed )

       x = (display.resolution[0]+border)/2
       y = display.resolution[1]*2/3
       self.lblRace = Label( (x,y), "" )
       controls.append( self.lblRace )
       y += border/2
       self.lblShip = Label( (x,y), "" )
       controls.append( self.lblShip )
       y += border/2
       self.lblTurrets = Label( (x,y), "" )
       controls.append( self.lblTurrets )
       y += border/2
       self.lblCanJump = Label( (x,y), "" )
       controls.append( self.lblCanJump )

       self.addControls( controls )
       self.eEnter = self.eOk

       self.changeSelected()

    def eQuit( self, sender, (x,y) ):
        self.quit = True

    def eOk( self, sender, (x,y) ):
        self.choice = self.options[ self.pOption ].ship

    def eNext( self, sender, (x,y) ):
        self.pOption = (self.pOption+1)%len(self.options)
        self.changeSelected()

    def ePrev( self, sender, (x,y) ):
        self.pOption = (self.pOption-1)%len(self.options)
        self.changeSelected()

    def changeSelected(self, option=None):
        if not option:
            option = self.options[ self.pOption ]

     #   self.pbEnergy.progress = option.energy/100.0
     #   self.pbOre.progress = option.ore/100.0
        self.pbShield.progress = option.shield/100.0
        self.pbHull.progress = option.hull/100.0
        self.pbHangar.progress = option.hangar/100.0
        self.pbCivilian.progress = option.civilians/100.0
        self.pbSpeed.progress = option.speed/100.0

        self.lblRace.text = self.texts.uiRaceS%self.texts[ option.race ]
        self.lblShip.text = self.texts.uiShipS%self.texts[ option.ship ]
        self.lblTurrets.text = self.texts.uiTurretsI%option.nbrTurrets
        if option.canJump:
            self.lblCanJump.text = self.texts.uiCanJump
        else:
            self.lblCanJump.text = ""
            
        self.ctrlShip.img = self.imgs[ self.options[ self.pOption ].ship ]

    def getInputs( self ):

        self.quit = self.manageInputs( display ) or self.quit

        choice = self.choice
        self.choice = None
        return self.quit, choice

