"""Generic representation of the Game Map."""
import logging
from functools import reduce
from operator import add

from consts import Tiles, TILES

logger = logging.getLogger("Map")
logger.setLevel(logging.DEBUG)


class Map:
    """Representation of a Map."""

    def __init__(self, filename, mapa=None, smap=None):
        if mapa == None:
            mapa = []
        self._map = mapa
        self._level = filename
        self._keeper = None
        if smap == None:
            smap = []
        # simplified map
        self._smap = smap             # preciso _antes do atributo 

        #map, smap either are [] or both of them is vailid
        if self._map == []: 
            with open(filename, "r") as f:
                for line in f:
                    codedline = []
                    codedline_aux = []
                    for c in line.rstrip():
                        assert c in TILES, f"Invalid character '{c}' in map file"
                        tile = TILES[c]
                        tile_aux = tile
                        if tile_aux in [Tiles.MAN, Tiles.GOAL, Tiles.MAN_ON_GOAL]:
                            tile_aux = Tiles.FLOOR
                        elif tile_aux in [Tiles.BOX, Tiles.BOX_ON_GOAL]:
                            tile_aux = Tiles.WALL
                            
                        codedline.append(tile)
                        codedline_aux.append(tile_aux)

                    self._map.append(codedline)
                    self._smap.append(codedline_aux)

            self.hor_tiles, self.ver_tiles = (
                max([len(line) for line in self._map]),
                len(self._map),
            )  # X, Y

            # Add extra tiles to make the map a rectangule
            for y, line in enumerate(self._map):
                while len(line) < self.hor_tiles:
                    self._map[y].append(Tiles.FLOOR)
                    self._smap[y].append(Tiles.WALL)
        else:
            self.hor_tiles, self.ver_tiles = (
                max([len(line) for line in self._map]),
                len(self._map),
            )  # X, Y

        for line in self._smap:
            for i in range(len(line)):
                if line[i] == Tiles.WALL:
                    for y in range(0,i):
                        line[y] = Tiles.WALL
                    break
        
        # list of adjcent free tiles
        self.aftiles = self.generate_aftiles()


    def __str__(self):
        map_str = ""
        screen = {tile: symbol for symbol, tile in TILES.items()}
        for line in self._map:
            for tile in line:
                map_str += screen[tile]
            map_str += "\n"

        return map_str.strip()

    def __hash__(self):
        aux = list(map(lambda x: tuple(x), self.map))
        return hash(tuple(aux))

    def __eq__(self, other):
        return self.map == other.map

    def __getstate__(self):
        return self._map

    def __setstate__(self, state):
        self._map = state
        self._keeper = None
        self.hor_tiles, self.ver_tiles = (
            max([len(line) for line in self._map]),
            len(self._map),
        )  # X, Y

    @property
    def map(self):
        return self._map

    @property
    def smap(self):
        return self._smap

    @property
    def str_smap(self):
        map_str = ""
        screen = {tile: symbol for symbol, tile in TILES.items()}
        for line in self._smap:
            for tile in line:
                map_str += screen[tile]
            map_str += "\n"

        return map_str.strip()

    @property
    def size(self):
        """Size of map."""
        return self.hor_tiles, self.ver_tiles

    @property
    def completed(self):
        """Map is completed when there are no empty_goals!"""
        return self.empty_goals == []

    @property
    def on_goal(self):
        """Number of boxes on goal.

           Counts per line and counts all lines using reduce
        """
        return reduce(
            add,
            [
                reduce(lambda a, b: a + int(b is Tiles.BOX_ON_GOAL), l, 0)
                for l in self._map
            ],
        )

    def filter_tiles(self, list_to_filter, smap=False):
        """Util to retrieve list of coordinates of given tiles."""
        mapa = self._map
        if smap == True:
            mapa = self._smap
        return [
            (x, y)
            for y, l in enumerate(mapa)
            for x, tile in enumerate(l)
            if tile in list_to_filter
        ]

    @property
    def keeper(self):
        """Coordinates of the Keeper."""
        if self._keeper is None:
            self._keeper = self.filter_tiles([Tiles.MAN, Tiles.MAN_ON_GOAL])[0]

        return self._keeper

    @property
    def boxes(self):
        """List of coordinates of the boxes."""
        return self.filter_tiles([Tiles.BOX, Tiles.BOX_ON_GOAL])

    @property
    def empty_goals(self):
        """List of coordinates of the empty goals locations."""
        return self.filter_tiles([Tiles.GOAL, Tiles.MAN_ON_GOAL])

    def get_tile(self, pos):
        """Retrieve tile at position pos."""
        x, y = pos
        return self._map[y][x]

    def set_tile(self, pos, tile, smap=False):
        """Set the tile at position pos to tile."""
        mapa = self._map
        if smap == True:
            mapa = self._smap
        x, y = pos
        mapa[y][x] = (
            tile & 0b1110 | mapa[y][x]
        )  # the 0b1110 mask avoid carring ON_GOAL to new tiles

        if (
            tile & Tiles.MAN == Tiles.MAN
        ):  # hack to avoid continuous searching for keeper
            self._keeper = pos

    def clear_tile(self, pos, smap=False):
        """Remove mobile entity from pos."""
        mapa = self._map
        if smap == True:
            mapa = self._smap
        x, y = pos
        mapa[y][x] = mapa[y][x] & 0b1  # lesser bit carries ON_GOAL

    def is_blocked(self, pos, smap=False):
        """Determine if mobile entity can be placed at pos."""
        mapa = self._map
        if smap == True:
            mapa = self._smap
        x, y = pos
        if x not in range(self.hor_tiles) or y not in range(self.ver_tiles):
            logger.error("Position out of map")
            return True
        if self._map[y][x] in [Tiles.WALL]:
            logger.debug("Position is a wall")
            return True
        return False

    def generate_aftiles(self):
        ftiles = self.filter_tiles([Tiles.FLOOR], smap=True)
        aftiles = []
        saft = []

        while(1):
            if ftiles == []:
               break
            lst = []
            tile = ftiles.pop()

            adj_tiles = adjacent_coords(tile)
            
            for adj in adj_tiles:
                if adj in ftiles:

                    lst.append(adj)
                    ftiles.remove(adj)
            lst.append(tile)
            saft.append(lst)

        change_flag = 1

        while(change_flag):
            
            change_flag = 0
            for i in range(len(saft)):
                for j in range(i + 1, len(saft) - 1):
                    if aux(saft[i], saft[j]):
                        saft[i].extend(saft[j])
                        saft.remove(saft[j])
                        saft.append([])
                        change_flag = 1

        aftiles = saft
            
        aftiles = list(filter(lambda x: x != [], aftiles))

        return aftiles
        
def aux(l1, l2):
    for l in l1:
        adj_tiles = adjacent_coords(l)
        for ll in l2:
            if ll in adj_tiles:
                return True
    return False

def adjacent_coords(pos):
    x, y = pos
    # 0-> up, 1-> right, 2-> down, 3-> left, clockwise
    return [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]


if __name__ == "__main__":
    mapa = Map("levels/1.xsb")
    print(mapa)
    assert mapa.keeper == (11, 8)
    assert mapa.get_tile((4, 2)) == Tiles.WALL
    assert mapa.get_tile((5, 2)) == Tiles.BOX
    assert mapa.get_tile((2, 7)) == Tiles.BOX
    assert mapa.get_tile(mapa.keeper) == Tiles.MAN
    # Fake move:
    mapa.clear_tile(mapa.keeper)
    mapa.set_tile((16, 7), Tiles.MAN)
    mapa.clear_tile((12, 7))
    mapa.set_tile((17, 7), Tiles.BOX)
    assert mapa.keeper == (16, 7)
    assert mapa.get_tile((17, 7)) == Tiles.BOX_ON_GOAL
    assert mapa.on_goal == 1
    assert mapa.boxes == [(5, 2), (7, 3), (5, 4), (7, 4), (2, 7), (17, 7)]
