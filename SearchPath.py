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
        sp_str = "["
        for p in self.pushes:
            sp_str+= str(p)
        return sp_str+"]"

    def __hash__(self):
        return hash(self.mapa.map)

## http://bomberman-aulas.ws.atnog.av.it.pt/table.html