from if3_game.engine import init, Game, Layer
from game_objects import RESOLUTION, Spaceship, Asteroid



init (RESOLUTION, "Asteroid")

game = Game ()
game_layer = Layer()
game.add (game_layer) # ajoute la layer au game

spaceship = Spaceship ((400,300))

asteroid32 = Asteroid ()



game_layer.add (spaceship)
game_layer.add (asteroid32)


 # ajoute le spaceship à la layer qu'on a créée


 


#dernière ligne ONLY
game.run ()