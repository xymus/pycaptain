from math import pi

from client.controls import *
from client.specialcontrols import *
from common.comms import COInput
from common import ids
from client import imgs

import scenarios

class ScenarioMenu( ControlFrame ):
    def __init__(self, display, imgs, ePlay=None, eBack=None ):
        ControlFrame.__init__( self )
        
        self.ctrlPlay =     LightControlLeft( (260,550), ePlay, "Play", imgs )
        self.ctrlBack =     LightControlRight( (600,550), eBack, "Back to menu", imgs )
        self.ctrlPrev =     LightControlLeft( (260,450), self.ePrev, "Previous scenario", imgs )
        self.ctrlNext =     LightControlRight( (600,450), self.eNext, "Next scenario", imgs )
        
        self.lblTitle =     Label( (80,76), "", textSize=20 )
        self.lblYear =     Label( (96,100), "" )
        self.lblDescription =      Label( (88,120), "", maxWidth=460, maxHeight=300 )
        
      #  self.imgScreen = ImageHolder( None, (620,60) )
        self.imgBack = ImageHolder( imgs.splashBack, (0,0) )
        
        controls =   [  self.imgBack,
      #                  self.imgScreen,
                       #ImageHolder( imgs.gameTitle, (40,40) ),
                        self.ctrlPlay,
                        self.ctrlBack,
                        self.ctrlPrev,
                        self.ctrlNext,
                        self.lblTitle,
                        self.lblDescription,
                        self.lblYear,
                        RotatingImageHolder( imgs[ ids.S_HUMAN_BASE ], (620,600), ri=0.015 ),
                        RotatingImageHolder( imgs[ ids.S_AI_FS_0 ], (620,503), ri=0.003 ),
                        #RotatingImageHolder( imgs[ ids.S_HUMAN_FS_1 ], (445,330), r=pi*3/8 ),
                        KeyCatcher( eBack, letter="q" ),
                        ]

        self.addControls( controls )
        
        self.scenarios = []
        self.scenarioImgs = []
        for name in scenarios.scenarioNames:
            imported = False
            try:
                exec( "from scenarios.%s import %s as Scenario"%( name.lower(), name.capitalize() ) )
                imported = True
            except Exception, ex:
                print ex
                
            if imported:
                self.scenarios.append( Scenario )
                img = None
                
                try:
                    img = imgs.loadImageWithDisplay( "scenarios/%s.jpg" % name )
                except Exception, ex:
                    print ex, "scenarios/%s.png" % name
                    
                if not img:
                    img = imgs.splashBack
                self.scenarioImgs.append( img ) # [ Scenario ]
                    
                    
              
    #    self.scenarios.sort( cmp=self.cmpScenarios )
               
        self.updateInfo( 0 )
    def cmpScenarios( self, x, y ):
        if x.title > y.title:
            return 1
        elif x.title < y.title:
            return -1
        else:
            return 0
            
    def updateInfo( self, kScenario=None ):
        if kScenario != None:
            self.kScenario = kScenario
            
        self.lblTitle.text = self.scenarios[ self.kScenario ].title
        self.lblDescription.text = self.scenarios[ self.kScenario ].description
        self.lblYear.text = "year %i" % self.scenarios[ self.kScenario ].year
        self.imgBack.img = self.scenarioImgs[ self.kScenario ]
       
    def ePrev( self, sender, (x,y) ):
        self.updateInfo( (self.kScenario-1)%len( self.scenarios ) )
       
    def eNext( self, sender, (x,y) ):
        self.updateInfo( (self.kScenario+1)%len( self.scenarios ) )
        
    selectedScenario = property( fget=lambda self: self.scenarios[ self.kScenario ] )
        
   # def manageInputs( self, display ):
   #     self.quit = ControlFrame.manageInputs( self, display ) or self.quit


