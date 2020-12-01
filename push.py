from tree_search import *
from consts import Tiles, TILES
import math
import copy
from SearchPath import *
from mapa import Map

class Push(SearchDomain):
    # construtor
    def __init__(self, m):
        self.m =  m

    # state = instancia de SearchPath
    # action = pushes possíveis

    # lista de accoes possiveis num estado
    def actions(self, state):
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
        # print(state.mapa.filter_tiles([Tiles.BOX, Tiles.BOX_ON_GOAL]))

        for aft in aftiles:
            # print("aft: " + str(aft))
            # print(state.mapa.keeper)
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
                            boxess.append(box)
                            break
            break

        #print(boxess)

        boxes = boxess
        for box in boxes:
            adj_tiles = adjacent_tiles(state.mapa, box)
            adj_coords = adjacent_coords(box)
            if not state.mapa.get_tile(adj_coords[0]) in aux1:
                if not state.mapa.is_blocked(adj_coords[2]) and adj_tiles[2] not in aux:
                    pushes.append((box, 's'))
            if not state.mapa.get_tile(adj_coords[1]) in aux1:
                if not state.mapa.is_blocked(adj_coords[3]) and adj_tiles[3] not in aux:
                    pushes.append((box, 'd'))
            if not state.mapa.get_tile(adj_coords[2]) in aux1:
                if not state.mapa.is_blocked(adj_coords[0]) and adj_tiles[0] not in aux:
                    pushes.append((box, 'w'))
            if not state.mapa.get_tile(adj_coords[3]) in aux1:
                if not state.mapa.is_blocked(adj_coords[1]) and adj_tiles[2] not in aux:
                    pushes.append((box, 'a'))
        
        
        aux = []
        for push in pushes: 
            newstate = self.result(state, push)
            if not is_deadlock(newstate.mapa):
                aux.append(push)


        # print(state.mapa)
        #print(aux)
        # exit(0)
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
        return 1

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
    return [tl, tr, tu,td]

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

# def unreachable(mapa, push):
#     xk, yk = mapa.keeper
#     xkd, ykd = keeper_destination(push)
#     box = push[0]

#     line_dir = get_line_dir(keeper_destination(push), box)
#     center = box
#     print("center: " + str(center))
#     size = mapa.size
#     print("size: " + str(size))
#     print("size[aux]: "+ str(size[aux]))
#     print("line dir: " + str(line_dir))

#     if line_dir == 'hor':
#         for i in range(center[aux], 0 , -1):
#             if not mapa.is_blocked((center[aux], i)) and mapa.get_tile((center[aux], i)) not in [Tiles.BOX, Tiles.BOX_ON_GOAL]:
#                 return False



#     for i in range(center[aux] - 1, 0 , -1):
#         print("i: " + str(i))
#         print("position_to_be_checked: " + str((center[opp(aux)], i)))
#         print("mapa.get_tile((center[aux], i))" + str(mapa.get_tile((center[aux], i))))
#         print("mapa.get_tile((center[aux], i)) not in [Tiles.Box]" + str(mapa.get_tile((center[aux], i)) not in [Tiles.BOX]))
#         if not mapa.is_blocked((center[aux], i)) and mapa.get_tile((center[aux], i)) not in [Tiles.BOX, Tiles.BOX_ON_GOAL]:
#             return False

#     for j in range(center[aux], size[aux]):
#         print(j)
#         if not mapa.is_blocked((center[aux], j)):
#             return False
#     return True

# def opp(aux):
#     if aux == 1:
#         return 0
#     return 1
    
    
# def get_line_dir(keeper, box):
#     x, y = keeper
#     x1, y1 = box
#     if x1 != x:
#         return 'ver'
#     elif y1 != y:
#         return 'hor'
    

