import dataclasses
from typing import Any

from .map import cell_id
from .models import ImmutableDataclass
from .buildings import Buildings
from .buildings import BuildingQueue
from .buildings import ConstructionList
from .exception import VillageNotFound
from .exception import BuildingSlotFull
from .exception import FailedConstructBuilding
from .exception import QueueFull
from .exception import WarehouseNotEnough
from .exception import BuildingAtMaxLevel
from .exception import TargetNotFound


class Villages:
    """ :class:`Villages` is where :class:`Village` object stored. This
    class provide an easy way to access :class:`Village` object by using
    'village' name.

    Usage::
        >>> v = Villages(driver)
        >>> v.pull()
        >>> v['my first village']
        <Village({'villageId': '537313245', 'playerId': '001',...})>
    """

    def __init__(self, client):
        self.client = client
        self.item = dict()

    def __getitem__(self, key):
        try:
            return self.item[key]
        except:
            raise VillageNotFound(f"Village {key} is not found")

    @property
    def dorps(self):
        """ :property:`dorps` is a :func:`generator` that yield
        :class:`Village` object.

        yield: :class:`Village`
        """
        for village in self.item.values():
            yield village

    def pull(self):
        """ :meth:`pull` for pulling data from TK. """
        r = self.client.cache.get({"names": ["Collection:Village:own"]})
        # store village object
        for village in r["cache"][0]["data"]["cache"]:
            self.item[village["data"]["name"]] = Village(
                client=self.client, data=village["data"]
            )

    def get_capital_village(self):
        """ :meth:`get_capital_village` for find capital village
        and return it.

        return: :class:`Village`
        """
        for village in self.dorps:
            if village.isMainVillage:
                return village


