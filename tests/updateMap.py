import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from mapa import Map
from student import *
from SearchPath import *

mapa = Map("../levels/1.xsb")

print(mapa)

map = mapa.__getstate__()

sb = SearchPath(map)

print(sb.map)
print("teste")

print("boxes at: " + str(mapa.filter_tiles([Tiles.BOX, Tiles.BOX_ON_GOAL])))

sb.updateMapa(mapa, ((1, 3), "w"))

mapa.__setstate__(sb.map)

print(mapa)

sb.updateMapa(mapa, ((1,2), "w"))

print_single_path(sb.map)