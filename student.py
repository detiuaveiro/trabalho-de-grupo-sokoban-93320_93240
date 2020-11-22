import asyncio
import getpass
import json
import os

import websockets
from mapa import Map 

#temp-------
from consts import Tiles, TILES
import copy
from SearchPath import *
import math
from path import *
import sys
from push import *

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
        # print("-----------------im in valid_pushes---------------")
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
        # print("mapa.keeper na função valid_pushes: " + str(mapa.keeper))
        # print(mapa)
        p = SearchProblem(pathDomain, mapa.keeper, keeper_dest)
        t = SearchTree(p, 'a*')
        lstates = t.search(limit=20)
        if lstates is not None:
            path = decode_moves(lstates)
            if path == ['d', 's', 'a']:
                sys.exit()
            pushes.append((push, path))
    return pushes

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

def get_mapa_goal(mapa):
    pass

    # await asyncio.sleep(0)

def main():
    async def solver(puzzle, solution):
        while True:
            game_properties = await puzzle.get()
            mapa = Map(game_properties["map"])
            #print(mapa)

            push = Push(mapa)
            p = SearchProblem(push, mapa.__getstate__(), get_mapa_goal(mapa))
            t = SearchTree(p, 'breadth')

            ## juntar os caminhos

            # keys = t.search()
            # await solution.put(''.join(keys))
            


    async def agent_loop(puzzle,solution, server_address="localhost:8000", agent_name="student"):
        async with websockets.connect(f"ws://{server_address}/player") as websocket:

            # Receive information about static game properties
            await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
            
            while True:
                try:
                    update = json.loads(
                        await websocket.recv()
                    )  #-> receive game update, this must be called timely or your game will get out of sync with the server

                    if "map" in update:
                        # we got a new level
                        game_properties = update
                        keys = ""
                        await puzzle.put(game_properties)

                    if not solution.empty():    #temos uma solucao
                        keys = await solution.get()             

                    key=""
                    if len(keys):
                        key =  keys[0]  #vai buscar o primeiro move da solucao pra enviar *
                        keys = keys[1:]  #atualiza as keys sem o primeiro move ja enviado para o servidor

                    await websocket.send(
                        json.dumps({"cmd": "key", "key": key}) # aqui envia a key*
                    )  # send key command to server - you must implement this send in the AI agent

                except websockets.exceptions.ConnectionClosedOK:
                    print("Server has cleanly disconnected us")
                    return                


    # DO NOT CHANGE THE LINES BELLOW
    # You can change the default values using the command line, example:
    # $ NAME='arrumador' python3 client.py
    loop = asyncio.get_event_loop()
    SERVER = os.environ.get("SERVER", "localhost")
    PORT = os.environ.get("PORT", "8000")
    NAME = os.environ.get("NAME", getpass.getuser())

    puzzle = asyncio.Queue(loop=loop)
    solution = asyncio.Queue(loop=loop)

    net_task = loop.create_task(agent_loop(puzzle, solution, f"{SERVER}:{PORT}", NAME))
    solver_task = loop.create_task(solver(puzzle, solution))

    loop.run_until_complete(asyncio.gather(net_task, solver_task))
    loop.close()


# ----
if __name__ == "__main__":
    main()
    