from threading import Thread
from queue import Queue
import logging
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tkpy.utilities import login, credential
from tkpy.map import Map
from tkpy.notepads import Notepad

logging.basicConfig(
    format='[%(asctime)s][%(levelname)s]: %(message)s',
    level=logging.INFO, datefmt='%d/%b/%Y:%H:%M:%S'
)
animals = {
    '1': 'mouse', '2': 'spider',
    '3': 'snake', '4': 'bat',
    '5': 'wild boar', '6': 'wolf',
    '7': 'bear', '8': 'crocodile',
    '9': 'tiger', '10': 'elephant'
}

soi = {'7', '8', '9', '10'}


def oasis_details(task):
    while True:
        oasis, results = task.get()
        if oasis is None:
            break
        r = oasis.details()
        if set(r['troops']['units']) & soi:
            results.append(
                (oasis, r['troops']['units'])
            )
        task.task_done()


if __name__ == '__main__':
    logging.info('login')
    email, password, gameworld, avatar = credential()
    driver = login(email, password, gameworld, avatar)

    logging.info('pulling map data...')
    maps = Map(driver)
    maps.pull()

    logging.info('processing... it will takes some time based on your connection')
    unoccupiedOasisList = [cell for cell in maps.oasis if cell['oasis']['oasisStatus'] == '3']
    task = Queue()
    threadsList = list()
    results = list()

    for _ in range(4):
        worker = Thread(target=oasis_details, args=(task,))
        worker.start()
        threadsList.append(worker)

    for oasis in unoccupiedOasisList:
        task.put((oasis, results))
        time.sleep(0.1)

    task.join()
    for _ in range(4):
        task.put((None, None))

    for thread in threadsList:
        thread.join()

    msg = ''
    for cell, units in results:
        msg += f'({cell.coordinate[0]}|{cell.coordinate[1]}) -> '
        for unit in units:
            msg += f'{animals[unit]}: {units[unit]} '
        msg += '\n'

    logging.info('create notepad...')
    n = Notepad(driver)
    logging.info('write notepad...')
    n.message(msg)
    logging.info('done')
