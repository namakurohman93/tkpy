from .utilities import send_troops, send_farmlist
from .farmlist import FarmList
from .map import cell_id


class VillageNotFound(Exception):
    """ Village not found """


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


class Village:
    def __init__(self, client, data):
        self.client = client
        self.data = data

    def __getitem__(self, key):
        try:
            return self.data[key]
        except:
            raise

    def __repr__(self):
        return str(self.data)

    @property
    def id(self):
        return int(self.data['villageId'])

    @property
    def name(self):
        return self.data['name']

    @property
    def coordinate(self):
        x, y = self.data['coordinate']['x'], self.data['coordinate']['y']
        return int(x), int(y)

    def units(self):
        r = self.client.cache.get({
            'names': [f'Collection:Troops:stationary:{self.id}']
        })
        for x in r['cache'][0]['data']['cache']:
            if x['data']['villageId'] == str(self.id):
                return x['data']['units']

    def _send_troops(self, x, y, destVillageId, movementType, redeployHero,
            spyMission, units):
        target = destVillageId or cell_id(x, y)
        troops = self.units()
        # check amount of every units if units
        if units:
            for k in units:
                if units[k] > int(troops.get(k, 0)):
                    raise SyntaxError(
                        f'Not enough troops {k}'
                    )
            if sum(units.values()) <= 0:
                raise SyntaxError(
                    'Send at least 1 troops'
                )
        else:
            # use all troops on village
            if sum(int(v) for v in troops.values()) <= 0:
                raise SyntaxError(
                    f'There is no troops on {self.name} village'
                )
            # set scout amount to 0
            if self.client.tribe_id in (1, 2):
                troops['4'] = 0
            else:
                troops['3'] = 0
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
            raise SyntaxError(
                'Set units first'
            )
        # set scout amount to 0
        if self.client.tribe_id in (1, 2):
            units['4'] = 0
        else:
            units['3'] = 0
        # check if ram exists
        if '7' not in units:
            raise SyntaxError(
                'Need at least 1 ram for siege'
            )
        # check total amount of units
        if sum(units.values()) < 1000:
            raise SyntaxError(
                'Need at least 1000 troops'
            )
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
