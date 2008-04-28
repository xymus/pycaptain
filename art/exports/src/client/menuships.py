from math import pi

from controls import *
from comms import * # COChoice, COInput # TODO remove when really implemented

import ids

class MenuShips( ControlFrame ):
    def __init__( self, display, imgs, texts ):
       ControlFrame.__init__( self )
       self.display = display
       self.imgs = imgs
       self.texts = texts

       self.quit = False
       self.choice = None

       self.shipR = 0
       self.shipRr = 0.01

       self.inputs = COInput()

       border = 50
       butsSize = (60,24)
       pbsSize = ((display.resolution[0]-3*border)/2,18) # 24

       self.options = [  COPossible( ids.S_FLAGSHIP_0, ids.R_HUMAN, 4, 15, 25, 30, 40, 50, 10 ) ] # , 
    #                    COPossible( ids.S_FLAGSHIP_1, ids.R_HUMAN, 10, 10, 20, 30, 40, 30, 10, 20 ), 
   #                     COPossible( ids.S_FLAGSHIP_2, ids.R_HUMAN, 4, 15, 30, 30, 40, 100, 10, 20 ), 

   #                     COPossible( ids.S_AI_FS_0, ids.R_AI, 3, 15, 30, 30, 40, 100, 10, 20 ), 
   #                     COPossible( ids.S_AI_FS_1, ids.R_AI, 6, 15, 30, 30, 40, 100, 10, 20 ), 
   #                     COPossible( ids.S_AI_FS_2, ids.R_AI, 8, 15, 30, 30, 40, 100, 10, 20 ), 

   #                     COPossible( ids.S_EVOLVED_FS_0, ids.R_EVOLVED, 4, 15, 30, 30, 40, 100, 10, 20 ), 
   #                     COPossible( ids.S_EVOLVED_FS_1, ids.R_EVOLVED, 5, 15, 30, 30, 40, 100, 10, 20 ) ] # TODO remove when really implemented
       self.pOption = 0 


       controls = [ LabelButton( (display.resolution[0]-3*border/2-2*butsSize[0], display.resolution[1]-border-butsSize[1]), butsSize, self.eQuit, texts.uiQuit ),
                    LabelButton( (display.resolution[0]-border-butsSize[0], display.resolution[1]-border-butsSize[1]), butsSize, self.eOk, texts.uiOk ),
                    LabelButton( (display.resolution[0]/2-border/2-butsSize[0], display.resolution[1]-border-butsSize[1]), butsSize, self.ePrev, texts.uiPrev ),
                    LabelButton( (display.resolution[0]/2+border/2, display.resolution[1]-border-butsSize[1]), butsSize, self.eNext, texts.uiNext ) ]

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

    def draw( self ):
        self.display.beginDraw()

        self.display.draw( self.imgs.splashBack, ( (self.display.resolution[0]-self.display.getWidth(self.imgs.splashBack))/2, (self.display.resolution[1]-self.display.getHeight(self.imgs.splashBack))/2 ) )
        for control in self.controls:
            control.draw( self.display )

        self.display.drawRo( self.imgs[ self.options[ self.pOption ].ship ], (self.display.resolution[0]/4,self.display.resolution[1]/2), self.shipR )
        self.shipR = (self.shipR+self.shipRr)%(2*pi)

        self.display.finalizeDraw()

    def getInputs( self ):
        (quit,self.inputs) = self.display.getInputs( self.inputs )
        self.quit = self.quit or quit

        if self.inputs.mouseUpped:
            for control in self.controls:
                if control.hits( self.inputs.mouseUpAt ):
                    self.focus = control
                    break

        if self.inputs.keys:
          for k in self.inputs.keys:
            self.keyInput( k[0], k[1] )

        choice = self.choice
        self.choice = None
        return self.quit, choice




