from tree_search import *
from consts import Tiles, TILES
import math
import copy
from SearchPath import *

class Push(SearchDomain):
    # construtor
    def __init__(self, mapa):
        self.mapa

    # state = instancia de SearchPath
    # action = pushes possíveis

    # lista de accoes possiveis num estado
    def actions(self, state):
        boxes = state.mapa.filter_tiles([Tiles.BOX, Tiles.BOX_ON_GOAL])
        pushes = set()
        aux = [Tiles.BOX, Tiles.BOX_ON_GOAL, Tiles.WALL]
        #print(mapa.keeper)
        for box in boxes:
            adj_tiles = adjacent_tiles(state.mapa, box)
            if adj_tiles[0] not in aux:
                if adj_tiles[2] not in aux:
                    pushes.add((box, 's'))
            if adj_tiles[1] not in aux:
                if adj_tiles[3] not in aux:
                    pushes.add((box, 'd'))
            if adj_tiles[2] not in aux:
                if adj_tiles[0] not in aux:
                    pushes.add((box, 'w'))
            if adj_tiles[3] not in aux:
                if adj_tiles[1] not in aux:
                    pushes.add((box, 'a'))

        for push in pushes:
            newstate = self.result(state, push)
            if is_deadlock(newstate.mapa):
                pushes.remove(push)
        return list(pushes)

    # resultado de uma accao num estado, ou seja, o estado seguinte
    def result(self, state, action):
        # action[0] = coords da caixa
        # action[1] = direção do push
        mapa = copy.deepcopy(state.mapa)
        x,y = action[0] #coords da box

        ##apaga o keeper anterior
        if(mapa.get_tile(mapa.keeper) == Tiles.MAN_ON_GOAL):
            mapa.clear_tile(mapa.keeper)
            mapa.set_tile(mapa.keeper,Tiles.GOAL)
        else:
            mapa.clear_tile(mapa.keeper)
            mapa.set_tile(mapa.keeper,Tiles.FLOOR)

        if dir == 'w': #up
            coords = (x,y-1)
        elif dir == 'd': #right
            coords = (x+1,y)
        elif dir == 's':   #down
            coords = (x,y+1)
        elif dir == 'a':   #left
            coords = (x-1,y)

        ## desenha a caixa no sítio certo
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

        return SearchPath(mapa, state.pushes)

    # custo de uma accao num estado
    def cost(self, state, action):
        return 1

    # custo estimado de chegar de um estado a outro
    def heuristic(self, state, goal):
        x, y = state
        x1, y1 = goal
        return math.sqrt((y1 - y)**2 + (x1 - x)**2)

        # tentativa 1
        # boxes = state.mapa.filter_tiles(Tiles.BOX)
        # goals = state.mapa.empty_goals
        # distances = []
        
        # for box in boxes:
        #     for g in goals:
        #         distances.append(abs(box[0]-g[0])+abs(box[1]-g[1]))
        # return int(sum(distances) / len(distances)) if distances else 0

        #tentativa 2
            # # heuristics.add(box, float("inf"))
            # for g in state.mapa.filter_tiles(Tiles.GOAL):
            #     distance = abs(box[0]-g[0])+abs(box[1]-g[1])
            #     if g not in heuristics.keys():
            #         heuristics[g] =  distance
            #     else:
            #         if heuristics[g] >= distance:
            #             min_dist = distance 

    # test if the given "goal" is satisfied in "state"
    def satisfies(self, state, goal):
        return state.mapa.completed


def adjacent_tiles(mapa,pos):
    x, y = pos

    tl = mapa.get_tile((x - 1, y))
    tr = mapa.get_tile((x + 1, y))
    tu = mapa.get_tile((x, y - 1))
    td = mapa.get_tile((x, y + 1))

def is_deadlock(mapa):
    # boxes out goal
    bogs = mapa.filter_tiles([Tiles.BOX])
    boxes = mapa.filter_tiles([Tiles.BOX_ON_GOAL, Tiles.BOX])

    for bog in bogs:
        if mapa.is_blocked((bog[0] - 1, bog[1])) and mapa.is_blocked((bog[0], bog[1] - 1)) or \
        mapa.is_blocked((bog[0] + 1, bog[1])) and mapa.is_blocked((bog[0], bog[1] - 1)) or \
        mapa.is_blocked((bog[0] + 1, bog[1])) and mapa.is_blocked((bog[0], bog[1] + 1)) or \
        mapa.is_blocked((bog[0] - 1, bog[1])) and mapa.is_blocked((bog[0], bog[1] + 1)):
            return True

        tiles = adjacent_tiles(mapa, bog)
        coords = adjacent_coords(bog)

        boxes.remove(bog)

        for box in boxes:
            if box in coords:
                if box in [coords[0], coords[2]]:
                    if box in [coords[0]]:
                        if mapa.is_blocked((bog[0] - 1, bog[1])) and mapa.is_blocked((bog[0] - 1, bog[1] - 1)) or mapa.is_blocked((bog[0] + 1, bog[1])) and mapa.is_blocked((bog[0] + 1, bog[1] - 1)):
                            return True
                    else:
                        if mapa.is_blocked((bog[0] - 1, bog[1])) and mapa.is_blocked((bog[0] - 1, bog[1] + 1)) or mapa.is_blocked((bog[0] + 1, bog[1])) and mapa.is_blocked((bog[0] + 1, bog[1] + 1)):
                            return True
                else:
                    if box in [coords[3]]:
                        if mapa.is_blocked((bog[0], bog[1] - 1)) and mapa.is_blocked((bog[0] - 1, bog[1] - 1)) or mapa.is_blocked((bog[0], bog[1] + 1)) and mapa.is_blocked((bog[0] - 1, bog[1] + 1)):
                            return True
                    else:
                        if mapa.is_blocked((bog[0], bog[1] - 1)) and mapa.is_blocked((bog[0] + 1, bog[1] - 1)) or mapa.is_blocked((bog[0], bog[1] + 1)) and mapa.is_blocked((bog[0] + 1, bog[1] + 1)):
                            return True
    return False