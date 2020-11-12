from mapa import Map
import copy 
from consts import Tiles, TILES
import math
from path import *

import copy

class SearchPath:
    def __init__(self, map,path):
        self._map = map 
        self.path = path

    # move[0] = coordenadas da caixa
    # move[1] = direção do push
    def pathBetween(self,keeper,move,mapa):
        
        # keeper_dest is goal
        keeper_dest = keeper_destination(move)

        pathDomain = Path(mapa, self.map)

        p = SearchProblem(pathDomain, keeper, keeper_dest)

        t = SearchTree(p, 'a*')

        moves = decode_moves([t.search()])
        print(keeper)
        print(keeper_dest)

        for move in moves:
            self.path.append(move)
        return

    def __str__(self):
        sp_str = "["
        for m in self.path:
            sp_str+=m
        return sp_str+"]"
    
    @property
    def map(self):
        return self._map

    def updateMapa(self, mapa, move):
        #atualizar o mapa com a nova direçao q foi adicionada ao array path
        mapa.__setstate__(self._map)
        print("mapa que chega a UpdateMapa")
        print(mapa)
        x,y = move[0]

        # print(" aa ")
        # print(mapa.get_tile(mapa.keeper))
        # print(move[0])
        # print(mapa.get_tile(move[0]))

        self.pathBetween(mapa.keeper,move,mapa)

        ##apaga o keeper anterior
        if(mapa.get_tile(mapa.keeper) == Tiles.MAN_ON_GOAL):
            mapa.clear_tile(mapa.keeper)
            mapa.set_tile(mapa.keeper,Tiles.GOAL)
        else:
            mapa.clear_tile(mapa.keeper)
            mapa.set_tile(mapa.keeper,Tiles.FLOOR)
        
        ## nova posicao da caixa
        if move[1] == 'w': #up
            if(mapa.get_tile((x,y-1)) == Tiles.GOAL):
                mapa.clear_tile((x,y-1))
                mapa.set_tile((x,y-1),Tiles.BOX_ON_GOAL)
            else:
                mapa.clear_tile((x,y-1))
                mapa.set_tile((x,y-1),Tiles.BOX)
        elif move[1] == 'd': #right
            if(mapa.get_tile((x+1,y)) == Tiles.GOAL):
                mapa.clear_tile((x+1,y))
                mapa.set_tile((x+1,y),Tiles.BOX_ON_GOAL)
            else:
                mapa.clear_tile((x+1,y))
                mapa.set_tile((x+1,y),Tiles.BOX)      
        elif move[1] == 's':   #down
            if(mapa.get_tile((x,y+1)) == Tiles.GOAL):
                mapa.clear_tile((x,y+1))
                mapa.set_tile((x,y+1),Tiles.BOX_ON_GOAL)
            else:
                mapa.clear_tile((x,y+1))
                mapa.set_tile((x,y+1),Tiles.BOX)      
        elif move[1] == 'a':   #left
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
            
        self.path.append(move[1]) #p+move[1]  #DAR APPEND DO CAMINHO DO KEEPER ATE POSICAO DA CAIXA ANTERIOR+MOVE
        self._map = mapa.__getstate__()
        return 

    def get_mapa(self):
        return self._map

def keeper_destination(move):
    x, y = move[0]
    if move[1] == 'w': #up
        keeperDest = (x,y+1)      
    elif move[1] == 'd': #right
        keeperDest = (x+1,y)
    elif move[1] == 's':   #down
        keeperDest = (x,y-1)
    elif move[1] == 'a':   #left
        keeperDest = (x-1,y)
    return keeperDest


def decode_moves(lstates):
    moves = []
    for i in range(len(lstates) - 1):
        state = lstates[i]
        next_state = lstates[i + 1]

        if state[0] > next_state[0]:
            moves.append('d')
        elif state[0] < next_state[0]:
            moves.append('a')
        else:
            if state[1] < next_state[1]:
                moves.append('w')
            elif state[1] > next_state[1]:
                moves.append('s')
            else:
                print("decode_moves: erro")
    return moves


#TODO 's: MARIA: Fazer funcao pra escolher a box a dar pushes.. objetivo: provocar deadlocks pra excluir logo esses caminhos
#MSGS pra trocar com o server (hello) -> keep alive para podermos continuar o jogo sem q ele desconecte


## http://bomberman-aulas.ws.atnog.av.it.pt/table.html

## por discutir:
