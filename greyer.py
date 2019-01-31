import sys
import time
import logging
from math import sqrt
from utils import advance_login, fishout
from utilities.players import Players
from utilities.map import Map

logging.basicConfig(
    format='[%(asctime)s][%(levelname)s]: %(message)s',
    level=logging.DEBUG, datefmt='%d/%b/%Y:%H:%M:%S'
)
MIN_POPULATION = 0 # minimum village population
MAX_POPULATION = 999999999 # maximum village population
CENTER = 0, 0 # x, y coordinate
MIN_DISTANCE = 0 # minimum distance from CENTER
MAX_DISTANCE = 100 # maximum distance from CENTER


def grey_finder(t5):
    village_list = list()
    inactive_players = inactive_players_list(t5)
    maps = Map(t5)
    maps.pull()
    for coord in maps:
        try:
            player_id = int(maps[coord]['playerId'])
            if player_id in inactive_players:
                village_list.append(maps[coord]['village'])
        except KeyError:
            continue
    return village_list


def inactive_players_list(t5):
    results = list()
    players = Players(t5)
    players.pull()
    inactive_players = players.inactive()
    for player_name in inactive_players:
        results.append(inactive_players[player_name].id)
    return results


def filter_population(village_list):
    result = list()
    for village in village_list:
        if MIN_POPULATION <= int(village['population']) <= MAX_POPULATION:
            result.append(village)
    return result


def filter_distance(village_list):
    result = list()
    for village in village_list:
        village_id = int(village['villageId'])
        x, y = fishout(village_id)
        d = sqrt((CENTER[0] - x)**2 + (CENTER[1] - y)**2)
        if MIN_DISTANCE <= d <= MAX_DISTANCE:
            result.append(village)
    return result


def create_farmlist(t5):
    r = t5.farmList.createList({'name': time.strftime('%d%b%y%H%M%S')})
    return r['cache'][0]['data']['cache'][0]['data']['listId']


def add_village_to_farmlist(t5, village_id, farmlist_id):
    t5.farmList.toggleEntry({'listId': farmlist_id, 'villageId': village_id})


if __name__ == '__main__':
    try:
        email = sys.argv[1]
        password = sys.argv[2]
        gameworld_name = sys.argv[3]
    except IndexError:
        errmsg = 'Missing arguments\n'+\
                 f'Usage: \tpython3 {sys.argv[0]} <email> <password> <gameworld>'
        print(errmsg)
        sys.exit()
    gameworld = advance_login(email, password, gameworld_name)
    if not gameworld.plus_account:
        print('need travian plus for running this utilities.')
        sys.exit()
    village_list = filter_distance(filter_population(grey_finder(gameworld)))
    for _ in range((len(village_list) // 100)+1):
        farmlist_id = int(create_farmlist(gameworld))
        for _ in range(100):
            village_id = village_list.pop()['villageId']
            add_village_to_farmlist(gameworld, village_id, farmlist_id)
            if not village_list:
                break
        time.sleep(0.1)
    print(f'done, please check your farmlist.')
