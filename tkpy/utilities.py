from .driver import Lobby
from .database import CredentialDb
import argparse


def credential():
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
    lobby = Lobby()
    lobby.authenticate(email, password)
    client = lobby.get_gameworld(gameworld, avatar)
    return client


def login(email, password, gameworld, avatar=None):
    db = CredentialDb(email, password, gameworld, avatar)
    try:
        driver = db.get()
        try:
            driver.is_authenticated()
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
