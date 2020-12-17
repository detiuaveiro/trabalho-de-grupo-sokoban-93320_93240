import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from mapa import Map
from path import *
from SearchPath import *
from push import *
import time

mapa = Map("../levels/1.xsb")

start_time = time.time()

mapa_obj = copy.deepcopy(mapa)

mapa.set_tile((1,1), Tiles.WALL)

print("--- %s seconds ---" % (time.time() - start_time))

start_time2 = time.time()

mapa_str = [x[:] for x in mapa.map]
smap_str = [x[:] for x in mapa.smap]

mapa_str[1][1] = Tiles.WALL

mapa_obj2 = Map("", mapa= mapa_str, smap=smap_str)

print("--- %s seconds ---" % (time.time() - start_time2))
