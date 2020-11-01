import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from mapa import Map
from student import valid_pushes

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

print(valid_pushes(mapa, map))

####
#-.#
#--###
#*@--#
#--$-#
#--###
####