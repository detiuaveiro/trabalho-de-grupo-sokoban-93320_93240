from mapa import Map
from consts import Tiles, TILES
import math

class SearchPath:

    def __init__(self, map):
        self._map = map
        self.path = []
    
    def pathBetween(self,initPos,finalPos):
        #descobrir como calcular o melhor caminho entre as duas posicoes do mapa 
        #return math.hypot(initPos, finalPos)
        pass

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
        x,y = move[0]

        p = self.pathBetween(mapa.keeper,move)

        ##apaga o keeper anterior
        if(mapa.get_tile((mapa.keeper)) == Tiles.MAN_ON_GOAL):
            mapa.set_tile((mapa.keeper),Tiles.GOAL)
        else:
            mapa.set_tile((mapa.keeper),Tiles.FLOOR)

        ##substitui a caixa pelo keeper 
        if(mapa.get_tile((x,y)) == Tiles.BOX_ON_GOAL):
            mapa.set_tile((x,y),Tiles.MAN_ON_GOAL)
        else:
            mapa.set_tile((x,y),Tiles.MAN)  
        
        ## nova posicao da caixa
        if move[1] == 'w': #up
            if(mapa.get_tile((x,y-1)) == Tiles.GOAL):
                mapa.set_tile((x,y-1),Tiles.BOX_ON_GOAL)
            else:
                mapa.set_tile((x,y-1),Tiles.BOX)
        elif move[1] == 'd': #right
            if(mapa.get_tile((x+1,y)) == Tiles.GOAL):
                mapa.set_tile((x+1,y),Tiles.BOX_ON_GOAL)
            else:
                mapa.set_tile((x+1,y),Tiles.BOX)      
        elif move[1] == 's':   #down
            if(mapa.get_tile((x,y+1)) == Tiles.GOAL):
                mapa.set_tile((x,y+1),Tiles.BOX_ON_GOAL)
            else:
                mapa.set_tile((x,y+1),Tiles.BOX)      
        elif move[1] == 'a':   #left
            if(mapa.get_tile((x-1,y)) == Tiles.GOAL):
                mapa.set_tile((x-1,y),Tiles.BOX_ON_GOAL)
            else:
                mapa.set_tile((x-1,y),Tiles.BOX)      

        self.path.append(move[1]) #p+move[1]  #DAR APPEND DO CAMINHO DO KEEPER ATE POSICAO DA CAIXA ANTERIOR+MOVE
        self._map = mapa.__getstate__()
        return 

    def get_mapa(self):
        return self._map

#TODO 's: MARIA: Fazer funcao pra escolher a box a dar pushes.. objetivo: provocar deadlocks pra excluir logo esses caminhos
#MSGS pra trocar com o server (hello) -> keep alive para podermos continuar o jogo sem q ele desconecte


## http://bomberman-aulas.ws.atnog.av.it.pt/table.html