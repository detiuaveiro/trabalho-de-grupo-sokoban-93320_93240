import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from mapa import Map
from student import valid_pushes
from SearchPath import *

# mapa = [
#     ["#", "#", "#", "#", "-", "-"]
#     ["#", "-", ".", "#", "-", "-"]
#     ["#", "-", "-", "#", "#", "#"]
#     ["#", "*", "@", "-", "-", "#"]
#     ["#", "-", "-", "$", "-", "#"]
#     ["#", "-", "-", "#", "#", "#"]
#     ["#", "#", "#", "#", "-", "-"]
# ]

mapa = Map("../levels/1.xsb")

map = mapa.__getstate__()

sb = SearchPath(map)

print(valid_pushes(mapa, map))

sb.updateMapa(mapa, ((1, 3), "w"))


print(valid_pushes(mapa, map))

####
#-.#
#--###
#*@--#
#--$-#
#--###
####