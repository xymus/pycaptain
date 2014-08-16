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
        
        self.ctrlLanguages = Selector( (40, 40), display, imgs, _("Language"), [], eSelectedChanged=None )
        self.ctrlDisplay = Selector( (360, 40), display, imgs, _("Graphics"), [], eSelectedChanged=None )
        self.ctrlResolution = Selector( (360, 280), display, imgs, _("Resolution"), [("800x600","800x600"),("1024x768","1024x768"),("1280x800","1280x800"),], eSelectedChanged=None )
        self.ctrlFullscreen = Selector( (40, 280), display, imgs, _("Window mode"), [("True","Fullscreen"),("False","Windowed"),], eSelectedChanged=None )
        self.ctrlVolume = Selector( (680, 40), display, imgs, _("Sound volume"), [("0",_("mute")),]+[ (str(v), str(v)+_("%")) for v in xrange( 5, 101, 5 ) ], eSelectedChanged=None )
        
        controls =   [  ImageHolder( imgs.splashBack, (0,0), fillScreen=True ),
        
                        self.crtlSave,
                        self.ctrlCancel,
                        
                        self.ctrlLanguages,
                        self.ctrlDisplay,
                        self.ctrlResolution,
                        self.ctrlFullscreen,
                        self.ctrlVolume,
                        
                        RotatingImageHolder( imgs[ ids.S_HUMAN_BASE ], (620,600), ri=0.015 ),
                        KeyCatcher( eCancel, letter="q" )
                        ]
        self.setControls( controls )
        
        self.reset( prefs )
        
    def eSave( self, sender, mousePos ):
        if self.eSaveOut:
            self.prefs.language = self.ctrlLanguages.selected
            self.prefs.display = self.ctrlDisplay.selected
            self.prefs.resolution = self.ctrlResolution.selected
            self.prefs.fullscreen = self.ctrlFullscreen.selected
            self.prefs.volume = self.ctrlVolume.selected
            self.eSaveOut( sender, mousePos )
      
    def reset( self, prefs ):
    
        Screen.reset(self)
        self.prefs = prefs.shallowCopy()
        
        self.ctrlLanguages.items = []
        for language in languages.languagesNames:
            try:
                exec( "from languages.%s import %s as Language" % (language.lower(),language.capitalize()) )
                self.ctrlLanguages.items.append( (language, Language.title) )
            except Exception as e:
                print "failed to load language %s: %s" % (language,e)
                
        self.ctrlDisplay.items = []
        for display in displays.displayNames:
            try:
                exec( "from client.displays.%s import %s as Display" % (display.lower(),display.capitalize()) )
                self.ctrlDisplay.items.append( (display, Display.title) )
            except Exception as e:
                print "failed to load display %s: %s" % (display,e)
        
        self.ctrlLanguages.setDefault( self.prefs.language )
        self.ctrlDisplay.setDefault( self.prefs.display )
        self.ctrlResolution.setDefault( self.prefs.resolution )
        self.ctrlFullscreen.setDefault( self.prefs.fullscreen )
        self.ctrlVolume.setDefault( self.prefs.volume )
       # try:
       #     languageKey = 0
       #     for item in self.ctrlLanguages.items:
       #         if item[0] == self.prefs.language:
       #     languageKey = self.ctrlLanguages.items.index( self.prefs.language )
       #     self.ctrlLanguages.changeSelected( languageKey )
       # except ValueError:
       #     pass
        
