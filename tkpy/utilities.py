from .driver import Lobby
from .database import CredentialDb
import argparse


def credential():
    """ :func:`credential` is an argument parser for parsing credential.

    Usage::
        >>> email, password, gameworld, avatar = credential()
    """
    parser = argparse.ArgumentParser(usage='python3 %(prog)s <email> <password> <gameworld> [--avatar]')

    parser.add_argument('email', metavar='email', type=str, help='your email', nargs=1)
    parser.add_argument('password', metavar='password', type=str, help='your password', nargs=1)
    parser.add_argument('gameworld', metavar='gameworld', type=str, help='gameworld name', nargs=1)
    parser.add_argument('--avatar', help='your avatar', type=str, default=None, nargs='*')

    args = parser.parse_args()

    email = args.email[0]
    password = args.password[0]
    gameworld = args.gameworld[0]

    avatar = ' '.join(args.avatar) if args.avatar else None

    return email, password, gameworld, avatar


def _login(email, password, gameworld, avatar):
    """ :func:`_login` internal function for login to gameworld and return
    :class:`Gameworld` object.
    """
    lobby = Lobby()
    lobby.authenticate(email, password)
    client = lobby.get_gameworld(gameworld, avatar)
    return client


def login(email, password, gameworld, avatar=None):
    """ :func:`login` login interface that used sqlite for storing
    :class:`Gameworld` object.
    """
    db = CredentialDb(email, password, gameworld, avatar)
    try:
        driver = db.get()
        try:
            driver.is_authenticated()
            driver.update_account()
        except:
            driver = _login(email, password, gameworld, avatar)
            db.update(driver=driver)
    except:
        driver = _login(email, password, gameworld, avatar)
        db.insert(driver=driver)
    return driver


def send_troops(driver, destVillageId, movementType, redeployHero, spyMission,
        units, villageId):
    return driver.troops.send({
        # 'catapultTargets': [
        #     99, # random
        #     3
        # ],
        'destVillageId': destVillageId,
        'movementType': movementType,
        'redeployHero': redeployHero,
        'spyMission': spyMission,
        'units': units,
        'villageId': villageId
    })


def send_farmlist(driver, listIds, villageId):
    return driver.troops.startFarmListRaid({
        'listIds': listIds,
        'villageId': villageId
    })


def instant_finish(driver, queueType, villageId):
    return driver.premiumFeature.finishNow({
        'price': 0,
        'queueType': queueType,
        'villageId': villageId
    })


def upgrade_building(driver, buildingType, locationId, villageId):
    return driver.building.upgrade({
        'buildingType': buildingType,
        'locationId': locationId,
        'villageId': villageId
    })


def queue_building(
        driver, buildingType, locationId,
        villageId, reserveResources):
    return driver.building.useMasterBuilder({
        'buildingType': buildingType,
        'locationId': locationId,
        'villageId': villageId,
        'reserveResources': reserveResources
    })
