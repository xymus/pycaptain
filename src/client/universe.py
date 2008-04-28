class Universe:
    def __init__(self):
        self.tick = 0
        self.astres = []
        self.gfxs = []
        self.players = []

    def doTurn( self ):
        removedGfx = []
        for gfx in self.gfxs:
            removedGfx = removedGfx + gfx.doTurn()

        for rg in removedGfx:
            self.gfxs.remove( rg )

    def getObjects( self, (cx,cy,cw,ch)):
        return self.astres


