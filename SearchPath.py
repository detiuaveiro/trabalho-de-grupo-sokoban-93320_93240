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
        for m in self.path:
            sp_str+=m
        return sp_str+"]"

    def __hash__(self):
        return hash(self.mapa.map)
    
    @property
    def map(self):
        return self._map

    def updateMapa(self, mapa, push):
        #atualizar o mapa com a nova direçao q foi adicionada ao array path
        mapa.__setstate__(self._map)
        x,y = push[0][0] #coords da box
        for j in push[1]:
            self.path.append(j)   #pathBetween

        ##apaga o keeper anterior
        if(mapa.get_tile(mapa.keeper) == Tiles.MAN_ON_GOAL):
            mapa.clear_tile(mapa.keeper)
            mapa.set_tile(mapa.keeper,Tiles.GOAL)
        else:
            mapa.clear_tile(mapa.keeper)
            mapa.set_tile(mapa.keeper,Tiles.FLOOR)

        dir = push[0][1]
        
        # print("MOVE "+ str(push[0][1]))
        ## nova posicao da caixa
        if dir == 'w': #up
            coords = (x,y-1)
        elif dir == 'd': #right
            coords = (x+1,y)
        elif dir == 's':   #down
            coords = (x,y+1)
        elif dir == 'a':   #left
            coords = (x-1,y)

        if(mapa.get_tile(coords) == Tiles.GOAL):
            mapa.clear_tile(coords)
            mapa.set_tile(coords,Tiles.BOX_ON_GOAL)
        else:
            mapa.clear_tile(coords)
            mapa.set_tile(coords,Tiles.BOX)

        ##substitui a caixa pelo keeper 
        if(mapa.get_tile((x,y)) == Tiles.BOX_ON_GOAL):
            mapa.clear_tile((x,y))
            mapa.set_tile((x,y),Tiles.MAN_ON_GOAL)
        else:
            mapa.clear_tile((x,y))
            mapa.set_tile((x,y),Tiles.MAN)
            
        self.path.append(dir) 
        self._map = mapa.__getstate__()
        return 

## http://bomberman-aulas.ws.atnog.av.it.pt/table.html