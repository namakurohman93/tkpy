from .exception import FarmListNotFound


class Farmlist:
    """:class:`Farmlist` is a represent of farmlist object. This class is
    the place where :class:`FarmlistEntry` stored. And the way to get
    :class:`FarmlistEntry` is just using farmlist name.

    Usage::
        >>> f = Farmlist(driver)
        >>> f.pull()
        >>> f['Startup farm list']
        <FarmListEntry({'listId': '1631', 'listName': 'Startup farm list', ...})>
    """
    def __init__(self, client):
        self.client = client
        self._raw = dict()
        self.item = dict()

    def __getitem__(self, key):
        try:
            return self.item[key]
        except:
            raise FarmListNotFound(f'{key}')

    def __repr__(self):
        return str(type(self))

    def pull(self):
        """ :meth:`pull` for pulling farmlist data from TK. """
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
        """ :property:`raw` is a :func:`generator` that yield raw farmlist
        data.

        yield: :class:`dict`
        """
        for x in self._raw['cache'][0]['data']['cache']:
            yield x['data']

    @property
    def list(self):
        """ :property:`list` is a :func:`generator` that yield
        :class:`FarmlistEntry`.

        yield: :class:`FarmlistEntry`
        """
        for x in self.raw:
            yield FarmlistEntry(self.client, x)

    def create_farmlist(self, name):
        """ :meth:`create_farmlist` for create new farmlist.

        :param name: - `str` name of new created farmlist

        return: :class:`dict`
        """
        self.client.farmList.createList({'name': name})
        self.pull()


class FarmlistEntry:
    """ :class:`FarmlistEntry` is a represent of farmlist entry. In this
    class contains farmlist entry data. You mostly maintain farmlist entry
    using this class.

    Usage::
        >>> f = Farmlist(driver)
        >>> f.pull()
        >>> f['Startup farm list'].add(536461288)
        >>> f['Startup farm list'].toggle(536442311)
        >>> f['Startup farm list'].send(536411586)
    """
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
        return f'<{type(self).__name__}({self.data})>'

    @property
    def name(self):
        """ :property:`name` return this farmlist entry name. """
        return self.data['listName']

    @property
    def id(self):
        """ :property:`id` return this farmlist entry id. """
        return int(self.data['listId'])

    @property
    def villageIds(self):
        """ :property:`villageIds` return :class:`list` of village id
        that stored on this farmlist entry.

        return: :class:`list`
        """
        return self.data['villageIds']

    @property
    def entryIds(self):
        """ :property:`entryIds` return :class:`list` contains entry id
        on this farmlist entry.

        return: :class:`list`
        """
        return self.data['entryIds']

    def send(self, villageId):
        """ :meth:`send` for send this farmlist entry from village using
        village id.

        :param villageId: - :class:`int` village id where this farmlist
                            is sent.

        return: :class:`dict`
        """
        return self.client.troops.startFarmListRaid({
            'listIds': [self.id],
            'villageId': villageId
        })

    def _update_data(self, r):
        for x in r['cache']:
            if x['name'] == f'FarmList:{self.id}':
                self.data.update(x['data'])

    def add(self, villageId):
        """ :meth:`add` for add village to this farmlist using village id.

        :param villageId: - :class:`int` village id that want to be added
                            to this farmlist entry.
        """
        r = self.client.farmList.addEntry({
            'listId': self.id,
            'villageId': villageId
        })
        self._update_data(r)

    def toggle(self, villageId):
        """ :meth:`toggle` for toggling village to this farmlist entry
        using village id.

        :param villageId: - :class:`int` village id that want to be toggled
                            to this farmlist entry.
        """
        r = self.client.farmList.toggleEntry({
            'listId': self.id,
            'villageId': villageId
        })
        self._update_data(r)

    def pull(self):
        """ :meth:`pull` for pulling entry data that exists in this farmlist
        entry.
        """
        self._raw.update(
            self.client.cache.get({
                'names': [f'Collection:FarmListEntry:{self.id}']
            })
        )

    @property
    def farmlistEntry(self):
        """ :meth:`farmlistEntry` is a :func:`generator` that yield
        :class:`EntryId`.

        yield: :class:`EntryId`
        """
        for x in self._raw['cache'][0]['data']['cache']:
            yield EntryId(self.client, x['data'])


class EntryId:
    """ :class:`EntryId` represent of entry from farmlist. This class contains
    more details about entry.

    Usage::
        >>> f = Farmlist(driver)
        >>> f.pull()
        >>> f['Startup farm list'].add(536461288)
        >>> f['Startup farm list'].pull()
        >>> entrys = list(f['Startup farm list'].farmlistEntry)
        >>> entrys[0].villageId
        536461288
        >>>
    """
    def __init__(self, client, data):
        self.client = client
        self.data = data

    def __repr__(self):
        return f'<{type(self).__name__}({self.data})>'

    def __getitem__(self, key):
        try:
            return self.data[key]
        except:
            raise

    @property
    def id(self):
        """ :property:`id` return id of this entry. """
        return self.data['entryId']

    @property
    def villageId(self):
        """ :property:`id` return village id of this entry. """
        return self.data['villageId']

    @property
    def notificationType(self):
        """ :property:`notificationType` return notification type of this
        entry.
        """
        try:
            return self.data['lastReport']['notificationType']
        except:
            return '0'

    @property
    def raidedSum(self):
        """ :property:`raidedSum` return raided sum of this entry. """
        try:
            return self.data['lastReport']['raidedResSum']
        except:
            return 0

    @property
    def capacity(self):
        """ :property:`capaciy` return capacity of this entry. """
        try:
            return self.data['lastReport']['capacity']
        except:
            return 0

    def copy(self, farmlistId):
        """ :meth:`copy` copy this entry to another farmlist using farmlist
        id.

        :param farmlistId: - :class:`int` farmlist id target for copying
                             this entry.
        """
        self.client.farmList.copyEntry({
            'entryId': self.id,
            'villageId': self.villageId,
            'newListId': farmlistId
        })

    def delete(self):
        """ :meth:`delete` delete this entry from this farmlist. """
        self.client.farmList.deleteEntry({
            'entryId': self.id
        })
