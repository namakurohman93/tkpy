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
            raise VillageNotFound(
                'Village name is case sensitive and make sure the name is correct'
            )

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
