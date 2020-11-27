import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from mapa import Map
from push import unreachable
from consts import Tiles


mapa = Map("../levels/1.xsb")

print(mapa)

print(unreachable(mapa, ((1,3), 'w')))

mapa.clear_tile((3,3))

mapa.set_tile((3, 3), Tiles.BOX)

print(mapa)
print(mapa.get_tile((3, 3)))

print(unreachable(mapa, ((3, 4), 'a')))