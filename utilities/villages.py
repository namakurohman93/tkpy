from utils import fishout
from primordial.gameworld import Gameworld


class Village:
    __attrs__ = ['villageId', 'playerId', 'name', 'isMainVillage']

    def __init__(self, client, data):
        self.client = client
        for attr in Village.__attrs__:
            setattr(self, attr, data[attr])
        self.coord = fishout(int(self.villageId))
        del data

    def troops(self):
        params = {'names':[f'Collection:Troops:stationary:{self.villageId}']}
        r = self.client.cache.get(params)
        units = r['cache'][0]['data']['cache'][0]['data']['units']
        return units

    def incoming_attack(self):
        names = f'Collection:TroopsMovementInfo:attackVillage:{self.villageId}'
        params = {'names':[names]}
        r = self.client.cache.get(params)
        # incoming = r['cache'][0]['data']['cache'][0]['data']
        # return incoming

    def merchants(self):
        params = {'names':[f'Merchants:{self.villageId}']}
        r = self.client.cache.get(params)
        merchants = r['cache'][0]['data']['max']
        return merchants

    def buildings(self):
        params = {'names':[f'Collection:Building:{self.villageId}']}
        r = self.client.cache.get(params)
        buildings = r['cache'][0]['data']['cache']
        return buildings

    def resources(self):
        params = {'names':[f'Village:{self.villageId}']}
        r = self.client.cache.get(params)
        production = r['cache'][0]['data']['production']
        storage = r['cache'][0]['data']['storage']
        storage_capacity = r['cache'][0]['data']['storageCapacity']
        print(f'production = {production}\nstorage = {storage}\ncapacity = {storage_capacity}')

    @property
    def is_capital(self):
        return self.isMainVillage


class Villages:
    def __init__(self, client, data=None):
        assert isinstance(client, Gameworld), 'Need Gameworld object'
        self.client = client
        self._data = data or dict()

    def __setitem__(self, key, value):
        self._data[key] = value

    def __getitem__(self, key):
        return self._data[key]

    def pull(self):
        """git pull like function for pulling own village data"""
        r = self.client.cache.get({'names':['Collection:Village:own']})
        for villages in r['cache'][0]['data']['cache']:
            village_name = villages['data']['name']
            village = Village(self.client, villages['data'])
            self.__setitem__(village_name, village)

    @property
    def list(self):
        for village in self._data:
            print(village)
