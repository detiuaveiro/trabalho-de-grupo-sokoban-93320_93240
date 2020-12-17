import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from mapa import Map
from path import *
from SearchPath import *
from push import *
import time

mapa = Map("../levels/68.xsb")

print("nível 68:")
print(mapa)
print()
print("pmap comun a todos os estados deste mapa:")
print(mapa.str_pmap)