@dataclasses.dataclass(frozen=True, repr=False)
class Village(ImmutableDataclass):
    """ :class:`Village` represent of village object. This class is
    where village data stored.
    """

    __slots__ = ["client", "buildings", "buildingQueue", "warehouse"]
    client: Any

    def __init__(self, client, data):
        super().__init__(data)
        object.__setattr__(self, "client", client)
        object.__setattr__(
            self,
            "buildings",
            Buildings(client=self.client, villageId=self.villageId),
        )
        object.__setattr__(
            self,
            "buildingQueue",
            BuildingQueue(client=self.client, villageId=self.villageId),
        )
        object.__setattr__(self, "warehouse", Warehouse(data))

    def pull(self):
        """ :meth:`pull` for pulling this village data from TK. """
        self.data.update(
            self.client.cache.get({
                "names": [f"Village:{self.villageId}"]
            })["cache"][0]["data"]
        )

    def units(self):
        """ :meth:`units` send requests to TK for perceive units that
        belong to this village.

        return: :class:`dict`
        """
        r = self.client.cache.get({
            "names": [f"Collection:Troops:stationary:{self.villageId}"]
        })
        for x in r["cache"][0]["data"]["cache"]:
            if x["data"]["villageId"] == str(self.villageId):
                return x["data"]["units"] or {}

    def troops_movement(self):
        """ :meth:`troops_movement` send requests to TK for perceive
        troops movement in and out of this village.

        return: :class:`list`
        """
        r = self.client.cache.get({
            "names": [f"Collection:Troops:moving:{self.villageId}"]
        })
        return [x["data"] for x in r["cache"][0]["data"]["cache"]]

    def _send_troops(
        self,
        x,
        y,
        destVillageId,
        movementType,
        redeployHero,
        spyMission,
        units,
    ):
        """ :meth:`_send_troops` is real troops sender. It send a requests
        to TK for sending troops to target.

        :param x: - :class:`int` x coordinate of target.
        :param y: - :class:`int` y coordinate of target.
        :param destVillageId: - :class:`int` cell id of target.
        :param movementType: - :class:`int` type of movement.
        :param redeployHero: - :class:`boolean` it is used for moving
                               hero's home to another account village.
        :param spyMission: - :class:`str` choose mission, is it either
                             'resources' or 'defend'
        :param units: - :class:`dict` units dict that want to be sent.

        return: :class:`dict`
        """
        target = destVillageId or cell_id(x, y)
        # check target
        r = self.client.cache.get({
            "names": [f"MapDetails:{target}"]
        })["cache"][0]["data"]

        if not (
            r["isOasis"]
            or int(r["hasVillage"])
            or int(r["hasNPC"])
        ):
            raise TargetNotFound("make sure your target is oasis or village")

        troops = self.units()
        # check amount of every units if units
        if units:
            for k, v in units.items():
                if int(v) == -1:
                    units[k] = int(troops.get(k, 0))
                if int(v) > int(troops.get(k, 0)):
                    raise SyntaxError(f"Not enough troops {k}")
            if sum(int(v) for v in units.values()) <= 0:
                raise SyntaxError("Send at least 1 troops")
            # check total amount of units if movementType 47 (siege)
            if movementType == 47:
                if sum(int(v) for v in units.values()) < 1000:
                    raise SyntaxError("Need at least 1000 troops")
                # check if ram exists
                if "7" not in units:
                    raise SyntaxError("Need at least 1 ram for siege")
        else:
            # since it send all unit on village, first
            # set scout amount to 0
            if self.client.tribe_id in (1, 2):
                troops["4"] = 0
            else:
                troops["3"] = 0
            # use all troops on village
            if sum(int(v) for v in troops.values()) <= 0:
                raise SyntaxError(f"There is no troops on {self.name} village")
        return self.client.troops.send({
            # 'catapultTargets': [
            #     99, # random
            #     3,
            # ],
            "destVillageId": target,
            "movementType": movementType,
            "redeployHero": redeployHero,
            "spyMission": spyMission,
            "units": units or troops,
            "villageId": self.villageId,
        })

    def attack(self, x=None, y=None, targetId=None, units=None):
        """ :meth:`attack` send requests to TK for attacking target.

        :param x: - :class:`int` (optional) value of x coordinate.
        :param y: - :class:`int` (optional) value of y coordinate.
        :param targetId: - :class:`int` (optional) cell id of target.
        :param units: - :class:`dict` (optional) units dict that want to sent.

        return: :class:`dict`
        """
        # TODO:
        # add building target when cata in units and rally point level >= 5
        return self._send_troops(
            x=x,
            y=y,
            destVillageId=targetId,
            movementType=3,
            redeployHero=False,
            spyMission="resources",
            units=units,
        )

    def raid(self, x=None, y=None, targetId=None, units=None):
        """ :meth:`raid` send requests to TK for raiding target.

        :param x: - :class:`int` (optional) value of x coordinate.
        :param y: - :class:`int` (optional) value of y coordinate.
        :param targetId: - :class:`int` (optional) cell id of target.
        :param units: - :class:`dict` (optional) units dict that want to sent.

        return: :class:`dict`
        """
        return self._send_troops(
            x=x,
            y=y,
            destVillageId=targetId,
            movementType=4,
            redeployHero=False,
            spyMission="resources",
            units=units,
        )

    def defend(
        self, x=None, y=None, targetId=None, units=None, redeployHero=False
    ):
        """ :meth:`defend` send a requests to TK for defending target.

        :param x: - :class:`int` (optional) value of x coordinate.
        :param y: - :class:`int` (optional) value of y coordinate.
        :param targetId: - :class:`int` (optional) cell id of target.
        :param units: - :class:`dict` (optional) units dict that want to sent.
        :param redeployHero: - :class:`boolean` (optional) it used for changing
                               hero's home. Default: False

        return: :class:`dict`
        """
        # TODO:
        # if redeployHero, check if hero in units
        # and check if target is one of village id in Village object
        return self._send_troops(
            x=x,
            y=y,
            destVillageId=targetId,
            movementType=5,
            redeployHero=redeployHero,
            spyMission="resources",
            units=units,
        )

    def spy(
        self, x=None, y=None, targetId=None, amount=0, mission="resources"
    ):
        """ :meth:`spy` send requests to TK for spying target.

        :param x: - :class:`int` (optional) value of x coordinate.
        :param y: - :class:`int` (optional) value of y coordinate.
        :param targetId: - :class:`int` (optional) cell id of target.
        :param amount: - :class:`int` (optional) amount of spy units that
                         want to sent. Default: 0
        :param mission: - :class:`str` (optional) type of spy mission,
                          it is either `'resources'` `'defend'`. Default: 'resources'

        return: :class:`dict`
        """
        if mission not in ("resources", "defence"):
            raise SyntaxError(
                "choose mission between 'resources' or 'defence'"
            )
        if self.client.tribe_id in (1, 2):
            units = {"4": amount}  # scout of roman and teuton
        else:
            units = {"3": amount}  # scout of gauls
        return self._send_troops(
            x=x,
            y=y,
            destVillageId=targetId,
            movementType=6,
            redeployHero=False,
            spyMission=mission,
            units=units,
        )

    def siege(self, x=None, y=None, targetId=None, units=None):
        """ :meth:`siege` send a requests to TK for siege target.

        :param x: - :class:`int` (optional) value of x coordinate.
        :param y: - :class:`int` (optional) value of y coordinate.
        :param targetId: - :class:`int` (optional) cell id of target.
        :param units: - :class:`dict` (optional) units dict that want to sent.

        return: :class:`dict`
        """
        # TODO
        # add building target if cata in units and rally point level >= 5
        if not units:
            raise SyntaxError("Set units first")
        return self._send_troops(
            x=x,
            y=y,
            destVillageId=targetId,
            movementType=47,
            redeployHero=False,
            spyMission="resources",
            units=units,
        )

    def send_farmlist(self, listIds):
        """ :meth:`send_farmlist` send requests to TK for send farmlist.

        :param listIds: - :class:`list` list of farmlist id that want to sent.

        return: :class:`dict`
        """
        return self.client.troops.startFarmListRaid({
            "listIds": listIds,
            "villageId": self.villageId
        })

    def upgrade(self, building):
        """ :meth:`upgrade` send requests to TK for upgrade building.

        :param building: - :class:`str` building name that want to be ugpraded.

        return: :class:`dict`
        """
        # update data with the newest one
        self.pull()
        self.buildings.pull()
        self.buildingQueue.pull()

        if self.buildings[building]:
            b = self.buildings[building][0]

            if b.isMaxLvl:
                return self._construct(building)

            for k, v in b.upgradeCosts.items():
                if self.warehouse[k] < v and self.warehouse.capacity[k] > v:
                    return self._check_queue(reserveResources=False, b=b)

                if self.warehouse.capacity[k] < v:
                    raise WarehouseNotEnough(
                        f"Warehouse / granary capacity not enough for upgrade {building}"
                    )

            if self.client.tribe_id == 1 and int(b.buildingType) < 5:
                return self._upgrade(slot="2", b=b)

            return self._upgrade(slot="1", b=b)

        # building didn't exists
        # construct it
        return self._construct(building)

    def _construct(self, building):
        if self.buildings.freeSlots:
            c = ConstructionList(
                client=self.client,
                villageId=self.villageId,
                locationId=self.buildings.freeSlots[0],
            )
            c.pull()

            try:
                b = c[building]
            except:
                raise BuildingAtMaxLevel(f"{building} already at max level")
            else:
                if b.buildable:
                    # construct it
                    for k, v in b.upgradeCosts.items():
                        if (
                            self.warehouse[k] < v
                            and self.warehouse.capacity[k] > v
                        ):
                            return self._check_queue(
                                reserveResources=False, b=b
                            )

                        if self.warehouse.capacity[k] < v:
                            raise WarehouseNotEnough(
                                f"Warehouse / granary capacity not enough for construct {building}"
                            )

                    return self._upgrade(slot="1", b=b)

                raise FailedConstructBuilding(
                    f"Failed construct {building} cause lack of required buildings"
                )

        raise BuildingSlotFull(f"Building slot at {self.name} full")

    def _upgrade(self, slot, b):
        if self.buildingQueue.freeSlots[slot] > 0:
            return b.upgrade()

        return self._check_queue(reserveResources=True, b=b)

    def _check_queue(self, reserveResources, b):
        if self.buildingQueue.freeSlots["4"] > 0:
            return b.queues(reserveResources)

        raise QueueFull("Queue full")


