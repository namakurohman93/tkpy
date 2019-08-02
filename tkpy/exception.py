class NotAuthenticated(Exception):
    """ Not authenticated """


class AvatarNotFound(Exception):
    """ Avatar not found """


class UnitNotFound(Exception):
    """ Unit not found """


class FarmListNotFound(Exception):
    """ Farmlist not found """


class DriverNotFound(Exception):
    """ Driver not found """


class VillageNotFound(Exception):
    """ Village not found """


class BuildingSlotFull(Exception):
    """ Building slot full """


class FailedConstructBuilding(Exception):
    """ Failed construct building """


class QueueFull(Exception):
    """ Building queue full """


class WarehouseNotEnough(Exception):
    """ Warehouse / granary not enough space """


class BuildingAtMaxLevel(Exception):
    """ Building at max level """


class TargetNotFound(Exception):
    """ Target not found """
