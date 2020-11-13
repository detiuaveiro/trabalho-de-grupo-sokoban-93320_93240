import asyncio
import getpass
import json
import os

import websockets
from mapa import Map

#-----------
import random 

#temp-------
from consts import Tiles, TILES
import copy
from SearchPath import *
import math
from path import *

def adjacent_coords(pos):
    x, y = pos
    # 0-> up, 1-> right, 2-> down, 3-> left, clockwise
    return [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]

def complete(mapa, map):
    mapa.__setstate__(map)
    return mapa.completed

def adjacent_tiles(mapa,pos):
    x, y = pos

    tl = mapa.get_tile((x - 1, y))
    tr = mapa.get_tile((x + 1, y))
    tu = mapa.get_tile((x, y - 1))
    td = mapa.get_tile((x, y + 1))

    return [tu, tr, td, tl] # up, right, down, left, clockwise

def is_deadlock(mapa, map):
    # boxes out goal
    mapa.__setstate__(map)

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

# TODO: escolher as caixas: 2 hipoteses..1)distancia manhattan 2) caixa c + nº validPushes 1º e em caso de empate (distancia de manhattan)
# move[0] = coords da caixa
# move[1] = direção
# path -> pathBetween
def valid_pushes(mapa, map):
    mapa.__setstate__(map)
    boxes = mapa.filter_tiles([Tiles.BOX, Tiles.BOX_ON_GOAL])
    possible_pushes = []
    pushes = []
    aux = [Tiles.BOX, Tiles.BOX_ON_GOAL]
    aux1 = aux + [Tiles.WALL]
    #print(mapa.keeper)
    for box in boxes:
        adj_coords = adjacent_coords(box)
        adj_tiles = adjacent_tiles(mapa, box)
        if not mapa.get_tile(adj_coords[0]) in aux1:
            if not mapa.is_blocked(adj_coords[2]) and adj_tiles[2] not in aux:
                possible_pushes.append((box, 's'))
        if not mapa.get_tile(adj_coords[1]) in aux1:
            if not mapa.is_blocked(adj_coords[3]) and adj_tiles[3] not in aux:
                possible_pushes.append((box, 'd'))
        if not mapa.get_tile(adj_coords[2]) in aux1:
            if not mapa.is_blocked(adj_coords[0]) and adj_tiles[0] not in aux:
                possible_pushes.append((box, 'w'))
        if not mapa.get_tile(adj_coords[3]) in aux1:
            if not mapa.is_blocked(adj_coords[1]) and adj_tiles[2] not in aux:
                possible_pushes.append((box, 'a'))

    for push in possible_pushes:
        pathDomain = Path(mapa, map)
        keeper_dest = keeper_destination(push)
        p = SearchProblem(pathDomain, mapa.keeper, keeper_dest)
        t = SearchTree(p, 'a*')
        lstates = t.search(limit=20)
        if lstates is not None:
            path = decode_moves(lstates)
            pushes.append((push, path))
    return pushes

def print_paths(mapa, paths):
    i = 0
    for path in paths:
        print("num: "+ str(i))
        mapa.__setstate__(path.map)
        print(mapa)
        print(path)
        i += 1
        print("\n")

def keeper_destination(move):
    x, y = move[0]
    if move[1] == 'w': #up
        keeperDest = (x,y - 1)      
    elif move[1] == 'd': #right
        keeperDest = (x-1,y)
    elif move[1] == 's':   #down
        keeperDest = (x,y+1)
    elif move[1] == 'a':   #left
        keeperDest = (x+1,y)
    return keeperDest

def decode_moves(lstates):
    moves = []
    for i in range(len(lstates) - 1):
        state = lstates[i]
        next_state = lstates[i + 1]

        if state[0] < next_state[0]:
            moves.append('d')
        elif state[0] > next_state[0]:
            moves.append('a')
        else:
            if state[1] > next_state[1]:
                moves.append('w')
            elif state[1] < next_state[1]:
                moves.append('s')
            else:
                print("decode_moves: erro")
    return moves