class Warehouse:
    """ :class:`Warehouse` represent storage data so it can be read by human. """

    def __init__(self, data):
        self.data = data
        self.resType = {"wood": "1", "clay": "2", "iron": "3", "crop": "4"}

    @property
    def storage(self):
        return self.data["storage"]

    @property
    def production(self):
        return {k: int(v) for k, v in self.data["production"].items()}

    @property
    def capacity(self):
        return {k: int(v) for k, v in self.data["storageCapacity"].items()}

    @property
    def wood(self):
        return self._print_res("1")

    @property
    def clay(self):
        return self._print_res("2")

    @property
    def iron(self):
        return self._print_res("3")

    @property
    def crop(self):
        return self._print_res("4")

    def _print_res(self, key):
        s = self.storage[key]
        c = self.capacity[key]
        p = self.production[key]
        return f"{s}/{c} {p}"

    def __getitem__(self, key):
        if key in ("1", "2", "3", "4"):
            return self.storage[key]
        elif key in ("wood", "clay", "iron", "crop"):
            return self.storage[self.resType[key]]
        else:
            raise KeyError(
                "The key is '1', '2', '3', '4' or 'wood', 'clay', 'iron', 'crop'"
            )

    def __repr__(self):
        return f"wood: {self.wood}\nclay: {self.clay}\niron: {self.iron}\ncrop: {self.crop}"
