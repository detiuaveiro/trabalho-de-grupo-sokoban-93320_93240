from tree_search import *

class Path(SearchDomain):
    # construtor
    def __init__(self, mapa, map):
        self.mapa = mapa            # mapa objecto
        self.map = map              # map string

    
    # state, estado -> coordenadas do keeper (x, y)
    # action, move -> 'w', 'a', ...

    # lista de accoes possiveis num estado
    # lista de available moves num determinado momento 
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    # coordenadas do estado seguinte, mediante a move
    def result(self, state, action):
        x, y = state
        if action == "w":
            return (x, y - 1)
        elif action == 'a':
            return (x - 1, y)
        elif action == 's':
            return (x, y + 1)
        elif action == 'd':
            return (x + 1, y)
        print("erro em result função path")

    # custo de uma accao num estado
    # é sempre 1 supostamente
    def cost(self, state, action):
        return 1

    # custo estimado de chegar de um estado a outro
    # heuristic -> distância em linha reta do instante atual do kepper para o goal
    def heuristic(self, state, goal):
        pass

    # test if the given "goal" is satisfied in "state"
    # keeper postition == destination_goal
    def satisfies(self, state, goal):
        return state[0] == goal[0] and state[1] == goal[1]