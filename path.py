from tree_search import *
from consts import Tiles, TILES
import math

class Path(SearchDomain):
    # construtor
    def __init__(self, mapa, map):
        self.mapa = mapa            # mapa objecto
        self.map = map              # map string

    
    # state, estado -> coordenadas do keeper (x, y)
    # action, move -> 'w', 'a', ...

    # lista de accoes possiveis num estado
    # lista de available moves num determinado momento 
    def actions(self, currPos):
        x,y = currPos
        valid = []
        if self.mapa.get_tile((x+1,y)) not in [Tiles.BOX, Tiles.WALL, Tiles.BOX_ON_GOAL]:
            valid.append("d")
        if self.mapa.get_tile((x-1,y)) not in [Tiles.BOX, Tiles.WALL, Tiles.BOX_ON_GOAL]:
            valid.append("a")
        if self.mapa.get_tile((x,y+1)) not in [Tiles.BOX, Tiles.WALL, Tiles.BOX_ON_GOAL]:
            valid.append("s")
        if self.mapa.get_tile((x,y-1)) not in [Tiles.BOX, Tiles.WALL, Tiles.BOX_ON_GOAL]:
            valid.append("w")
        return valid

    # resultado de uma accao num estado, ou seja, o estado seguinte
    # coordenadas do estado seguinte, mediante a move
    def result(self, currPos, action):
        x, y = currPos
        if action == 'w':
            return (x, y - 1)
        elif action == 'a':
            return (x - 1, y)
        elif action == 's':
            return (x, y + 1)
        elif action == 'd':
            return (x + 1, y)
        print("erro em result função path")

    # custo de uma accao num estado
    # é sempre 1 supostamente
    def cost(self, currPos, action):
        return 1

    # custo estimado de chegar de um estado a outro
    # heuristic -> distância em linha reta do instante atual do kepper para o goal
    def heuristic(self, currPos, finalPos):
        x, y = currPos
        x1, y1 = finalPos
        return math.sqrt((y1 - y)**2 + (x1 - x)**2)

    # test if the given "goal" is satisfied in "state"
    # keeper postition == destination_goal
    def satisfies(self, currPos, finalPos):
        return currPos[0] == finalPos[0] and currPos[1] == finalPos[1]