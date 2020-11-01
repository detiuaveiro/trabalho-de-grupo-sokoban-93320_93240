from mapa import Map
from consts import Tiles, TILES

## NOTA: POR TESTAR

class SearchPath:

    def __init__(self, map):
        self.map = map
        self.path = []
    
    def updateMapa(self, mapa, move):
        #atualizar o mapa com a nova direçao q foi adicionada ao array path
        mapa.__setstate__(self.map)
        x,y = move[0]

        p = pathBetween(mapa._keeper,coord)

        ##apaga o keeper anterior
        if(mapa.get_tile(mapa._keeper) == Tiles.MAN_ON_GOAL)
            mapa.set_tile(mapa.keeper) = Tiles.GOAL
        else:
            mapa.set_tile = Tiles.FLOOR

        ##substitui a caixa pelo keeper 
        if(mapa.get_tile(coord) == Tiles.BOX_ON_GOAL)
            mapa.set_tile(coord,Tiles.MAN_ON_GOAL)
        else:
            mapa.set_tile(coord,Tiles.MAN)  
        
        switch(move[1]):
            ## nova posicao da caixa
            case 'w':   #up
                if(mapa.get_tile(x,y-1) == Tiles.GOAL)
                    mapa.set_tile((x,y-1),Tiles.BOX_ON_GOAL)
                else:
                    mapa.set_tile((x,y-1)),Tiles.BOX)             
            case 'd':   #right
                if(mapa.get_tile(x+1,y) == Tiles.GOAL)
                    mapa.set_tile((x+1,y),Tiles.BOX_ON_GOAL)
                else:
                    mapa.set_tile((x+1,y)),Tiles.BOX)      
            case 's':   #down
                    mapa.set_tile((x-1,y),Tiles.BOX_ON_GOAL)
                else:
                    mapa.set_tile((x-1,y)),Tiles.BOX)
                if(mapa.get_tile(x,y+1) == Tiles.GOAL)
                    mapa.set_tile((x,y+1),Tiles.BOX_ON_GOAL)
                else:
                    mapa.set_tile((x,y+1)),Tiles.BOX)      
            case 'a':   #left
                if(mapa.get_tile(x-1,y) == Tiles.GOAL)
                    mapa.set_tile((x-1,y),Tiles.BOX_ON_GOAL)
                else:
                    mapa.set_tile((x-1,y)),Tiles.BOX)    
            default:
                pass        

        self.path.append(p+move[1])   #DAR APPEND DO CAMINHO DO KEEPER ATE POSICAO DA CAIXA ANTERIOR+MOVE
        self.map = mapa.__getstate__()
        return 

    def pathBetween(initPos,finalPos):
            #descobrir como calcular o melhor caminho entre as duas posicoes do mapa 
        return []

#TODO 's: MARIA: Fazer funcao pra escolher a box a dar pushes.. objetivo: provocar deadlocks pra excluir logo esses caminhos
#MSGS pra trocar com o server (hello) -> keep alive para podermos continuar o jogo sem q ele desconecte
