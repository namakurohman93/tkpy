import sys
import time
import logging
from threading import Thread
from queue import Queue
from utils import basic_login
from utilities.notepads import Notepad
from utilities.map import Map

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


def thread_1(task):
    while True:
        msg = ''
        result, results_2 = task.get()
        if result is None:
            break
        r = result.details()
        x, y = result.coord
        units = r['cache'][0]['data']['troops']['units']
        if set(units) & SOI:
            for unit in units:
                msg += f'{ZOOS[unit]}: {units[unit]} '
            results_2.append((x, y, msg))
        task.task_done()


def zoo(t5):
    results = list()
    results_2 = list()
    maps = Map(t5)
    maps.init()
    oasis = maps.oasis()
    for coord in oasis:
        if int(oasis.coordinate(*coord)['oasis']['oasisStatus']) == 3:
            results.append(oasis.coordinate(*coord))
        else:
            continue
    task = Queue()
    threads = list()
    for _ in range(8):
        worker = Thread(target=thread_1, args=(task,))
        worker.start()
        threads.append(worker)
    # dispatch thread
    for result in results:
        task.put((result, results_2))
        time.sleep(0.1)
    # cleaning up
    task.join()
    for _ in range(8):
        task.put((None, None))
    for thread in threads:
        thread.join()
    # collecting results
    new_msg = ''
    for x, y, msg in results_2:
        new_msg += f'({x}|{y}) -> {msg}\n'
    # print to note
    notepad = Notepad(t5)
    notepad.new_notepad()
    notepad.message(new_msg)


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
    print(f'done, please check your {gameworld_name}\'s notepad.')
