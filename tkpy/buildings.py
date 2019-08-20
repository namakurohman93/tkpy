import dataclasses
from typing import Any

from .fixtures import buildingDict
from .models import ImmutableDataclass


class Buildings:
    """ :class:`Buildings` is where building data of village is stored.
    This class provide an easy way to access building data by using building name.
    It return a :class:`list` of :class:`Building` and sorted based on their level.

    Usage::
        >>> v = Villages(driver)
        >>> v.pull()
        >>> v['first village'].buildings.pull()
        >>> v['first village'].buildings['main building']
        >>> [<Building({"buildingType": "15", "villageId": "536461288", "locationId": "27",...})>]
    """

    def __init__(self, client, villageId):
        self.client = client
        self.villageId = villageId
        self._raw = dict()

    def __getitem__(self, key):
        return sorted(
            [
                Building(client=self.client, data=x)
                for x in self.raw
                if x["buildingType"] == buildingDict[key]
            ],
            key=lambda k: int(k["lvl"]),
        )

    def __repr__(self):
        return str(type(self))

    def pull(self):
        """ :meth:`pull` for pulling building data of this village from TK. """
        self._raw.update(
            self.client.cache.get({
                "names": [f"Collection:Building:{self.villageId}"]
            })
        )

    @property
    def freeSlots(self):
        """ :property:`freeSlots` is for check whether there is a free slot or not
        on this village for construct new building.

        return: :class:`list`
        """
        return [x["locationId"] for x in self.raw if x["buildingType"] == "0"]

    @property
    def raw(self):
        """ :property:`raw` is a :func:`generator` that yield raw building data.

        yield: :class:`dict`
        """
        for x in self._raw["cache"][0]["data"]["cache"]:
            yield x["data"]


@dataclasses.dataclass(frozen=True, repr=False)
class Building(ImmutableDataclass):
    """ :class:`Building` is a :class:`dict` - like object that represent
    of 'Building' object for TK. This class is where building data from TK
    stored.

    Usage::
        >>> v = Villages(driver)
        >>> v.pull()
        >>> v['first village'].buildings.pull()
        >>> # Since we know there is only 1 main building on village, so we can do
        ...
        >>> main_building = v['first village'].buildings['main building'][0]
        >>> # for upgrade main building, use :meth:`upgrade`
        ...
        >>> main_building.upgrade()
    """

    __slots__ = ["client"]
    client: Any

    def upgrade(self):
        """ :meth:`upgrade` for upgrade this building.

        return: :class:`dict`
        """
        return self.client.building.upgrade({
            "buildingType": self.buildingType,
            "locationId": self.locationId,
            "villageId": self.villageId,
        })

    def queues(self, reserveResources):
        """ :meth:`upgrade` for upgrade this building.

        return: :class:`dict`
        """
        return self.client.building.upgrade({
            "buildingType": self.buildingType,
            "locationId": self.locationId,
            "villageId": self.villageId,
        })


@dataclasses.dataclass(frozen=True, repr=False)
class BuildingQueue(ImmutableDataclass):
    """ :class:`BuildingQueue` represent building queue of TK. This class
    is where building queue data is stored. The idea of this class is just
    to make access data of building queue easier.

    Usage::
        >>> v = Villages(driver)
        >>> v.pull()
        >>> v['first village'].buildingQueue.pull()
        >>> v['first village'].buildingQueue.freeSlots
        {'1': 1, '2': 1, '4': 2, '5': 1}
    """

    __slots__ = ['client', 'villageId']
    client: Any
    villageId: int

    def __init__(self, client, villageId, data={}):
        super().__init__(data)
        object.__setattr__(self, 'client', client)
        object.__setattr__(self, 'villageId', villageId)

    def pull(self):
        """ :meth:`pull` for pulling building queue data from TK of this village. """
        self.data.update(
            self.client.cache.get({
                'names': [f'BuildingQueue:{self.villageId}']
            })['cache'][0]['data']
        )

    def finish_now(self, queueType):
        """ :meth:`finishNow` is for instant finish building that upgrade
        progress time is less than 5 minutes.

        :param queueType: - `str` it is either '1' or '2'.
                            '1' if building is building.
                            '2' if building is resources.

        return: :class:`dict`
        """
        return self.client.premiumFeature.finishNow({
            'price': 0,
            'queueType': queueType,
            'villageId': self.villageId,
        })


class ConstructionList:
    """ :class:`ConstructionList` is a class that stored data of building
    that can be constructed on this village. It pulling data from TK using
    :meth:`pull` and stored the data so it can be accessed easily. It
    return :class:`Building` object.

    Usage::
        >>> v = Villages(driver)
        >>> v.pull()
        >>> v['first village'].buildings.pull()
        >>> construction_list = ConstructionList(
        ...     client=driver,
        ...     villageId=v['first village'].id,
        ...     locationId=v['first village'].buildings.freeSlots[0]
        ... )
        >>> construction_list.pull()
        >>> construction_list['sawmill']
        >>> <Building({'buildingType': '5', 'locationToBuild': '20', ...})>
        >>> construction_list['sawmill'].upgrade()
        """

    def __init__(self, client, villageId, locationId):
        self.client = client
        self.villageId = villageId
        self.location = locationId
        self._raw = dict()

    def __getitem__(self, key):
        for x in self.buildable:
            if x["buildingType"] == int(buildingDict[key]):
                x["buildable"] = True
                return Building(client=self.client, data=x)
        for x in self.notBuildable:
            if x["buildingType"] == int(buildingDict[key]):
                x["buildable"] = False
                return Building(client=self.client, data=x)
        raise KeyError(f"{key}")

    def __repr__(self):
        return str(type(self))

    def pull(self):
        """ :meth:`pull` for pulling construction list data from TK. """
        self._raw.update(
            self.client.building.getBuildingList({
                "locationId": self.location, "villageId": self.villageId
            })
        )

    @property
    def buildable(self):
        """ :property:`buildable` return :class:`list` of raw building data
        that can be constructed cause required building already filled.

        return: :class:`list`
        """
        return self._raw["response"]["buildings"]["buildable"]

    @property
    def notBuildable(self):
        """ :property:`notBuildable` return :class:`list` of raw building
        data that can't be constructed cause lack of required building.

        return: :class:`list`
        """
        return self._raw["response"]["buildings"]["notBuildable"]
