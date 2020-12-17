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
smap1 = copy.deepcopy(mapa.smap)
print("--- %s seconds ---" % (time.time() - start_time))

start_time2 = time.time()
smap2 = [x[:] for x in mapa.smap]
print("--- %s seconds ---" % (time.time() - start_time2))

mapa.smap[1][1] = Tiles.WALL
smap2[4][4] = Tiles.MAN

print(mapa.smap)
print(smap2)