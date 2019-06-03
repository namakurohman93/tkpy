from .map import cell_id as vid
from .master_builder import MasterBuilder


class Village:
    __attrs__ = ['villageId', 'playerId', 'name', 'isMainVillage']

    def __init__(self, client, data):
        self.client = client
        self.master_builder = MasterBuilder(self)
        for attr in Village.__attrs__:
            setattr(self, attr, data[attr])
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
        merchants = r['cache'][0]['data']
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
        amount = r['cache'][0]['data']['storage']
        stor_cap = r['cache'][0]['data']['storageCapacity']
        results = dict()
        results['production'] = {k: int(v) for k, v in production.items()}
        results['amount'] = {k: int(v) for k, v in amount.items()}
        results['storage capacity'] = {k: int(v) for k, v in stor_cap.items()}
        return results

    def cranny(self):
        """return amount of cranny of village"""
        results = 0
        buildings = self.buildings()
        for building in buildings:
            if building['data']['buildingType'] == '23':
                results += building['data']['effect'][0]
        return results

    def _send_troops(self, target, target_id, move_type, units):
        troop = units or self.troops()
        id = vid(*target) or target_id
        r = self.client.troops.send(
            {
                'destVillageId': id,
                'movementType': move_type,
                'redeployHero': False,
                'spyMission': 'resources',
                'units': troop,
                'villageId': self.villageId
            }
        )
        return r

    def attack(self, x=None, y=None, target_id=None, units=None):
        return self._send_troops(
            target=(x, y), target_id=target_id,
            move_type=3, units=units
        )

    def raid(self, x=None, y=None, target_id=None, units=None):
        return self._send_troops(
            target=(x, y), target_id=target_id,
            move_type=4, units=units
        )

    def defend(self, x=None, y=None, target_id=None, units=None):
        return self._send_troops(
            target=(x, y), target_id=target_id,
            move_type=5, units=units
        )

    def upgrade(self, building):
        self.master_builder.upgrade(building)

    @property
    def is_capital(self):
        return self.isMainVillage


class Villages:
    """a container for own village"""
    def __init__(self, client, data=None):
        self.client = client
        self._data = data or dict()

    def __setitem__(self, key, value):
        self._data[key] = value

    def __getitem__(self, key):
        return self._data[key]

    def __delitem__(self, key):
        del self._data[key]

    def __iter__(self):
        return iter(list(self._data.keys()))

    def __repr__(self):
        return f'{type(self).__name__}({dict(self._data.items())})'

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
