from .utilities import send_troops, send_farmlist
from .map import cell_id
from .buildings import Buildings, BuildingQueue, ConstructionList
from .exception import (
    VillageNotFound, BuildingSlotFull, FailedConstructBuilding,
    QueueFull, WarehouseNotEnough, BuildingAtMaxLevel
)


class Villages:
    def __init__(self, client):
        self.client = client
        self._raw = dict()
        self.item = dict()

    def __getitem__(self, key):
        try:
            return self.item[key]
        except:
            raise VillageNotFound(f'Village {key} is not found')

    def __iter__(self):
        return iter(self.item.keys())

    @property
    def dorps(self):
        """ return village object """
        for x in self.item:
            yield self.item[x]

    @property
    def raw(self):
        """ return raw data """
        for x in self._raw['cache'][0]['data']['cache']:
            yield x['data']

    def pull(self):
        self._raw.update(
            self.client.cache.get(
                {'names': ['Collection:Village:own']}
            )
        )
        # store village object
        for x in self.raw:
            self.item[x['name']] = Village(self.client, x)

    def get_capital_village(self):
        for village in self.dorps:
            if village.isMainVillage:
                return village


class Village:
    def __init__(self, client, data):
        self.client = client
        self.data = data
        self.buildings = Buildings(self.client, self.id)
        self.buildingQueue = BuildingQueue(self.client, self.id)
        self.warehouse = Warehouse(self.data)

    def __getitem__(self, key):
        try:
            return self.data[key]
        except:
            raise

    def __repr__(self):
        return str(self.data)

    def pull(self):
        r = self.client.cache.get({
            'names': [f'Village:{self.id}']
        })
        self.data.update(r['cache'][0]['data'])

    @property
    def id(self):
        return int(self.data['villageId'])

    @property
    def name(self):
        return self.data['name']

    @property
    def coordinate(self):
        x, y = self.data['coordinates']['x'], self.data['coordinates']['y']
        return int(x), int(y)

    @property
    def isMainVillage(self):
        return self.data['isMainVillage']

    def units(self):
        r = self.client.cache.get({
            'names': [f'Collection:Troops:stationary:{self.id}']
        })
        for x in r['cache'][0]['data']['cache']:
            if x['data']['villageId'] == str(self.id):
                return x['data']['units']

    def troops_movement(self):
        r = self.client.cache.get({
            'names': [f'Collection:Troops:moving:{self.id}']
        })
        return [x['data'] for x in r['cache'][0]['data']['cache']]

    def _send_troops(self, x, y, destVillageId, movementType, redeployHero,
            spyMission, units):
        target = destVillageId or cell_id(x, y)
        troops = self.units()
        # check amount of every units if units
        if units:
            for k in units:
                if int(units[k]) == -1:
                    units[k] = int(troops.get(k, 0))
                if int(units[k]) > int(troops.get(k, 0)):
                    raise SyntaxError(
                        f'Not enough troops {k}'
                    )
            if sum(int(v) for v in units.values()) <= 0:
                raise SyntaxError(
                    'Send at least 1 troops'
                )
            # check total amount of units if movementType 47 (siege)
            if movementType == 47:
                if sum(int(v) for v in units.values()) < 1000:
                    raise SyntaxError(
                        'Need at least 1000 troops'
                    )
                # check if ram exists
                if '7' not in units:
                    raise SyntaxError(
                        'Need at least 1 ram for siege'
                    )
        else:
            # since it send all unit on village, first
            # set scout amount to 0
            if self.client.tribe_id in (1, 2):
                troops['4'] = 0
            else:
                troops['3'] = 0
            # use all troops on village
            if sum(int(v) for v in troops.values()) <= 0:
                raise SyntaxError(
                    f'There is no troops on {self.name} village'
                )
        return send_troops(
            driver=self.client,
            destVillageId=target,
            movementType=movementType,
            redeployHero=redeployHero,
            spyMission=spyMission,
            units=units or troops,
            villageId=self.id
        )

    def attack(self, x=None, y=None, targetId=None, units=None):
        # TODO:
        # add building target when cata in units and rally point level >= 5
        return self._send_troops(
            x=x,
            y=y,
            destVillageId=targetId,
            movementType=3,
            redeployHero=False,
            spyMission='resources',
            units=units,
        )

    def raid(self, x=None, y=None, targetId=None, units=None):
        return self._send_troops(
            x=x,
            y=y,
            destVillageId=targetId,
            movementType=4,
            redeployHero=False,
            spyMission='resources',
            units=units
        )

    def defend(self, x=None, y=None, targetId=None, units=None,
            redeployHero=False):
        # TODO:
        # if redeployHero, check if hero in units
        # and check if target is one of village id in Village object
        return self._send_troops(
            x=x,
            y=y,
            destVillageId=targetId,
            movementType=5,
            redeployHero=redeployHero,
            spyMission='resources',
            units=units
        )

    def spy(self, x=None, y=None, targetId=None, amount=0,
            mission='resources'):
        if mission not in ('resources', 'defence'):
            raise SyntaxError(
                'choose mission between \'resources\' or \'defence\''
            )
        if self.client.tribe_id in (1, 2):
            units = {'4': amount} # scout of roman and teuton
        else:
            units = {'3': amount} # scout of gauls
        return self._send_troops(
            x=x,
            y=y,
            destVillageId=targetId,
            movementType=6,
            redeployHero=False,
            spyMission=mission,
            units=units
        )

    def siege(self, x=None, y=None, targetId=None, units=None):
        # TODO
        # add building target if cata in units and rally point level >= 5
        if not units:
            raise SyntaxError('Set units first')
        return self._send_troops(
            x=x,
            y=y,
            destVillageId=targetId,
            movementType=47,
            redeployHero=False,
            spyMission='resources',
            units=units
        )

    def send_farmlist(self, listIds):
        return send_farmlist(
            driver=self.client,
            listIds=listIds,
            villageId=self.id
        )

    def upgrade(self, building):
        # update data with the newest one
        self.pull()
        self.buildings.pull()
        self.buildingQueue.pull()

        if self.buildings[building]:
            b = self.buildings[building][0]

            if b.isMaxLvl:
                return self._construct(building)

            for k, v in b.upgradeCost.items():
                if self.warehouse[k] < v and self.warehouse.capacity[k] > v:
                    return self._check_queue(reserveResources=False, b=b)

                if self.warehouse.capacity[k] < v:
                    raise WarehouseNotEnough(
                        f'Warehouse / granary capacity not enough for upgrade {building}'
                    )

            if self.client.tribe_id == 1 and int(b.id) < 5:
                return self._upgrade(slot='2', b=b)

            return self._upgrade(slot='1', b=b)

        # building didn't exists
        # construct it
        return self._construct(building)

    def _construct(self, building):
        if self.buildings.freeSlots:
            c = ConstructionList(
                client=self.client,
                villageId=self.id,
                locationId=self.buildings.freeSlots[0]
            )
            c.pull()

            b = c[building]

            if b:
                if b['buildable']:
                    # construct it
                    for k, v in b.upgradeCost.items():
                        if self.warehouse[k] < v and self.warehouse.capacity[k] > v:
                            return self._check_queue(reserveResources=False, b=b)

                        if self.warehouse.capacity[k] < v:
                            raise WarehouseNotEnough(
                                f'Warehouse / granary capacity not enough for construct {building}'
                            )

                    return self._upgrade(slot='1', b=b)

                raise FailedConstructBuilding(
                    f'Failed construct {building} cause lack of required buildings'
                )

            raise BuildingAtMaxLevel(f'{building} already at max level')

        raise BuildingSlotFull(f'Building slot at {self.name} full')

    def _upgrade(self, slot, b):
        if self.buildingQueue.freeSlots[slot] > 0:
            return b.upgrade()

        return self._check_queue(reserveResources=True, b=b)

    def _check_queue(self, reserveResources, b):
        if self.buildingQueue.freeSlots['4'] > 0:
            return b.queues(reserveResources)

        raise QueueFull('Queue full')


