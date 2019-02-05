import sys
import logging
import threading
import queue
import time
from math import sqrt
from utils import extended_login
from utilities.map import Map
from utilities.players import Players

logging.basicConfig(
    format='[%(asctime)s][%(levelname)s]: %(message)s',
    level=logging.DEBUG, datefmt='%d/%b/%Y:%H:%M:%S'
)
CENTER = 0, 0 # x, y coordinate
RADIUS = 100


def players_list(t5, maps):
    results = dict()
    player_list = list()
    players = Players(t5)
    players.pull()
    for coord in maps:
        try:
            player_id = int(maps[coord]['playerId'])
            player_list.append(player_id)
        except KeyError:
            continue
    for player_name in players:
        if players[player_name].id in player_list:
            results[player_name] = players[player_name]
    return Players(t5, results)


def filter_inactive(players):
    for player_name in players:
        if not players[player_name].active:
            del players[player_name]
    return players


def filter_kingdom(players, kingdom_id):
    if kingdom_id == 0:
        return players
    for player_name in players:
        if players[player_name].kingdomId == kingdom_id:
            del players[player_name]
    return players


def map_of_interest(t5):
    maps = Map(t5)
    maps.pull()
    for coord in maps:
        if not inside_area(*coord):
            del maps[coord]
    return maps


def chicken_player(players):
    results = list()
    threads = list()
    task = queue.Queue()
    for _ in range(8):
        worker = threading.Thread(target=thread_1, args=(task,))
        worker.start()
        threads.append(worker)
    for player in players:
        task.put((players[player], results))
        time.sleep(0.1)
    task.join()
    for _ in range(8):
        task.put((None, None))
    for thread in threads:
        thread.join()
    return results


def thread_1(task):
    while True:
        player, results = task.get()
        if results is None:
            break
        eq = player.hero_equipment()
        for x in eq['cache'][0]['data']['cache']:
            slot = int(x['data']['slot'])
            item_id = int(x['data']['itemId'])
            if slot == 5 and item_id in [121, 122, 123]:
                results.append(player.id)
        task.task_done()


def inside_area(x, y):
    d = sqrt((CENTER[0] - x)**2 + (CENTER[1] - y)**2)
    return 0 <= d <= RADIUS


def mark_player(t5, players):
    player_marker_dict = dict()
    r = t5.cache.get({'names':['Collection:MapMarker:']})
    for x in r['cache'][0]['data']['cache']:
        if x['data']['type'] == '1':
            if int(x['data']['targetId']) in players:
                marker_id = int(x['data']['id'])
                player_marker_dict[int(x['data']['targetId'])] = marker_id
    for player_id in players:
        if player_id in player_marker_dict:
            marker_id = player_marker_dict[player_id]
            threading.Thread(
                target=edit_mark,
                args=(t5, player_id, marker_id)
            ).start()
            time.sleep(0.1)
        else:
            threading.Thread(
                target=create_mark,
                args=(t5, player_id)
            ).start()
            time.sleep(0.1)


def edit_mark(t5, player_id, marker_id):
    t5.post(
        action='editMapMarkers',
        controller='map',
        params={
            'markers':[
                {
                    'color': 10,
                    'editType': 1,
                    'id': marker_id,
                    'owner': 1,
                    'ownerId': t5.player_id,
                    'targetId': player_id,
                    'type': 1
                }
            ]
        }
    )


def create_mark(t5, player_id):
    t5.post(
        action='editMapMarkers',
        controller='map',
        params={
            'markers':[
                {
                    'color': 10,
                    'editType': 3,
                    'owner': 1,
                    'ownerId': t5.player_id,
                    'targetId': player_id,
                    'type': 1
                }
            ]
        }
    )


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
    gameworld = extended_login(email, password, gameworld_name)
    maps = map_of_interest(gameworld)
    players = filter_kingdom(
        filter_inactive(
            players_list(gameworld, maps)
        ), gameworld.kingdom_id
    )
    player_list = chicken_player(players)
    mark_player(gameworld, player_list)
    logging.info('done, please check the map.')
