from random import randint, random, choice
from math import pi, sin, cos, hypot, atan2

from common import config
from common import utils

class CommunicationManager:
    def __init__( self ):
        self.communications = []
        
    def addCommunication( self, game, communication ):
        self.communications.append( communication )
        if communication.sender:
            communication.sender.msgs.append( communication.getMessageArchived( game, communication.sender ) )
        
    def addWideBroadcast( self, game, player, text, ship=None ):
        if not ship:
            ship = player.flagship
        encryption = ship.cryptionStrength
        origin = ship.pos
        self.addCommunication( game, MessageActive( game, player, text, encryption=encryption, origin=origin ) )
     
    def addDirectedBroadcast( self, game, player, text, (x,y), ship=None ):
        if not ship:
            ship = player.flagship
        encryption = ship.cryptionStrength
        origin = ship.pos
        angle = utils.angleBetween( origin, (x,y) )
        dist = utils.distBetween( origin, (x,y) )
        radiusAtTarget = max( 100, min( 500,   dist/25   ) )
        angleCover = atan2( radiusAtTarget, dist )
       # origin = (origin[0]-1*cos(angle), origin[1]-1*cos(angle)) # overwrite to allow sender to receive message
       # print text, encryption, origin, angle, dist+radiusAtTarget, angleCover
        self.addCommunication( game, MessageActive( game, player, text, encryption=encryption, origin=origin, angle=angle, radius=dist+radiusAtTarget, angleCover=angleCover ) )
        
    def doTurn( self, game ):
        newList = []
        for communication in self.communications:
            communication.doTurn( game )
            if communication.alive:
                newList.append( communication )
        self.communications = newList

class MessageArchived:
    def __init__( self, sender, text, sentAt, receivedAt ):
        self.sender = sender
        self.text = text
        self.sentAt = sentAt
        self.receivedAt = receivedAt

class MessageActive:
    speed = 1000/config.fps
    overlap = 0.5
    angleCover = pi/20 # half
    pDegradation = 0.03
    
    pCryptSwitch = 0.3
    
    fullCharset = [ chr( o ) for o in range( ord("A"), ord("Z")+1 ) ] \
        + [ chr( o ) for o in range( ord("a"), ord("z")+1 ) ] # \
       # + [ chr( o ) for i in range( ord("0"), ord("9")+1 ) ]
    
    def __init__( self, game, sender, text, origin=None, radius=None, angle=None, angleCover=None, encryption=None ):
        self.sender = sender
        self.text = text
        self.sentAt = game.tick
        
        if encryption == None:
            self.encryption = self.sender.flagship.cryptionStrength
        else:
            self.encryption = encryption
            
        if not origin:
            self.origin = self.sender.flagship.pos
        else:
            self.origin = origin
            
        if not radius:
            self.maxRadius = 10000 #config.universeWidth/3
        else:
            self.maxRadius = radius
            
        if angleCover:
            self.angleCover = angleCover
            
        self.angle = angle
        self.radius = 0
     #   self.speed = 100/config.fps
        
        self.alive = True
        
    def doTurn( self, game ):
        oldRadius = self.radius
        self.radius += self.speed
        
        for player in game.players:
            if (player != self.sender or oldRadius != 0 ) \
               and player.flagship and player.flagship.alive: # ship listening
                    dist = utils.distBetween( self.origin, player.flagship.pos )
                    if dist < self.radius and dist >= oldRadius-self.overlap: # ship in area covered this turn
                        if self.angle:
                            angle = utils.angleBetween( self.origin, player.flagship.pos )
                            if player.name == "xymus":
                                print "Angle", angle > self.angle-self.angleCover, angle < self.angle+self.angleCover
                                print "Angles", self.angle-self.angleCover, angle, self.angle+self.angleCover
                            inAngle = angle > self.angle-self.angleCover and angle < self.angle+self.angleCover
                        else:
                            inAngle = True
                            
                        if inAngle:
                            player.msgs.append( self.getMessageArchived( game, player ) )
                            
        if self.radius > self.maxRadius*5:
            self.alive = False
        elif self.radius > self.maxRadius:
            # degrade message quality
            if random() < self.pDegradation: # *len(self.text): # probability
                if len( self.text ) == 1:
                    self.alive = False
                else:
                    posLost = randint( 0, len( self.text )-1 ) # pos to lose
                    self.text = self.text[:posLost]+self.text[posLost+1:]
    #    print "new text:", self.radius, self.text
    
    def getMessageArchived( self, game, player, ship=None ):
        if not ship:
            ship = player.flagship
            
        return MessageArchived( self.sender.name, 
            text=self.getHeardText( game, player,  ),
            sentAt=self.sentAt,
            receivedAt=game.tick )
                        
    def getHeardText( self, game, listener, decryption=0 ):
        if game.getRelationBetween( self.sender, listener ) <= 0: # TODO update to allies only, maybe
            # keys hidden from ennemies, handicap
            decryption = max( 0, decryption-1 )
            
        print "crypt", self.encryption, decryption
        if decryption >= self.encryption:
            return self.text
        else:
           # charset = [ chr(c) for c in filter( lambda c: chr(c) in self.text, range( 0,128 ) ) ]
           # if " " in charset:
           #     charset.remove( " " )
                
            scrambledText = self.text
            key = game.tick
            
            # variable to encryption strength
            for i in xrange( self.encryption-decryption ):
                # add random characters
               # charset += choice( self.fullCharset )
                
                # switch letters
                skipNext = False
                for p in xrange( 0, len( self.text )-1 ):
                    if skipNext:
                        skipNext = False
                    elif random() < self.pCryptSwitch:
                        scrambledText = scrambledText[:p] +scrambledText[ p+1 ]+scrambledText[ p ]+ scrambledText[p+2:]
                        skipNext = True
                
            # encryption, same to all strength
            # REMOVED because it made text too scrambled
           # rotatedText = ""
           # for c in scrambledText:
           #     if c in " ":
           #         newLetter = c
           #     else:
           #         newLetter = charset[ (charset.index( c )+game.tick)%len(charset) ]     
           #     rotatedText += newLetter
            
                
          #  scrambledText = #[ (c+key)%len(charset) for c in scrambledText ]
          #  print i, scrambledText, rotatedText
            return scrambledText # rotatedText
             
