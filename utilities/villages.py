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
        for troop in r['cache'][0]['data']['cache']:
            if troop['data']['villageId'] == self.villageId:
                units = troop['data']['units']
        return units

    def incoming_attack(self):
        troop_id = list()
        incoming = list()
        names = f'Collection:TroopsMovementInfo:attackVillage:{self.villageId}'
        params = {'names':[names]}
        r = self.client.cache.get(params)
        for caches in r['cache'][0]['data']['cache']:
            troop_id.append(caches['data']['troopId'])
        params = {'names': [f'Collection:Troops:moving:{self.villageId}']}
        r = self.client.cache.get(params)
        for caches in r['cache'][0]['data']['cache']:
            id = caches['data']['troopId']
            if id in troop_id:
                incoming.append(caches['data'])
        return incoming

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
        results = f'production = {production}\nstorage = {storage}\n'+\
                  f'capacity = {storage_capacity}'
        print(results)

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

    def __iter__(self):
        return iter(list(self._data.keys()))

    def pull(self):
        """git pull like function for pulling own village data"""
        r = self.client.cache.get({'names':['Collection:Village:own']})
        for villages in r['cache'][0]['data']['cache']:
            village_name = villages['data']['name']
            village = Village(self.client, villages['data'])
            self.__setitem__(village_name, village)

    def id(self, id):
        """use village id as a key for getting the item"""
        for key in self._data:
            if self._data[key].villageId == id:
                return self._data[key]

    def keys(self):
        return self._data.keys()

    @property
    def list(self):
        for village in self._data:
            print(village)