def main():
    async def agent_loop(server_address="localhost:8001", agent_name="student"):
        async with websockets.connect(f"ws://{server_address}/player") as websocket:

            # Receive information about static game properties
            await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
            
            key = "s"

            while True:
                try:
                    update = json.loads(
                        await websocket.recv()
                    )  #-> receive game update, this must be called timely or your game will get out of sync with the server

                    if "map" in update:
                        # we got a new level
                        game_properties = update
                        mapa = Map(update["map"])
                        print(mapa)
                    else:
                        # we got a current map state update
                        state = update
                        paths = []

                        ## mapa em str
                        map = mapa.__getstate__()
                        pushes = valid_pushes(mapa, map)
                        for push in pushes:
                            sp = SearchPath(copy.deepcopy(map),[])
                            sp.updateMapa(mapa, push)
                            paths.append(sp)
                            #print("Push")
                            #print(push)
                            #print("Path")
                            #print(sp.path)
                            #print("!!!!!!!")
                            #print(mapa)
                            #print_paths(mapa, paths)
                        
                        ## problema: ele dá este print várias vezes

                        ## justificação:
                        # ele chega à resposta (AQUI), dá break e sai e volta a correr o algoritmo para o mesmo mapa,
                        # pk nós não mandamos o suposto caminho de resolução do nível(AQUI2)

                        #AQUI -> ele chega à resposta bué facilmente pk eu fiz bué cagada no valid pushes, tenho de corrigir (Pedro)
                        # AQUI2 -> o print do caminho quando ele deteta que o mapa está completo é apenas 1 move, ou seja, que temos de fazre uma deepcopy
                        # não só do sp.map com dp sp.path, (que no fundo corresponde a fazer deepcopy de tudo)
                        print("eu estou aqui e começei de novo!")

                        while not len(paths) == 0:
                            print("checkpoint! mapa a que se deu pop:")

                            spi = paths.pop(0)
                            
                            mapa.__setstate__(spi.map)
                            #print(mapa)
                            #print("***********")
                            
                            #msg para keep alive temos q manter isto a funcionar (tens de interromper em menos de 100 ms se nao n tens tempo de processar as cenas e receber as mensagens a tempo????)
                            update = json.loads(await websocket.recv())                              
                            
                            #currentMap = maps.pop(0)  

                            if complete(mapa, spi.map):
                                print("MAPA CORRETO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                print(mapa)
                                print("path para a resolução: "+str(spi.path))
                                print("SUPOSTO FIM !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                                break
                            else:
                                if is_deadlock(mapa, spi.map):
                                    print("este mapa tem deadlock!")
                                    continue
                                else:
                                    pushes = valid_pushes(mapa, spi.map)
                                    # print(".......")
                                    for push in pushes:
                                        aux  = copy.deepcopy(spi)
                                        # print(mapa)
                                        #print("-----------")
                                        # print(mapa)
                                        # print("////////////")
                                        #print(push)
                                        # print("AUX: ")
                                        # print(aux.map)
                                        # print(aux.path)
                                        sp = SearchPath(aux.map, aux.path) 
                                        sp.updateMapa(mapa, push)
                                        paths.append(sp)
                                        #print("AFTER PUSH ----------")
                                        #print(mapa)
                                        #print_paths(mapa, paths)
                                
                        # print("\n")
                        #print(Map(f"levels/{state['level']}.xsb"))

                    await websocket.send(
                        json.dumps({"cmd": "key", "key": key})
                    )  # send key command to server - you must implement this send in the AI agent
                    # break
                except websockets.exceptions.ConnectionClosedOK:
                    print("Server has cleanly disconnected us")
                    return

                # # Next line is not needed for AI agent
                # pygame.display.flip()

                


    # DO NOT CHANGE THE LINES BELLOW
    # You can change the default values using the command line, example:
    # $ NAME='arrumador' python3 client.py
    loop = asyncio.get_event_loop()
    SERVER = os.environ.get("SERVER", "localhost")
    PORT = os.environ.get("PORT", "8001")
    NAME = os.environ.get("NAME", getpass.getuser())
    loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))


# ----
if __name__ == "__main__":
    main()

## ------------------------------------------##----------------------------------##----------------------------

# from consts import Tiles, TILES
# import copy
# from mapa import Map

# #temp----------
# import gc       # consider using garbage collector


# def solution(mapa):

#     print(mapa)

#     return dfs(mapa)



# def dfs(mapa):
    
#     maps = []
#     paths = []

#     moves = (valid_moves(mapa, "//"))

#     # print("moves iniciais: " + str (moves))

#     for move in moves:
#         paths.append(move)
#         m1 = copy.deepcopy(mapa)

#         m2 = update_map(m1, move)

