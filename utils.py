import requests
from primordial.lobby import Lobby
from utilities.database import Database

COLOR = {
    'BLUE': 1,
    'YELLOW': 2,
    'BROWN': 3,
    'OWN': 4,
    'TEAL' : 5,
    'DARK GREEN': 6,
    'LIGHT GREEN': 7,
    'DARK BLUE': 8,
    'ALLIANCE': 9,
    'PURPLE': 10,
    'PINK': 11,
    'RED': 12,
    'ENEMY': 13,
    'NEUTRAL': 15,
    'TREATY COLOR NAP': 16,
    'TREATY COLOR BND': 17
}


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


def add_attribute(t5):
    t5.client.session.headers['cookie'] = f'msid={t5.msid}'
    cookie_dict = requests.utils.dict_from_cookiejar(t5.client.session.cookies)
    for k, v in cookie_dict.items():
        t5.client.session.headers['cookie'] += f'; {k}={v}'
    r = t5.cache.get({'names':['Collection:Village:own']})
    t5.player_id = r['cache'][0]['data']['cache'][0]['data']['playerId']
    r = t5.cache.get({'names':[f'Player:{t5.player_id}']})
    t5.plus_account = int(r['cache'][0]['data']['plusAccountTime'])
    t5.kingdom_id = int(r['cache'][0]['data']['kingdomId'])
    t5.tribe_id = int(r['cache'][0]['data']['tribeId'])
    return t5


def extended_login(*args, **kwargs):
    database = Database(*args, **kwargs)
    t5 = database.get_driver()
    if t5:
        # saved account
        if t5.is_authenticated(): # check session
            # session can be used again
            client = add_attribute(t5)
        else:
            # session expired
            t5 = basic_login(*args, **kwargs)
            database.update_data(t5)
            client = add_attribute(t5)
    else:
        # new account
        t5 = basic_login(*args, **kwargs)
        database.insert_data(t5)
        client = add_attribute(t5)
    return client


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


def send_troops(client, target, source, move_type, units):
    r = client.troops.send(
        {
            'destVillageId': target,
            'movementType': move_type,
            'redeployHero': False,
            'spyMission': 'resources',
            'units': units,
            'villageId': source
        }
    )
    return r['cache'][0]['data']['cache'][0]['data']['troopId']


def abort_troop_movement(client, id):
    client.troops.abortTroopMovement({'troopId': id})


def delete_player_marker(client):
    r = client.cache.get({'names':['Collection:MapMarker:']})
    results = list()
    for x in r['cache'][0]['data']['cache']:
        if x['data']['type'] == '1':
            results.append(int(x['data']['id']))
    for id in results:
        client.post(
            action='editMapMarkers',
            controller='map',
            params={
                'markers':[{'editType': 2, 'id': id}]
            }
        )
