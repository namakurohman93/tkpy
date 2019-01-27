from utils import vid


class Player:
    __attrs__ = ['tribeId', 'kingdomId', 'active']

    def __init__(self, client, id, data):
        self.client = client
        self.id = id
        self.name = data['name']
        for attr in Player.__attrs__:
            setattr(self, attr, int(data[attr]))
        del data

    def __repr__(self):
        return f'{type(self).__name__}(name: {self.name}, id: {self.id})'

    def details(self):
        r = self.client.cache.get({'names':[f'Player:{self.id}']})
        return r


class Players:
    """a container for all players who play on the game"""
    def __init__(self, client, data=None):
        self.client = client
        self._data = data or dict()

    def __setitem__(self, key, value):
        self._data[key] = value

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(list(self._data.keys()))

    def __repr__(self):
        return f'{type(self).__name__}(Total players: {len(self._data)})'

    def pull(self):
        """git pull like function for pulling map data from server"""
        req_list = list()
        for x in range(-13, 14):
            for y in range(-13, 14):
                req_list.append(vid(x, y))
        r = self.client.map.getByRegionIds(
            {
                'regionIdCollection': {
                    '1': req_list
                }
            }
        )
        for pid in r['response']['1']['player']:
            player_name = r['response']['1']['player'][pid]['name']
            id = int(pid)
            data = r['response']['1']['player'][pid]
            self.__setitem__(player_name, Player(self.client, id, data))

    def inactive(self):
        results = dict()
        for name in self._data:
            if not self._data[name].active:
                results[name] = self._data[name]
        return Players(self.client, results)

    @property
    def list(self):
        for name in self._data:
            print(f'{name}: {self._data[name].id}')
