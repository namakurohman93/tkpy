import dataclasses
from typing import Any

from .exception import FarmListNotFound
from .models import ImmutableDataclass
from .models import ImmutableDict


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
        self.item = dict()

    def __getitem__(self, key):
        try:
            return self.item[key]
        except:
            raise FarmListNotFound(f"{key}")

    def __repr__(self):
        return str(type(self))

    def pull(self):
        """ :meth:`pull` for pulling farmlist data from TK. """
        r = self.client.cache.get({"names": ["Collection:FarmList:"]})
        for x in r["cache"][0]["data"]["cache"]:
            self.item[x["data"]["listName"]] = FarmlistEntry(
                client=self.client, data=x["data"], raw=ImmutableDict()
            )

    @property
    def list(self):
        """ :property:`list` is a :func:`generator` that yield
        :class:`FarmlistEntry`.

        yield: :class:`FarmlistEntry`
        """
        for x in self.item.values():
            yield x

    def create_farmlist(self, name):
        """ :meth:`create_farmlist` for create new farmlist.

        :param name: - `str` name of new created farmlist

        return: :class:`dict`
        """
        self.client.farmList.createList({"name": name})
        self.pull()


@dataclasses.dataclass(frozen=True, repr=False)
class FarmlistEntry(ImmutableDataclass):
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

    __slots__ = ["client", "raw"]
    client: Any
    raw: ImmutableDict

    def send(self, villageId):
        """ :meth:`send` for send this farmlist entry from village using
        village id.

        :param villageId: - :class:`int` village id where this farmlist
                            is sent.

        return: :class:`dict`
        """
        return self.client.troops.startFarmListRaid({
            "listIds": [self.listId],
            "villageId": villageId,
        })

    def _update_data(self, r):
        for x in r["cache"]:
            if x["name"] == f"FarmList:{self.listId}":
                self.data.update(x["data"])

    def add(self, villageId):
        """ :meth:`add` for add village to this farmlist using village id.

        :param villageId: - :class:`int` village id that want to be added
                            to this farmlist entry.
        """
        self._update_data(
            self.client.farmList.addEntry({
                "listId": self.listId,
                "villageId": villageId,
            })
        )

    def toggle(self, villageId):
        """ :meth:`toggle` for toggling village to this farmlist entry
        using village id.

        :param villageId: - :class:`int` village id that want to be toggled
                            to this farmlist entry.
        """
        self._update_data(
            self.client.farmList.toggleEntry({
                "listId": self.listId,
                "villageId": villageId,
            })
        )

    def pull(self):
        """ :meth:`pull` for pulling entry data that exists in this farmlist
        entry.
        """
        self.raw.update(
            self.client.cache.get({
                "names": [f"Collection:FarmListEntry:{self.listId}"]
            })
        )

    @property
    def farmlistEntry(self):
        """ :meth:`farmlistEntry` is a :func:`generator` that yield
        :class:`EntryId`.

        yield: :class:`EntryId`
        """
        for x in self.raw["cache"][0]["data"]["cache"]:
            yield EntryId(client=self.client, data=x["data"])


@dataclasses.dataclass(frozen=True, repr=False)
class EntryId(ImmutableDataclass):
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

    __slots__ = ["client"]
    client: Any

    @property
    def notification_type(self):
        """ :property:`notificationType` return notification type of this
        entry.
        """
        try:
            return self.data["lastReport"]["notificationType"]
        except:
            return "0"

    @property
    def raided_sum(self):
        """ :property:`raidedSum` return raided sum of this entry. """
        try:
            return self.data["lastReport"]["raidedResSum"]
        except:
            return 0

    @property
    def capacity(self):
        """ :property:`capaciy` return capacity of this entry. """
        try:
            return self.data["lastReport"]["capacity"]
        except:
            return 0

    def copy(self, farmlistId):
        """ :meth:`copy` copy this entry to another farmlist using farmlist
        id.

        :param farmlistId: - :class:`int` farmlist id target for copying
                             this entry.
        """
        self.client.farmList.copyEntry({
            "entryId": self.entryId,
            "villageId": self.villageId,
            "newListId": farmlistId,
        })

    def delete(self):
        """ :meth:`delete` delete this entry from this farmlist. """
        self.client.farmList.deleteEntry({"entryId": self.entryId})