#         maps.append(m2)

#     print("paths iniciais: " + str(paths))
#     print("maps iniciais: " + str(maps))
 
        
#     assert len(paths) == len(maps)

#     # print("\nentrada no ciclo while\n")

#     while not len(paths) == 0:
#         # mapa rotacional
#         mapa_rot = maps.pop(0)

#         # print("type de mapa_rot: " + str(type(mapa_rot)))
#         # print("\ncontexto de mapa atual_início de ciclo: \n" + str(mapa_rot))

#         if mapa_rot.completed:
#             print("crates on place!")
#             break
#         else:
#             # fazer stack.pop() para obter o próximo caminho possível, e carrega-lo na variável path p.e.
#             path = paths.pop(0)

#             if is_deadlock(mapa_rot):
#                 # print("deadlock")
#                 continue
#             else:

#                 # print("path: " + str(path))
#                 moves = valid_moves(mapa_rot, path[len(path) - 1])

#                 # print("available moves: " + str(moves) + " for path: " + str(path))

#                 mapa_aux = None

#                 for move in moves:
#                     # print("move2add: " + str(move))
#                     path_aux = path + move
#                     # print("path_aux: " + str(path_aux))
#                     paths.append(path_aux)

#                     mapa_aux_2 = copy.deepcopy(mapa_rot)

#                     mapa_aux = update_map(mapa_aux_2, move)

#                     # print("id-> " + str(id(mapa_aux)))

#                     # print("contexto do mapa atualizado_ao_fazer_append_das_moves: \n"+ str(mapa_aux))

#                     maps.append(mapa_aux)

#     # path encontrado
#     print(path)
#     return path       

        
# def is_deadlock(mapa):
#     # boxes out goal
#     bogs = mapa.filter_tiles([Tiles.BOX])
#     boxes = mapa.filter_tiles([Tiles.BOX_ON_GOAL, Tiles.BOX])

#     for bog in bogs:
#         if mapa.is_blocked((bog[0] - 1, bog[1])) and mapa.is_blocked((bog[0], bog[1] - 1)) or \
#         mapa.is_blocked((bog[0] + 1, bog[1])) and mapa.is_blocked((bog[0], bog[1] - 1)) or \
#         mapa.is_blocked((bog[0] + 1, bog[1])) and mapa.is_blocked((bog[0], bog[1] + 1)) or \
#         mapa.is_blocked((bog[0] - 1, bog[1])) and mapa.is_blocked((bog[0], bog[1] + 1)):
#             return True

#         tiles = adjacent_tiles(mapa, bog)
#         coords = adjacent_coords(bog)

#         boxes.remove(bog)

#         for box in boxes:
#             if box in coords:
#                 if box in [coords[0], coords[2]]:
#                     if box in [coords[0]]:
#                         if mapa.is_blocked((bog[0] - 1, bog[1])) and mapa.is_blocked((bog[0] - 1, bog[1] - 1)) or mapa.is_blocked((bog[0] + 1, bog[1])) and mapa.is_blocked((bog[0] + 1, bog[1] - 1)):
#                             return True
#                     else:
#                         if mapa.is_blocked((bog[0] - 1, bog[1])) and mapa.is_blocked((bog[0] - 1, bog[1] + 1)) or mapa.is_blocked((bog[0] + 1, bog[1])) and mapa.is_blocked((bog[0] + 1, bog[1] + 1)):
#                             return True
#                 else:
#                     if box in [coords[3]]:
#                         if mapa.is_blocked((bog[0], bog[1] - 1)) and mapa.is_blocked((bog[0] - 1, bog[1] - 1)) or mapa.is_blocked((bog[0], bog[1] + 1)) and mapa.is_blocked((bog[0] - 1, bog[1] + 1)):
#                             return True
#                     else:
#                         if mapa.is_blocked((bog[0], bog[1] - 1)) and mapa.is_blocked((bog[0] + 1, bog[1] - 1)) or mapa.is_blocked((bog[0], bog[1] + 1)) and mapa.is_blocked((bog[0] + 1, bog[1] + 1)):
#                             return True
#     return False

# def valid_moves(mapa, last_move):
#     moves = []
#     keeper = mapa.keeper

#     tiles = adjacent_tiles(mapa, keeper)

#     coords = adjacent_coords(keeper)

