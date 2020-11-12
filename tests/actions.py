import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from mapa import Map
from path import *

mapa = Map("../levels/3.xsb")

map = mapa.__getstate__()

p = Path(mapa, map)

print(mapa)
print(mapa.keeper)
print(p.actions((3, 4)))



