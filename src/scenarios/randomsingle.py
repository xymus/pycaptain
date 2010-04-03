from scenarios.randommultiple import Randommultiple

class Randomsingle( Randommultiple ):
    title = "Random Single System"
    description = "A randomly generated scenario."
    year = 2544
    name = "Randomsingle"
    
    def __init__(self, game):

        Randommultiple.__init__(self, game, nSystems=1, 
                                            nPlanets=4, 
                                            nAsteroidFields=5 )