#     for i in range(0, 4):
#         if not tiles[i] == Tiles.FLOOR  and not tiles[i] == Tiles.GOAL:
#             if tiles[i] in [Tiles.BOX, Tiles.BOX_ON_GOAL]:
#                 if i == 0:
#                     if not mapa.is_blocked((keeper[0], keeper[1] - 2)):
#                         moves.append(["w"])
#                 elif i == 1:
#                     if not mapa.is_blocked((keeper[0] + 2, keeper[1])):
#                         moves.append(["d"])
#                 elif i == 2:
#                     if not mapa.is_blocked((keeper[0], keeper[1] + 2)):
#                         moves.append(["s"])
#                 else:
#                     if not mapa.is_blocked((keeper[0] - 2, keeper[1])):
#                         moves.append(["a"])
#         else:
#             moves.append([direction(i)])

#     if not last_move == "//":
#         if not len(moves) == 1:
#             moves.remove([opposite(last_move)])
#             return moves

#     assert not len(moves) == 0, "moves is empty!"

#     return moves

# def adjacent_tiles(mapa,pos):
#     x, y = pos

#     tl = mapa.get_tile((x - 1, y))
#     tr = mapa.get_tile((x + 1, y))
#     tu = mapa.get_tile((x, y - 1))
#     td = mapa.get_tile((x, y + 1))

#     return [tu, tr, td, tl] # up, right, down, left, clockwise

# def adjacent_coords(pos):
#     x, y = pos
#     # 0-> up, 1-> right, 2-> down, 3-> left, clockwise
#     return [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]

# def direction(number):

#     assert number < 4
#     if number == 0:
#         return "w"      # up
#     elif number == 1:
#         return "d"      # right
#     elif number == 2:
#         return "s"      # down
#     else:   
#         return "a"      # left

# def update_map(mapa, move):

#     tile = Tiles.FLOOR

#     keeper = mapa.keeper

#     # keeper | to_move | move_to

#     to_move = ()
#     move_to = ()

#     if move == ["w"]:
#         tile = mapa.get_tile((keeper[0], keeper[1] - 1))
#         to_move = (keeper[0], keeper[1] - 1)
#         move_to = (keeper[0], keeper[1] - 2)
#     elif move == ["d"]:
#         tile = mapa.get_tile((keeper[0] + 1, keeper[1]))
#         to_move = (keeper[0] + 1, keeper[1])
#         move_to = (keeper[0] + 2, keeper[1])
#     elif move == ["s"]:
#         tile = mapa.get_tile((keeper[0], keeper[1] + 1))
#         to_move = (keeper[0], keeper[1] + 1)
#         move_to = (keeper[0], keeper[1] + 2)
#     else:
#         tile = mapa.get_tile((keeper[0] - 1, keeper[1]))
#         to_move = (keeper[0] - 1, keeper[1])
#         move_to = (keeper[0] - 2, keeper[1])

#     # print(move)
#     # print("tile- >" + str(tile))
#     # print(to_move)
    
#     # tile is crate or crate_on_goal
#     if tile in [Tiles.BOX_ON_GOAL, Tiles.BOX]:

#         flag_move_to_goal = mapa.get_tile(move_to) == Tiles.GOAL
#         flag_to_move_crate_on_goal = tile == Tiles.BOX_ON_GOAL
            
#         # clear crate
#         mapa.clear_tile(to_move)

#         # set move_to to crate
#         mapa.set_tile(move_to, (Tiles.BOX_ON_GOAL if flag_move_to_goal else Tiles.BOX))

#         # clear keeper
#         mapa.clear_tile(keeper)

#         # set keeper
#         mapa.set_tile(to_move, (Tiles.MAN_ON_GOAL if flag_to_move_crate_on_goal else Tiles.MAN))
#         mapa._keeper = to_move
#     else:

#         # move the keeper, 1st clear it, then represent it again

#         # clear keeper
#         mapa.clear_tile(keeper)

#         flag_to_move_goal = tile == Tiles.GOAL

#         mapa.set_tile(to_move, (Tiles.MAN_ON_GOAL if flag_to_move_goal else Tiles.MAN))
#         mapa._keeper = to_move

#     # print(mapa)


#     return mapa


# def opposite(last_move):
#     if last_move == "w":
#         return "s"
#     elif last_move == "s":
#         return "w"
#     elif last_move == "a":
#         return "d"
#     else:
#         return "a"
    

    


            



        
    