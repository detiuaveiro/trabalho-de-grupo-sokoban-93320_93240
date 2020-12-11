import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from mapa import Map
from path import *
from SearchPath import *
from push import *
import time

start_time = time.time()

mapa = Map("../levels/1.xsb")

# tiles = copy.deepcopy(mapa.map)

# tiles[5][1] = Tiles.WALL
# tiles[5][2] = Tiles.WALL

# print(tiles)



mapa2 = Map("", mapa=copy.deepcopy(mapa.map), smap=mapa.smap)


mapa.set_tile((1, 1), Tiles.WALL)
mapa.set_tile((1, 2), Tiles.WALL)

print(mapa)
print(mapa2)

print("--- %s seconds ---" % (time.time() - start_time))