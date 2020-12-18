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

    def __hash__(self):
        return hash(self.mapa)

    def __eq__(self, other):
        return self.mapa.__eq__(other.mapa)
