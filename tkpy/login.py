import pickle
from primordial import Lobby
from .enums.tribe import Tribe
from .enums.troop import RomanTroop
from .enums.troop import TeutonTroop
from .enums.troop import GaulTroop
from .models.credential import Lobby as LobbyModel
from .models.credential import Gameworld as GameworldModel
from .exception import AvatarNotFound


def login(email, password, gameworld_name):
    lobby = Lobby()
    lobby.authenticate(email, password)
    gameworld_id = get_gameworld_id(lobby, gameworld_name)
    gameworld = lobby.connect_to_gameworld(gameworld_name, gameworld_id)

    gameworld_detail = get_gameworld_detail(gameworld)

    if gameworld_detail["tribe_id"] == 1:
        gameworld.tribe_id = Tribe.ROMAN
        gameworld.troop = RomanTroop
    elif gameworld_detail["tribe_id"] == 2:
        gameworld.tribe_id = Tribe.TEUTON
        gameworld.troop = TeutonTroop
    else:
        gameworld.tribe_id = Tribe.GAUL
        gameworld.troop = GaulTroop

    return gameworld


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


def authenticate(email, password, gameworld_name):
    lobby_id = None
    driver = None

    lobby = LobbyModel.find_one(email=email)

    if lobby:
        if LobbyModel.verify_password(lobby["password"], password):
            lobby_id = lobby["id"]
        else:
            raise Exception(
                "Password in database and password that provided is different"
            )
    else:
        lobby_id = LobbyModel.create(email, password)

    gameworld = GameworldModel.find_one(
        lobby_id=lobby_id, gameworld_name=gameworld_name
    )

    if gameworld:
        driver = pickle.loads(gameworld["driver"])
        if not driver.is_authenticated():
            driver = login(email, password, gameworld_name)
            GameworldModel.update(
                {"driver": pickle.dumps(driver)}, {"id": gameworld["id"]}
            )
    else:
        driver = login(email, password, gameworld_name)
        GameworldModel.create(gameworld_name, pickle.dumps(driver), lobby_id)

    return driver
