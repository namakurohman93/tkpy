import math
import dataclasses
from typing import Any

from .models import ImmutableDataclass


def cell_id(x, y):
    """ :func:`cell_id` will convert :class:`int` x and :class:`int` y
    into cell id that understand for TK.

    :param x: - :class:`int` x cell's coordinate.
    :param y: - :class:`int` y cell's coordinate.

    return: :class:`int`
    """
    return (536887296 + x) + (y * 32768)


def reverse_id(vid):
    """ :func:`reverse_id` will convert cell id into x, y tuple coordinate
    that read able for human.

    :param vid: - :class:`int` cell id

    return: :class:`tuple`
    """
    binary = f"{vid:b}"
    if len(binary) < 30:
        binary = "0" + binary
    xcord, ycord = binary[15:], binary[:15]
    realx = int(xcord, 2) - 16384
    realy = int(ycord, 2) - 16384
    return realx, realy


regionIds = {
    cell_id(x, y): [
        cell_id(xx, yy)
        for xx in range(0 + (x * 7), 7 + (x * 7))
        for yy in range(0 + (y * 7), 7 + (y * 7))
    ]
    for x in range(-13, 14)
    for y in range(-13, 14)
}


@dataclasses.dataclass(frozen=True)
class Point:
    """ :class:`Point` is a class that provide an easy way to organize
    coordinate.
    In addition, it can calculate the distance between :class:`Point`.
    And it accept :class:`list`, :class:`tupel` and :class:`dict`.

    Usage:
        >>> c1 = Point(0, 0)
        >>> c2 = Point(0, 1)
        >>> c1
        Point(x=0, y=0)
        >>> c1 >> c2
        1.0
        >>> c1 >> (0, 1)
        1.0
        >>> c1 >> [0, 1]
        1.0
        >>> c1 >> {'x': 0, 'y': 1}
        1.0
    """

    __slots__ = ["x", "y"]
    x: int
    y: int

    def __rrshift__(self, other):
        return self.__rshift__(other)

    def __rshift__(self, other):
        if isinstance(other, Point):
            return self.distance_to(other.x, other.y)
        elif isinstance(other, (tuple, list)):
            return self.distance_to(other[0], other[1])
        elif isinstance(other, dict):
            return self.distance_to(other["x"], other["y"])
        raise TypeError(
            f"unsupported operand type(s) for >>: '{type(self).__name__}' and '{type(other)}'"
        )

    def __dir__(self):
        return [d for d in object.__dir__(self) if not d.startswith("_")]

    @classmethod
    def from_cell_id(cls, id):
        """ :meth:`from_cell_id` instantiate :class:`Point` using cell id
        as argument.

        return: :class:`Point`
        """
        return cls(*reverse_id(int(id)))

    @property
    def id(self):
        return cell_id(self.x, self.y)

    def distance_to(self, x, y):
        """ Calculate distance between two points.

        return :class:`float`
        """
        return math.sqrt(pow(self.x - x, 2) + pow(self.y - y, 2))


