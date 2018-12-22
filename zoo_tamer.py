import sys
import time
import logging
from threading import Thread
from queue import Queue
from utils import basic_login, vid, fishout

logging.basicConfig(
    format='[%(asctime)s][%(levelname)s]: %(message)s',
    level=logging.DEBUG, datefmt='%d/%b/%Y:%H:%M:%S'
)
ZOOS = {
    '1': 'mouse', '2': 'spider',
    '3': 'snake', '4': 'bat',
    '5': 'wild boar', '6': 'wolf',
    '7': 'bear', '8': 'crocodile',
    '9': 'tiger', '10': 'elephant'
}
SOI = { # set of interest
    '8', '9', '10'
}


def thread_1(t5, task):
    while True:
        x, y, results = task.get()
        if x is None:
            break
        r = t5.map.getByRegionIds(
            {
                'regionIdCollection': {
                    '1': [
                        vid(x, y)
                    ]
                }
            }
        )
        for result in r['response']['1']['region'][f'{vid(x, y)}']:
            try:
                oasis_status = int(result['oasis']['oasisStatus'])
                if oasis_status == 3:
                    results.append(result['id'])
            except KeyError:
                continue
        task.task_done()


def thread_2(t5, task):
    while True:
        msg = ''
        result, results_2 = task.get()
        if result is None:
            break
        r = t5.cache.get(
            {
                'names': [
                    f'MapDetails:{result}'
                ]
            }
        )
        x, y = fishout(int(result))
        units = r['cache'][0]['data']['troops']['units']
        if set(units) & SOI:
            for unit in units:
                msg += f'{ZOOS[unit]}: {units[unit]} '
            results_2.append((x, y, msg))
        task.task_done()


def zoo(t5):
    results = list()
    results_2 = list()
    # prepare thread
    task = Queue()
    threads_1 = list()
    for _ in range(8):
        worker = Thread(target=thread_1, args=(t5, task))
        worker.start()
        threads_1.append(worker)
    # dispatch thread
    for x in range(-13, 14):
        for y in range(-13, 14):
            task.put((x, y, results))
            time.sleep(0.1)
    # cleaning up
    task.join()
    for _ in range(8):
        task.put((None, None, None))
    for thread in threads_1:
        thread.join()
    # threading for next step
    task = Queue()
    threads_2 = list()
    for _ in range(8):
        worker = Thread(target=thread_2, args=(t5, task))
        worker.start()
        threads_2.append(worker)
    # dispatch thread
    for result in results:
        task.put((result, results_2))
        time.sleep(0.1)
    # cleaning up
    task.join()
    for _ in range(8):
        task.put((None, None))
    for thread in threads_2:
        thread.join()
    # collecting results
    new_msg = ''
    for x, y, msg in results_2:
        new_msg += f'({x}|{y}) -> {msg}\n'
    # print to note
    r = t5.cache.get({'names':['Collection:Notepad:']})
    if r['cache'][0]['data']['cache']:
        t5.post(
            action='changeSettings',
            controller='player',
            params= {
                'newSettings': {
                    'notpadsVisible': True
                }
            }
        )
        r = t5.player.addNote(
            {
                'x': 4.5,
                'y': 10.5
            }
        )
        nid = r['cache'][0]['data']['cache'][0]['data']['id']
        t5.player.changeNote(
            {
                'newSettings': {
                    'id': nid,
                    'positionX': 4.5,
                    'positionY': 10.5,
                    'sizeX': 225,
                    'sizeY': 100,
                    'text': ''
                }
            }
        )
        t5.player.changeNote(
            {
                'newSettings': {
                    'id': nid,
                    'positionX': 4.5,
                    'positionY': 10.5,
                    'sizeX': 225,
                    'sizeY': 100,
                    'text': f'{new_msg}'
                }
            }
        )
    else:
        t5.post(
            action='changeSettings',
            controller='player',
            params= {
                'newSettings': {
                    'notpadsVisible': False
                }
            }
        )
        r = t5.post(
            action='addNote',
            controller='player',
            params={}
        )
        nid = r['cache'][0]['data']['cache'][0]['data']['id']
        t5.post(
            action='changeSettings',
            controller='player',
            params= {
                'newSettings': {
                    'notpadsVisible': True
                }
            }
        )
        t5.player.changeNote(
            {
                'newSettings': {
                    'id': nid,
                    'positionX': 4.5,
                    'positionY': 10.5,
                    'sizeX': 225,
                    'sizeY': 100,
                    'text': ''
                }
            }
        )
        t5.player.changeNote(
            {
                'newSettings': {
                    'id': nid,
                    'positionX': 4.5,
                    'positionY': 10.5,
                    'sizeX': 225,
                    'sizeY': 100,
                    'text': f'{new_msg}'
                }
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
    gameworld = basic_login(email, password, gameworld_name)
    zoo(gameworld)
