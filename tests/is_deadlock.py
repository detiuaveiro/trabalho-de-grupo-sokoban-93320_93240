import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from mapa import Map
from student import is_deadlock

mapa = Map("../levels/1.xsb")

map = mapa.__getstate__()

print(is_deadlock(mapa, map))