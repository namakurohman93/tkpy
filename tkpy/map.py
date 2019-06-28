from math import sqrt


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
    :param source: x, y tuple of source coordinates
    :param target: x, y tuple of target coordinates
    """
    return sqrt((source[0] - target[0])**2 + (source[1] - target[1])**2)


regionIds = {
    cell_id(x, y): [
        cell_id(xx, yy) for xx in range(0+(x*7), 7+(x*7)) for yy in range(0+(y*7), 7+(y*7))
    ] for x in range(-13, 14) for y in range(-13, 14)
}


class Map:
    def __init__(self, client):
        self.client = client
        self._raw = dict()

    def pull(self):
        r = self.client.map.getByRegionIds(
            params={
                'regionIdCollection': {
                    '1': list(regionIds.keys())
                }
            }
        )
        del r['response']['1']['reports']
        self._raw.update(r)

    def _pull(self, region_id=[]):
        ids = (x for x in list(range(1, len(region_id)//49 + 2)))
        req_list = {
            str(id): [
                region_id.pop() for _ in range(49) if region_id
            ] for id in ids
        }
        r = self.client.map.getByRegionIds({
            'regionIdCollection': req_list
        })
        self._raw.update(r)

    @property
    def cell(self):
        for c in self._raw['response']:
            try:
                for region_id in self._raw['response'][c]['region']:
                    for cell in self._raw['response'][c]['region'][region_id]:
                        # yield cell
                        yield Cell(self.client, cell)
            except:
                continue

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
        for c in self._raw['response']:
            try:
                for x in self._raw['response'][c]['kingdom']:
                    yield Kingdom(x, self._raw['response'][c]['kingdom'][x])
            except:
                continue

    def kingdom(self, name=None, id=None, default={}):
        for kingdom in self.kingdoms:
            if kingdom.id == str(id) or kingdom.name == name:
                return kingdom
        return default

    @property
    def players(self):
        for c in self._raw['response']:
            try:
                for x in self._raw['response'][c]['player']:
                    yield Player(
                        self.client, x, self._raw['response'][c]['player'][x]
                    )
            except:
                continue


    def player(self, name=None, id=None, default={}):
        for player in self.players:
            if player.id == str(id) or player.name == name:
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


class Player:
    def __init__(self, client, id, data):
        self.client = client
        self.id = id
        self.data = data

    def __getitem__(self, key):
        try:
            return self.data[key]
        except:
            raise

    def __repr__(self):
        return str(self.data)

    def hero_equipment(self):
        return self.client.cache.get({
            'names': [f'Collection:HeroItem:{self.id}']
        })['cache'][0]['data']['cache']

    def details(self):
        return self.client.cache.get({
            'names': [f'Player:{self.id}']
        })['cache'][0]['data']

    @property
    def name(self):
        return self.data['name']

    @property
    def tribe_id(self):
        return self.data['tribeId']

    @property
    def is_active(self):
        if self.data['active'] == '1':
            return True
        return False


class Kingdom:
    def __init__(self, id, data):
        self.id = id
        self.data = data

    def __getitem__(self, key):
        try:
            return self.data[key]
        except:
            raise

    def __repr__(self):
        return str(self.data)

    @property
    def name(self):
        return self.data['tag']
