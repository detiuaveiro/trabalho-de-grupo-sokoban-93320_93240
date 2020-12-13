import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from mapa import Map
from consts import Tiles, TILES
import copy

mapa = Map("../levels/1.xsb")

print("mapa1")
print(mapa)
print("smap")
print(mapa.str_smap)
print("pmap")
print(mapa.str_pmap)

mapa2 = Map("", mapa=copy.deepcopy(mapa.map), smap=mapa.smap, pmap=mapa._pmap)

print("mapa1")
print(mapa2)
print("smap")
print(mapa2.str_smap)
print("pmap")
print(mapa2.str_pmap)



# print(mapa2.smap)

# print(mapa2.str_smap)

# print(mapa2.filter_tiles([Tiles.FLOOR], smap=True))


# mapa.set_tile((1, 1), Tiles.WALL)
# print(mapa)
# print(mapa.map)
# print(mapa.str_smap)
# print(mapa.aftiles)
# print(mapa2)
# print(mapa2.map)
# print(mapa2.str_smap)
# print(mapa2.aftiles)
