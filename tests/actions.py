import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from mapa import Map
from path import *
from SearchPath import *
from push import *

mapa = Map("../levels/12.xsb")

sp = SearchPath(mapa, [])

p = Push(sp.mapa)

print(p.actions(sp))