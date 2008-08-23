from math import pi
import os
import sys
from threading import Thread
import cPickle as pickle
from gzip import open

from . import Screen
from client.controls import *
from client.specialcontrols import *
from client.specialcontrols.boxes import Box
from common import ids
from common import config

from server.players import Human
from server.game import LoadGame

class Save:
    def __init__( self, filename, filepath, modified="" ):
        self.filename = filename
        self.filepath = filepath
        
        self.loading = False
        self.loaded = False
        self.valid = False

    def getInformation( self, f ):
    #    self.loading = True
    #    f = open( self.filepath, "r" )
        if f:
            try:
                infoDict = pickle.load( f )
                
                self.title = infoDict.get( "title", "" ) # pickle.load( f )
                self.year = "year %s" % infoDict.get( "year", "" ) # pickle.load( f )
                self.timePlayed = infoDict.get( "timePlayed", "" ) # pickle.load( f )
                self.description = infoDict.get( "description", "" ) # pickle.load( f )
                self.username = infoDict.get( "username", "" ) # pickle.load( f )
                self.ship = infoDict.get( "ship", "" ) # pickle.load( f )
                
                self.valid = True
            except Exception, ex:
                self.valid = False
                print ex
            f.close()
            
        self.loaded = True
        

class LoadMenu( Screen ):
    def __init__(self, display, imgs, eLoad=None, eBack=None ):
        ControlFrame.__init__( self )
        
        self.crtlLoad =  LightControlLeft( (260,550), eLoad, "Load", imgs )
        self.ctrlQuit =     LightControlRight( (600,550), eBack, "Back to main menu", imgs )
        
        self.ctrlListUp = LightControlDown( (50, 40), self.eListUp, "", imgs )
        self.ctrlListDown = LightControlUp( (50, display.resolution[1]-140), self.eListDown, "", imgs )
        
        self.lblTitle =     Label( (400,76), "", textSize=20 )
        self.lblYear =      Label( (416,100), "" )
        self.lblUsername =      Label( (416,120), "" )
        self.lblTimePlayer =    Label( (416,140), "" )
        self.lblDescription =   Label( (408,160), "", maxWidth=500, maxHeight=100 )
        
        self.imgShip = RotatingImageHolder( None, (655, display.resolution[1]/2), ri=0.005 )
        self.imgs = imgs
        
        controls =   [  ImageHolder( imgs.splashBack, (0,0) ),
                        Box( imgs, (390,66), (530,200) ),
                   #     ImageHolder( imgs.gameTitle, (40,40) ),
                        self.crtlLoad,
                        self.ctrlQuit,
                        
                        self.ctrlListUp,
                        self.ctrlListDown,
                        
                        self.lblTitle,
                        self.lblDescription,
                        self.lblYear,
                        self.lblUsername,
                        self.lblTimePlayer,
                        
                        self.imgShip,
                        
                        RotatingImageHolder( imgs[ ids.S_HUMAN_BASE ], (620,600), ri=0.015 ),
                        KeyCatcher( eBack, letter="q" )
                        ]
                        
        
        self.listControls = []
        y = 80
        self.listMaxLength = 7    
        for x in xrange(0,self.listMaxLength) :
            ctrl = LightControlRight( (-10,y), self.eSelect, "", imgs )
            ctrl.visible = False
            self.listControls.append( ctrl )
            y += 60
            
        self.setControls( controls+self.listControls )
        
        self.saveGameRoot = os.path.join( sys.path[0], "client", "saves" )
         
        self.saves = []   
        self.selectedSave = None
      #  self.reset( display, imgs )
        
    def eSelect( self, sender, (x,y) ):
        self.changeSelected( sender.uid )
       # print sender, sender.uid
       
    def fGetInformation( self, save, f ):
        save.getInformation( f )
        if save == self.selectedSave:
            self.changeSelected( save )
       
    def changeSelected( self, selected=None ):
        if not selected:
            selected = self.selectedSave
        self.selectedSave = selected
            
        if selected:
            if selected.loaded:
                if selected.valid:
                    self.selectedPath = selected.filepath
                    self.lblTitle.text = selected.title
                    self.lblDescription.text = selected.description
                    self.lblYear.text = selected.year
                    self.lblUsername.text = selected.username
                    
                    if selected.ship:
                        self.imgShip.img = self.imgs[ selected.ship ]
                    else:
                        self.imgShip.img = None
                    
                    if selected.timePlayed < 60:
                        self.lblTimePlayer.text = "%i sec"%selected.timePlayed
                    elif selected.timePlayed < 60*60:
                        self.lblTimePlayer.text = "%.1f min"%(selected.timePlayed/60.0)
                    else:
                        self.lblTimePlayer.text = "%.1f hours"%(selected.timePlayed/60.0/60)
                        
                        
                        
                    self.crtlLoad.enabled = True
                else:
                    self.lblTitle.text = "Invalid file"
                    self.lblDescription.text = ""
                    self.lblYear.text = ""
                    self.lblUsername.text = ""
                    self.lblTimePlayer.text = ""
                    self.imgShip.img = None
                    self.crtlLoad.enabled = False
            else:
                self.crtlLoad.enabled = False
                self.lblTitle.text = "Loading..."
                self.lblDescription.text = ""
                self.lblYear.text = ""
                self.lblUsername.text = ""
                self.lblTimePlayer.text = ""
                self.imgShip.img = None
                if not selected.loading:
                    selected.loading = True
                    f = open( selected.filepath, "r" )
                #    self.fGetInformation( selected, f )
                    t = Thread( target=self.fGetInformation, args=(selected,f) )
                    t.start()
         #   if selected.game:
         #   else:
         #       self.crtlLoad.enabled = False
        else:
            self.lblTitle.text = ""
            self.lblDescription.text = ""
            self.lblYear.text = ""
            self.lblUsername.text = ""
            self.lblTimePlayer.text = ""
            self.crtlLoad.enabled = False
        
    def reset( self, display, imgs ):
        ControlFrame.reset(self)
      #  selectCtrls = []
        
      #  y = 80
        filenames = filter( lambda name: len( name ) >= 5 and name[-5:] == ".game.pyfl", os.listdir(self.saveGameRoot) )
        filenames.sort()
        self.saves = [ Save( filename, os.path.join( self.saveGameRoot, filename ) ) for filename in filenames ]
     #   for filename in filenames:
      #      try:
      #          filepath =  os.path.join( self.saveGameRoot, filename )
      #          game = LoadGame(  )
      #      except Exceptions, ex:
                
        if self.saves:
            self.changeSelected( self.saves[0] )
            
       #     for filename in filenames:
       #         filepath =  os.path.join( self.saveGameRoot, filename )
       #         selectCtrls.append( LightControlRight( (-10,y), self.eSelect, filename, imgs, uid=filepath ) )
       #         y += 60
        #        print filepath
        else:
            self.changeSelected( None )
            
        self.changeList()
        
    def changeList( self, firstKey=0 ):
        self.firstKey = firstKey
        
        for k, save in zip( xrange(0,min(self.listMaxLength,len(self.saves))), 
                self.saves[ firstKey:min(firstKey+self.listMaxLength,len(self.saves)) ] ):
         #   filepath =  os.path.join( self.saveGameRoot, filename )
            self.listControls[ k ].text = save.filename
            self.listControls[ k ].uid = save
            self.listControls[ k ].visible = True
            
        for k in xrange( min(self.listMaxLength,len(self.saves)), self.listMaxLength ):
            self.listControls[ k ].visible = False
            
            
        self.ctrlListUp.enabled = self.firstKey
        self.ctrlListDown.enabled =  self.firstKey+self.listMaxLength < len(self.saves)
        
    def eListUp( self, sender, (x,y) ):
        self.changeList( self.firstKey-1 )
        
    def eListDown( self, sender, (x,y) ):
        self.changeList( self.firstKey+1 )
   
   # def manageInputs( self, display ):
   #     self.quit = ControlFrame.manageInputs( self, display ) or self.quit


