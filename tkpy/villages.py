from .buildings import Buildings
from .buildings import BuildingQueue
from .buildings import ConstructionList
from .rally_point import RallyPoint
from .exception import VillageNotFound
from .exception import BuildingSlotFull
from .exception import FailedConstructBuilding
from .exception import QueueFull
from .exception import WarehouseNotEnough
from .exception import BuildingAtMaxLevel


class Villages:
    """ :class:`Villages` is where :class:`Village` object stored. This
    class provide an easy way to access :class:`Village` object by using
    'village' name.

    Usage::
        >>> v = Villages(driver)
        >>> v.pull()
        >>> v['my first village']
        >>> <Village({'villageId': '537313245', 'playerId': '001', 'name': 'my first village',...})>
    """

    def __init__(self, client):
        self.client = client
        self._raw_data = dict()

    def __getitem__(self, key):
        try:
            return self._raw_data[key]
        except:
            raise VillageNotFound(f"Village {key} is not found")

    def __iter__(self):
        return iter(self._raw_data.keys())

    def __repr__(self):
        return str(type(self))

    def pull(self):
        """ :meth:`pull` for pulling data from Travian: Kingdom. """
        r = self.client.cache.get({"names": ["Collection:Village:own"]})

        for village in r["cache"][0]["data"]["cache"]:
            self._raw_data[village["data"]["name"]] = Village(
                self.client, village["data"]
            )

    def keys(self):
        return self._raw_data.keys()

    def items(self):
        return self._raw_data.items()

    def values(self):
        return self._raw_data.values()

    def get_capital_village(self):
        """ :meth:`get_capital_village` for find capital village and return it.

        return: :class:`Village`
        """
        for village in self.values():
            if village.is_main_village:
                return village


