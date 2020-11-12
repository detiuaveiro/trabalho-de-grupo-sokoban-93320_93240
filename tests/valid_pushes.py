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

print(mapa)

sb = SearchPath(map, [])

pushes = valid_pushes(mapa, map)

for push in pushes:
    print(push)

####
#-.#
#--###
#*@--#
#--$-#
#--###
####