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
    async def solver(puzzle, solution):
        while True:
            game_properties = await puzzle.get()
            mapa = Map(game_properties["map"])
            print(mapa)
            percurso = []

            push = Push()
            sp = SearchPath(mapa, [])
            p = SearchProblem(push, sp, None)
            t = SearchTree(p, 'new')

            ## juntar os caminhos
            keys = await t.search()
            for i in range(len(keys)-1):
                # print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
                # print(keys[i].mapa)
                # print(keys[i].mapa.str_smap)
                # print("next move: " + str(keys[i+1].pushes[len(keys[i+1].pushes)-1]))
                # print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
                pathDomain = Path(keys[i].mapa, keys[i].mapa.map)
                p = SearchProblem(pathDomain, keys[i].mapa.keeper, keeper_destination(keys[i+1].pushes[len(keys[i+1].pushes)-1]))
                t = SearchTree(p, 'new')
                lstates = await t.search(sleep=False)
                if lstates is not None:
                    percurso.extend(decode_moves(lstates))
                percurso.append(keys[i+1].pushes[len(keys[i+1].pushes)-1][1])

            print(percurso)
            await solution.put(''.join(percurso))
            


    async def agent_loop(puzzle,solution, server_address="localhost:8001", agent_name="student"):
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
                    sys.exit()
                    return                


    # DO NOT CHANGE THE LINES BELLOW
    # You can change the default values using the command line, example:
    # $ NAME='arrumador' python3 client.py
    loop = asyncio.get_event_loop()
    SERVER = os.environ.get("SERVER", "localhost")
    PORT = os.environ.get("PORT", "8001")
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
    