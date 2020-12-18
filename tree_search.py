import asyncio
import mapa
import bisect

# Module: tree_search
# 
# This module provides a set o classes for automated
# problem solving through tree search:
#    SearchDomain  - problem domains
#    SearchProblem - concrete problems to be solved
#    SearchNode    - search tree nodes
#    SearchTree    - search tree with the necessary methods for searhing
#
#  (c) Luis Seabra Lopes
#  Introducao a Inteligencia Artificial, 2012-2019,
#  Inteligência Artificial, 2014-2019

from abc import ABC, abstractmethod

# Dominios de pesquisa
# Permitem calcular
# as accoes possiveis em cada estado, etc
class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state, goal):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal
    def goal_test(self, state):
        return self.domain.satisfies(state,self.goal)

# Nos de uma arvore de pesquisa
class SearchNode:  
    def __init__(self,state,parent): 
        self.state = state
        self.parent = parent
        self.depth = self.parent.depth + 1 if self.parent != None else 0     # 1.2
        self.cost = 0   # 1.7
        self.heuristic = 0
    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + ")"
    def __repr__(self):
        return str(self)
    def __hash__(self):
        return hash(self.state)
    def __eq__(self, other):
        if other == None:
            return False
        return self.state == other.state
    def __gt__(self,other):
        return sorter_astar(self) > sorter_astar(other)
    def __lt__(self,other):
        return sorter_astar(self) < sorter_astar(other)

# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self,problem): 
        self.problem = problem
        root = SearchNode(problem.initial, None)
        self.open_nodes = [root]
        self.length = 0
        self.cost = 0       # 1.9

    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self,node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return (path)

    # procurar a solucao
    async def search(self, limit = None, sleep=True):
        while self.open_nodes != []:
            # if sleep:
            await asyncio.sleep(0)
            node = self.open_nodes.pop(0)
            if self.problem.goal_test(node.state):
                return self.get_path(node)

            #lnewnodes = []
            for newstate in self.problem.domain.actions(node.state):
                newnode = SearchNode(newstate,node)
                newnode.cost = node.cost + 1
                newnode.heuristic = self.problem.domain.heuristic(newnode.state, self.problem.goal)
                bisect.insort(self.open_nodes,newnode)
        return None

def sorter_astar(item):
    return item.cost + item.heuristic




            




