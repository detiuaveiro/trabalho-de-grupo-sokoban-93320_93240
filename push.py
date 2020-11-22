from tree_search import *
from consts import Tiles, TILES
import math

class Push(SearchDomain):
    # construtor
    def __init__(self, mapa):
        pass

    # lista de accoes possiveis num estado
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    def heuristic(self, state, goal):
        pass

    # test if the given "goal" is satisfied in "state"
    def satisfies(self, state, goal):
        pass