from mapa import Map
import copy 
from consts import Tiles, TILES
import math
from path import *
import sys

import copy

class SearchPath:
    def __init__(self, mapa, pushes):
        self.mapa = mapa
        self.pushes = pushes

    def __str__(self):
        return str(self.mapa)

    # def __repr__(self):
    #     return str(self.mapa)

    def __hash__(self):
        # print("hash em Search path")
        # print(self.mapa)
        return hash(self.mapa)

    def __eq__(self, other):
        return self.mapa.__eq__(other.mapa)

## http://bomberman-aulas.ws.atnog.av.it.pt/table.html
