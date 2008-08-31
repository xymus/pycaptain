from math import pi

from client.controls import *
from client.specialcontrols import *
from common.comms import *
from common import ids

class MenuShips( ControlFrame ):
    def __init__( self, display, imgs, texts, eQuit=None, eOk=None ):
       ControlFrame.__init__( self )
       self.imgs = imgs
       self.texts = texts

       border = 50
       butsSize = (60,24)
       pbsSize = ((display.resolution[0]-3*border)/2,18) # 24
       
       self.options = []
       self.pOption = 0 

       self.ctrlOk =    LightControlLeft( (260,550), eOk, _( "Ok" ), imgs )
       self.ctrlQuit =  LightControlRight( (600,550), eQuit, _( "Main menu" ), imgs )
       self.ctrlPrev =  LightControlRight( (-30,100), self.ePrev, _( "Prev" ), imgs )
       self.ctrlNext =  LightControlRight( (-30,500), self.eNext, _( "Next" ), imgs )
       
       self.ctrlShip = RotatingImageHolder( None, (display.resolution[0]/4,display.resolution[1]/2), ri=0.01 )
       

        
       controls = [    ImageHolder( imgs.splashBack, (0,0) ),
       
                       self.ctrlOk,
                       self.ctrlQuit,
                       self.ctrlPrev,
                       self.ctrlNext,
                       
                       self.ctrlShip,
                       RotatingImageHolder( imgs[ ids.S_HUMAN_BASE ], (620,600), ri=0.015 ),
                       KeyCatcher( eQuit, letter="q" ) ]

       x = (display.resolution[0]+border)/2

       y = border
       controls.append( Label( (x,y), _( "Hangar size" ) ) )
       self.pbHangar = ProgressBar( (x,y+18), pbsSize )
       controls.append( self.pbHangar )

       y += border
       controls.append( Label( (x,y), _( "Shield" ) ) )
       self.pbShield = ProgressBar( (x,y+18), pbsSize )
       controls.append( self.pbShield )

       y += border
       controls.append( Label( (x,y), _( "Hull" ) ) )
       self.pbHull = ProgressBar( (x,y+18), pbsSize )
       controls.append( self.pbHull )

       y += border
       controls.append( Label( (x,y), _( "Civilian appreciation" ) ) )
       self.pbCivilian = ProgressBar( (x,y+18), pbsSize )
       controls.append( self.pbCivilian )

       y += border
       controls.append( Label( (x,y), _( "Speed" ) ) )
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
       self.eEnter = eOk

       self.changeSelected()
       
    selectedOption = property( fget=lambda self: self.options[ self.pOption ].ship )

    def eNext( self, sender, (x,y) ):
        if self.options:
            self.pOption = (self.pOption+1)%len(self.options)
        self.changeSelected()

    def ePrev( self, sender, (x,y) ):
        self.pOption = (self.pOption-1)%len(self.options)
        self.changeSelected()

    def changeSelected(self, option=None, options=None):
        if options:
            self.options = options
            self.pOption = 0
            
        if self.options:
            if not option:
                option = self.options[ self.pOption ]

         #   self.pbEnergy.progress = option.energy/100.0
         #   self.pbOre.progress = option.ore/100.0
            self.pbShield.progress = option.shield/100.0
            self.pbHull.progress = option.hull/100.0
            self.pbHangar.progress = option.hangar/100.0
            self.pbCivilian.progress = option.civilians/100.0
            self.pbSpeed.progress = option.speed/100.0

            self.lblRace.text = _( "Race: %s" ) % self.texts[ option.race ]
            self.lblShip.text = _( "Ship class: %s" ) % self.texts[ option.ship ]
            self.lblTurrets.text = _( "%i turrets" ) % option.nbrTurrets
            if option.canJump:
                self.lblCanJump.text = _( "Equipped for faster than light jump" )
            else:
                self.lblCanJump.text = ""
                
            self.ctrlShip.img = self.imgs[ self.options[ self.pOption ].ship ]