class Map:
    """ :class:`Map` is represent of map object for TK. Map data from TK
    is stored in here. This class provide an easy way to access map data
    by using :meth:`coordinate` for accessing specific cell based on their
    coordinate, or using :property:`villages` for yield cell that contains
    village data on it, or by using another property.

    Usage::
        >>> m = Map(driver)
        >>> m.pull()
        >>> m.coordinate(0, 0)
        <Cell({'id': '536887296', 'landscape': '9013', 'owner': '0'})>
        >>> villages = list(m.villages)
    """

    def __init__(self, client):
        self.client = client
        self._cell = dict()
        self._players = Players()
        self._kingdoms = dict()

    def __repr__(self):
        return f"<{type(self).__name__}(cell={len(self._cell)}, player={len(self._players.item)}, kingdom={len(self._kingdoms)})>"

    def __dir__(self):
        return [*filter(lambda d: d.startswith('_'), dir(Map))]

    def _create_index(self, response):
        for c in response:
            try:
                for region_id in response[c]['region']:
                    for cell in response[c]['region'][region_id]:
                        self._cell[int(cell['id'])] = Cell(
                            client=self.client,
                            data=cell
                        )
                for player_id in response[c]['player']:
                    player = Player(
                        id=player_id,
                        client=self.client,
                        data=response[c]['player'][player_id]
                    )
                    name = response[c]['player'][player_id]['name']
                    self._players.insert(
                        player_id=player_id,
                        player_name=name,
                        player=player
                    )
                for kingdom_id in response[c]['kingdom']:
                    self._kingdoms[int(kingdom_id)] = Kingdom(
                        id=kingdom_id,
                        data=response[c]['kingdom'][kingdom_id]
                    )
            except:
                continue

    def pull(self, region_id=[]):
        """ :meth:`pull` for pulling map data from TK. If `region_id`
        specified, it will pull specific region data from TK.

        :param region_id: - :class:`list` (optional) list of region id
                            that want to requested to TK. Default: []
        """
        if region_id:
            ids = (x for x in list(range(1, len(region_id) // 49 + 2)))
            req_list = {
                str(id): [region_id.pop() for _ in range(49) if region_id]
                for id in ids
            }
        else:
            req_list = {'1': list(regionIds.keys())}

        r = self.client.map.getByRegionIds({
            'regionIdCollection': req_list
        })
        self._create_index(r['response'])

    @property
    def cell(self):
        """ :property:`cell` is a :func:`generator` that yield :class:`Cell`
        object.

        yield: :class:`Cell`
        """
        for cell in self._cell.values():
            yield cell

    @property
    def villages(self):
        """ :property:`villages` is a :func:`generator` that yield :class:`Cell`
        that have 'village' data on it.

        yield: :class:`Cell`
        """
        for cell in self.cell:
            if "village" in cell:
                yield cell
            else:
                continue

    @property
    def tiles(self):
        """ :property:`tiles` is a :func:`generator that yield :class:`Cell`
        known as Abandoned valley in game.

        yield: :class:`Cell`
        """
        for cell in self.cell:
            if "village" not in cell and "resType" in cell:
                yield cell
            else:
                continue

    @property
    def oasis(self):
        """ :property:`oasis` is a :func:`generator` that yield :class:`Cell`
        that have 'oasis' data on it.

        yield: :class:`Cell`
        """
        for cell in self.cell:
            if "oasis" in cell:
                yield cell
            else:
                continue

    @property
    def wilderness(self):
        """ :property:`wilderness` is a :func:`generator` that yield :class:`Cell`
        alsow know as Wilderness in game.

        yield: :class:`Cell`
        """
        for cell in self.cell:
            if "oasis" not in cell and "resType" not in cell:
                yield cell
            else:
                continue

    def coordinate(self, x, y, default={}):
        """ :meth:`coordinate` is used for find specific :cell:`Cell` object
        based on cell's coordinate.

        :param x: - :class:`int` x cell's coordinate.
        :param y: - :class:`int` y cell's coordinate.
        :param default: - :class:`dict` (optional) default value if :cell:`Cell`
                          object didnt' found. Default: {}

        return: :class:`Cell`
        """
        try:
            return self.hash_table[cell_id(x, y)]
        except:
            return default

    def tile(self, id, default={}):
        """ :meth:`tile` is used for find specific :cell:`Cell` object
        based on cell's id.

        :param id: - :class:`int` cell id.
        :param default: - :class:`dict` (optional) default value if :cell:`Cell`
                          object didn't found. Default: {}

        return: :class:`Cell`
        """
        try:
            return self.hash_table[int(id)]
        except:
            return default

    @property
    def kingdoms(self):
        """ :property:`kingdoms` is a :func:`generator` that yield :class:`Kingdom`
        object.

        yield: :class:`Kingdom`
        """
        for kingdom in self._kingdoms.values():
            yield kingdom

    @property
    def players(self):
        """ :property:`players` is a :func:`generator` that yield
        :class:`Player` object.
        yield: :class:`Player`
        """
        for player in self._players.item.values():
            yield player

    def player(self, name=None, id=None, default={}):
        """ :meth:`player` is used for find :class:`Player` object
        used player name or id.

        :param id: - :class:`int` player's id.
        :param default: - :class:`dict` (optional) default value when
                          :class:`Player` object not found. Default: {}

        return: :class:`Player`
        """
        return self._players.get(
            player_name=name, player_id=id, default=default
        )


class Players:
    def __init__(self):
        self.item = dict()
        self.players_name = dict()

    def insert(self, player_id, player_name, player):
        self.item[player_id] = player
        self.players_name[player_name] = self.item[player_id]

    def get(self, player_id=None, player_name=None, default={}):
        try:
            if player_id:
                return self.item[player_id]
            elif player_name:
                return self.players_name[player_name]
            else:
                return default
        except:
            return default


@dataclasses.dataclass(frozen=True, repr=False)
class Cell(ImmutableDataclass):
    """ :class:`Cell` is a class that represent cell object. This class
    is where cell data stored.
    """

    __slots__ = ["client"]
    client: Any

    def details(self):
        """ :meth:`details` send requests to TK for perceive more details
        about this cell.

        return: :class:`dict`
        """
        return self.client.cache.get(
            {"names": [f"MapDetails:{self.id}"]}
        )["cache"][0]["data"]

    @property
    def coordinate(self):
        """ :property:`coordinate` return this cell coordinate.

        return: :class:`Point`
        """
        return Point.from_cell_id(self.id)


@dataclasses.dataclass(frozen=True, repr=False)
class Player(ImmutableDataclass):
    """ :class:`Player` is represent of player object. This class is where
    player data stored.
    """

    __slots__ = ["client", "id"]
    client: Any
    id: int

    def hero_equipment(self):
        """ :meth:`hero_equipment` send requests to TK for perceive
        hero equipment of this player.

        return: :class:`dict`
        """
        return self.client.cache.get(
            {"names": [f"Collection:HeroItem:{self.id}"]}
        )["cache"][0]["data"]["cache"]

    def details(self):
        """ :meth:`details` send requests to Tk for perceive this player
        details.

        return: :class:`dict`
        """
        return self.client.cache.get(
            {"names": [f"Player:{self.id}"]}
        )["cache"][0]["data"]

    @property
    def is_active(self):
        """ :property:`is_active` return whether this player is active or not.

        return: :class:`boolean`
        """
        if self.data["active"] == "1":
            return True
        return False


@dataclasses.dataclass(frozen=True, repr=False)
class Kingdom(ImmutableDataclass):
    """ :class:`Kingdom` represent of kingdom object. This class is where
    kingdom data stored.
    """

    __slots__ = ["id"]
    id: int

    @property
    def name(self):
        """ :property:`name` return this kingdom name. """
        return self.data["tag"]
