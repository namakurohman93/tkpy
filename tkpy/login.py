import pickle
from primordial import Lobby
from .enums.tribe import Tribe
from .enums.troop import RomanTroop
from .enums.troop import TeutonTroop
from .enums.troop import GaulTroop
from .models.credential import Lobby as LobbyModel
from .models.credential import Gameworld as GameworldModel
from .exception import AvatarNotFound


def get_gameworld_detail(driver):
    # maybe I need this for get another detail
    result = dict()

    r = driver.cache.get({"names": [f"Player:{driver.player_id}"]})

    result["tribe_id"] = int(r["cache"][0]["data"]["tribeId"])

    return result


def get_gameworld_id(lobby, gameworld_name):
    r = lobby.cache.get({"names": ["Collection:Avatar"]})
    for avatar in r["cache"][0]["data"]["cache"]:
        if gameworld_name == avatar["data"]["worldName"].lower():
            return avatar["data"]["consumersId"]
    raise AvatarNotFound(f"Avatar on {gameworld_name} not found")


def get_gameworld_object(lobby, gameworld_name):
    gameworld_id = get_gameworld_id(lobby, gameworld_name)
    driver = lobby.connect_to_gameworld(gameworld_name, gameworld_id)
    gameworld_detail = get_gameworld_detail(driver)

    if gameworld_detail["tribe_id"] == 1:
        driver.tribe_id = Tribe.ROMAN
        driver.troop = RomanTroop

    elif gameworld_detail["tribe_id"] == 2:
        driver.tribe_id = Tribe.TEUTON
        driver.troop = TeutonTroop

    else:
        driver.tribe_id = Tribe.GAUL
        driver.troop = GaulTroop

    return driver


def get_driver(email, password, gameworld_name):
    lobby = Lobby()
    lobby.authenticate(email=email, password=password)
    driver = get_gameworld_object(lobby, gameworld_name)
    return driver


def authenticate(email, password, gameworld_name):
    lobby = LobbyModel.find_one(email=email, include=True)

    if lobby is None:
        lobby = LobbyModel.create(email=email, password=password)

    gameworld = lobby.find_gameworld(gameworld_name)

    if gameworld is None:
        driver = get_driver(email, password, gameworld_name)
        lobby.add_gameworld(gameworld_name=gameworld_name, driver=pickle.dumps(driver))
    else:
        driver = pickle.loads(gameworld.driver)
        if not driver.is_authenticated():
            driver = get_driver(email, password, gameworld_name)
            gameworld.driver = pickle.dumps(driver)
            gameworld.save()

    return driver
