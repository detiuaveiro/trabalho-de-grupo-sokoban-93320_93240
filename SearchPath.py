from mapa import Map
import copy 
from consts import Tiles, TILES
import math
from path import *
import sys

import copy

class SearchPath:
    def __init__(self, map,path):
        self._map = map 
        self.path = path

    def __str__(self):
        sp_str = "["
        for m in self.path:
            sp_str+=m
        return sp_str+"]"
    
    @property
    def map(self):
        return self._map

    def updateMapa(self, mapa, push):
        #atualizar o mapa com a nova direçao q foi adicionada ao array path
        mapa.__setstate__(self._map)
        # print("------------------im in UpdateMapa----------------")
        # print(mapa)
        # print("COORDS DA CAIXA: "+str(push[0][0]))
        # print("move:" + str(push[0][1]))
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
            if(mapa.get_tile((x,y-1)) == Tiles.GOAL):
                mapa.clear_tile((x,y-1))
                mapa.set_tile((x,y-1),Tiles.BOX_ON_GOAL)
            else:
                mapa.clear_tile((x,y-1))
                mapa.set_tile((x,y-1),Tiles.BOX)
        elif dir == 'd': #right
            if(mapa.get_tile((x+1,y)) == Tiles.GOAL):
                mapa.clear_tile((x+1,y))
                mapa.set_tile((x+1,y),Tiles.BOX_ON_GOAL)
            else:
                mapa.clear_tile((x+1,y))
                mapa.set_tile((x+1,y),Tiles.BOX)      
        elif dir == 's':   #down
            if(mapa.get_tile((x,y+1)) == Tiles.GOAL):
                mapa.clear_tile((x,y+1))
                mapa.set_tile((x,y+1),Tiles.BOX_ON_GOAL)
            else:
                mapa.clear_tile((x,y+1))
                mapa.set_tile((x,y+1),Tiles.BOX)      
        elif dir == 'a':   #left
            if(mapa.get_tile((x-1,y)) == Tiles.GOAL):
                mapa.clear_tile((x-1,y))
                mapa.set_tile((x-1,y),Tiles.BOX_ON_GOAL)
            else:
                mapa.clear_tile((x-1,y))
                mapa.set_tile((x-1,y),Tiles.BOX) 

        ##substitui a caixa pelo keeper 
        if(mapa.get_tile((x,y)) == Tiles.BOX_ON_GOAL):
            mapa.clear_tile((x,y))
            mapa.set_tile((x,y),Tiles.MAN_ON_GOAL)
        else:
            mapa.clear_tile((x,y))
            mapa.set_tile((x,y),Tiles.MAN)
            
        self.path.append(dir) #p+push[0][1]  #DAR APPEND DO CAMINHO DO KEEPER ATE POSICAO DA CAIXA ANTERIOR+MOVE
        # print("path so far: " + str(self.path))
        self._map = mapa.__getstate__()
        # print("mapa atualizado1: ")
        # print(mapa)
        # if self.path == ['s', 'a', 'w']:
        #     print(self.path)
        #     print('aqui2!')
            # sys.exit()
        return 

    def get_mapa(self):
        return self._map

## http://bomberman-aulas.ws.atnog.av.it.pt/table.html

## por discutir: