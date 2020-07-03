from .exception import TargetNotFound
from .map import cell_id


class RallyPoint:
    """ :class:`RallyPoint` is an object that will be used for trigger action
    related to troops such as attacking, raiding, sent farmlist, siege, etc
    or for just get information related to troops.
    """

    def __init__(self, client, village_id):
        self.client = client
        self.village_id = village_id
        self.unit_stationary = []
        self.unit_moving = []
        self.unit_trapped = []
        self.unit_elsewhere = []

    def pull(self):
        """ :meth:`pull` pulling data about units on this village. """
        r = self.client.cache.get(
            {
                "names": [
                    f"Collection:Troops:stationary:{self.village_id}",
                    f"Collection:Troops:moving:{self.village_id}",
                    f"Collection:Troops:trapped:{self.village_id}",
                    f"Collection:Troops:elsewhere:{self.village_id}",
                ]
            }
        )

        for cache in r["cache"]:
            if "stationary" in cache["name"]:
                self.unit_stationary = [
                    troop["data"] for troop in cache["data"]["cache"]
                ]
            elif "moving" in cache["name"]:
                self.unit_moving = [troop["data"] for troop in cache["data"]["cache"]]
            elif "trapped" in cache["name"]:
                self.unit_trapped = [troop["data"] for troop in cache["data"]["cache"]]
            elif "elsewhere" in cache["name"]:
                self.unit_elsewhere = [
                    troop["data"] for troop in cache["data"]["cache"]
                ]
            else:
                continue

    @property
    def unit_available(self):
        """ :meth:`unit_available` filter unit on `self.unit_stationary`
        that available on this this village.
        """
        troop = {}

        for unit in self.unit_stationary:
            if unit["villageId"] == self.village_id:
                troop = unit
                break
            else:
                continue

        return troop

    def check_target(self, target):
        """ :meth:`check_target` is for check target. """
        r = self.client.post(
            "troops",
            "checkTarget",
            {
                "destVillageId": int(target),
                "heroPresent": False,
                "movementType": 5,  # need to check it later
                "redeployHero": False,
                "villageId": self.village_id,
                "selectedUnits": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "7": 0,
                    "8": 0,
                    "9": 0,
                    "10": 0,
                    "11": 0,
                },
            },
        )

        return r["response"]

    def _send_troops(
        self, target, movement_type, redeploy_hero, spy_mission, units, check_target
    ):
        """ :meth:`_send_troops` is low level method for sent troops. 

        :param target: - :class:`int` or :class:`str` target id.
        :param movement_type: - :class:`int` or :class:`str` movement type.
        :param redeploy_hero: - :class:`boolean` is used for moving hero to another village.
        :param spy_mission: - :class:`str` choose mission, it is either 'resources' or 'defend'
        :param unit: - :class:`dict` units that want to be sent to the target.
        :param check_target: - :class:`boolean` whether check target or not.

        return: :class:`dict`
        """
        if check_target:
            r = self.check_target(target)
            if "errors" in r:
                raise TargetNotFound()

        # sent troops
        r = self.client.troops.send(
            {
                # 'catapultTargets': [
                #     99, # random
                #     3,
                # ],
                "destVillageId": target,
                "movementType": movement_type,
                "redeployHero": redeploy_hero,
                "spyMission": spy_mission,
                "units": units,
                "villageId": self.village_id,
            }
        )

        return r

    def _check_units(self, units):
        """ :meth:`_check_units` is for check units. 

        :param units: - :class:`dict` units that want to be checked.

        return: `None`
        """
        unit_available = self.unit_available["units"]
        total_units = sum(int(v) for v in units.values())

        # check total troops
        if total_units < 1:
            raise SyntaxError("Send at least 1 troops")

        # check if every amount of unit is enough with unit_available
        for k in units:
            if int(units[k]) > int(unit_available[k]):
                raise SyntaxError(f"Not enough troops with id: {k}")

    def _is_all_scout(self, units):
        """ :meth:`_is_all_scout` is for checkout if units is all scouts or not.

        :param units: - :class:`dict` units that want to be checked.

        return: :class:`boolean`
        """
        total_units = sum(int(v) for v in units.values())

        if self.client.tribe_id.value in (1, 2):
            if "4" in units and total_units == int(units["4"]):
                return True
            else:
                return False
        else:
            if "3" in units and total_units == int(units["3"]):
                return True
            else:
                return False

    def send_attack(
        self, x=None, y=None, units=None, target_id=None, check_target=True
    ):
        """ :meth:`send_attack` for send an attack from this village. 

        :param x: - :class:`int` (optional) x coordinate.
        :param y: - :class:`int` (optional) y coordinate.
        :param unit: - :class:`dict` units that want to be sent to the target.
        :param target_id: - :class:`int` or :class:`str` (optional) target id.
        :param check_target: - :class:`boolean` (optional) whether check target or not. Default True.

        return: :class:`dict`
        """
        # TODO:
        # add catapult target

        target = target_id or cell_id(x, y)

        if units:
            # check if all scout
            if self._is_all_scout(units):
                raise SyntaxError("You cant attack with only scouts.")
        else:
            # send all unit available.
            units = self.unit_available["units"]

        # check units
        self._check_units(units)

        r = self._send_troops(
            target=target,
            movement_type=3,
            redeploy_hero=False,
            spy_mission="resources",
            units=units,
            check_target=check_target,
        )

        return r

    def send_raid(self, x=None, y=None, units=None, target_id=None, check_target=True):
        """ :meth:`send_raid` for send a raid from this village.

        :param x: - :class:`int` (optional) x coordinate.
        :param y: - :class:`int` (optional) y coordinate.
        :param unit: - :class:`dict` units that want to be sent to the target.
        :param target_id: - :class:`int` or :class:`str` (optional) target id.
        :param check_target: - :class:`boolean` (optional) whether check target or not. Default True.

        return: :class:`dict`
        """
        target = target_id or cell_id(x, y)

        if units:
            # check if all scout
            if self._is_all_scout(units):
                raise SyntaxError("You cant attack with only scouts.")
        else:
            # send all unit available.
            units = self.unit_available["units"]

        # check units
        self._check_units(units)

        r = self._send_troops(
            target=target,
            movement_type=4,
            redeploy_hero=False,
            spy_mission="resources",
            units=units,
            check_target=check_target,
        )

        return r

    def send_defend(
        self,
        x=None,
        y=None,
        units=None,
        redeploy_hero=False,
        target_id=None,
        check_target=True,
    ):
        """ :meth:`send_defend` for send defend from this village. 

        :param x: - :class:`int` (optional) x coordinate.
        :param y: - :calss:`int` (optional) y coordinate.
        :param unit: - :class:`dict` units that want to be sent to the target.
        :param redeploy_hero: - :class:`boolean` (optional) whether to redeploy the hero or not.
                                                 Default False
        :param target_id: - :class:`int` or :class:`str` (optional) target id.
        :param check_target: - :class:`boolean` (optional) whether check target or not. Default True.

        return: :class:`dict`
        """
        # TODO:
        # if redeployHero, check if hero in units
        # and check if target is one of village id in Village object

        target = target_id or cell_id(x, y)

        if not units:
            units = self.unit_available["units"]

        # check units
        self._check_units(units)

        r = self._send_troops(
            target=target,
            movement_type=5,
            redeploy_hero=redeploy_hero,
            spy_mission="resources",
            units=units,
            check_target=check_target,
        )

        return r

    def send_spy(
        self,
        x=None,
        y=None,
        amount=1,
        mission="resources",
        target_id=None,
        check_target=True,
    ):
        """ :meth:`send_spy` send spy mission from this village.

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
        target = target_id or cell_id(x, y)
        units = {}

        if mission not in ("resources", "defence"):
            raise SyntaxError("choose mission between 'resources' or 'defence'")

        if self.client.tribe_id.value in (1, 2):
            # roman or teuton
            units["4"] = amount
        else:
            # gauls
            units["3"] = amount

        # check units
        self._check_units(units)

        r = self._send_troops(
            target=target,
            movement_type=6,
            redeploy_hero=False,
            spy_mission=mission,
            units=units,
            check_target=check_target,
        )

        return r

    def send_siege(self, x=None, y=None, units=None, target_id=None, check_target=True):
        """ :meth:`send_siege` send siege from this village.

        :param x: - :class:`int` (optional) x coordinate.
        :param y: - :class:`int` (optional) y coordinate.
        :param unit: - :class:`dict` units that want to be sent to the target.
        :param target_id: - :class:`int` or :class:`str` (optional) target id.
        :param check_target: - :class:`boolean` (optional) whether check target or not. Default True.

        return: :class:`dict`
        """
        # TODO:
        # add catapult target

        # there is flaw in this method.
        # if player sent 1000 scout + 1 ram, should it be success or should it be failed?

        target = target_id or cell_id(x, y)

        if units:
            # check if all scout
            if self._is_all_scout(units):
                raise SyntaxError("You cant attack with only scouts.")
        else:
            # send all unit available.
            units = self.unit_available["units"]

        # check units
        self._check_units(units)

        # check if amount more than 1000
        if sum(int(v) for v in units.values()) < 1000:
            raise SyntaxError("Need at least 1000 troops.")

        # check if ram is exists
        if "7" not in units:
            raise SyntaxError("Need at least 1 ram.")

        r = self._send_troops(
            target=target,
            movement_type=47,
            redeploy_hero=False,
            spy_mission="resources",
            units=units,
            check_target=check_target,
        )

        return r