class Warehouse:
    def __init__(self, data):
        self.data = data
        self.resType = {'wood': '1', 'clay': '2', 'iron': '3', 'crop': '4'}

    @property
    def storage(self):
        return self.data['storage']

    @property
    def production(self):
        return {k: int(v) for k, v in self.data['production'].items()}

    @property
    def capacity(self):
        return {k: int(v) for k, v in self.data['storageCapacity'].items()}

    @property
    def wood(self):
        return self._print_res('1')

    @property
    def clay(self):
        return self._print_res('2')

    @property
    def iron(self):
        return self._print_res('3')

    @property
    def crop(self):
        return self._print_res('4')

    def _print_res(self, key):
        s = self.storage[key]
        c = self.capacity[key]
        p = self.production[key]
        return f'{s}/{c} {p}'

    def __getitem__(self, key):
        if key in ('1', '2', '3', '4'):
            return self.storage[key]
        elif key in ('wood', 'clay', 'iron', 'crop'):
            return self.storage[self.resType[key]]
        else:
            raise KeyError('The key is \'1\', \'2\', \'3\', \'4\' or \'wood\', \'clay\', \'iron\', \'crop\'')

    def __repr__(self):
        return f'wood: {self.wood}\nclay: {self.clay}\niron: {self.iron}\ncrop: {self.crop}'
