from .utilities import send_farmlist
from .exception import FarmListNotFound


class Farmlist:
    def __init__(self, client):
        self.client = client
        self._raw = dict()
        self.item = dict()

    def __getitem__(self, key):
        try:
            return self.item[key]
        except:
            raise FarmListNotFound(f'{key}')

    def pull(self):
        self._raw.update(
            self.client.cache.get({
                'names': ['Collection:FarmList:']
            })
        )
        # store farmlistEntry object
        for x in self.raw:
            self.item[x['listName']] = FarmlistEntry(self.client, x)

    @property
    def raw(self):
        for x in self._raw['cache'][0]['data']['cache']:
            yield x['data']

    @property
    def list(self):
        for x in self.raw:
            yield FarmlistEntry(self.client, x)

    def create_farmlist(self, name):
        self.client.farmList.createList({'name': name})
        self.pull()


class FarmlistEntry:
    def __init__(self, client, data):
        self.client = client
        self.data = data
        self._raw = dict()

    def __getitem__(self, key):
        try:
            return self.data[key]
        except:
            raise

    def __repr__(self):
        return str(self.data)

    @property
    def name(self):
        return self.data['listName']

    @property
    def id(self):
        return int(self.data['listId'])

    @property
    def villageIds(self):
        return self.data['villageIds']

    @property
    def entryIds(self):
        return self.data['entryIds']

    def send(self, villageId):
        return send_farmlist(
            driver=self.client,
            listIds=[self.id],
            villageId=villageId
        )

    def _update_data(self, r):
        for x in r['cache']:
            if x['name'] == f'FarmList:{self.id}':
                self.data.update(x['data'])

    def add(self, villageId):
        r = self.client.farmList.addEntry({
            'listId': self.id,
            'villageId': villageId
        })
        self._update_data(r)

    def toggle(self, villageId):
        r = self.client.farmList.toggleEntry({
            'listId': self.id,
            'villageId': villageId
        })
        self._update_data(r)

    def pull(self):
        self._raw.update(
            self.client.cache.get({
                'names': [f'Collection:FarmListEntry:{self.id}']
            })
        )

    @property
    def farmlistEntry(self):
        for x in self._raw['cache'][0]['data']['cache']:
            yield EntryId(self.client, x['data'])


class EntryId:
    def __init__(self, client, data):
        self.client = client
        self.data = data

    def __repr__(self):
        return str(self.data)

    def __getitem__(self, key):
        try:
            return self.data[key]
        except:
            raise

    @property
    def id(self):
        return self.data['entryId']

    @property
    def villageId(self):
        return self.data['villageId']

    @property
    def notificationType(self):
        try:
            return self.data['lastReport']['notificationType']
        except:
            return '0'

    @property
    def raidedSum(self):
        try:
            return self.data['lastReport']['raidedResSum']
        except:
            return 0

    @property
    def capacity(self):
        try:
            return self.data['lastReport']['capacity']
        except:
            return 0

    def copy(self, farmlistId):
        self.client.farmList.copyEntry({
            'entryId': self.id,
            'villageId': self.villageId,
            'newListId': farmlistId
        })

    def delete(self):
        self.client.farmList.deleteEntry({
            'entryId': self.id
        })
