import pickle
from primordial import Lobby
from ..models.credential import Lobby as LobbyModel
from ..models.credential import Gameworld as GameworldModel
from ..exception import AvatarNotFound

def login(email, password, gameworld_name):
    lobby = Lobby()
    lobby.authenticate(email, password)
    gameworld_id = get_gameworld_id(lobby, gameworld_name)
    return lobby.connect_to_gameworld(gameworld_name, gameworld_id)

def get_gameworld_id(lobby, gameworld_name):
    r = lobby.cache.get({'names':['Collection:Avatar']})
    for avatar in r['cache'][0]['data']['cache']:
        if gameworld_name == avatar['data']['worldName'].lower():
            return avatar['data']['consumersId']
    raise AvatarNotFound(f'Avatar on {gameworld_name} not found')

def authenticate(email, password, gameworld_name):
    lobby_id = None
    driver = None

    lobby = LobbyModel.find_by_email(email)

    if lobby:
        lobby_id = lobby['id']
    else:
        lobby_id = LobbyModel.create(email, password)

    gameworld = GameworldModel.find_by_lobby_id_and_gameworld_name(lobby_id, gameworld_name)

    if gameworld:
        driver = pickle.loads(gameworld['driver'])
    else:
        driver = login(email, password, gameworld_name)
        GameworldModel.create(gameworld_name, pickle.dumps(driver), lobby_id)

    return driver
