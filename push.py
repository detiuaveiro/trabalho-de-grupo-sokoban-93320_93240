from tree_search import *
from consts import Tiles, TILES
import math
import copy
from SearchPath import *
from mapa import Map

past_states = set()

class Push(SearchDomain):
    # construtor
    def __init__(self):
        self.past_states = set()

    # state = instancia de SearchPath
    # action = pushes possíveis

    # lista de accoes possiveis num estado
    def actions(self, state):
        self.past_states.add(state) 
        boxes = state.mapa.filter_tiles([Tiles.BOX, Tiles.BOX_ON_GOAL])
        pushes = []
        aux = [Tiles.BOX, Tiles.BOX_ON_GOAL]
        aux1 = aux + [Tiles.WALL]
        #print(mapa.keeper)

        # print(state.mapa)
        # print(state.mapa.map)
        # print(state.mapa.aftiles)
        # print(state.mapa.smap)
        # print(state.mapa.aftiles)

        boxess = []

        aftiles = state.mapa.aftiles
        # print("--------------------------------------------------")
        # print(aftiles)
        # print("MAPA: ")
        # print(state.mapa)
        # print(state.mapa.str_smap)
        # print(aftiles)
        # print(state.mapa.filter_tiles([Tiles.BOX, Tiles.BOX_ON_GOAL]))

        for aft in aftiles:
            # print("aft: " + str(aft))
            # print("keeper: " + str(state.mapa.keeper))
            # print(state.mapa.str_smap)
            if state.mapa.keeper in aft:
                #print(boxes)
                for box in boxes:
                    # print("box")
                    # print(box)
                    adj_tiles = adjacent_coords(box)
                    # print("tiles")
                    # print(adj_tiles)
                    # print("----")
                    for adj in adj_tiles:
                        if adj in aft:
                            boxess.append((box, adj))
                break

        # print(boxess)

        for boxs in boxess:
            dir_s = get_direction(boxs[1], boxs[0])
            coords_tile2check = next_tile(boxs[0], dir_s)
            if not state.mapa.is_blocked(coords_tile2check, smap=True):
            # print(boxs)
            # print(dir_s)
                pushes.append((boxs[0], dir_s))
        
        aux = []
        for push in pushes:
            # print(state.mapa)
            newstate = self.result(state, push)
            if not newstate in self.past_states:
                if not is_deadlock(newstate.mapa):
                    self.past_states.add(newstate)
                    aux.append(push)
            #else:
                #print("encontrei um estado igual!")
        return aux

    # resultado de uma accao num estado, ou seja, o estado seguinte
    def result(self, state, action):
        # action[0] = coords da caixa
        # action[1] = direção do push
        mapa = copy.deepcopy(state.mapa)
        newSmap = copy.deepcopy(state.mapa.smap)
        mapa._smap = newSmap
        newpushes = copy.deepcopy(state.pushes)
        x,y = action[0] #coords da box
        # print("|||||||||||||||||||")
        # print(mapa)
        # print(mapa.str_smap)

        ##apaga o keeper anterior
        if(mapa.get_tile(mapa.keeper) == Tiles.MAN_ON_GOAL):
            mapa.clear_tile(mapa.keeper)
            mapa.set_tile(mapa.keeper,Tiles.GOAL)
        else:
            mapa.clear_tile(mapa.keeper)
            mapa.set_tile(mapa.keeper,Tiles.FLOOR)

        dir  = action[1]
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
        
        mapa.clear_tile(coords,smap=True)
        mapa.set_tile(coords,Tiles.WALL,smap=True)

        ##substitui a caixa pelo keeper 
        if(mapa.get_tile((x,y)) == Tiles.BOX_ON_GOAL):
            mapa.clear_tile((x,y))
            mapa.set_tile((x,y),Tiles.MAN_ON_GOAL)
        else:
            mapa.clear_tile((x,y))
            mapa.set_tile((x,y),Tiles.MAN)

        mapa.clear_tile((x,y),smap=True)
        mapa.set_tile((x,y),Tiles.FLOOR,smap=True)

        newpushes.append(action)

        return SearchPath(Map("", mapa=mapa.map, smap=mapa.smap), newpushes)

    # custo de uma accao num estado
    def cost(self, state, action):
        return len(state.mapa.empty_goals) # -> apartir do 60 [3000] SCORE (9, 807, 185, 6410, 0)
        # return 0 -> apartir do 60 [3000] SCORE (5, 457, 111, 4885, 0)




    # custo estimado de chegar de um estado a outro
    def heuristic(self, state, goal):
        boxes = state.mapa.filter_tiles(Tiles.BOX)
        goals = state.mapa.empty_goals
        dist = dict()
        
        for g in goals:
            min_dist = float("inf")
            box  = (0,0)
            for b in boxes:
                if b not in dist.keys():
                    d = abs(b[0]-g[0])+abs(b[1]-g[1])
                    if d < min_dist:
                        min_dist = d
                        box = b
            dist[box] = (min_dist,g)   
     
        return sum(n for _, n in dist)

    def satisfies(self, state, goal):
        return state.mapa.completed


def adjacent_tiles(mapa,pos):
    x, y = pos

    tl = mapa.get_tile((x - 1, y))
    tr = mapa.get_tile((x + 1, y))
    tu = mapa.get_tile((x, y - 1))
    td = mapa.get_tile((x, y + 1))

    # up, right, down, left
    return [tu, tr, td, tl]

def adjacent_coords(pos):
    x, y = pos
    # 0-> up, 1-> right, 2-> down, 3-> left, clockwise
    return [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]

def keeper_destination(move):
    x, y = move[0]
    if move[1] == 'w': #up
        keeperDest = (x, y + 1)      
    elif move[1] == 'd': #right
        keeperDest = (x - 1,y)
    elif move[1] == 's':   #down
        keeperDest = (x, y - 1)
    elif move[1] == 'a':   #left
        keeperDest = (x + 1,y)
    return keeperDest

def get_direction(c1, c2):
    if c1[0] < c2[0]:
        return 'd'
    elif c1[0] > c2[0]:
        return 'a'
    else:
        if c1[1] > c2[1]:
            return 'w'
        elif c1[1] < c2[1]:
            return 's'

def next_tile(box, dir):
    x, y = box
    if dir == 'w':
        return (x, y - 1)
    elif dir == 's':
        return (x, y + 1)
    elif dir == 'a':
        return (x - 1, y)
    elif dir == 'd':
        return (x + 1, y)

def is_deadlock(mapa):
    # boxes out goal
    bogs = mapa.filter_tiles([Tiles.BOX])
    boxes = mapa.filter_tiles([Tiles.BOX_ON_GOAL, Tiles.BOX])
    # print(boxes)

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
                # print("estou aqui!")
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