class Village:
    """ :class:`Village` represent of village object. This class is where
    village data stored.
    """

    def __init__(self, client, data):
        self.client = client
        self.data = data
        self.buildings = Buildings(self.client, self.id)
        self.buildingQueue = BuildingQueue(self.client, self.id)
        self.warehouse = Warehouse(self.data)
        self.rally_point = RallyPoint(self.client, self.data["villageId"])

    def __getitem__(self, key):
        try:
            return self.data[key]
        except:
            raise

    def __repr__(self):
        return f"<{type(self).__name__}({self.data})>"

    def pull(self):
        """ :meth:`pull` for pulling this village data from Travian: Kingdom. """
        r = self.client.cache.get({"names": [f"Village:{self.id}"]})
        self.data.update(r["cache"][0]["data"])

    @property
    def id(self):
        """ :property:`id` return this village id. """
        return int(self.data["villageId"])

    @property
    def name(self):
        """ :property:`name` return this village name. """
        return self.data["name"]

    @property
    def coordinate(self):
        """ :property:`coordinate` return this village coordinate. """
        x, y = self.data["coordinates"]["x"], self.data["coordinates"]["y"]
        return int(x), int(y)

    @property
    def is_main_village(self):
        """ :property:`is_main_village` return whether this village is capital
        village or not.
        """
        return self.data["isMainVillage"]

    def send_attack(
        self, x=None, y=None, units=None, target_id=None, check_target=True
    ):
        """ :meth:`send_attack` send requests to Travian: Kingdom for attacking target.

        :param x: - :class:`int` (optional) x coordinate.
        :param y: - :class:`int` (optional) y coordinate.
        :param unit: - :class:`dict` units that want to be sent to the target.
        :param target_id: - :class:`int` or :class:`str` (optional) target id.
        :param check_target: - :class:`boolean` (optional) whether check target or not. Default True.

        return: :class:`dict`
        """
        self.rally_point.pull()
        return self.rally_point.send_attack(x, y, units, target_id, check_target)

    def send_raid(self, x=None, y=None, units=None, target_id=None, check_target=True):
        """ :meth:`send_raid` send requests to Travian: Kingdom for raiding target.

        :param x: - :class:`int` (optional) x coordinate.
        :param y: - :class:`int` (optional) y coordinate.
        :param unit: - :class:`dict` units that want to be sent to the target.
        :param target_id: - :class:`int` or :class:`str` (optional) target id.
        :param check_target: - :class:`boolean` (optional) whether check target or not. Default True.

        return: :class:`dict`
        """
        self.rally_point.pull()
        return self.rally_point.send_raid(x, y, units, target_id, check_target)

    def send_defend(
        self,
        x=None,
        y=None,
        units=None,
        redeploy_hero=False,
        target_id=None,
        check_target=True,
    ):
        """ :meth:`send_defend` send a requests to Travian: Kingdom for defending target.

        :param x: - :class:`int` (optional) x coordinate.
        :param y: - :calss:`int` (optional) y coordinate.
        :param unit: - :class:`dict` units that want to be sent to the target.
        :param redeploy_hero: - :class:`boolean` (optional) whether to redeploy the hero or not.
                                                 Default False
        :param target_id: - :class:`int` or :class:`str` (optional) target id.
        :param check_target: - :class:`boolean` (optional) whether check target or not. Default True.

        return: :class:`dict`
        """
        self.rally_point.pull()
        return self.rally_point.send_defend(
            x, y, units, redeploy_hero, target_id, check_target
        )

    def send_spy(
        self,
        x=None,
        y=None,
        amount=1,
        mission="resources",
        target_id=None,
        check_target=True,
    ):
        """ :meth:`send_spy` send requests to Travian: Kingdom for spying target.

        :param x: - :class:`int` (optional) value of x coordinate.
        :param y: - :class:`int` (optional) value of y coordinate.
        :param amount: - :class:`int` (optional) amount of spy units that
                         want to sent. Default: 1
        :param mission: - :class:`str` (optional) type of spy mission,
                          it is either `'resources'` `'defend'`. Default: 'resources'
        :param target_id: - :class:`int` or :class:`str` (optional) target id.
        :param check_target: - :class:`boolean` (optional) whether check target or not. Default True.

        return: :class:`dict`
        """
        self.rally_point.pull()
        return self.rally_point.send_spy(x, y, amount, mission, target_id, check_target)

    def send_siege(self, x=None, y=None, units=None, target_id=None, check_target=True):
        """ :meth:`send_siege` send a requests to Travian: Kingdom for siege target.

        :param x: - :class:`int` (optional) x coordinate.
        :param y: - :class:`int` (optional) y coordinate.
        :param unit: - :class:`dict` units that want to be sent to the target.
        :param target_id: - :class:`int` or :class:`str` (optional) target id.
        :param check_target: - :class:`boolean` (optional) whether check target or not. Default True.

        return: :class:`dict`
        """
        self.rally_point.pull()
        return self.rally_point.send_siege(x, y, units, target_id, check_target)

    def send_farmlist(self, listIds):
        """ :meth:`send_farmlist` send requests to Travian: Kingdom for send farmlist.

        :param listIds: - :class:`list` list of farmlist id that want to sent.

        return: :class:`dict`
        """
        return self.client.troops.startFarmListRaid(
            {"listIds": listIds, "villageId": self.id}
        )

    def _is_enough_resources(self, b):
        """ :meth:`_is_enough_resources` is for check whether enough resources or not for
        upgrade building.
        """
        for k, v in b.upgrade_cost.items():
            if self.warehouse[k] < v:
                return False

        return True

    def _is_enough_warehouse_capacity(self, b):
        """ :meth:`_is_enough_warehouse_capacity` is for check whether enough warehouse
        capacity or not for upgrade building.
        """
        for k, v in b.upgrade_cost.items():
            if self.warehouse.capacity[k] < v:
                return False

        return True

    def _upgrade_or_queue(self, b, reserve_resource):
        """ :meth:`_upgrade_or_queue` is for upgrade building. It will put to queue if
        there is no free slot.
        """
        slot = "1"

        if self.client.tribe_id.value == 1 and int(b.id) < 5:
            slot = "2"

        if self.buildingQueue.freeSlots[slot] > 0:
            return b.upgrade()

        elif self.buildingQueue.freeSlots["4"] > 0:
            return b.queues(reserve_resource)

        else:
            raise QueueFull("Queue full")

    def upgrade(self, building):
        """ :meth:`upgrade` send requests to Travian: Kingdom for upgrade building.

        :param building: - :class:`BuildingType` building type that want to be ugpraded.

        return: :class:`dict`
        """
        self.pull()
        self.buildings.pull()
        self.buildingQueue.pull()

        if self.buildings[building]:
            b = self.buildings[building][0]

            if b.is_max_level:
                raise BuildingAtMaxLevel(f"{building.name} already at max level")

            if self._is_enough_resources(b):
                return self._upgrade_or_queue(b, True)

            elif self._is_enough_warehouse_capacity(b):
                return self._upgrade_or_queue(b, False)

            else:
                raise WarehouseNotEnough(
                    f"Warehouse / granary capacity not enough for upgrade {building.name}"
                )

        else:
            raise Exception(f"{building.name} didnt exists, please construct it first")

    def construct(self, building):
        """ :meth:`construct` send requests to Travian: Kingdom for construct building.

        :param building: - :class:`BuildingType` building type that want to be constructed.

        return: :class:`dict`
        """
        self.pull()
        self.buildings.pull()
        self.buildingQueue.pull()

        if self.buildings.freeSlots:
            c = ConstructionList(
                client=self.client,
                villageId=self.id,
                locationId=self.buildings.freeSlots[0],
            )
            c.pull()

            try:
                b = c[building]
            except:
                raise
            else:
                if b["buildable"]:
                    if self._is_enough_resources(b):
                        return self._upgrade_or_queue(b, True)

                    elif self._is_enough_warehouse_capacity(b):
                        return self._upgrade_or_queue(b, False)

                    else:
                        raise WarehouseNotEnough(
                            f"Warehouse / granary capacity not enough for construct {building.name}"
                        )

                else:
                    raise FailedConstructBuilding(
                        f"Failed construct {building.name} cause lack of required building"
                    )

        else:
            raise BuildingSlotFull(f"Building slot at {self.name} full")


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
