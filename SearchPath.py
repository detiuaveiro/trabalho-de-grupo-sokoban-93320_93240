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

# mapa = Map("levels/1.xsb")

# mapa2 = copy.deepcopy(mapa)

# sp1 = SearchPath(mapa, ['a', 'd'])
# sp2 = SearchPath(mapa, ['a', 'w'])
# sp3 = sp2
# sp4 = SearchPath(mapa2, ['a', 'd'])

# myset = set()
# num_set = set()

# print(hash('3'))
# print(hash('4'))

# num_set.add('3')
# num_set.add('3')
# num_set.add('4')

# print('3' in num_set)
# print('4' in num_set)

# print(num_set)

# print("hashes: ")
# print(hash(sp1))
# print(hash(sp2))
# print(hash(sp3))
# print(hash(sp4))

# print(sp1 in myset)



# myset.add(sp1)
# myset.add(sp2)
# myset.add(sp1)
# myset.add(sp2)
# myset.add(sp3)
# myset.add(sp4)

# print(sp1 in myset)
# print(sp3 in myset)

# # print(str(set(list(myset))))

# print(myset)