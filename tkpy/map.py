from math import sqrt


def cell_id(x, y):
    """ :func:`cell_id` will convert :class:`int` x and :class:`int` y
    into cell id that being used for Travian: Kingdom.

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
    binary = f'{vid:b}'
    if len(binary) < 30:
        binary = '0' + binary
    xcord, ycord = binary[15:], binary[:15]
    realx = int(xcord, 2) - 16384
    realy = int(ycord, 2) - 16384
    return realx, realy


regionIds = {
    cell_id(x, y): [
        cell_id(xx, yy) for xx in range(0+(x*7), 7+(x*7)) for yy in range(0+(y*7), 7+(y*7))
    ] for x in range(-13, 14) for y in range(-13, 14)
}


class Map:
    """ :class:`Map` is represent of map object for Travian: Kingdom. Map
    data from Travian: Kingdom is stored in here. This class provide an
    easy way to access map data by using :meth:`coordinate` for accessing
    specific cell based on their coordinate, or using :property:`villages`
    for yield cell that contains village data on it, or by using another
    property.

    Usage::
        >>> m = Map(driver)
        >>> m.pull()
        >>> m.coordinate(0, 0)
        <Cell({'id': '536887296', 'landscape': '9013', 'owner': '0'})>
        >>> villages = list(m.villages)
    """
    def __init__(self, client):
        self.client = client
        self._raw_data = dict()

    def __repr__(self):
        return str(type(self))

    def pull(self):
        """ :meth:`pull` for pulling map data from Travian: Kingdom. """
        r = self.client.map.getByRegionIds({
            'regionIdCollection': {
                '1': list(regionIds.keys())
            }
        })
        self._raw_data.update(r)

    def pull_region_id(self, region_id=[]):
        """ :meth:`pull_region_id` will pull specific region data from
        Travian: Kingdom.

        :param region_id: - :class:`list` (optional) list of region id
                            that want to requested to Travian: Kingdom.
                            Default: []
        """
        r = self.client.map.getByRegionIds({
            'regionIdCollection': {
                '1': region_id
            }
        })
        self._raw_data.update(r)

    def gen_tiles(self):
        """ :meth:`gen_tiles` is a :func:`generator` that yield :class:`Cell`
        object.

        yield: :class:`Cell`
        """
        for region_id in self._raw_data['response']['1']['region']:
            for cell in self._raw_data['response']['1']['region'][region_id]:
                yield Cell(self.client, cell)

    def gen_villages(self):
        """ :meth:`gen_villages` is a :func:`generator` that yield :class:`Cell`
        that have 'village' data on it.

        yield: :class:`Cell`
        """
        for cell in self.gen_tiles():
            if 'village' in cell:
                yield cell
            else:
                continue

    def gen_grey_villages(self):
        """ :meth: `gen_grey_villages` is a :func:`generator` that yield :class:`Cell`
        that have 'village' data on it and it already grey (inactive).

        yield: :class:`Cell`
        """
        players = [player['playerId'] for player in self.gen_players() if player.is_active]

        for village in self.gen_villages():
            if village['playerId'] in players:
                yield village
            else:
                continue

    def gen_abandoned_valley(self):
        """ :meth:`gen_abandoned_valley` is a :func:`generator that yield
        :class:`Cell` that known as abandoned valley in the game.

        yield: :class:`Cell`
        """
        for cell in self.gen_tiles():
            if 'village' not in cell and 'resType' in cell:
                yield cell
            else:
                continue

    def gen_oases(self):
        """ :meth:`gen_oases` is a :func:`generator` that yield :class:`Cell`
        that have 'oasis' data on it.

        yield: :class:`Cell`
        """
        for cell in self.gen_tiles():
            if 'oasis' in cell:
                yield cell
            else:
                continue

    def gen_unoccupied_oases(self):
        """ :meth:`gen_unoccupied_oases` is a :func:`generator` that yield :class:`Cell`
        that have 'oasis' data on it and it unoccupied.

        yield: :class:`Cell`
        """
        for oasis in self.gen_oases():
            if (oasis['oasisStatus'] == '3'):
                yield oasis
            else:
                continue

    def gen_wilderness(self):
        """ :meth:`gen_wilderness` is a :func:`generator` that yield :class:`Cell`
        that known as wilderness in the game.

        yield: :class:`Cell`
        """
        for cell in self.gen_tiles():
            if 'oasis' not in cell and 'resType' not in cell:
                yield cell
            else:
                continue

    def get_village(self, name=None, village_id=None, default={}):
        """ :meth:`get_village` is used for find specific :class:`Cell` object
        that have village data on it based on village name or village id.

        :param name: - :class:`str` village name.
        :param village_id: - :class:`int` village id.
        :param default: - :class:`dict` (optional) default value if :cell:`Cell` object
                          didn't found. Default: {}.

        return: :class:`Cell`
        """
        for village in self.gen_villages():
            if village['id'] == str(village_id) or village['village']['name'] == name:
                return village
        return default

    def coordinate(self, x, y, default={}):
        """ :meth:`coordinate` is used for find specific :class:`Cell` object
        based on cell's coordinate.

        :param x: - :class:`int` x cell's coordinate.
        :param y: - :class:`int` y cell's coordinate.
        :param default: - :class:`dict` (optional) default value if :class:`Cell`
                          object didn't found. Default: {}

        return: :class:`Cell`
        """
        for cell in self.gen_tiles():
            if cell['id'] == str(cell_id(x, y)):
                return cell
        return default

    def get_tile_by_id(self, cell_id, default={}):
        """ :meth:`get_tile_by_id` is used for find specific :class:`Cell` object
        based on cell's id.

        :param cell_id: - :class:`int` cell id.
        :param default: - :class:`dict` (optional) default value if :class:`Cell`
                          object didn't found. Default: {}

        return: :class:`Cell`
        """
        for cell in self.gen_tiles():
            if cell['id'] == str(cell_id):
                return cell
        return default

    def gen_players(self):
        """ :property:`gen_players` is a :func:`generator` that yield
        :class:`Player` object.

        yield: :class:`Player`
        """
        for player_id in self._raw_data['response']['1']['player']:
            yield Player(self.client, player_id, self._raw_data['response']['1']['player'][player_id])

    def get_player(self, name=None, player_id=None, default={}):
        """ :meth:`player` is used for find :class:`Player` object
        used player name or id.

        :param name: - :class:`str` player's name.
        :param player_id: - :class:`int` player's id.
        :param default: - :class:`dict` (optional) default value when
                          :class:`Player` object not found. Default: {}

        return: :class:`Player`
        """
        for player in self.gen_players():
            if player.id == str(player_id) or player.name == name:
                return player
        return default

    def gen_kingdoms(self):
        """ :meth:`gen_kingdoms` is a :func:`generator` that yield :class:`Kingdom`
        object.

        yield: :class:`Kingdom`
        """
        for kingdom_id in self._raw_data['response']['1']['kingdom']:
            yield Kingdom(kingdom_id, self._raw_data['response']['1']['kingdom'][kingdom_id])

    def get_kingdom(self, name=None, kingdom_id=None, default={}):
        """ :meth:`kingdom` is used for find :class:`Kingdom` object
        using name or id of kingdom.

        :param name: - :class:`str` kingdom's name.
        :param kingdom_id: - :class:`int` kingdom's id.
        :param default: - :class:`dict` (optional) default value when
                          :class:`Kingdom` object not found. Default: {}

        return: :class:`Kingdom`
        """
        for kingdom in self.gen_kingdoms():
            if kingdom.id == str(kingdom_id) or kingdom.name == name:
                return kingdom
        return default

    @staticmethod
    def distance(source, target):
        return sqrt((source.coordinate.x - target.coordinate.x) ** 2 + (source.coordinate.y - target.coordinate.y) ** 2)


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def generate_by_id(cls, cellId):
        return cls(*reverse_id(int(cellId)))


class Cell:
    """ :class:`Cell` is a class that represent cell object. This class
    is where cell data stored.
    """
    def __init__(self, client, data):
        self.client = client
        self.data = data
        self.coordinate = Coordinate.generate_by_id(self.id)

    def __contains__(self, item):
        return self.data.__contains__(item)

    def __getitem__(self, key):
        try:
            return self.data[key]
        except:
            raise

    def __repr__(self):
        return f'<{type(self).__name__}({self.data})>'

    def details(self):
        """ :meth:`details` send requests to Travian: Kingdom for perceive more
        details about this cell.

        return: :class:`dict`
        """
        r = self.client.cache.get({'names':[f'MapDetails:{self.id}']})
        return r['cache'][0]['data']

    @property
    def id(self):
        """ :property:`id` return this cell id. """
        return int(self.data['id'])


class Player:
    """ :class:`Player` is represent of player object. This class is where
    player data stored.
    """
    def __init__(self, client, playerId, data):
        self.client = client
        self.id = playerId
        self.data = data
        self.data['playerId'] = playerId

    def __getitem__(self, key):
        try:
            return self.data[key]
        except:
            raise

    def __repr__(self):
        return f'<{type(self).__name__}({self.data})>'

    def hero_equipment(self):
        """ :meth:`hero_equipment` send requests to TK for perceive
        hero equipment of this player.

        return: :class:`dict`
        """
        return self.client.cache.get({
            'names': [f'Collection:HeroItem:{self.id}']
        })['cache'][0]['data']['cache']

    def details(self):
        """ :meth:`details` send requests to Tk for perceive this player
        details.

        return: :class:`dict`
        """
        return self.client.cache.get({
            'names': [f'Player:{self.id}']
        })['cache'][0]['data']

    @property
    def name(self):
        """ :property:`name` return this player name. """
        return self.data['name']

    @property
    def tribe_id(self):
        """ :property:`tribe_id` return this player tribe id. """
        return self.data['tribeId']

    @property
    def is_active(self):
        """ :property:`is_active` return whether this player is active or not.

        return: :class:`boolean`
        """
        if self.data['active'] == '1':
            return True
        return False


class Kingdom:
    """ :class:`Kingdom` represent of kingdom object. This class is where
    kingdom data stored.
    """
    def __init__(self, kingdomId, data):
        self.id = kingdomId
        self.data = data
        self.data['kingdomId'] = kingdomId

    def __getitem__(self, key):
        try:
            return self.data[key]
        except:
            raise

    def __repr__(self):
        return f'<{type(self).__name__}({self.data})>'

    @property
    def name(self):
        """ :property:`name` return this kingdom name. """
        return self.data['tag']
