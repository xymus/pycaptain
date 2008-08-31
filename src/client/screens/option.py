from math import pi
import os
import sys

from . import Screen
from client.controls import *
from client.specialcontrols import *
from client.specialcontrols.option import *
from common import ids
from common import config
import languages

from client import displays

class OptionMenu( Screen ):
    def __init__(self, display, imgs, prefs, eSave=None, eCancel=None ):
        ControlFrame.__init__( self )
        
        self.eSaveOut = eSave
        self.crtlSave =     LightControlLeft( (260,550), self.eSave, _("Ok"), imgs )
        self.ctrlCancel =     LightControlRight( (600,550), eCancel, _("Cancel"), imgs )
        
        self.ctrlLanguages = Selector( (80, 80), display, imgs, _("Language"), [], eSelectedChanged=None )
        self.ctrlDisplay = Selector( (480, 80), display, imgs, _("Graphics"), [("sdl","pygame - SDL"),], eSelectedChanged=None ) # TODO add variable display list
        
        controls =   [  ImageHolder( imgs.splashBack, (0,0) ),
        
                        self.crtlSave,
                        self.ctrlCancel,
                        
                        self.ctrlLanguages,
                        self.ctrlDisplay,
                        
                        RotatingImageHolder( imgs[ ids.S_HUMAN_BASE ], (620,600), ri=0.015 ),
                        KeyCatcher( eCancel, letter="q" )
                        ]
        self.setControls( controls )
        
        self.reset( prefs )
        
    def eSave( self, sender, mousePos ):
        if self.eSaveOut:
            self.prefs.language = self.ctrlLanguages.selected
            self.prefs.display = self.ctrlDisplay.selected
            self.eSaveOut( sender, mousePos )
      
    def reset( self, prefs ):
    
        Screen.reset(self)
        self.prefs = prefs.shallowCopy()
        
        self.ctrlLanguages.items = []
        for language in languages.languagesNames:
            try:
                exec( "from languages.%s import %s as Language" % (language.lower(),language.capitalize()) )
                self.ctrlLanguages.items.append( (language, Language.title) )
            except:
                pass
                
        self.ctrlDisplay.items = []
        for display in displays.displayNames:
            try:
                exec( "from client.displays.%s import %s as Display" % (display.lower(),display.capitalize()) )
                self.ctrlDisplay.items.append( (display, Display.title) )
            except:
                pass
                
                
        
        self.ctrlLanguages.setDefault( self.prefs.language )
        self.ctrlDisplay.setDefault( self.prefs.display )
       # try:
       #     languageKey = 0
       #     for item in self.ctrlLanguages.items:
       #         if item[0] == self.prefs.language:
       #     languageKey = self.ctrlLanguages.items.index( self.prefs.language )
       #     self.ctrlLanguages.changeSelected( languageKey )
       # except ValueError:
       #     pass
        
