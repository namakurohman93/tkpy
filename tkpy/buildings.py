from .utilities import instant_finish, upgrade_building, queue_building
from .fixtures import buildingDict
from .exception import BuildingAtMaxLevel


class Buildings:
    def __init__(self, client, villageId):
        self.client = client
        self.villageId = villageId
        self._raw = dict()

    def __getitem__(self, key):
        return sorted(
            [Building(self.client, x) for x in self.raw
                if x['buildingType'] == buildingDict[key]],
            key=lambda k: int(k['lvl'])
        )

    def __repr__(self):
        return str(type(self))

    def pull(self):
        self._raw.update(
            self.client.cache.get({
                'names': [f'Collection:Building:{self.villageId}']
            })
        )

    @property
    def freeSlots(self):
        return [x['locationId'] for x in self.raw if x['buildingType'] == '0']

    @property
    def raw(self):
        for x in self._raw['cache'][0]['data']['cache']:
            yield x['data']


class Building:
    def __init__(self, client, data):
        self.client = client
        self.data = data

    def __getitem__(self, key):
        try:
            return self.data[key]
        except:
            raise

    def __repr__(self):
        return f'<{type(self).__name__}({self.data})>'

    @property
    def id(self):
        return self.data['buildingType']

    @property
    def location(self):
        return self.data['locationId']

    @property
    def lvl(self):
        return int(self.data['lvl'])

    @property
    def isMaxLvl(self):
        return self.data['isMaxLvl']

    @property
    def upgradeCost(self):
        return self.data['upgradeCosts']

    @property
    def villageId(self):
        return self.data['villageId']

    def upgrade(self):
        return upgrade_building(
            driver=self.client,
            buildingType=self.id,
            locationId=self.location,
            villageId=self.villageId
        )

    def queues(self, reserveResources):
        return queue_building(
            driver=self.client,
            buildingType=self.id,
            locationId=self.location,
            villageId=self.villageId,
            reserveResources=reserveResources
        )


class BuildingQueue:
    def __init__(self, client, villageId):
        self.client = client
        self.villageId = villageId
        self._raw = dict()

    def pull(self):
        self._raw.update(
            self.client.cache.get({
                'names': [f'BuildingQueue:{self.villageId}']
            })
        )

    @property
    def tribe_id(self):
        return self.client.tribe_id

    @property
    def freeSlots(self):
        return self._raw['cache'][0]['data']['freeSlots']

    @property
    def queues(self):
        return self._raw['cache'][0]['data']['queues']

    def finishNow(self, queueType):
        return instant_finish(
            driver=self.client,
            queueType=queueType,
            villageId=self.villageId
        )


class ConstructionList:
    def __init__(self, client, villageId, locationId):
        self.client = client
        self.villageId = villageId
        self.location = locationId
        self._raw = dict()

    def __getitem__(self, key):
        for x in self.buildable:
            if x['buildingType'] == int(buildingDict[key]):
                x['buildable'] = True
                return Building(self.client, x)
        for x in self.notBuildable:
            if x['buildingType'] == int(buildingDict[key]):
                x['buildable'] = False
                return Building(self.client, x)
        return {}

    def __repr__(self):
        return str(type(self))

    def pull(self):
        self._raw.update(
            self.client.building.getBuildingList({
                'locationId': self.location,
                'villageId': self.villageId
            })
        )

    @property
    def buildable(self):
        return self._raw['response']['buildings']['buildable']

    @property
    def notBuildable(self):
        return self._raw['response']['buildings']['notBuildable']
