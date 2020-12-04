import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from mapa import Map
from consts import Tiles, TILES
import copy


mapa = Map("../levels/19.xsb")
print(mapa)
print(mapa.str_smap)
print(mapa.keeper)
print("mapa.aftiles: " + str(mapa.aftiles))