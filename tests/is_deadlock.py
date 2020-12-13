import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from mapa import Map
from student import is_deadlock
from consts import *

mapa = Map("../levels/68.xsb")
print(mapa)
mapa.set_tile((3, 2), Tiles.BOX)
print(mapa)

print(is_deadlock(mapa))