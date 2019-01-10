from primordial.lobby import Lobby


def basic_login(email, password, gameworld_name):
    lobby = Lobby()
    lobby.authenticate(email, password)
    caches = lobby.cache.get({'names':['Collection:Avatar']})
    avatars = caches['cache'][0]['data']['cache']
    for avatar in avatars:
        if gameworld_name == avatar['data']['worldName'].lower():
            gameworld_id = avatar['data']['consumersId']
            break
    gameworld = lobby.connect_to_gameworld(
        gameworld_name=gameworld_name,
        gameworld_id=gameworld_id
    )
    return gameworld


def advance_login(*args, **kwargs):
    t5 = basic_login(*args, **kwargs)
    r = t5.cache.get({'names':['Collection:Village:own']})
    t5.player_id = r['cache'][0]['data']['cache'][0]['data']['playerId']
    return t5


def vid(x, y):
    return (536887296 + x) + (y * 32768)


def fishout(vid):
    binary = f'{vid:b}'
    if len(binary) < 30:
        binary = '0' + binary
    xcord, ycord = binary[15:], binary[:15]
    realx = int(xcord, 2) - 16384
    realy = int(ycord, 2) - 16384
    return realx, realy
