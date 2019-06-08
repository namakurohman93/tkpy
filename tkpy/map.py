from math import sqrt
from collections import namedtuple

class Map:
    def __init__(self, client):
        self.client = client
        self._raw = dict()
        self.Player = namedtuple('Player', ['id', 'data'])
        self.Kingdom = namedtuple('Kingdom', ['id', 'name'])

    def pull(self):
        req_list = (
            cell_id(x, y) for x in range(-13, 14) for y in range(-13, 14)
        )
        r = self.client.map.getByRegionIds(
            params={
                'regionIdCollection': {
                    '1': list(req_list)
                }
            }
        )
        del r['response']['1']['reports']
        self._raw.update(r)

    @property
    def cell(self):
        for region_id in self._raw['response']['1']['region']:
            for cell in self._raw['response']['1']['region'][region_id]:
                # yield cell
                yield Cell(self.client, cell)

    @property
    def villages(self):
        for cell in self.cell:
            if 'village' in cell:
                yield cell
            else:
                continue

    @property
    def tiles(self):
        """Known as Abandoned valley"""
        for cell in self.cell:
            if 'village' not in cell and 'resType' in cell:
                yield cell
            else:
                continue

    @property
    def oasis(self):
        for cell in self.cell:
            if 'oasis' in cell:
                yield cell
            else:
                continue

    @property
    def wilderness(self):
        for cell in self.cell:
            if 'oasis' not in cell and 'resType' not in cell:
                yield cell
            else:
                continue

    def village(self, name=None, id=None, default={}):
        for village in self.villages:
            if village['id'] == str(id) or village['village']['name'] == name:
                return village
        return default

    def coordinate(self, x, y, default={}):
        for cell in self.cell:
            if cell['id'] == str(cell_id(x, y)):
                return cell
        return default

    def tile(self, id, default={}):
        for cell in self.cell:
            if cell['id'] == str(id):
                return cell
        return default

    @property
    def kingdoms(self):
        for x in self._raw['response']['1']['kingdom']:
            yield self.Kingdom(
                id=x,
                name=self._raw['response']['1']['kingdom'][x]['tag']
            )

    def kingdom(self, name=None, id=None, default={}):
        for kingdom in self.kingdoms:
            if kingdom.id == str(id) or kingdom.name == name:
                return kingdom
        return default

    @property
    def players(self):
        for x in self._raw['response']['1']['player']:
            yield self.Player(
                id=x,
                data=self._raw['response']['1']['player'][x]
            )

    def player(self, name=None, id=None, default={}):
        for player in self.players:
            if player.id == str(id) or player.data['name'] == name:
                return player
        return default


class Cell:
    def __init__(self, client, data):
        self.client = client
        self.data = data

    def __contains__(self, item):
        return self.data.__contains__(item)

    def __getitem__(self, key):
        try:
            return self.data[key]
        except:
            raise

    def __repr__(self):
        return str(self.data)

    def details(self):
        r = self.client.cache.get({'names':[f'MapDetails:{self.id}']})
        return r['cache'][0]['data']

    @property
    def id(self):
        return int(self.data['id'])

    @property
    def coordinate(self):
        return reverse_id(self.id)


def cell_id(x, y):
    return (536887296 + x) + (y * 32768)


def reverse_id(vid):
    binary = f'{vid:b}'
    if len(binary) < 30:
        binary = '0' + binary
    xcord, ycord = binary[15:], binary[:15]
    realx = int(xcord, 2) - 16384
    realy = int(ycord, 2) - 16384
    return realx, realy


def distance(source, target):
    """
    :param source: x, y tuple object of source coordinates
    :param target: x, y tuple object of target coordinates
    """
    return sqrt((source[0] - target[0])**2 + (source[1] - target[1])**2)
