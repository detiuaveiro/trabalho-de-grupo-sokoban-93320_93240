from mapa import Map
import copy 
from consts import Tiles, TILES
import math
from path import *

import copy

class SearchPath:
    def __init__(self, map):
        self._map = copy.deepcopy(map)
        self.path = []

    # move[0] = coordenadas da caixa
    # move[1] = direção do push
    def pathBetween(self,keeper,move,mapa):

        # keeper_dest is goal
        keeper_dest = keeper_destination(move)

        path = Path(mapa, self.map)

        p = SearchProblem(path, keeper, keeper_dest)

        t = SearchTree(p, 'a*')

        print t
        
        return t

        # x,y = move[0]
        # dirs = []
        # #print(keeper)
        # #destino do keeper
        # if move[1] == 'w': #up
        #     keeperDest = (x,y+1)      
        # elif move[1] == 'd': #right
        #     keeperDest = (x+1,y)
        # elif move[1] == 's':   #down
        #     keeperDest = (x,y-1)
        # elif move[1] == 'a':   #left
        #     keeperDest = (x-1,y)
        # #print(keeperDest)
        # #print("........")
        
        # # xdest < xi
        # while True:
        #     print("teste1")
        #     if keeperDest == keeper:
        #         break
        #     elif keeperDest[0] == keeper[0]:  #se x ta bem mudar y
        #         if keeperDest[1] > keeper[1]:
        #             #print(mapa.get_tile((keeper[0], keeper[1]+1)))
        #             if mapa.get_tile((keeper[0], keeper[1]+1)) not in (Tiles.BOX, Tiles.BOX_ON_GOAL, Tiles.WALL):
        #                 #print(keeper[0], keeper[1]+1)
        #                 dirs.append('s')
        #                 keeper = (keeper[0], keeper[1]+1)
        #         else:
        #             #print(mapa.get_tile((keeper[0], keeper[1]-1)))
        #             if mapa.get_tile((keeper[0], keeper[1]-1)) not in (Tiles.BOX, Tiles.BOX_ON_GOAL, Tiles.WALL):
        #                 #print(keeper[0], keeper[1]-1)
        #                 dirs.append('w')
        #                 keeper = (keeper[0], keeper[1]-1)
        #     elif keeperDest[1] == keeper[1]:
        #         if keeperDest[0] < keeper[0]:
        #             #print(mapa.get_tile((keeper[0]-1, keeper[1])))
        #             if mapa.get_tile((keeper[0]-1, keeper[1])) not in (Tiles.BOX, Tiles.BOX_ON_GOAL, Tiles.WALL):
        #                 #print(keeper[0]-1, keeper[1])
        #                 dirs.append('a')
        #                 keeper = (keeper[0]-1, keeper[1])
        #         else:
        #             #print(mapa.get_tile((keeper[0]+1, keeper[1])))
        #             if mapa.get_tile((keeper[0]+1, keeper[1])) not in (Tiles.BOX, Tiles.BOX_ON_GOAL, Tiles.WALL):
        #                 #print(keeper[0]+1, keeper[1])
        #                 dirs.append('d')
        #                 keeper = (keeper[0]+1, keeper[1])

        #     elif keeperDest[0] < keeper[0]:
        #         #print(mapa.get_tile((keeper[0]-1, keeper[1])))
        #         if mapa.get_tile((keeper[0]-1, keeper[1])) not in (Tiles.BOX, Tiles.BOX_ON_GOAL, Tiles.WALL):
        #             #print(keeper[0]-1, keeper[1])
        #             dirs.append('a')
        #             keeper = (keeper[0]-1, keeper[1])
        #         else:   #se n pode começar a mover para o lado certo tem q mover para cima/baixo
        #             if keeperDest[1] > keeper[1]:
        #                 #print(mapa.get_tile((keeper[0], keeper[1]+1)))
        #                 if mapa.get_tile((keeper[0], keeper[1]+1)) not in (Tiles.BOX, Tiles.BOX_ON_GOAL, Tiles.WALL):
        #                     #print(keeper[0], keeper[1]+1)
        #                     dirs.append('s')
        #                     keeper = (keeper[0], keeper[1]+1)
        #             else:
        #                 #print(mapa.get_tile((keeper[0], keeper[1]-1)))
        #                 if mapa.get_tile((keeper[0], keeper[1]-1)) not in (Tiles.BOX, Tiles.BOX_ON_GOAL, Tiles.WALL):
        #                     #print(keeper[0], keeper[1]-1)
        #                     dirs.append('w')
        #                     keeper = (keeper[0], keeper[1]-1)
        #     #se nao consegue mover pra cima/baixo, nem para o lado suposto deve 
        #     elif keeperDest[0] > keeper[0]:
        #         #print(mapa.get_tile((keeper[0]+1, keeper[1])))
        #         if mapa.get_tile((keeper[0]+1, keeper[1])) not in (Tiles.BOX, Tiles.BOX_ON_GOAL, Tiles.WALL):
        #             #print(keeper[0]+1, keeper[1])
        #             dirs.append('d')
        #             keeper = (keeper[0]+1, keeper[1])
        #         else:   #se n pode começar a mover para os lados tem q mover para cima/baixo
        #             if keeperDest[1] < keeper[1]:
        #                 #print(mapa.get_tile((keeper[0], keeper[1]-1)))
        #                 if mapa.get_tile((keeper[0], keeper[1]-1)) not in (Tiles.BOX, Tiles.BOX_ON_GOAL, Tiles.WALL):
        #                     #print(keeper[0], keeper[1]-1)
        #                     dirs.append('w')
        #                     keeper = (keeper[0], keeper[1]-1)
        #                 else:
        #                     if mapa.get_tile((keeper[0], keeper[1]+1)) not in (Tiles.BOX, Tiles.BOX_ON_GOAL, Tiles.WALL):
        #                         #print(keeper[0], keeper[1]+1)
        #                         dirs.append('s')
        #                         keeper = (keeper[0], keeper[1]+1)
        
        # #print(" ---- ")
        # #print(keeper)
        # print("caminho do keeper: ")
        # print(dirs)
        # #print(move)
        # return dirs

    # def a_star_search(graph: WeightedGraph, start: Location, goal: Location):
    #     frontier = PriorityQueue()
    #     frontier.put(start, 0)
    #     came_from: Dict[Location, Optional[Location]] = {}
    #     cost_so_far: Dict[Location, float] = {}
    #     came_from[start] = None
    #     cost_so_far[start] = 0
        
    #     while not frontier.empty():
    #         current: Location = frontier.get()
            
    #         if current == goal:
    #             break
            
    #         for next in graph.neighbors(current):
    #             new_cost = cost_so_far[current] + graph.cost(current, next)
    #             if next not in cost_so_far or new_cost < cost_so_far[next]:
    #                 cost_so_far[next] = new_cost
    #                 priority = new_cost + heuristic(next, goal)
    #                 frontier.put(next, priority)
    #                 came_from[next] = current
        
    #     return came_from, cost_so_far

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
        print(mapa)
        x,y = move[0]

        print("teste")

        # print(" aa ")
        # print(mapa.get_tile(mapa.keeper))
        # print(move[0])
        # print(mapa.get_tile(move[0]))

        p = self.pathBetween(mapa.keeper,move,mapa)

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
        if(mapa.get_tile(move[0]) == Tiles.BOX_ON_GOAL):
            mapa.clear_tile(move[0])
            mapa.set_tile(move[0],Tiles.MAN_ON_GOAL)
        else:
            mapa.clear_tile(move[0])
            mapa.set_tile((x,y),Tiles.MAN)
            
        self.path.append(move[1]) #p+move[1]  #DAR APPEND DO CAMINHO DO KEEPER ATE POSICAO DA CAIXA ANTERIOR+MOVE
        self._map = mapa.__getstate__()
        return 

    def get_mapa(self):
        return self._map

def keeper_destination(move):
    if move[1] == 'w': #up
        keeperDest = (x,y+1)      
    elif move[1] == 'd': #right
        keeperDest = (x+1,y)
    elif move[1] == 's':   #down
        keeperDest = (x,y-1)
    elif move[1] == 'a':   #left
        keeperDest = (x-1,y)
    return keeperDest

#TODO 's: MARIA: Fazer funcao pra escolher a box a dar pushes.. objetivo: provocar deadlocks pra excluir logo esses caminhos
#MSGS pra trocar com o server (hello) -> keep alive para podermos continuar o jogo sem q ele desconecte


## http://bomberman-aulas.ws.atnog.av.it.pt/table.html